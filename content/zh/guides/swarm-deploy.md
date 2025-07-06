---
title: 部署到 Swarm
keywords: swarm, swarm 服务, 堆栈
description: 了解如何描述和部署一个简单的 Docker Swarm 应用程序。
aliases:
  - /get-started/part4/
  - /get-started/swarm-deploy/
  - /guides/deployment-orchestration/swarm-deploy/
summary: |
  了解如何使用 Docker Swarm 部署和管理 Docker 容器。
tags: [deploy]
params:
  time: 10 分钟
---

{{% include "swarm-mode.md" %}}

## 先决条件

- 按照[获取 Docker](/get-started/get-docker.md) 中的说明下载并安装 Docker Desktop。
- 在 [Docker 研讨会第 2 部分](/get-started/workshop/02_our_app.md)中完成应用程序的容器化
- 通过键入 `docker system info` 并查找消息 `Swarm: active`（您可能需要向上滚动一点）来确保在您的 Docker Desktop 上启用了 Swarm。

  如果 Swarm 未运行，只需在 shell 提示符下键入 `docker swarm init` 即可进行设置。

## 简介

现在您已经证明了应用程序的各个组件可以作为独立的容器运行，并展示了如何使用 Kubernetes 进行部署，您可以看看如何安排它们由 Docker Swarm 管理。Swarm 提供了许多用于扩展、联网、保护和维护您的容器化应用程序的工具，这些工具超出���容器本身的能力。

为了验证您的容器化应用程序在 Swarm 上运行良好，您将在您的开发机器上使用 Docker Desktop 内置的 Swarm 环境来部署您的应用程序，然后再将其交给在生产环境中的完整 Swarm 集群上运行。Docker Desktop 创建的 Swarm 环境是功能齐全的，这意味着它具有您的应用程序在真实集群上将享有的所有 Swarm 功能，并且可以从您的开发机器方便地访问。

## 使用堆栈文件描述应用程序

Swarm 从不像您在本教程的上一步中所做的那样创建单个容器。相反，所有 Swarm 工作负载都作为服务进行调度，服务是具有 Swarm 自动维护的附加网络功能的可扩展容器组。此外，所有 Swarm 对象都可以并且应该在称为堆栈文件的清单中进行描述。这些 YAML 文件描述了您的 Swarm 应用程序的所有组件和配置，并且可以用于在任何 Swarm 环境中创建和销毁您的应用程序。

现在，您可以编写一个简单的堆栈文件来运行和管理您的 Todo 应用程序，即在教程的[第 2 部分](02_our_app.md)中创建的容器 `getting-started` 镜像。将以下内容放在一个名为 `bb-stack.yaml` 的文件中：

{{% include "swarm-compose-compat.md" %}}

```yaml
version: "3.7"

services:
  bb-app:
    image: getting-started
    ports:
      - "8000:3000"
```

在这个 Swarm YAML 文件中，有一个对象，一个 `service`，描述一个可扩展的相同容器组。在这种情况下，您将只得到一个容器（默认值），并且该容器将基于您在教程的[第 2 部分](02_our_app.md)中创建的 `getting-started` 镜像。此外，您已要求 Swarm 将到达您开发机器上端口 8000 的所有流量转发到我们的 getting-started 容器内的端口 3000。

> **Kubernetes 服务和 Swarm 服务非常不同**
>
> 尽管名称相似，但这两个编排器对
> “服务”一词的含义却大相径庭。在 Swarm 中，服务提供调度和
> 网络功能，创建容器并提供用于将
> 流量路由到它们的工具。在 Kubernetes 中，调度和网络是分开处理的
> ，部署（或其他控制器）处理
> 容器作为 pod 的调度，而服务仅负责向
> 这些 pod 添加网络功能。

## 部署和检查您的应用程序

1. 将您的应用程序部署到 Swarm：

   ```console
   $ docker stack deploy -c bb-stack.yaml demo
   ```

   如果一切顺利，Swarm 将报告创建了所有堆栈对象，并且没有任何抱怨：

   ```shell
   Creating network demo_default
   Creating service demo_bb-app
   ```

   请注意，除了您的服务之外，Swarm 默认情况下还会创建一个 Docker 网络，以隔离作为堆栈一部分部署的容器。

2. 通过列出您的服务来确保一切正常：

   ```console
   $ docker service ls
   ```

   如果一切顺利，您的服务将报告其 1/1 个副本已创建：

   ```shell
   ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
   il7elwunymbs        demo_bb-app         replicated          1/1                 getting-started:latest   *:8000->3000/tcp
   ```

   这表示您作为服务一部分要求的 1/1 个容器已启动并正在运行。此外，您会看到开发机器上的端口 8000 正在转发到您的 getting-started 容器中的端口 3000。

3. 打开浏览器并访问您的 Todo 应用程序，地址为 `localhost:8000`；您应该会看到您的 Todo 应用程序，与您在教程的[第 2 部分](02_our_app.md)中将其作为独立容器运行时相同。

4. 满意后，拆除您的应用程序：

   ```console
   $ docker stack rm demo
   ```

## 结论

此时，您已成功使用 Docker Desktop 将您的应用程序部署到您开发机器上功能齐全的 Swarm 环境中。您现在可以向您的应用程序添加其他组件，并利用 Swarm 的所有功能和强大功能，就在您自己的机器上。

除了部署��� Swarm 之外，您还已将您的应用程序描述为堆栈文件。这个简单的文本文件包含创建处于运行状态的应用程序所需的一切；您可以将其签入版本控制并与您的同事共享，从而可以将您的应用程序分发到其他集群（例如可能在您的开发环境之后的测试和生产集群）。

## Swarm 和 CLI 参考

本文中使用的所有新 Swarm 对象和 CLI 命令的进一步文档可在此处获得：

- [Swarm 模式](/manuals/engine/swarm/_index.md)
- [Swarm 模式服务](/manuals/engine/swarm/how-swarm-mode-works/services.md)
- [Swarm 堆栈](/manuals/engine/swarm/stack-deploy.md)
- [`docker stack *`](/reference/cli/docker/stack/)
- [`docker service *`](/reference/cli/docker/service/)
