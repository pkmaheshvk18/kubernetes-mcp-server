from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_pvs() -> dict:
    """List PersistentVolumes in the Kubernetes cluster."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pvs = v1.list_persistent_volume()

        result = []

        for pv in pvs.items:
            result.append({
                "name": pv.metadata.name,
                "status": pv.status.phase,
                "capacity": (
                    pv.spec.capacity.get("storage")
                    if pv.spec.capacity
                    else None
                ),
                "access_modes": pv.spec.access_modes or [],
                "reclaim_policy": pv.spec.persistent_volume_reclaim_policy,
                "storage_class": pv.spec.storage_class_name,
                "claim": (
                    f"{pv.spec.claim_ref.namespace}/"
                    f"{pv.spec.claim_ref.name}"
                    if pv.spec.claim_ref
                    else None
                )
            })

        return {
            "pv_count": len(result),
            "pvs": result
        }

    except ApiException as e:
        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }