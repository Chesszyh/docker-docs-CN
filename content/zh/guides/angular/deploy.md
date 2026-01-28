---
title: 测试您的 Angular 部署
linkTitle: 测试您的部署
weight: 60
keywords: deploy, kubernetes, angular
description: 了解如何在本地部署以测试和调试您的 Kubernetes 部署

---

## 前提条件

在开始之前，请确保您已完成以下内容：
- 完成本指南的所有前面章节，从[容器化 Angular 应用程序](containerize.md)开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

> **Kubernetes 新手？**
> 访问 [Kubernetes 基础教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/) 熟悉集群、Pod、部署和服务的工作原理。

---

## 概述

本节将指导您使用 [Docker Desktop 内置的 Kubernetes](/desktop/kubernetes/) 在本地部署容器化的 Angular 应用程序。在本地 Kubernetes 集群中运行应用程序可以紧密模拟真实的生产环境，使您能够在将工作负载推广到预发布或生产环境之前，自信地测试、验证和调试。

---

## 创建 Kubernetes YAML 文件

按照以下步骤定义您的部署配置：

1. 在项目根目录中，创建一个名为 angular-sample-kubernetes.yaml 的新文件

2. 在 IDE 或首选文本编辑器中打开该文件。

3. 添加以下配置，并确保将 `{DOCKER_USERNAME}` 和 `{DOCKERHUB_PROJECT_NAME}` 替换为您在前面[使用 GitHub Actions 自动化构建](configure-github-actions.md)中使用的实际 Docker Hub 用户名和仓库名称。


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: angular-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: angular-sample
  template:
    metadata:
      labels:
        app: angular-sample
    spec:
      containers:
        - name: angular-container
          image: {DOCKER_USERNAME}/{DOCKERHUB_PROJECT_NAME}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
            requests:
              cpu: "250m"
              memory: "128Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: angular-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: angular-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

此清单定义了两个关键的 Kubernetes 资源，由 `---` 分隔：

- Deployment（部署）
  在 Pod 中部署 Angular 应用程序的单个副本。Pod 使用由 GitHub Actions CI/CD 工作流程构建和推送的 Docker 镜像
  （参考[使用 GitHub Actions 自动化构建](configure-github-actions.md)）。
  容器监听端口 `8080`，这通常是 [Nginx](https://nginx.org/en/docs/) 用于提供生产 Angular 应用程序服务的端口。

- Service（服务，NodePort 类型）
  将部署的 Pod 暴露给您的本地机器。
  它将来自主机端口 `30001` 的流量转发到容器内的端口 `8080`。
  这允许您在浏览器中通过 [http://localhost:30001](http://localhost:30001) 访问应用程序。

> [!NOTE]
> 要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

---

## 部署并检查您的应用程序

按照以下步骤将容器化的 Angular 应用程序部署到本地 Kubernetes 集群，并验证它是否正常运行。

### 步骤 1. 应用 Kubernetes 配置

在终端中，导航到 `angular-sample-kubernetes.yaml` 文件所在的目录，然后使用以下命令部署资源：

```console
  $ kubectl apply -f angular-sample-kubernetes.yaml
```

如果一切配置正确，您将看到确认 Deployment 和 Service 都已创建的消息：

```shell
  deployment.apps/angular-sample created
  service/angular-sample-service created
```

这确认 Deployment 和 Service 都已成功创建，现在正在本地集群中运行。

### 步骤 2. 检查 Deployment 状态

运行以下命令检查部署的状态：

```console
  $ kubectl get deployments
```

您应该看到类似以下的输出：

```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  angular-sample       1/1     1            1           14s
```

这确认您的 Pod 已启动并运行，有一个可用的副本。

### 步骤 3. 验证 Service 暴露

检查 NodePort 服务是否将您的应用程序暴露给本地机器：

```console
$ kubectl get services
```

您应该看到类似以下的内容：

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
angular-sample-service   NodePort    10.100.185.105    <none>        8080:30001/TCP   1m
```

此输出确认您的应用程序可通过端口 30001 上的 NodePort 访问。

### 步骤 4. 在浏览器中访问您的应用程序

打开浏览器并导航到 [http://localhost:30001](http://localhost:30001)。

您应该看到生产就绪的 Angular 示例应用程序正在运行 — 由您的本地 Kubernetes 集群提供服务。

### 步骤 5. 清理 Kubernetes 资源

测试完成后，您可以使用以下命令删除部署和服务：

```console
  $ kubectl delete -f angular-sample-kubernetes.yaml
```

预期输出：

```shell
  deployment.apps "angular-sample" deleted
  service "angular-sample-service" deleted
```

这确保您的集群保持干净，为下一次部署做好准备。

---

## 总结

在本节中，您学习了如何使用 Docker Desktop 将 Angular 应用程序部署到本地 Kubernetes 集群。此设置允许您在部署到云之前在类生产环境中测试和调试容器化应用程序。

您完成的内容：

- 为 Angular 应用程序创建了 Kubernetes Deployment 和 NodePort Service
- 使用 `kubectl apply` 在本地部署应用程序
- 验证应用程序正在运行并可在 `http://localhost:30001` 访问
- 测试后清理了 Kubernetes 资源

---

## 相关资源

探索官方参考和最佳实践以优化您的 Kubernetes 部署工作流程：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 了解核心概念、工作负载、服务等。
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md) – 使用 Docker Desktop 内置的 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用 Deployment 管理和扩展应用程序。
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 了解如何将应用程序暴露给内部和外部流量。
