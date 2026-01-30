---
description: Swarm 模式下的 Raft 一致性算法
keywords: docker, container, cluster, swarm, raft, 容器, 集群
title: Swarm 模式下的 Raft 一致性
---

当 Docker Engine 在 Swarm 模式下运行时，管理节点 (manager nodes) 实现了 [Raft 一致性算法 (Raft Consensus Algorithm)](http://thesecretlivesofdata.com/raft/) 来管理全局集群状态。

Swarm 模式使用一致性算法的原因是为了确保负责管理和调度集群中任务的所有管理节点都存储着相同的、一致的状态。

在整个集群中保持相同的一致状态意味着在发生故障的情况下，任何管理节点都可以接管任务并将服务恢复到稳定状态。例如，如果负责在集群中调度任务的 Leader 管理节点意外宕机，任何其他管理节点都可以接管调度任务并重新平衡任务以匹配期望状态。

在分布式系统中使用一致性算法来复制日志的系统确实需要特别注意。它们通过要求大多数节点对值达成一致，确保集群状态在存在故障的情况下保持一致。

Raft 最多允许 `(N-1)/2` 个节点故障，并要求大多数节点 (即法定人数 quorum，数量为 `(N/2)+1`) 对提议给集群的值达成一致。这意味着在一个由 5 个运行 Raft 的管理节点组成的集群中，如果 3 个节点不可用，系统将无法再处理调度额外任务的请求。现有任务会继续运行，但如果管理节点集合不健康，调度程序将无法重新平衡任务以应对故障。

Swarm 模式中一致性算法的实现意味着它具备了分布式系统固有的特性：

- 在容错系统中对值达成一致。(参考 [FLP 不可能性定理](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/) 以及 [Raft 一致性算法论文](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf))
- 通过领导者选举过程实现互斥
- 集群成员管理
- 全局一致的对象排序和 CAS (compare-and-swap) 原语
