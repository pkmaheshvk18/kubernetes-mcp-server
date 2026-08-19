from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def pod_resource_usage(namespace: str = "default") -> dict:
    """Get current CPU and memory usage for pods."""

    try:
        config.load_kube_config()

        custom_objects = client.CustomObjectsApi()

        metrics = custom_objects.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )

        result = []

        for pod in metrics.get("items", []):
            containers = []

            total_cpu = 0
            total_memory = 0

            for container in pod.get("containers", []):
                usage = container.get("usage", {})

                cpu = usage.get("cpu", "0")
                memory = usage.get("memory", "0")

                containers.append({
                    "name": container.get("name"),
                    "cpu": cpu,
                    "memory": memory
                })

            result.append({
                "name": pod["metadata"]["name"],
                "namespace": pod["metadata"]["namespace"],
                "containers": containers
            })

        return {
            "namespace": namespace,
            "pod_count": len(result),
            "pods": result
        }

    except ApiException as e:
        return {
            "error": f"Kubernetes Metrics API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }


def node_resource_usage() -> dict:
    """Get current CPU and memory usage for Kubernetes nodes."""

    try:
        config.load_kube_config()

        custom_objects = client.CustomObjectsApi()

        metrics = custom_objects.list_cluster_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            plural="nodes"
        )

        result = []

        for node in metrics.get("items", []):
            usage = node.get("usage", {})

            result.append({
                "name": node["metadata"]["name"],
                "cpu": usage.get("cpu", "0"),
                "memory": usage.get("memory", "0")
            })

        return {
            "node_count": len(result),
            "nodes": result
        }

    except ApiException as e:
        return {
            "error": f"Kubernetes Metrics API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }