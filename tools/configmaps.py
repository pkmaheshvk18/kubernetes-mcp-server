from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_configmaps(namespace: str = "default") -> dict:
    """List ConfigMaps in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        configmaps = v1.list_namespaced_config_map(
            namespace=namespace
        )

        result = []

        for configmap in configmaps.items:
            result.append({
                "name": configmap.metadata.name,
                "namespace": configmap.metadata.namespace,
                "keys": list(configmap.data.keys())
                if configmap.data
                else []
            })

        return {
            "namespace": namespace,
            "configmap_count": len(result),
            "configmaps": result
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