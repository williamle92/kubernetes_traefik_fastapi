#!/bin/bash
# Delete the cluster to stop all compute charges immediately
gcloud container clusters delete backend-cluster --region us-west2 --quiet

# Optional: List images to remind yourself to delete old versions if needed
gcloud artifacts docker images list us-west2-docker.pkg.dev/fastapi-celery-traefik/hyperion
