from fastmcp import FastMCP

from tools.pod import list_pods
from tools.namespaces import list_namespaces
from tools.deployments import list_deployments
from tools.replicasets import list_replicasets
from tools.statefulsets import list_statefulsets
from tools.daemonsets import list_daemonsets
from tools.jobs import list_jobs
from tools.services import list_services
from tools.ingresses import list_ingresses
from tools.endpointslices import list_endpoint_slices
from tools.nodes import list_nodes
from tools.events import list_events
from tools.configmaps import list_configmaps
from tools.logs import get_pod_logs
from tools.describe import describe_pod
from tools.pod_events import get_pod_events
from tools.deployment_replicas import deployment_replicas
from tools.deployment_describe import  describe_deployment
from tools.deployment_events import deployment_events
from tools.service_describe import describe_service
from tools.service_endpoints import service_endpoints
from tools.service_events import service_events
from tools.pod_config import pod_config
from tools.secrets import list_secrets
from tools.pvc import list_pvcs
from tools.pv import list_pvs
from tools.resource_usage import pod_resource_usage
from tools.resource_usage import node_resource_usage
from tools.diagnose_pod_failure import diagnose_pod_failure


mcp = FastMCP("Kubernetes MCP Server")


mcp.tool(list_pods)
mcp.tool(list_namespaces)
mcp.tool(list_deployments)
mcp.tool(list_replicasets)
mcp.tool(list_statefulsets)
mcp.tool(list_daemonsets)
mcp.tool(list_jobs)
mcp.tool(list_services)
mcp.tool(list_ingresses)
mcp.tool(list_endpoint_slices)
mcp.tool(list_nodes)
mcp.tool(list_events)
mcp.tool(list_configmaps)
mcp.tool(get_pod_logs)
mcp.tool(describe_pod)
mcp.tool(get_pod_events)
mcp.tool(deployment_replicas)
mcp.tool(describe_deployment)
mcp.tool(deployment_events)
mcp.tool()(describe_service)
mcp.tool()(service_endpoints)
mcp.tool()(service_events)
mcp.tool()(pod_config)
mcp.tool()(list_secrets)
mcp.tool()(list_pvcs)
mcp.tool()(list_pvs)
mcp.tool()(pod_resource_usage)
mcp.tool()(node_resource_usage)
mcp.tool()(diagnose_pod_failure)
if __name__ == "__main__":
    mcp.run()