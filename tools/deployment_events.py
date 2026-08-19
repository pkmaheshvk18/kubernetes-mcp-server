from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def deployment_events(
    name: str,
    namespace: str = "default"
) -> dict:
    """Get Kubernetes events related to a Deployment."""

    try:
        config.load_kube_config()

        core_v1 = client.CoreV1Api()

        events = core_v1.list_namespaced_event(
            namespace=namespace
        )

        result = []

        for event in events.items:
            involved_object = event.involved_object

            if involved_object.name != name:
                continue

            if involved_object.kind != "Deployment":
                continue

            result.append({
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "count": event.count,
                "first_timestamp": (
                    event.first_timestamp.isoformat()
                    if event.first_timestamp
                    else None
                ),
                "last_timestamp": (
                    event.last_timestamp.isoformat()
                    if event.last_timestamp
                    else None
                ),
                "source": (
                    event.source.component
                    if event.source
                    else None
                )
            })

        return {
            "deployment": name,
            "namespace": namespace,
            "event_count": len(result),
            "events": result
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