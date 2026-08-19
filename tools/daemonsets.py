from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_daemonsets(namespace: str = "default") -> dict:
    """List DaemonSets in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        daemonsets = apps_v1.list_namespaced_daemon_set(
            namespace=namespace
        )

        result = []

        for ds in daemonsets.items:
            result.append({
                "name": ds.metadata.name,
                "namespace": ds.metadata.namespace,
                "desired_nodes": ds.status.desired_number_scheduled or 0,
                "current_nodes": ds.status.current_number_scheduled or 0,
                "ready_nodes": ds.status.number_ready or 0,
                "available_nodes": ds.status.number_available or 0
            })

        return {
            "namespace": namespace,
            "daemonset_count": len(result),
            "daemonsets": result
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