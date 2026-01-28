---
description: Docker Engine Swarm mode overview
keywords: docker, container, cluster, swarm, docker engine
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

当前版本的 Docker 包含 Swarm 模式，用于原生管理一组 Docker Engine 集群，称为 swarm（集群）。使用 Docker CLI 来创建 swarm、将应用服务部署到 swarm，以及管理 swarm 的行为。

Docker Swarm 模式内置于 Docker Engine 中。请勿将 Docker Swarm 模式与 [Docker Classic Swarm](https://github.com/docker/classicswarm) 混淆，后者已不再积极开发。

## 功能亮点

### 与 Docker Engine 集成的集群管理

使用 Docker Engine CLI 来创建 Docker Engine 的 swarm，您可以在其中部署应用服务。您不需要额外的编排软件来创建或管理 swarm。

### 去中心化设计

Docker Engine 不是在部署时处理节点角色的差异，而是在运行时处理任何专业化配置。您可以使用 Docker Engine 部署两种类型的节点：管理节点（manager）和工作节点（worker）。这意味着您可以从单个磁盘镜像构建整个 swarm。

### 声明式服务模型

Docker Engine 使用声明式方法，让您定义应用栈中各种服务的期望状态。例如，您可以描述一个由 Web 前端服务、消息队列服务和数据库后端组成的应用。

### 伸缩

对于每个服务，您可以声明要运行的任务数量。当您扩展或缩减时，swarm 管理节点会通过添加或移除任务来自动适应以维持期望状态。

### 期望状态协调

swarm 管理节点持续监控集群状态，并协调实际状态与您声明的期望状态之间的任何差异。例如，如果您设置一个服务运行 10 个容器副本，而托管其中两个副本的工作机器崩溃了，管理节点会创建两个新副本来替换崩溃的副本。swarm 管理节点会将新副本分配给正在运行且可用的工作节点。

### 多主机网络

您可以为服务指定 overlay 网络。当 swarm 管理节点初始化或更新应用时，它会自动为 overlay 网络上的容器分配地址。

### 服务发现

Swarm 管理节点为 swarm 中的每个服务分配唯一的 DNS 名称，并对运行的容器进行负载均衡。您可以通过 swarm 中内嵌的 DNS 服务器查询 swarm 中运行的每个容器。

### 负载均衡

您可以将服务的端口暴露给外部负载均衡器。在内部，swarm 允许您指定如何在节点之间分发服务容器。

### 默认安全

swarm 中的每个节点都强制执行 TLS 双向认证和加密，以保护其自身与所有其他节点之间的通信安全。您可以选择使用自签名根证书或来自自定义根 CA 的证书。

### 滚动更新

在发布时，您可以将服务更新增量应用到节点。swarm 管理节点允许您控制服务部署到不同节点组之间的延迟时间。如果出现任何问题，您可以回滚到服务的先前版本。

## 下一步

* 学习 Swarm 模式的[核心概念](key-concepts.md)。
* 开始学习 [Swarm 模式教程](swarm-tutorial/_index.md)。
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
