#!/bin/bash

echo "Starting teardown of billable resources..."
read -p "This will delete your GKE cluster and VM. Are you sure? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
# 1. Delete the GKE Cluster
# This removes the control plane and all Autopilot-managed pods/nodes.
gcloud container clusters delete hyperion --region us-west2 --quiet

# 2. Delete the Database VM
# Using 'delete' instead of 'stop' ensures you aren't charged for the 10GB-50GB SSD disk.
gcloud compute instances delete postgres --zone us-west1-b	 --quiet

# 3. Clean up orphaned Load Balancers
# GKE Ingresses often leave behind Forwarding Rules that cost ~$18/month.
echo "Checking for remaining Load Balancer rules..."
gcloud compute forwarding-rules list

# 4. Release Unused Static External IPs
# Google charges for reserved IPs that are NOT currently attached to a resource.
echo "Checking for orphaned Static IPs..."
gcloud compute addresses list
