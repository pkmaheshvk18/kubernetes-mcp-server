from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def get_pod_logs(
    pod_name: str,
    namespace: str = "default",
    tail_lines: int = 100,
    previous: bool = False
) -> dict:
    """Get current or previous container logs from a Kubernetes pod."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            previous=previous
        )

        return {
            "pod": pod_name,
            "namespace": namespace,
            "tail_lines": tail_lines,
            "previous": previous,
            "logs": logs
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