from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def pod_config(
    pod_name: str,
    namespace: str = "default"
) -> dict:
    """Check ConfigMap and Secret references used by a Kubernetes Pod."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pod = v1.read_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )

        configmaps = []
        secrets = []

        def check_configmap(name: str, source: str):
            exists = True

            try:
                v1.read_namespaced_config_map(
                    name=name,
                    namespace=namespace
                )
            except ApiException as e:
                if e.status == 404:
                    exists = False
                else:
                    raise

            configmaps.append({
                "name": name,
                "source": source,
                "exists": exists
            })

        def check_secret(name: str, source: str):
            exists = True

            try:
                v1.read_namespaced_secret(
                    name=name,
                    namespace=namespace
                )
            except ApiException as e:
                if e.status == 404:
                    exists = False
                else:
                    raise

            secrets.append({
                "name": name,
                "source": source,
                "exists": exists
            })

        for container in pod.spec.containers:
            for env_from in container.env_from or []:

                if env_from.config_map_ref:
                    check_configmap(
                        env_from.config_map_ref.name,
                        f"container:{container.name}:envFrom"
                    )

                if env_from.secret_ref:
                    check_secret(
                        env_from.secret_ref.name,
                        f"container:{container.name}:envFrom"
                    )

            for env in container.env or []:

                if env.value_from:
                    if env.value_from.config_map_key_ref:
                        check_configmap(
                            env.value_from.config_map_key_ref.name,
                            f"container:{container.name}:env:{env.name}"
                        )

                    if env.value_from.secret_key_ref:
                        check_secret(
                            env.value_from.secret_key_ref.name,
                            f"container:{container.name}:env:{env.name}"
                        )

        for volume in pod.spec.volumes or []:

            if volume.config_map:
                check_configmap(
                    volume.config_map.name,
                    f"volume:{volume.name}"
                )

            if volume.secret:
                check_secret(
                    volume.secret.secret_name,
                    f"volume:{volume.name}"
                )

        return {
            "pod": pod_name,
            "namespace": namespace,
            "configmaps": configmaps,
            "secrets": secrets
        }

    except ApiException as e:
        if e.status == 404:
            return {
                "error": f"Pod '{pod_name}' not found in namespace '{namespace}'."
            }

        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }