from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_replicasets(namespace: str = "default") -> dict:
    """List ReplicaSets in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        replicasets = apps_v1.list_namespaced_replica_set(
            namespace=namespace
        )

        result = []

        for rs in replicasets.items:
            result.append({
                "name": rs.metadata.name,
                "namespace": rs.metadata.namespace,
                "desired_replicas": rs.spec.replicas,
                "ready_replicas": rs.status.ready_replicas or 0,
                "available_replicas": rs.status.available_replicas or 0
            })

        return {
            "namespace": namespace,
            "replicaset_count": len(result),
            "replicasets": result
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