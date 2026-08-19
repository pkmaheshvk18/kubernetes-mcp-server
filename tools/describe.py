from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def describe_pod(
    pod_name: str,
    namespace: str = "default"
) -> dict:
    """Get detailed information about a Kubernetes pod."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pod = v1.read_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )

        containers = []

        for container in pod.spec.containers:
            containers.append({
                "name": container.name,
                "image": container.image,
                "image_pull_policy": container.image_pull_policy
            })

        container_statuses = []

        for status in pod.status.container_statuses or []:
            container_statuses.append({
                "name": status.name,
                "ready": status.ready,
                "restart_count": status.restart_count,
                "state": str(status.state),
                "last_state": str(status.last_state)
            })

        return {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "node": pod.spec.node_name,
            "phase": pod.status.phase,
            "pod_ip": pod.status.pod_ip,
            "containers": containers,
            "container_statuses": container_statuses
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