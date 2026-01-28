---
title: 测试您的 Deno 部署
linkTitle: 测试您的部署
weight: 50
keywords: deploy, kubernetes, deno
description: 学习如何使用 Kubernetes 进行本地开发
aliases:
- /language/deno/deploy/
---

## 前提条件

- 完成本指南的所有前置章节，从[容器化 Deno 应用程序](containerize.md)开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals//desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将应用程序部署到开发机器上功能完整的 Kubernetes 环境中。这使您可以在部署之前在本地的 Kubernetes 上测试和调试工作负载。

## 创建 Kubernetes YAML 文件

在您的 `deno-docker` 目录中，创建一个名为
`docker-kubernetes.yml` 的文件。在 IDE 或文本编辑器中打开该文件并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker 用户名和您在[为 Deno 应用程序配置 CI/CD](configure-ci-cd.md)中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-deno-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: deno-api
  template:
    metadata:
      labels:
        app: deno-api
    spec:
      containers:
       - name: deno-api
         image: DOCKER_USERNAME/REPO_NAME
         imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    app: deno-api
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

 - 一个 Deployment（部署），描述一组可扩展的相同 Pod。在这种情况下，
   您将只获得一个副本，即 Pod 的一个副本。该 Pod 在 `template` 下描述，其中只有一个容器。该容器是由[为 Deno 应用程序配置 CI/CD](configure-ci-cd.md)中 GitHub Actions 构建的镜像创建的。
 - 一个 NodePort 服务，它将流量从主机的 30001 端口路由到它所路由的 Pod 内部的 8000 端口，使您可以从网络访问应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查您的应用程序

1. 在终端中，导航到 `deno-docker` 并将应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-kubernetes.yml
   ```

   您应该看到类似以下的输出，表明您的 Kubernetes 对象已成功创建。

   ```text
   deployment.apps/docker-deno-demo created
   service/service-entrypoint created
   ```

2. 通过列出部署来确保一切正常工作。

   ```console
   $ kubectl get deployments
   ```

   您的部署应该如下所示：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE    AGE
   docker-deno-demo       1/1     1            1           10s
   ```

   这表明您在 YAML 中请求的所有 Pod 都已启动并运行。对服务进行同样的检查。

   ```console
   $ kubectl get services
   ```

   您应该得到类似以下的输出。

   ```shell
   NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
   service-entrypoint   NodePort    10.105.145.223   <none>        8000:30001/TCP   83s
   ```

   除了默认的 `kubernetes` 服务外，您可以看到您的 `service-entrypoint` 服务，在 30001/TCP 端口接受流量。

3. 在浏览器中，访问以下地址。您应该看到消息 `{"Status" : "OK"}`。

   ```console
   http://localhost:30001/
   ```

4. 运行以下命令来清除您的应用程序。

   ```console
   $ kubectl delete -f docker-kubernetes.yml
   ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将 Deno 应用程序部署到开发机器上功能完整的 Kubernetes 环境中。

相关信息：
   - [Kubernetes 文档](https://kubernetes.io/docs/home/)
   - [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)
   - [Swarm 模式概述](/manuals/engine/swarm/_index.md)
