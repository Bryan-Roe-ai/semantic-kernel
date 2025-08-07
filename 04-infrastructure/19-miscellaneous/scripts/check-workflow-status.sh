#!/bin/bash

# Function to check the status of a workflow
check_workflow_status() {
  local workflow_id=$1
  local run_id=$2
  local status=$(gh run view $run_id --json status --jq '.status')

  echo "Workflow ID: $workflow_id, Run ID: $run_id, Status: $status"
  echo $status
}

# Function to retry a workflow
retry_workflow() {
  local workflow_id=$1
  local run_id=$2
  local retries=0
  local max_retries=3

  while [ $retries -lt $max_retries ]; do
    status=$(check_workflow_status $workflow_id $run_id)
    if [ "$status" == "completed" ]; then
      echo "Workflow $workflow_id completed successfully."
      return 0
    else
      echo "Retrying workflow $workflow_id (Attempt $((retries + 1))/$max_retries)..."
      gh workflow run $workflow_id
      retries=$((retries + 1))
      sleep 10
    fi
  done

  echo "Workflow $workflow_id failed after $max_retries attempts."
  return 1
}

# Get the list of workflows
workflows=$(gh workflow list --json name,id --jq '.[] | {name: .name, id: .id}')

# Iterate through each workflow and check its status
for workflow in $(echo "$workflows" | jq -c '.'); do
  workflow_id=$(echo "$workflow" | jq -r '.id')
  workflow_name=$(echo "$workflow" | jq -r '.name')

  echo "Checking status of workflow: $workflow_name (ID: $workflow_id)"

  # Get the latest run ID for the workflow
  run_id=$(gh run list --workflow $workflow_id --json databaseId --jq '.[0].databaseId')

  if [ -n "$run_id" ]; then
    retry_workflow $workflow_id $run_id
  else
    echo "No runs found for workflow: $workflow_name"
  fi
done
