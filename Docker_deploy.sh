#!/bin/bash

# Usage: ./CloudRun_deploy.sh {GCP_ID} {SERVICE} v{VERSION}

PROJECT=$1
SERVICE=$2
VERSION=$3
IMAGE=europe-west1-docker.pkg.dev/"$PROJECT"/eu-west1/"$SERVICE"/"$VERSION"

# --------------------------
# Build Docker image
# --------------------------
docker build --platform linux/amd64 \
  -t "$PROJECT-$SERVICE:$VERSION" \
  -t $IMAGE \
  .

buildStatus="$?"
if [[ $buildStatus -eq 1 ]]; then
  echo "Build failed"
  exit $buildStatus
fi

# --------------------------
# Push to Artifact Registry
# --------------------------
echo "Pushing image: $IMAGE"
docker push "$IMAGE"

# --------------------------
# Deploy to Cloud Run (service, not job)
# --------------------------
echo "Deploying to Cloud Run"
gcloud run deploy "$PROJECT"-"$SERVICE" --image "$IMAGE" --region "europe-west1" --project "$PROJECT" --service-account=rag-chat@mwm-cb-workspace.iam.gserviceaccount.com

