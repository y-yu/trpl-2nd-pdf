#!/bin/bash

set -ex

if [[ "${TRAVIS_OS_NAME}" == "linux" && "${TRAVIS_BRANCH}" == "master" && "${TRAVIS_PULL_REQUEST}" == "false" ]]; then
  docker login -u "$REGISTRY_USER" -p "$REGISTRY_PASSWORD"
  docker tag "$IMAGE_NAME" "${IMAGE_NAME}:latest"
  docker push "${IMAGE_NAME}:latest"
fi
