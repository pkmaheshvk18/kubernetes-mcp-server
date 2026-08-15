from fastmcp import FastMCP
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

mcp = FastMCP("Kubernetes MCP Server")


@mcp.tool
def list_pods(namespace: str = "default") -> dict:
    """List pods in a Kubernetes namespace with status and node information."""

    try:
        # Load the user's Kubernetes kubeconfig
        config.load_kube_config()

        # Create Kubernetes Core API client
        v1 = client.CoreV1Api()

        # Get pods from the requested namespace
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


if __name__ == "__main__":
    mcp.run()