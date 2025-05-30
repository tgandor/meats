#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

for remote in $(git remote); do
    if git ls-remote --exit-code --heads "$remote" "$branch" > /dev/null 2>&1; then
        echo "Pushing to $remote/$branch"
        git push "$remote" "$branch"
    else
        echo "Skipping $remote — branch '$branch' not found"
    fi
done
