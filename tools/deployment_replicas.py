from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def deployment_replicas(
    name: str,
    namespace: str = "default"
) -> dict:
    """Collect deployment-level evidence for troubleshooting."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        deployment = apps_v1.read_namespaced_deployment(
            name=name,
            namespace=namespace
        )

        status = deployment.status
        spec = deployment.spec

        return {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "desired_replicas": spec.replicas or 0,
            "updated_replicas": status.updated_replicas or 0,
            "ready_replicas": status.ready_replicas or 0,
            "available_replicas": status.available_replicas or 0,
            "unavailable_replicas": status.unavailable_replicas or 0,
            "strategy": spec.strategy.type,
            "conditions": [
                {
                    "type": condition.type,
                    "status": condition.status,
                    "reason": condition.reason,
                    "message": condition.message
                }
                for condition in (status.conditions or [])
            ]
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