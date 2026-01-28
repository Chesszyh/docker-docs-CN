---
title: 测试你的 React.js 部署
linkTitle: 测试你的部署
weight: 60
keywords: deploy, kubernetes, react, react.js
description: 了解如何在本地部署以测试和调试你的 Kubernetes 部署

---

## 先决条件

在开始之前，请确保你已完成以下内容：
- 完成本指南的所有前几节，从 [容器化 React.js 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [启用 Kubernetes](/manuals/desktop/features/kubernetes.md#install-and-turn-on-kubernetes)。

> **Kubernetes 新手？**
> 访问 [Kubernetes 基础教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/) 熟悉集群、Pod、部署和服务的工作原理。

---

## 概述

本节指导你使用 [Docker Desktop 的内置 Kubernetes](/desktop/kubernetes/) 在本地部署容器化的 React.js 应用程序。在本地 Kubernetes 集群中运行你的应用程序允许你密切模拟真实的生产环境，使你能够在将工作负载提升到暂存或生产环境之前充满信心地测试、验证和调试它们。

---

## 创建 Kubernetes YAML 文件

按照以下步骤定义你的部署配置：

1. 在项目的根目录下，创建一个名为：reactjs-sample-kubernetes.yaml 的新文件

2. 在你的 IDE 或首选文本编辑器中打开该文件。

3. 添加以下配置，并确保将 `{DOCKER_USERNAME}` 和 `{DOCKERHUB_PROJECT_NAME}` 替换为你之前的 [使用 GitHub Actions 自动化你的构建](configure-github-actions.md) 中的实际 Docker Hub 用户名和存储库名称。


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reactjs-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: reactjs-sample
  template:
    metadata:
      labels:
        app: reactjs-sample
    spec:
      containers:
        - name: reactjs-container
          image: {DOCKER_USERNAME}/{DOCKERHUB_PROJECT_NAME}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name:  reactjs-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app:  reactjs-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

此清单定义了两个关键的 Kubernetes 资源，用 `---` 分隔：

- Deployment
  在 Pod 中部署 React.js 应用程序的单个副本。该 Pod 使用由 GitHub Actions CI/CD 工作流构建并推送的 Docker 镜像
  （请参阅 [使用 GitHub Actions 自动化你的构建](configure-github-actions.md)）。
  容器侦听端口 `8080`，这是 [Nginx](https://nginx.org/en/docs/) 通常用于服务生产 React 应用程序的端口。

- Service (NodePort)
  将部署的 Pod 暴露给你的本地机器。
  它将来自主机端口 `30001` 的流量转发到容器内的端口 `8080`。
  这让你可以在浏览器中通过 [http://localhost:30001](http://localhost:30001) 访问应用程序。

> [!NOTE]
> 要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

---

## 部署并检查你的应用程序

按照以下步骤将容器化的 React.js 应用程序部署到本地 Kubernetes 集群并验证其是否正确运行。

### 第一步：应用 Kubernetes 配置

在终端中，导航到你的 `reactjs-sample-kubernetes.yaml` 文件所在的目录，然后使用以下命令部署资源：

```console
  $ kubectl apply -f reactjs-sample-kubernetes.yaml
```

如果一切配置正确，你将看到 Deployment 和 Service 都已创建的确认信息：

```shell
  deployment.apps/reactjs-sample created
  service/reactjs-sample-service created
```
   
此输出意味着 Deployment 和 Service 都已成功创建，并且正在本地集群内运行。

### 第二步：检查部署状态

运行以下命令检查部署的状态：
   
```console
  $ kubectl get deployments
```

你应该看到类似以下的输出：

```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  reactjs-sample       1/1     1            1           14s
```

这确认了你的 Pod 已启动并运行，并且有一个副本可用。

### 第三步：验证服务暴露

检查 NodePort 服务是否将你的应用程序暴露给本地机器：

```console
$ kubectl get services
```

你应该看到类似以下内容：

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
reactjs-sample-service   NodePort    10.100.244.65    <none>        8080:30001/TCP   1m
```

此输出确认你的应用程序已通过 NodePort 在端口 30001 上可用。

### 第四步：在浏览器中访问你的应用程序

打开浏览器并导航到 [http://localhost:30001](http://localhost:30001)。

你应该看到生产就绪的 React.js 示例应用程序正在运行 —— 由你的本地 Kubernetes 集群提供服务。

### 第五步：清理 Kubernetes 资源

完成测试后，你可以使用以下命令删除部署和服务：

```console
  $ kubectl delete -f reactjs-sample-kubernetes.yaml
```

预期输出：

```shell
  deployment.apps "reactjs-sample" deleted
  service "reactjs-sample-service" deleted
```

这确保了你的集群保持清洁并准备好进行下一次部署。
   
---

## 总结

在本节中，你学习了如何使用 Docker Desktop 将 React.js 应用程序部署到本地 Kubernetes 集群。此设置允许你在将容器化应用程序部署到云之前，在类似生产的环境中对其进行测试和调试。

你完成了什么：

- 为你的 React.js 应用程序创建了 Kubernetes Deployment 和 NodePort Service
- 使用 `kubectl apply` 在本地部署了应用程序
- 验证了应用程序正在运行且可在 `http://localhost:30001` 访问
- 测试后清理了 Kubernetes 资源

---

## 相关资源

探索官方参考和最佳实践以磨练你的 Kubernetes 部署工作流程：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 了解核心概念、工作负载、服务等。
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md) – 使用 Docker Desktop 的内置 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用 Deployments 管理和扩展应用程序。
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 了解如何向内部和外部流量暴露你的应用程序。
