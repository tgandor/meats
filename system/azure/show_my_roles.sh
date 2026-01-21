#!/bin/bash

az role assignment list --assignee $(az account show --query user.name -o tsv) --output table
