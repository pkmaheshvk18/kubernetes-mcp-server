from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


def list_jobs(namespace: str = "default") -> dict:
    """List Jobs in a Kubernetes namespace."""

    try:
        config.load_kube_config()

        batch_v1 = client.BatchV1Api()

        jobs = batch_v1.list_namespaced_job(
            namespace=namespace
        )

        result = []

        for job in jobs.items:
            result.append({
                "name": job.metadata.name,
                "namespace": job.metadata.namespace,
                "active": job.status.active or 0,
                "succeeded": job.status.succeeded or 0,
                "failed": job.status.failed or 0
            })

        return {
            "namespace": namespace,
            "job_count": len(result),
            "jobs": result
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