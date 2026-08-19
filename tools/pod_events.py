from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def get_pod_events(
    pod_name: str,
    namespace: str = "default"
) -> dict:
    """Get Kubernetes events related to a specific pod."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        events = v1.list_namespaced_event(
            namespace=namespace,
            field_selector=f"involvedObject.name={pod_name}"
        )

        result = []

        for event in events.items:
            result.append({
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "count": event.count,
                "first_timestamp": str(event.first_timestamp),
                "last_timestamp": str(event.last_timestamp)
            })

        return {
            "pod": pod_name,
            "namespace": namespace,
            "event_count": len(result),
            "events": result
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