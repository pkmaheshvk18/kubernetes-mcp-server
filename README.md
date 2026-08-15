# Kubernetes MCP Server

A custom Kubernetes Model Context Protocol (MCP) server built with Python, FastMCP, and the Kubernetes Python Client.

This project allows an MCP-compatible AI client such as Claude Desktop to interact with a Kubernetes cluster through controlled tools.

## Architecture

```text
Claude Desktop
      |
      | MCP Protocol
      v
Kubernetes MCP Server
      |
      | FastMCP
      v
Python Kubernetes Client
      |
      | Kubernetes API
      v
Minikube / Kubernetes Cluster