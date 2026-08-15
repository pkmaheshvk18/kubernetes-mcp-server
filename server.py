from fastmcp import FastMCP

from tools.pod import list_pods
from tools.namespaces import list_namespaces


mcp = FastMCP("Kubernetes MCP Server")


mcp.tool(list_pods)
mcp.tool(list_namespaces)

if __name__ == "__main__":
    mcp.run()