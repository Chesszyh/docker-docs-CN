---
description: Docker Engine Swarm 模式概览
keywords: docker, container, cluster, swarm, docker engine, 容器, 集群
title: Swarm 模式
weight: 80
aliases:
- /api/swarm-api/
- /engine/userguide/networking/overlay-standalone-swarm/
- /network/overlay-standalone.swarm/
- /release-notes/docker-swarm/
- /swarm/
- /swarm/api/
- /swarm/configure-tls/
- /swarm/discovery/
- /swarm/get-swarm/
- /swarm/install-manual/
- /swarm/install-w-machine/
- /swarm/multi-host-networking/
- /swarm/multi-manager-setup/
- /swarm/networking/
- /swarm/overview/
- /swarm/plan-for-production/
- /swarm/provision-with-machine/
- /swarm/reference/
- /swarm/reference/create/
- /swarm/reference/help/
- /swarm/reference/join/
- /swarm/reference/list/
- /swarm/reference/manage/
- /swarm/reference/swarm/
- /swarm/release-notes/
- /swarm/scheduler/
- /swarm/scheduler/filter/
- /swarm/scheduler/rescheduling/
- /swarm/scheduler/strategy/
- /swarm/secure-swarm-tls/
- /swarm/status-code-comparison-to-docker/
- /swarm/swarm-api/
- /swarm/swarm_at_scale/
- /swarm/swarm_at_scale/02-deploy-infra/
- /swarm/swarm_at_scale/03-create-cluster/
- /swarm/swarm_at_scale/04-deploy-app/
- /swarm/swarm_at_scale/about/
- /swarm/swarm_at_scale/deploy-app/
- /swarm/swarm_at_scale/deploy-infra/
- /swarm/swarm_at_scale/troubleshoot/
---

{{% include "swarm-mode.md" %}}

当前版本的 Docker 包含 Swarm 模式，用于原生管理 Docker Engine 集群 (称为 Swarm)。使用 Docker CLI 可以创建 Swarm、将应用程序服务部署到 Swarm 以及管理 Swarm 行为。

Docker Swarm 模式内置在 Docker Engine 中。请勿将 Docker Swarm 模式与 [Docker Classic Swarm](https://github.com/docker/classicswarm) 混淆，后者已不再积极开发。

## 功能亮点

### 集成在 Docker Engine 中的集群管理

使用 Docker Engine CLI 创建 Docker Engine 集群，并在其中部署应用程序服务。您不需要额外的编排软件来创建或管理 Swarm。

### 去中心化设计

Docker Engine 在运行时处理节点角色的专门化，而不是在部署时区分。您可以使用 Docker Engine 部署管理节点 (managers) 和工作节点 (workers) 这两类节点。这意味着您可以从单个磁盘镜像构建整个 Swarm。

### 声明式服务模型

Docker Engine 采用声明式方法，让您定义应用程序栈中各种服务的期望状态。例如，您可以描述一个由带有消息队列服务和数据库后端的 Web 前端服务组成的应用程序。

### 扩展 (Scaling)

对于每个服务，您可以声明想要运行的任务数量。当您向上或向下扩展时，Swarm 管理节点会自动通过添加或删除任务来维持期望状态。

### 期望状态协调 (Reconciliation)

Swarm 管理节点会持续监控集群状态，并协调实际状态与您表达的期望状态之间的任何差异。例如，如果您设置一个服务运行 10 个容器副本，而托管其中两个副本的工作机器崩溃了，管理节点会创建两个新副本以替换崩溃的副本。管理节点会将新副本分配给正在运行且可用的工作节点。

### 多主机联网 (Multi-host networking)

您可以为服务指定 overlay 网络。当 Swarm 管理节点初始化或更新应用程序时，会自动为 overlay 网络上的容器分配地址。

### 服务发现 (Service discovery)

Swarm 管理节点为 Swarm 中的每个服务分配一个唯一的 DNS 名称，并对运行中的容器进行负载均衡。您可以通过 Swarm 内部集成的 DNS 服务器查询 Swarm 中运行的每个容器。

### 负载均衡 (Load balancing)

您可以将服务的端口暴露给外部负载均衡器。在内部，Swarm 允许您指定如何在节点之间分配服务容器。

### 默认安全 (Secure by default)

Swarm 中的每个节点都强制执行 TLS 双向身份验证和加密，以确保其与所有其他节点之间的通信安全。您可以选择使用自签名根证书或来自自定义根 CA 的证书。

### 滚动更新 (Rolling updates)

在发布时，您可以增量地对节点应用服务更新。Swarm 管理节点允许您控制服务部署到不同节点组之间的延迟。如果出现任何问题，您可以回滚到服务的先前版本。

## 下一步

* 学习 Swarm 模式的 [核心概念](key-concepts.md)。
* 通过 [Swarm 模式教程](swarm-tutorial/_index.md) 入门。
* 探索 Swarm 模式 CLI 命令
  * [swarm init](/reference/cli/docker/swarm/init.md)
  * [swarm join](/reference/cli/docker/swarm/join.md)
  * [service create](/reference/cli/docker/service/create.md)
  * [service inspect](/reference/cli/docker/service/inspect.md)
  * [service ls](/reference/cli/docker/service/ls.md)
  * [service rm](/reference/cli/docker/service/rm.md)
  * [service scale](/reference/cli/docker/service/scale.md)
  * [service ps](/reference/cli/docker/service/ps.md)
  * [service update](/reference/cli/docker/service/update.md)
