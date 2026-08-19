from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def service_endpoints(
    name: str,
    namespace: str = "default"
) -> dict:
    """Get backend endpoints associated with a Kubernetes Service."""

    try:
        config.load_kube_config()

        discovery_v1 = client.DiscoveryV1Api()

        endpoint_slices = discovery_v1.list_namespaced_endpoint_slice(
            namespace=namespace,
            label_selector=f"kubernetes.io/service-name={name}"
        )

        endpoints = []

        for slice_obj in endpoint_slices.items:
            for endpoint in slice_obj.endpoints:

                conditions = endpoint.conditions

                addresses = endpoint.addresses or []

                endpoints.append({
                    "addresses": addresses,
                    "ready": conditions.ready if conditions else None,
                    "serving": conditions.serving if conditions else None,
                    "terminating": conditions.terminating if conditions else None,
                    "node_name": endpoint.node_name,
                    "target_ref": {
                        "kind": endpoint.target_ref.kind,
                        "name": endpoint.target_ref.name,
                        "namespace": endpoint.target_ref.namespace
                    } if endpoint.target_ref else None
                })

        return {
            "service": name,
            "namespace": namespace,
            "endpoint_slice_count": len(endpoint_slices.items),
            "endpoint_count": len(endpoints),
            "endpoints": endpoints
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