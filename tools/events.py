from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_events(namespace: str = "default") -> dict:
    """List Kubernetes events in a namespace."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        events = v1.list_namespaced_event(
            namespace=namespace
        )

        result = []

        for event in events.items:
            result.append({
                "name": event.metadata.name,
                "namespace": event.metadata.namespace,
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "object": (
                    event.involved_object.name
                    if event.involved_object
                    else None
                ),
                "object_kind": (
                    event.involved_object.kind
                    if event.involved_object
                    else None
                )
            })

        return {
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