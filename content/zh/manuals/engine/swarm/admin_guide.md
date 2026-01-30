---
description: 管理节点管理指南
keywords: docker, container, swarm, manager, raft, 容器, 管理节点
title: 管理和维护 Docker Engine Swarm
aliases:
- /engine/swarm/manager-administration-guide/
---

当您运行 Docker Engine Swarm 集群时，管理节点 (manager nodes) 是管理 Swarm 和存储 Swarm 状态的关键组件。了解管理节点的一些关键特性对于正确部署和维护 Swarm 至关重要。

参考 [节点如何工作](how-swarm-mode-works/nodes.md) 获取 Docker Swarm 模式的简要概览以及管理节点与工作节点 (worker nodes) 之间的区别。

## 在 Swarm 中操作管理节点

Swarm 管理节点使用 [Raft 一致性算法 (Raft Consensus Algorithm)](raft.md) 来管理 Swarm 状态。您只需要了解 Raft 的一些通用概念即可管理 Swarm。

管理节点的数量没有限制。实施多少个管理节点是在性能和容错性之间的权衡。向 Swarm 添加管理节点会使 Swarm 的容错性更高。然而，额外的管理节点会降低写入性能，因为必须有更多的节点确认更新 Swarm 状态的提议。这意味着更多的网络往返流量。

Raft 要求大多数管理节点 (也称为法定人数 quorum) 达成一致，才能对 Swarm 进行提议的更新，例如节点的添加或移除。成员操作受状态复制相同的约束。

### 维持管理节点的法定人数 (Quorum)

如果 Swarm 失去了管理节点的法定人数，Swarm 将无法执行管理任务。如果您的 Swarm 有多个管理节点，请始终保持两个以上。要维持法定人数，必须有大多数管理节点可用。建议使用奇数个管理节点，因为下一个偶数并不会使法定人数更容易维持。例如，无论您有 3 个还是 4 个管理节点，您都只能失去 1 个管理节点并维持法定人数。如果您有 5 个还是 6 个管理节点，您仍然只能失去两个。

即使 Swarm 失去了管理节点的法定人数，现有工作节点上的 Swarm 任务仍会继续运行。但是，无法添加、更新或移除 Swarm 节点，也无法启动、停止、移动或更新新任务或现有任务。

如果您确实失去了管理节点的法定人数，请参阅 [从失去法定人数中恢复](#recover-from-losing-the-quorum) 了解故障排查步骤。

## 配置管理节点在静态 IP 地址上通告

在初始化 Swarm 时，必须指定 `--advertise-addr` 标志，以便向 Swarm 中的其他管理节点通告您的地址。有关更多信息，请参阅 [在 Swarm 模式下运行 Docker Engine](swarm-mode.md#configure-the-advertise-address)。由于管理节点应该是基础设施中的稳定组件，因此您应该为通告地址使用 *固定 IP 地址*，以防止 Swarm 在机器重启时变得不稳定。

如果整个 Swarm 重启，且每个管理节点随后都获得了一个新的 IP 地址，那么任何节点都无法联系到现有的管理节点。因此，当节点尝试在旧 IP 地址处相互联系时，Swarm 会挂起。

工作节点可以使用动态 IP 地址。

## 添加管理节点以提高容错能力

您应该在 Swarm 中维持奇数个管理节点，以支持管理节点故障。拥有奇数个管理节点可以确保在发生网络分区时，如果网络被分成两部分，法定人数仍有较高概率可用于处理请求。如果您遇到两个以上的网络分区，则无法保证维持法定人数。

| Swarm 大小 |  大多数 (法定人数)  |  容错能力  |
|:------------:|:----------:|:-----------------:|
|      1       |     1      |         0         |
|      2       |     2      |         0         |
|    **3**     |     2      |       **1**       |
|      4       |     3      |         1         |
|    **5**     |     3      |       **2**       |
|      6       |     4      |         2         |
|    **7**     |     4      |       **3**       |
|      8       |     5      |         3         |
|    **9**     |     5      |       **4**       |

例如，在具有 *5 个节点* 的 Swarm 中，如果您失去了 *3 个节点*，您就没有法定人数了。因此，在您恢复其中一个不可用的管理节点或通过灾难恢复命令恢复 Swarm 之前，您无法添加或移除节点。参见 [从灾难中恢复](#recover-from-disaster)。

虽然可以将 Swarm 缩减到单个管理节点，但无法降级最后一个管理节点。这确保了您能够维持对 Swarm 的访问，并且 Swarm 仍然可以处理请求。将 Swarm 缩减到单个管理节点是一项不安全的操作，不予推荐。如果在降级操作期间最后一个节点意外离开 Swarm，Swarm 将变得不可用，直到您重启该节点或使用 `--force-new-cluster` 重新启动。

您可以使用 `docker swarm` 和 `docker node` 子系统管理 Swarm 成员。参考 [向 Swarm 添加节点](join-nodes.md) 了解更多关于如何添加工作节点以及如何将工作节点提升为管理节点的信息。

### 分布管理节点

除了维持奇数个管理节点外，在放置管理节点时还要注意数据中心拓扑。为了获得最佳容错能力，请将管理节点分布在至少 3 个可用区 (availability-zones) 中，以应对整套机器故障或常见的维护场景。如果您在其中任何一个区域遭受故障，Swarm 应维持管理节点的法定人数，以便处理请求并重新平衡工作负载。

| Swarm 管理节点数 |  再分配 (分布在 3 个可用区) |
|:-------------------:|:--------------------------------------:|
| 3                   |                  1-1-1                 |
| 5                   |                  2-2-1                 |
| 7                   |                  3-2-2                 |
| 9                   |                  3-3-3                 |

### 运行仅限管理任务的节点

默认情况下，管理节点也充当工作节点。这意味着调度程序可以将任务分配给管理节点。对于小型且非关键的 Swarm，只要您在调度服务时对 CPU 和内存设置资源限制，将任务分配给管理节点是相对较低风险的。

然而，由于管理节点使用 Raft 一致性算法以一致的方式复制数据，它们对资源匮乏非常敏感。您应该将 Swarm 中的管理节点与可能阻塞 Swarm 操作 (如 Swarm 心跳或领导者选举) 的进程隔离开来。

为了避免干扰管理节点的操作，您可以将管理节点设置为 drain 状态，使其不可作为工作节点使用：

```console
$ docker node update --availability drain <NODE>
```

当您 drain (排空) 一个节点时，调度程序会将运行在该节点上的任何任务重新分配给 Swarm 中其他可用的工作节点。它还会防止调度程序将任务分配给该节点。

## 添加工作节点以实现负载均衡

[向 Swarm 添加节点](join-nodes.md) 以平衡您的 Swarm 负载。随着时间的推移，只要工作节点符合服务的要求，复制的服务任务就会尽可能均匀地分布在 Swarm 中。当限制服务仅在特定类型的节点上运行时 (例如具有特定 CPU 数量或内存量的节点)，请记住不满足这些要求的工作节点无法运行这些任务。

## 监控 Swarm 健康状况

您可以通过 `/nodes` HTTP 端点以 JSON 格式查询 Docker `nodes` API 来监控管理节点的健康状况。参考 [nodes API 文档](/reference/api/engine/v1.25/#tag/Node) 获取更多信息。

在命令行中，运行 `docker node inspect <id-node>` 来查询节点。例如，要查询该节点作为管理节点的可达性：


```console
$ docker node inspect manager1 --format "{{ .ManagerStatus.Reachability }}"
reachable
```


要查询该节点作为接受任务的工作节点的状态：


```console
$ docker node inspect manager1 --format "{{ .Status.State }}"
ready
```


通过这些命令，我们可以看到 `manager1` 既处于作为管理节点的 `reachable` (可达) 状态，也处于作为工作节点的 `ready` (就绪) 状态。

`unreachable` (不可达) 健康状态意味着这个特定的管理节点无法从其他管理节点访问。在这种情况下，您需要采取行动恢复不可达的管理节点：

- 重启守护进程，看看管理节点是否恢复为可达状态。
- 重启机器。
- 如果重启守护进程和重启机器都不起作用，您应该添加另一个管理节点或将一个工作节点提升为管理节点。您还需要使用 `docker node demote <NODE>` 和 `docker node rm <id-node>` 干净地从管理节点集合中移除失败的节点条目。

或者，您也可以通过管理节点使用 `docker node ls` 获取 Swarm 健康状况的概览：

```console
$ docker node ls
ID                           HOSTNAME  MEMBERSHIP  STATUS  AVAILABILITY  MANAGER STATUS
1mhtdwhvsgr3c26xxbnzdc3yp    node05    Accepted    Ready   Active
516pacagkqp2xc3fk9t1dhjor    node02    Accepted    Ready   Active        Reachable
9ifojw8of78kkusuc4a6c23fx *  node01    Accepted    Ready   Active        Leader
ax11wdpwrrb6db3mfjydscgk7    node04    Accepted    Ready   Active
bb1nrq2cswhtbg4mrsqnlx1ck    node03    Accepted    Ready   Active        Reachable
di9wxgz8dtuh9d2hn089ecqkf    node06    Accepted    Ready   Active
```

## 为管理节点排障

您永远不应通过从另一个节点复制 `raft` 目录来重启管理节点。数据目录对于节点 ID 是唯一的。一个节点只能使用一次节点 ID 加入 Swarm。节点 ID 空间应该是全局唯一的。

要让一个管理节点干净地重新加入集群：

1. 使用 `docker node demote <NODE>` 将其降级为工作节点。
2. 使用 `docker node rm <NODE>` 将其从 Swarm 中移除。
3. 使用 `docker swarm join` 以全新状态重新加入 Swarm。

有关将管理节点加入 Swarm 的更多信息，请参阅 [将节点加入 Swarm](join-nodes.md)。

## 强制移除节点

在大多数情况下，在通过 `docker node rm` 命令将节点从 Swarm 中移除之前，您应该先关闭该节点。如果一个节点变得不可达、无响应或遭到破坏，您可以通过传递 `--force` 标志在不关闭它的情况下强制移除该节点。例如，如果 `node9` 遭到破坏：

```none
$ docker node rm node9

Error response from daemon: rpc error: code = 9 desc = node node9 is not down and can't be removed

$ docker node rm --force node9

Node node9 removed from swarm
```

在强制移除管理节点之前，必须先将其降级为工作节点角色。如果您降级或移除一个管理节点，请确保您始终拥有奇数个管理节点。

## 备份 Swarm

Docker 管理节点将 Swarm 状态和管理日志存储在 `/var/lib/docker/swarm/` 目录中。此数据包含用于加密 Raft 日志的密钥。没有这些密钥，您将无法恢复 Swarm。

您可以使用任何一个管理节点备份 Swarm。请按以下步骤操作：

1.  如果 Swarm 启用了自动锁定 (auto-lock)，您需要解锁密钥才能从备份中恢复 Swarm。必要时检索解锁密钥并将其存储在安全位置。如果您不确定，请阅读 [锁定您的 Swarm 以保护其加密密钥](swarm_manager_locking.md)。

2.  在备份数据之前停止管理节点上的 Docker，以便在备份期间不会更改任何数据。虽然可以在管理节点运行期间进行备份 (“热”备份)，但不推荐这样做，且恢复时的结果较难预测。当管理节点停机时，其他节点会继续生成不属于此备份的 Swarm 数据。

    > [!NOTE]
    > 
    > 务必维持 Swarm 管理节点的法定人数。在管理节点关闭期间，如果进一步丢失节点，您的 Swarm 将更容易失去法定人数。运行的管理节点数量是一种权衡。如果您定期停用管理节点进行备份，请考虑运行五个管理节点的 Swarm，这样在备份运行期间您可以再丢失一个管理节点而不会中断服务。

3.  备份整个 `/var/lib/docker/swarm` 目录。

4.  重启管理节点。

要进行恢复，请参阅 [从备份恢复](#restore-from-a-backup)。

## 从灾难中恢复

### 从备份恢复

按照 [备份 Swarm](#back-up-the-swarm) 中描述的方法备份 Swarm 后，使用以下步骤将数据恢复到新的 Swarm。

1.  关闭要恢复 Swarm 的目标主机上的 Docker。

2.  移除新 Swarm 上 `/var/lib/docker/swarm` 目录的内容。

3.  使用备份内容恢复 `/var/lib/docker/swarm` 目录。

    > [!NOTE]
    > 
    > 新节点使用与旧节点相同的磁盘存储加密密钥。目前无法更改磁盘存储加密密钥。
    >
    > 对于启用了自动锁定的 Swarm，解锁密钥也与旧 Swarm 相同，恢复 Swarm 需要解锁密钥。

4.  在新节点上启动 Docker。必要时解锁 Swarm。使用以下命令重新初始化 Swarm，以便此节点不会尝试连接到原本属于旧 Swarm、且想必已不再存在的节点。

    ```console
    $ docker swarm init --force-new-cluster
    ```

5.  验证 Swarm 状态是否符合预期。这可能包括特定于应用程序的测试，或者只是检查 `docker service ls` 的输出以确保所有预期的服务都存在。

6.  如果您使用自动锁定，请 [轮换解锁密钥](swarm_manager_locking.md#rotate-the-unlock-key)。

7.  添加管理节点和工作节点，使您的新 Swarm 达到运行容量。

8.  在新 Swarm 上重新建立之前的备份方案。

### 从失去法定人数中恢复

Swarm 对故障具有弹性，可以从任何数量的临时节点故障 (机器重启或崩溃后重启) 或其他瞬时错误中恢复。但是，如果 Swarm 失去了法定人数，它就无法自动恢复。现有工作节点上的任务会继续运行，但无法执行管理任务，包括扩展或更新服务以及在 Swarm 中加入或移除节点。恢复的最佳方法是将丢失的管理节点重新上线。如果无法做到这一点，请继续阅读有关恢复 Swarm 的一些选项。

在具有 `N` 个管理节点的 Swarm 中，必须始终有大多数管理节点可用。例如，在具有五个管理节点的 Swarm 中，必须至少有三个管理节点处于运行状态且彼此能够通信。换句话说，Swarm 最多可以容忍 `(N-1)/2` 个永久性故障，超过此数值，涉及 Swarm 管理的请求将无法处理。这些类型的故障包括数据损坏或硬件故障。

如果您失去了管理节点的法定人数，您将无法管理 Swarm。如果您失去了法定人数并尝试对 Swarm 执行任何管理操作，将会发生错误：

```none
Error response from daemon: rpc error: code = 4 desc = context deadline exceeded
```

恢复失去法定人数状态的最佳方法是将失败的节点重新上线。如果您无法做到这一点，从该状态恢复的唯一方法是从管理节点使用 `--force-new-cluster` 操作。这会移除除运行该命令的管理节点之外的所有管理节点。由于现在只有一个管理节点，法定人数得以实现。然后提升节点为管理节点，直到您拥有所需数量的管理节点。

在要恢复的节点上，运行：

```console
$ docker swarm init --force-new-cluster --advertise-addr node01:2377
```

当您运行带有 `--force-new-cluster` 标志的 `docker swarm init` 命令时，您运行该命令所在的 Docker Engine 将成为单节点 Swarm 的管理节点，该 Swarm 能够管理和运行服务。管理节点拥有所有关于服务和任务的先前信息，工作节点仍然是 Swarm 的一部分，且服务仍在运行。您需要添加或重新添加管理节点，以实现之前的任务分配，并确保您有足够的管理节点来维持高可用性并防止再次失去法定人数。

## 强制 Swarm 重新平衡

通常情况下，您不需要强制 Swarm 重新平衡其任务。当您向 Swarm 添加新节点，或者节点在一段时间不可用后重新连接到 Swarm 时，Swarm 不会自动将工作负载分配给空闲节点。这是一个设计决定。如果 Swarm 为了平衡而定期将任务转移到不同节点，那么使用这些任务的客户端将会受到干扰。目标是避免为了整个 Swarm 的平衡而干扰正在运行的服务。当新任务启动时，或者当具有运行中任务的节点变得不可用时，这些任务会被分配给负载较轻的节点。目标是实现最终的平衡，并对终端用户产生最小的干扰。

您可以在 `docker service update` 命令中使用 `--force` 或 `-f` 标志来强制服务在可用的工作节点之间重新分配其任务。这会导致服务任务重启。客户端应用程序可能会受到干扰。如果您配置了滚动更新，您的服务将使用 [滚动更新 (rolling update)](swarm-tutorial/rolling-update.md)。

如果您使用的是较早版本，并且想要在工作节点之间实现均衡的负载分配且不介意干扰运行中的任务，您可以通过临时向上扩展服务来强制 Swarm 重新平衡。使用 `docker service inspect --pretty <servicename>` 查看服务的配置规模。当您使用 `docker service scale` 时，任务数最少的节点将优先接收新的工作负载。您的 Swarm 中可能有多个负载不足的节点。您可能需要分几次适度地增加服务规模，以在所有节点之间实现您想要的平衡。

当负载平衡达到您的满意程度后，您可以将服务规模缩减回原始大小。您可以使用 `docker service ps` 来评估服务当前在节点之间的平衡情况。

另请参阅 [`docker service scale`](/reference/cli/docker/service/scale.md) 和 [`docker service ps`](/reference/cli/docker/service/ps.md)。
