---
title: 部署到 Swarm
keywords: swarm, swarm services, stacks
description: 了解如何在 Docker Swarm 上描述和部署一个简单的应用程序。
aliases:
  - /get-started/part4/
  - /get-started/swarm-deploy/
  - /guides/deployment-orchestration/swarm-deploy/
summary: |
  探索如何使用 Docker Swarm 部署和管理 Docker 容器。
tags: [deploy]
params:
  time: 10 minutes
---

{{% include "swarm-mode.md" %}}

## 先决条件

- 按照 [获取 Docker](/get-started/get-docker.md) 中的描述下载并安装 Docker Desktop。
- 完成 [Docker 研讨会第 2 部分](/get-started/workshop/02_our_app.md) 中的应用程序容器化。
- 通过输入 `docker system info` 并查找消息 `Swarm: active`（你可能需要向上滚动一点），确保你的 Docker Desktop 上已启用 Swarm。

  如果 Swarm 未运行，只需在 shell 提示符下输入 `docker swarm init` 即可进行设置。

## 介绍

既然你已经证明了应用程序的各个组件可以作为独立容器运行，并且展示了如何使用 Kubernetes 部署它，现在你可以看看如何安排它们由 Docker Swarm 管理。Swarm 提供了许多用于扩展、联网、保护和维护容器化应用程序的工具，这些功能超出了容器本身的能力。

为了验证你的容器化应用程序在 Swarm 上运行良好，你将直接在开发机器上使用 Docker Desktop 内置的 Swarm 环境来部署你的应用程序，然后再将其移交给生产环境中的完整 Swarm 集群运行。Docker Desktop 创建的 Swarm 环境功能齐全，这意味着它具有你的应用程序在真实集群上将享有的所有 Swarm 功能，并且可以从你的开发机器方便地访问。

## 使用 stack 文件描述应用程序

Swarm 从不创建像你在本教程上一步中所做的那样创建单独的容器。相反，所有 Swarm 工作负载都被调度为服务（services），这些服务是具有 Swarm 自动维护的附加网络功能的可扩展容器组。此外，所有 Swarm 对象都可以并且应该在称为 stack 文件的清单中进行描述。这些 YAML 文件描述了 Swarm 应用程序的所有组件和配置，并可用于在任何 Swarm 环境中创建和销毁你的应用程序。

现在你可以编写一个简单的 stack 文件来运行和管理你的 Todo 应用程序，即本教程 [第 2 部分](02_our_app.md) 中创建的 `getting-started` 镜像容器。将以下内容放置在名为 `bb-stack.yaml` 的文件中：

{{% include "swarm-compose-compat.md" %}}

```yaml
version: "3.7"

services:
  bb-app:
    image: getting-started
    ports:
      - "8000:3000"
```

在这个 Swarm YAML 文件中，有一个对象，一个 `service`，描述了一组可扩展的相同容器。在这种情况下，你将只得到一个容器（默认值），并且该容器将基于你在本教程 [第 2 部分](02_our_app.md) 中创建的 `getting-started` 镜像。此外，你已要求 Swarm 将到达开发机器端口 8000 的所有流量转发到 getting-started 容器内的端口 3000。

> **Kubernetes Services 和 Swarm Services 非常不同**
>
> 尽管名称相似，但这两个编排器对“服务（service）”一词的含义截然不同。在 Swarm 中，服务提供调度和网络设施，创建容器并提供将流量路由到它们的工具。在 Kubernetes 中，调度和网络是分开处理的，部署（或其他控制器）处理将容器调度为 Pod，而服务仅负责为这些 Pod 添加网络功能。

## 部署并检查你的应用程序

1. 将你的应用程序部署到 Swarm：

   ```console
   $ docker stack deploy -c bb-stack.yaml demo
   ```

   如果一切顺利，Swarm 将报告创建所有 stack 对象且没有任何抱怨：

   ```shell
   Creating network demo_default
   Creating service demo_bb-app
   ```

   请注意，除了你的服务之外，Swarm 默认还会创建一个 Docker 网络，以隔离作为 stack 一部分部署的容器。

2. 通过列出你的服务来确保一切正常：

   ```console
   $ docker service ls
   ```

   如果一切顺利，你的服务将报告其副本已创建 1/1：

   ```shell
   ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
   il7elwunymbs        demo_bb-app         replicated          1/1                 getting-started:latest   *:8000->3000/tcp
   ```

   这表示你作为服务一部分请求的 1/1 个容器已启动并正在运行。此外，你会看到开发机器上的端口 8000 正在转发到 getting-started 容器中的端口 3000。

3. 打开浏览器并访问 `localhost:8000` 上的 Todo 应用程序；你应该看到你的 Todo 应用程序，就像你在本教程 [第 2 部分](02_our_app.md) 中作为独立容器运行它时一样。

4. 满意后，拆除你的应用程序：

   ```console
   $ docker stack rm demo
   ```

## 结论

至此，你已成功使用 Docker Desktop 将应用程序部署到开发机器上功能齐全的 Swarm 环境中。你现在可以向应用程序添加其他组件，并充分利用 Swarm 的所有功能和强大之处，一切都在你自己的机器上进行。

除了部署到 Swarm 之外，你还将应用程序描述为 stack 文件。这个简单的文本文件包含以运行状态创建应用程序所需的一切；你可以将其检入版本控制并与同事共享，从而允许你将应用程序分发到其他集群（如开发环境之后的测试和生产集群）。

## Swarm 和 CLI 参考

本文中使用的所有新 Swarm 对象和 CLI 命令的更多文档可在此处获得：

- [Swarm 模式](/manuals/engine/swarm/_index.md)
- [Swarm 模式服务](/manuals/engine/swarm/how-swarm-mode-works/services.md)
- [Swarm Stacks](/manuals/engine/swarm/stack-deploy.md)
- [`docker stack *`](/reference/cli/docker/stack/)
- [`docker service *`](/reference/cli/docker/service/)
