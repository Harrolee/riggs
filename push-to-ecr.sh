#!/bin/bash

TAG=$1
AWS_SSO_PROFILE=personal-lee
ECR_URI=310753928788.dkr.ecr.us-east-2.amazonaws.com

aws ecr get-login-password --region us-east-2 --profile "$AWS_SSO_PROFILE" | docker login --username AWS --password-stdin "$ECR_URI"

docker buildx build . --platform=linux/amd64  --push      \
-t "$ECR_URI/riggs/promomaker:latest"                     \
-t "$ECR_URI/drive-gooder-final:$TAG"