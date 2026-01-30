---
description: Swarm 节点如何工作
keywords: docker, container, cluster, swarm mode, node, 容器, 集群, 节点
title: 节点如何工作
weight: 10
aliases:
- /engine/swarm/how-swarm-mode-works/
---

Swarm 模式允许您创建一个或多个 Docker Engine 组成的集群，称为 Swarm。Swarm 由一个或多个节点 (运行 Docker Engine 的物理机或虚拟机) 组成。

节点有两种类型：[管理节点 (managers)](#manager-nodes) 和 [工作节点 (workers)](#worker-nodes)。

![Swarm 模式集群](/engine/swarm/images/swarm-diagram.webp)

如果您还没有阅读过，请阅读 [Swarm 模式概览](../_index.md) 和 [核心概念](../key-concepts.md)。

## 管理节点 (Manager nodes)

管理节点处理集群管理任务：

* 维护集群状态
* 调度服务
* 提供 Swarm 模式 [HTTP API 端点](/reference/api/engine/_index.md)

通过使用 [Raft](https://raft.github.io/raft.pdf) 协议实现，管理节点维护整个 Swarm 及其上运行的所有服务的一致内部状态。出于测试目的，运行只有一个管理节点的 Swarm 是可以的。如果单管理节点 Swarm 中的管理节点出现故障，您的服务仍会继续运行，但您需要创建一个新集群才能恢复。

为了利用 Swarm 模式的容错特性，我们建议您根据组织的可用性要求实施奇数个节点。当您有多个管理节点时，您可以从管理节点故障中恢复而无需停机。

* 一个三管理节点的 Swarm 最多容忍丢失一个管理节点。
* 一个五管理节点的 Swarm 最多容忍同时丢失两个管理节点。
* 集群中奇数个管理节点 `N` 最多允许丢失 `(N-1)/2` 个管理节点。Docker 建议一个 Swarm 最多部署七个管理节点。

    > [!IMPORTANT]
    >
    > 添加更多的管理节点并不意味着增加可扩展性或更高的性能。通常情况下，情况恰恰相反。

## 工作节点 (Worker nodes)

工作节点也是 Docker Engine 实例，其唯一目的是执行容器。工作节点不参与 Raft 分布式状态维护、不做出调度决策，也不提供 Swarm 模式 HTTP API 服务。

您可以创建一个只有一个管理节点的 Swarm，但如果没有至少一个管理节点，您就不能拥有工作节点。默认情况下，所有管理节点也都是工作节点。在只有单个管理节点的集群中，您可以运行类似 `docker service create` 的命令，调度程序会将所有任务放置在本地 Engine 上。

为了防止调度程序在多节点 Swarm 的管理节点上放置任务，请将管理节点的可用性设置为 `Drain`。调度程序会优雅地停止处于 `Drain` 模式的节点上的任务，并在 `Active` 节点上调度这些任务。调度程序不会向具有 `Drain` 可用性的节点分配新任务。

参考 [`docker node update`](/reference/cli/docker/node/update.md) 命令行参考，了解如何更改节点可用性。

## 更改角色 (Change roles)

您可以通过运行 `docker node promote` 将工作节点提升为管理节点。例如，当您将一个管理节点脱机维护时，可能需要提升一个工作节点。参见 [node promote](/reference/cli/docker/node/promote.md)。

您也可以将管理节点降级为工作节点。参见 [node demote](/reference/cli/docker/node/demote.md)。


## 了解更多

* 阅读 Swarm 模式 [服务 (services)](services.md) 如何工作。
* 了解 [PKI](pki.md) 在 Swarm 模式下如何工作。
