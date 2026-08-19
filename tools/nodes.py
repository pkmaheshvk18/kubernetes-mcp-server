from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_nodes() -> dict:
    """List Kubernetes nodes with status and resource information."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        nodes = v1.list_node()

        result = []

        for node in nodes.items:
            conditions = {}

            for condition in node.status.conditions or []:
                conditions[condition.type] = condition.status

            result.append({
                "name": node.metadata.name,
                "kubernetes_version": node.status.node_info.kubelet_version,
                "os": node.status.node_info.os_image,
                "architecture": node.status.node_info.architecture,
                "ready": conditions.get("Ready"),
                "cpu": node.status.capacity.get("cpu"),
                "memory": node.status.capacity.get("memory")
            })

        return {
            "node_count": len(result),
            "nodes": result
        }

    except ApiException as e:
        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }