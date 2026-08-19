from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def describe_deployment(
    name: str,
    namespace: str = "default"
) -> dict:
    """Get detailed information about a Kubernetes Deployment."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        deployment = apps_v1.read_namespaced_deployment(
            name=name,
            namespace=namespace
        )

        containers = []

        for container in deployment.spec.template.spec.containers:
            containers.append({
                "name": container.name,
                "image": container.image,
                "image_pull_policy": container.image_pull_policy,
                "ports": [
                    {
                        "container_port": port.container_port,
                        "protocol": port.protocol
                    }
                    for port in (container.ports or [])
                ]
            })

        return {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "labels": deployment.metadata.labels or {},
            "annotations": deployment.metadata.annotations or {},
            "replicas": deployment.spec.replicas or 0,
            "strategy": deployment.spec.strategy.type,
            "selector": deployment.spec.selector.match_labels or {},
            "containers": containers
        }

    except ApiException as e:
        if e.status == 404:
            return {
                "error": f"Deployment '{name}' not found in namespace '{namespace}'."
            }

        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }