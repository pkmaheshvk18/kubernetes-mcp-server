from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_pvcs(namespace: str = "default") -> dict:
    """List PersistentVolumeClaims in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pvcs = v1.list_namespaced_persistent_volume_claim(
            namespace=namespace
        )

        result = []

        for pvc in pvcs.items:
            result.append({
                "name": pvc.metadata.name,
                "namespace": pvc.metadata.namespace,
                "status": pvc.status.phase,
                "volume": pvc.spec.volume_name,
                "storage_class": pvc.spec.storage_class_name,
                "requested_storage": (
                    pvc.spec.resources.requests.get("storage")
                    if pvc.spec.resources
                    and pvc.spec.resources.requests
                    else None
                ),
                "access_modes": pvc.spec.access_modes or []
            })

        return {
            "namespace": namespace,
            "pvc_count": len(result),
            "pvcs": result
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