from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def describe_service(
    name: str,
    namespace: str = "default"
) -> dict:
    """Get detailed information about a Kubernetes Service."""

    try:
        config.load_kube_config()

        core_v1 = client.CoreV1Api()

        service = core_v1.read_namespaced_service(
            name=name,
            namespace=namespace
        )

        ports = []

        for port in service.spec.ports or []:
            ports.append({
                "name": port.name,
                "protocol": port.protocol,
                "port": port.port,
                "target_port": str(port.target_port),
                "node_port": port.node_port
            })

        return {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
            "cluster_ip": service.spec.cluster_ip,
            "external_ips": service.spec.external_i_ps or [],
            "selector": service.spec.selector or {},
            "session_affinity": service.spec.session_affinity,
            "ports": ports
        }

    except ApiException as e:
        if e.status == 404:
            return {
                "error": f"Service '{name}' not found in namespace '{namespace}'."
            }

        return {
            "error": f"Kubernetes API error: {e.reason}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }