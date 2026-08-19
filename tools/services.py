from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_services(namespace: str = "default") -> dict:
    """List Services in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        services = v1.list_namespaced_service(
            namespace=namespace
        )

        result = []

        for service in services.items:
            result.append({
                "name": service.metadata.name,
                "namespace": service.metadata.namespace,
                "type": service.spec.type,
                "cluster_ip": service.spec.cluster_ip,
                "ports": [
                    {
                        "port": port.port,
                        "target_port": str(port.target_port),
                        "protocol": port.protocol
                    }
                    for port in service.spec.ports
                ]
            })

        return {
            "namespace": namespace,
            "service_count": len(result),
            "services": result
        }

    except ApiException as e:
        if e.status == 404:
            return {"error": f"Namespace '{namespace}' not found."}

        return {"error": f"Kubernetes API error: {e.reason}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}