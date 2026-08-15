from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_namespaces() -> dict:
    """List all Kubernetes namespaces."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        namespaces = v1.list_namespace()

        result = []

        for namespace in namespaces.items:
            result.append({
                "name": namespace.metadata.name,
                "status": namespace.status.phase
            })

        return {
            "namespace_count": len(result),
            "namespaces": result
        }

    except ApiException as e:
        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }