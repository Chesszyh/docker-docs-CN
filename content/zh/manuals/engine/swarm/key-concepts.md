---
description: 介绍 Docker Engine Swarm 模式的核心概念
keywords: docker, container, cluster, swarm mode, docker engine, 核心概念, Swarm 模式
title: Swarm 模式核心概念
---

本主题介绍了 Docker Engine 1.12 中特有的集群管理和编排功能的一些概念。

## 什么是 Swarm？

Docker Engine 中嵌入的集群管理和编排功能是使用 [swarmkit](https://github.com/docker/swarmkit/) 构建的。Swarmkit 是一个独立的项目，实现了 Docker 的编排层，并直接在 Docker 内部使用。

Swarm 由多个运行在 Swarm 模式下的 Docker 主机组成，这些主机分别充当管理节点 (managers，用于管理成员身份和授权) 和工作节点 (workers，运行 [Swarm 服务](#services-and-tasks))。给定的 Docker 主机可以作为管理节点、工作节点，或者同时担任这两个角色。当您创建服务时，您定义了它的最佳状态 —— 副本数量、可用的网络和存储资源、服务向外界暴露的端口等。Docker 会致力于维持这种期望状态。例如，如果一个工作节点变得不可用，Docker 会将该节点的任务调度到其他节点上。任务 (task) 是一个正在运行的容器，它是 Swarm 服务的一部分，由 Swarm 管理节点管理，这与独立容器 (standalone container) 不同。

与独立容器相比，Swarm 服务的一个关键优势是您可以修改服务的配置，包括它连接的网络和卷，而无需手动重启服务。Docker 会更新配置，停止配置过时的服务任务，并创建符合期望配置的新任务。

当 Docker 以 Swarm 模式运行时，您仍然可以在参与 Swarm 的任何 Docker 主机上运行独立容器，以及运行 Swarm 服务。独立容器和 Swarm 服务之间的一个关键区别是，只有 Swarm 管理节点可以管理 Swarm，而独立容器可以在任何守护进程上启动。Docker 守护进程可以作为管理节点、工作节点或两者兼而有之参与 Swarm。

正如您可以使用 [Docker Compose](/manuals/compose/_index.md) 定义和运行容器一样，您也可以定义和运行 [Swarm 服务](services.md) 栈。

继续阅读以了解与 Docker Swarm 服务相关的概念，包括节点、服务、任务和负载均衡。

## 节点 (Nodes)

节点 (node) 是参与 Swarm 的 Docker Engine 实例。您也可以将其视为 Docker 节点。您可以在单个物理计算机或云服务器上运行一个或多个节点，但生产环境的 Swarm 部署通常包括分布在多个物理和云机器上的 Docker 节点。

要将应用程序部署到 Swarm，您需要向管理节点提交服务定义。管理节点将被称为 [任务 (tasks)](#services-and-tasks) 的工作单元分发给工作节点。

管理节点还执行维持 Swarm 期望状态所需的编排和集群管理功能。管理节点会选出一个 Leader 来执行编排任务。

工作节点接收并执行从管理节点分发而来的任务。默认情况下，管理节点也作为工作节点运行服务，但您可以将其配置为仅运行管理任务，成为专用管理节点。每个工作节点上都运行着一个代理 (agent)，并向其汇报分配给它的任务。工作节点会通知管理节点其分配任务的当前状态，以便管理节点可以维持每个工作节点的期望状态。

## 服务与任务 (Services and tasks)

服务 (service) 是指在管理节点或工作节点上执行的任务的定义。它是 Swarm 系统的核心结构，也是用户与 Swarm 交互的主要根源。

创建服务时，您需要指定使用哪个容器镜像以及在运行的容器内部执行哪些命令。

在“复制服务 (replicated services)”模型中，Swarm 管理节点根据您在期望状态中设置的规模，在节点之间分配特定数量的副本任务。

对于“全局服务 (global services)”，Swarm 在集群中的每个可用节点上运行该服务的一个任务。

任务 (task) 承载着一个 Docker 容器以及在容器内运行的命令。它是 Swarm 的原子调度单位。管理节点根据服务规模中设置的副本数量，将任务分配给工作节点。任务一旦分配给某个节点，就不能移动到另一个节点。它只能在分配的节点上运行或运行失败。

## 负载均衡 (Load balancing)

Swarm 管理节点使用入口负载均衡 (ingress load balancing) 来暴露您希望在 Swarm 外部可用的服务。Swarm 管理节点可以自动为服务分配一个发布端口 (published port)，或者您可以为服务配置一个发布端口。您可以指定任何未使用的端口。如果您不指定端口，Swarm 管理节点会为服务分配一个 30000-32767 范围内的端口。

外部组件 (如云负载均衡器) 可以通过集群中任何节点的发布端口访问该服务，无论该节点当前是否正在运行该服务的任务。Swarm 中的所有节点都会将入站连接路由到正在运行的任务实例。

Swarm 模式具有一个内部 DNS 组件，它会自动为 Swarm 中的每个服务分配一个 DNS 条目。Swarm 管理节点使用内部负载均衡，根据服务的 DNS 名称在集群内部的服务之间分发请求。

## 下一步

* 阅读 [Swarm 模式概览](index.md)。
* 通过 [Swarm 模式教程](swarm-tutorial/_index.md) 入门。
