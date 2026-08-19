from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_endpoint_slices(namespace: str = "default") -> dict:
    """List EndpointSlices in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        discovery_v1 = client.DiscoveryV1Api()

        endpoint_slices = discovery_v1.list_namespaced_endpoint_slice(
            namespace=namespace
        )

        result = []

        for slice_obj in endpoint_slices.items:
            endpoints = []

            for endpoint in slice_obj.endpoints:
                endpoints.append({
                    "addresses": endpoint.addresses,
                    "ready": endpoint.conditions.ready
                })

            result.append({
                "name": slice_obj.metadata.name,
                "namespace": slice_obj.metadata.namespace,
                "address_type": slice_obj.address_type,
                "endpoints": endpoints
            })

        return {
            "namespace": namespace,
            "endpoint_slice_count": len(result),
            "endpoint_slices": result
        }

    except ApiException as e:
        if e.status == 404:
            return {"error": f"Namespace '{namespace}' not found."}

        return {"error": f"Kubernetes API error: {e.reason}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}