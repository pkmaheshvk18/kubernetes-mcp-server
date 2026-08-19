from tools.describe import describe_pod
from tools.pod_events import get_pod_events
from tools.logs import get_pod_logs
from tools.pod_config import pod_config
from tools.resource_usage import pod_resource_usage
from tools.pvc import list_pvcs


def diagnose_pod_failure(
    pod_name: str,
    namespace: str = "default",
    tail_lines: int = 100
) -> dict:
    """Collect Kubernetes evidence for troubleshooting a Pod failure."""

    evidence = {
        "pod": pod_name,
        "namespace": namespace,
        "pod_details": None,
        "events": None,
        "current_logs": None,
        "previous_logs": None,
        "configuration": None,
        "resource_usage": None,
        "pvcs": None
    }

    # 1. Pod details
    try:
        evidence["pod_details"] = describe_pod(
            pod_name=pod_name,
            namespace=namespace
        )
    except Exception as e:
        evidence["pod_details"] = {
            "error": f"Failed to collect pod details: {str(e)}"
        }

    # 2. Pod events
    try:
        evidence["events"] = get_pod_events(
            pod_name=pod_name,
            namespace=namespace
        )
    except Exception as e:
        evidence["events"] = {
            "error": f"Failed to collect pod events: {str(e)}"
        }

    # 3. Current container logs
    try:
        evidence["current_logs"] = get_pod_logs(
            pod_name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            previous=False
        )
    except Exception as e:
        evidence["current_logs"] = {
            "error": f"Failed to collect current logs: {str(e)}"
        }

    # 4. Previous container logs
    try:
        evidence["previous_logs"] = get_pod_logs(
            pod_name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            previous=True
        )
    except Exception as e:
        evidence["previous_logs"] = {
            "error": f"Failed to collect previous logs: {str(e)}"
        }

    # 5. ConfigMap and Secret references
    try:
        evidence["configuration"] = pod_config(
            pod_name=pod_name,
            namespace=namespace
        )
    except Exception as e:
        evidence["configuration"] = {
            "error": f"Failed to collect configuration references: {str(e)}"
        }

    # 6. Pod resource usage
    try:
        evidence["resource_usage"] = pod_resource_usage(
            namespace=namespace
        )
    except Exception as e:
        evidence["resource_usage"] = {
            "error": f"Failed to collect resource usage: {str(e)}"
        }

    # 7. PVC information
    try:
        evidence["pvcs"] = list_pvcs(
            namespace=namespace
        )
    except Exception as e:
        evidence["pvcs"] = {
            "error": f"Failed to collect PVC information: {str(e)}"
        }

    return {
        "pod": pod_name,
        "namespace": namespace,
        "evidence": evidence
    }