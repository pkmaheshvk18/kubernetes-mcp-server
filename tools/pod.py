from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_pods(namespace: str = "default") -> dict:
    """List pods in a Kubernetes namespace with status and node information."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pods = v1.list_namespaced_pod(namespace=namespace)

        result = []

        for pod in pods.items:
            result.append({
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name
            })

        return {
            "namespace": namespace,
            "pod_count": len(result),
            "pods": result
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