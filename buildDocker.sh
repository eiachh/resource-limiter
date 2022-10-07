#!/bin/bash

eval $(minikube docker-env)
docker build -t eiachh/resource-limiter ./
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)