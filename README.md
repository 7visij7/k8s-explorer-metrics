# Explorer-metrics
> Prometheus exporter for Php-fpm, Beanstalk, Gearman, Memcached and Supervisord servers metric which runs in K8S cluster.
> Application gets list of pods in cluster and depends on name try to get metrics for this service.
> Idea is two conteiners works togehter in one pod with shared volume, one container collects metric and store it in file, other container works like API and responde with set of metrics from preperad file.
---

## Required variables and config
> Required enviroment variables: 
+ K8S_HOST - url to API K8S

Also you can change [port](https://github.com/7visij7/k8s-explorer-metrics/blob/main/explorer/config/__init__.py) for app.

[Here](https://github.com/7visij7/k8s-explorer-metrics/blob/main/explorer/config/swagger.yaml) is configuration for swagger.

---
## Docker
> Build Docker image from a [Dockerfile](https://github.com/7visij7/k8s-explorer-metrics/blob/main/Dockerfile)
```
docker build -t IMAGE_NAME
```
---

## Kubernetes

> Deploy to kubernetes cluster.
```Bash
kubectl create namespace monitoring
kubectl apply -f k8s/ -n namespace monitoring
```
---

## Jenkins pipelins

>  Change for you configuration next parameters in [Jenkinsfile](https://github.com/7visij7/k8s-explorer-metrics/blob/main/Jenkinsfile):
+ REGISTRY = 'registry.company.com'
+ REGCREDS = 'registry-admin-jenkins'
+ KUBECONFIG = path_to_creds
+ IMAGE_NAME = 'IMAGE_NAME'

