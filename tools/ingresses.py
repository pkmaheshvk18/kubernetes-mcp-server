from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_ingresses(namespace: str = "default") -> dict:
    """List Ingresses in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        networking_v1 = client.NetworkingV1Api()

        ingresses = networking_v1.list_namespaced_ingress(
            namespace=namespace
        )

        result = []

        for ingress in ingresses.items:
            result.append({
                "name": ingress.metadata.name,
                "namespace": ingress.metadata.namespace,
                "class_name": (
                    ingress.spec.ingress_class_name
                    if ingress.spec
                    else None
                ),
                "hosts": [
                    rule.host
                    for rule in (ingress.spec.rules or [])
                    if rule.host
                ]
            })

        return {
            "namespace": namespace,
            "ingress_count": len(result),
            "ingresses": result
        }

    except ApiException as e:
        if e.status == 404:
            return {"error": f"Namespace '{namespace}' not found."}

        return {"error": f"Kubernetes API error: {e.reason}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}