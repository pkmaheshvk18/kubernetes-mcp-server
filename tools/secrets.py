from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_secrets(namespace: str = "default") -> dict:
    """List Kubernetes Secrets without exposing secret values."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        secrets = v1.list_namespaced_secret(
            namespace=namespace
        )

        result = []

        for secret in secrets.items:
            result.append({
                "name": secret.metadata.name,
                "namespace": secret.metadata.namespace,
                "type": secret.type,
                "data_key_count": len(secret.data or {})
            })

        return {
            "namespace": namespace,
            "secret_count": len(result),
            "secrets": result
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