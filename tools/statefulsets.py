from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_statefulsets(namespace: str = "default") -> dict:
    """List StatefulSets in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        statefulsets = apps_v1.list_namespaced_stateful_set(
            namespace=namespace
        )

        result = []

        for sts in statefulsets.items:
            result.append({
                "name": sts.metadata.name,
                "namespace": sts.metadata.namespace,
                "desired_replicas": sts.spec.replicas,
                "ready_replicas": sts.status.ready_replicas or 0,
                "current_replicas": sts.status.current_replicas or 0
            })

        return {
            "namespace": namespace,
            "statefulset_count": len(result),
            "statefulsets": result
        }

    except ApiException as e:
        if e.status == 404:
            return {
                "error": f"Namespace '{namespace}' not found."
            }

        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }