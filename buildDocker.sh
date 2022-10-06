#!/bin/bash

eval $(minikube docker-env)
docker build -t eiachh/resource-limiter ./