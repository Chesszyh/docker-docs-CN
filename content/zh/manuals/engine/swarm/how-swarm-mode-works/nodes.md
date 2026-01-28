---
description: How swarm nodes work
keywords: docker, container, cluster, swarm mode, node
title: 节点工作原理
weight: 10
aliases:
- /engine/swarm/how-swarm-mode-works/
---

Swarm 模式允许你创建一个由一个或多个 Docker 引擎组成的集群，称为 swarm。一个 swarm 由一个或多个节点（node）组成：运行 Docker 引擎的物理机或虚拟机。

节点有两种类型：[管理节点（manager）](#manager-nodes)和[工作节点（worker）](#worker-nodes)。

![Swarm mode cluster](/engine/swarm/images/swarm-diagram.webp)

如果你还没有阅读过，请先阅读 [Swarm 模式概述](../_index.md)和[关键概念](../key-concepts.md)。

## 管理节点

管理节点负责处理集群管理任务：

* 维护集群状态
* 调度服务
* 提供 Swarm 模式 [HTTP API 端点](/reference/api/engine/_index.md)

管理节点使用 [Raft](https://raft.github.io/raft.pdf) 实现来维护整个 swarm 及其上运行的所有服务的一致内部状态。出于测试目的，使用单个管理节点运行 swarm 是可以的。如果单管理节点 swarm 中的管理节点发生故障，你的服务会继续运行，但你需要创建一个新的集群来恢复。

为了利用 Swarm 模式的容错功能，我们建议你根据组织的高可用性要求实施奇数个节点。当你拥有多个管理节点时，你可以在不停机的情况下从管理节点故障中恢复。

* 一个三管理节点的 swarm 最多可以容忍一个管理节点的丢失。
* 一个五管理节点的 swarm 最多可以同时容忍两个管理节点的丢失。
* 集群中奇数 `N` 个管理节点最多可以容忍 `(N-1)/2` 个管理节点的丢失。
Docker 建议一个 swarm 最多使用七个管理节点。

    > [!IMPORTANT]
    >
    > 添加更多管理节点并不意味着可扩展性增加或性能提高。通常情况恰恰相反。

## 工作节点

工作节点也是 Docker 引擎的实例，其唯一目的是执行容器。工作节点不参与 Raft 分布式状态、不做调度决策，也不提供 swarm 模式 HTTP API。

你可以创建一个只有一个管理节点的 swarm，但如果没有至少一个管理节点，你就不能拥有工作节点。默认情况下，所有管理节点也是工作节点。在单管理节点集群中，你可以运行 `docker service create` 等命令，调度器会将所有任务放在本地引擎上。

要防止调度器在多节点 swarm 中将任务放置在管理节点上，请将管理节点的可用性设置为 `Drain`。调度器会优雅地停止处于 `Drain` 模式的节点上的任务，并将任务调度到 `Active` 状态的节点上。调度器不会将新任务分配给可用性为 `Drain` 的节点。

请参阅 [`docker node update`](/reference/cli/docker/node/update.md) 命令行参考了解如何更改节点可用性。

## 更改角色

你可以通过运行 `docker node promote` 将工作节点提升为管理节点。例如，当你需要将管理节点下线进行维护时，你可能希望提升一个工作节点。参见 [node promote](/reference/cli/docker/node/promote.md)。

你也可以将管理节点降级为工作节点。参见 [node demote](/reference/cli/docker/node/demote.md)。


## 了解更多

* 阅读了解 Swarm 模式[服务](services.md)的工作原理。
* 了解 [PKI](pki.md) 在 Swarm 模式中的工作原理。
