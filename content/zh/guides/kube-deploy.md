---
title: 部署到 Kubernetes
keywords: kubernetes, pod, 部署, kubernetes 服务
description: 了解如何描述和部署一个简单的 Kubernetes 应用程序。
aliases:
  - /get-started/kube-deploy/
  - /guides/deployment-orchestration/kube-deploy/
summary: |
  了解如何使用 Kubernetes 部署和编排 Docker 容器。
tags: [deploy]
params:
  time: 10 分钟
---

## 先决条件

- 按照[获取 Docker](/get-started/get-docker.md) 中的说明下载并安装 Docker Desktop。
- 在[第 2 部分](02_our_app.md)中完成应用程序的容器化。
- 确保在 Docker Desktop 中已启用 Kubernetes：
  如果 Kubernetes 未运行，请按照[编排](orchestration.md)中的说明完成设置。

## 简介

现在您已经证明了应用程序的各个组件可以作为独立的容器运行，是时候安排它们由像 Kubernetes 这样的编排器来管理了。Kubernetes 提供了许多用于扩展、联网、保护和维护您的容器化应用程序的工具，这些工具超出了容器本身的能力。

为了验证您的容器化应用程序在 Kubernetes 上运行良好，您将在您的开发���器上使用 Docker Desktop 内置的 Kubernetes 环境来部署您的应用程序，然后再将其交给在生产环境中的完整 Kubernetes 集群上运行。Docker Desktop 创建的 Kubernetes 环境是_功能齐全的_，这意味着它具有您的应用程序在真实集群上将享有的所有 Kubernetes 功能，并且可以从您的开发机器方便地访问。

## 使用 Kubernetes YAML 描述应用程序

Kubernetes 中的所有容器都作为 pod 进行调度，pod 是共享某些资源的共存容器组。此外，在实际应用程序中，您几乎从不创建单个 pod。相反，您的大部分工作负载都作为部署进行调度，部署是 Kubernetes 自动维护的可扩展 pod 组。最后，所有 Kubernetes 对象都可以并且应该在称为 Kubernetes YAML 文件的清单中进行描述。这些 YAML 文件描述了您的 Kubernetes 应用程序的所有组件和配置，并且可以用于在任何 Kubernetes 环境中创建和销毁您的应用程序。

您已经在���教程的编排概述部分编写了一个基本的 Kubernetes YAML 文件。现在，您可以编写一个稍微复杂一些的 YAML 文件来运行和管理您的 Todo 应用程序，即在快速入门教程的[第 2 部分](02_our_app.md)中创建的容器 `getting-started` 镜像。将以下内容放在一个名为 `bb.yaml` 的文件中：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bb-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      bb: web
  template:
    metadata:
      labels:
        bb: web
    spec:
      containers:
        - name: bb-site
          image: getting-started
          imagePullPolicy: Never
---
apiVersion: v1
kind: Service
metadata:
  name: bb-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    bb: web
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，用 `---` 分隔：

- 一个 `Deployment`，描述一个可扩展的相同 pod 组。在这种情况下，您将只得到一个 `replica`，即您的 pod 的一个副本，并且该 pod（在 `template:` 键下描述）中只有一个容器，基于您在本教程上一步中创建的 `getting-started` 镜像。
- 一个 `NodePort` 服务，它将把来自您主机上端口 30001 的流量路由到它所路由到的 pod 内的端口 3000，从而允许您从网络访问您的 Todo 应用程序。

此外，请注意，虽然 Kubernetes YAML 最初可能看起来很长很复杂，但它几乎总是遵循相同的模式：

- `apiVersion`，指示解析此对象的 Kubernetes API
- `kind`，指示这是哪种对象
- 一些 `metadata`，将名称等应用于您的对象
- `spec`，指定您的对象的所有参数和配置。

## 部署和检查您的应用程序

1. 在终端中，导航到您创建 `bb.yaml` 的位置，并将您的应用程序部署到 Kubernetes：

   ```console
   $ kubectl apply -f bb.yaml
   ```

   您应该会看到类似于以下的输出，表明您的 Kubernetes 对象已成功创建：

   ```shell
   deployment.apps/bb-demo created
   service/bb-entrypoint created
   ```

2. 通过列出您的部署来确保一切正常：

   ```console
   $ kubectl get deployments
   ```

   如果一切顺利，您的部署应如下所示：

   ```shell
   NAME      READY   UP-TO-DATE   AVAILABLE   AGE
   bb-demo   1/1     1            1           40s
   ```

   这表明您在 YAML 中要求的所有一个 pod 都已启动并正在运行。对您的服务执行相同的检查：

   ```console
   $ kubectl get services

   NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   bb-entrypoint   NodePort    10.106.145.116   <none>        3000:30001/TCP   53s
   kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          138d
   ```

   除了默认的 `kubernetes` 服务之外，我们还看到了我们的 `bb-entrypoint` 服务，它在端口 30001/TCP 上��受流量。

3. 打开浏览器并访问您的 Todo 应用程序，地址为 `localhost:30001`。您应该会看到您的 Todo 应用程序，与您在教程的[第 2 部分](02_our_app.md)中将其作为独立容器运行时相同。

4. 满意后，拆除您的应用程序：

   ```console
   $ kubectl delete -f bb.yaml
   ```

## 结论

此时，您已成功使用 Docker Desktop 将您的应用程序部署到您开发机器上功能齐全的 Kubernetes 环境中。您现在可以向您的应用程序添加其他组件，并利用 Kubernetes 的所有功能和强大功能，就在您自己的机器上。

除了部署到 Kubernetes 之外，您还已将您的应用程序描述为 Kubernetes YAML 文件。这个简单的文本文件包含创建处于运行状态的应用程序所需的一切。您可以将其签入版本控制并与您的同事共享。这使您可以将您的应用程序分发到其他集群（例如可能在您的开发环境之后的测试和生产集群）。

## Kubernetes 参考

本文中使用的所有新 Kubernetes 对象的进一步文档可在此处获得：

- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
