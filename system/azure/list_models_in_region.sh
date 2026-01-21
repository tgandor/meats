#!/bin/bash

REGION=${REGION:-swedencentral}

echo "Models in $REGION (use REGION env var to change)"

az rest --method get \
  --uri "https://management.azure.com/subscriptions/$(az account show --query id -o tsv)/providers/Microsoft.CognitiveServices/locations/${REGION}/models?api-version=2024-10-01" \
  --query "value[].{format:model.format,name:model.name,version:model.version,sku:skuName}" \
  -o table

