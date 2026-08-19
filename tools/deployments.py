from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_deployments(namespace: str = "default") -> dict:
    """List deployments in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        deployments = apps_v1.list_namespaced_deployment(
            namespace=namespace
        )

        result = []

        for deployment in deployments.items:
            result.append({
                "name": deployment.metadata.name,
                "namespace": deployment.metadata.namespace,
                "replicas": deployment.spec.replicas,
                "available_replicas": deployment.status.available_replicas or 0,
                "ready_replicas": deployment.status.ready_replicas or 0
            })

        return {
            "namespace": namespace,
            "deployment_count": len(result),
            "deployments": result
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