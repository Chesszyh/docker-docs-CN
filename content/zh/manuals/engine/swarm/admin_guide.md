---
description: Manager administration guide
keywords: docker, container, swarm, manager, raft
title: 管理和维护 Docker Engine 的 swarm
aliases:
- /engine/swarm/manager-administration-guide/
---

当您运行 Docker Engine 的 swarm 时，管理节点是管理 swarm 和存储 swarm 状态的关键组件。理解管理节点的一些关键特性对于正确部署和维护 swarm 非常重要。

请参阅[节点工作原理](how-swarm-mode-works/nodes.md)，了解 Docker Swarm 模式以及管理节点和工作节点之间的区别的简要概述。

## 在 swarm 中运行管理节点

Swarm 管理节点使用 [Raft 共识算法](raft.md)来管理 swarm 状态。您只需了解 Raft 的一些基本概念即可管理 swarm。

管理节点的数量没有限制。决定实现多少个管理节点是性能和容错能力之间的权衡。向 swarm 添加管理节点会使 swarm 更具容错能力。然而，额外的管理节点会降低写入性能，因为更多节点必须确认更新 swarm 状态的提案。这意味着更多的网络往返流量。

Raft 要求大多数管理节点（也称为法定人数/quorum）同意向 swarm 提出的更新，例如节点添加或移除。成员资格操作受到与状态复制相同的约束。

### 维持管理节点的法定人数

如果 swarm 失去了管理节点的法定人数，swarm 就无法执行管理任务。如果您的 swarm 有多个管理节点，请始终保持两个以上的管理节点。要维持法定人数，必须有大多数管理节点可用。建议使用奇数个管理节点，因为下一个偶数并不会使法定人数更容易保持。例如，无论您有 3 个还是 4 个管理节点，您仍然只能失去 1 个管理节点并维持法定人数。如果您有 5 个或 6 个管理节点，您仍然只能失去两个。

即使 swarm 失去了管理节点的法定人数，现有工作节点上的 swarm 任务仍会继续运行。但是，无法添加、更新或移除 swarm 节点，也无法启动、停止、移动或更新新的或现有的任务。

请参阅[从失去法定人数中恢复](#recover-from-losing-the-quorum)以了解在失去管理节点法定人数时的故障排除步骤。

## 配置管理节点在静态 IP 地址上广告

启动 swarm 时，您必须指定 `--advertise-addr` 标志来向 swarm 中的其他管理节点广告您的地址。有关更多信息，请参阅[以 swarm 模式运行 Docker Engine](swarm-mode.md#configure-the-advertise-address)。由于管理节点应该是基础设施的稳定组件，您应该为广告地址使用*固定 IP 地址*，以防止 swarm 在机器重启时变得不稳定。

如果整个 swarm 重启，并且每个管理节点随后都获得新的 IP 地址，则没有任何节点能够联系现有的管理节点。因此，当节点尝试使用旧 IP 地址相互联系时，swarm 会挂起。

工作节点使用动态 IP 地址是可以的。

## 添加管理节点以实现容错

您应该在 swarm 中维护奇数个管理节点以支持管理节点故障。拥有奇数个管理节点可确保在网络分区期间，如果网络被分成两组，法定人数仍有更高的可能性保持可用以处理请求。如果遇到两个以上的网络分区，则不能保证保持法定人数。

| Swarm 大小 |  多数  |  容错能力  |
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

例如，在一个有 *5 个节点*的 swarm 中，如果您失去了 *3 个节点*，您就没有法定人数了。因此，在您恢复一个不可用的管理节点或使用灾难恢复命令恢复 swarm 之前，您无法添加或移除节点。请参阅[从灾难中恢复](#recover-from-disaster)。

虽然可以将 swarm 缩减到单个管理节点，但无法降级最后一个管理节点。这确保您保持对 swarm 的访问权限，并且 swarm 仍然可以处理请求。缩减到单个管理节点是不安全的操作，不建议这样做。如果在降级操作期间最后一个节点意外离开 swarm，则 swarm 将变得不可用，直到您重新启动节点或使用 `--force-new-cluster` 重新启动。

您可以使用 `docker swarm` 和 `docker node` 子系统管理 swarm 成员资格。有关如何添加工作节点以及将工作节点提升为管理节点的更多信息，请参阅[向 swarm 添加节点](join-nodes.md)。

### 分布管理节点

除了维持奇数个管理节点外，在放置管理节点时还要注意数据中心拓扑。为了实现最佳容错能力，请将管理节点分布在至少 3 个可用区，以支持整组机器的故障或常见维护场景。如果您在任何一个区域遭受故障，swarm 应该维持可用的管理节点法定人数以处理请求和重新平衡工作负载。

| Swarm 管理节点数 |  分布（在 3 个可用区） |
|:-------------------:|:--------------------------------------:|
| 3                   |                  1-1-1                 |
| 5                   |                  2-2-1                 |
| 7                   |                  3-2-2                 |
| 9                   |                  3-3-3                 |

### 运行仅管理节点

默认情况下，管理节点也充当工作节点。这意味着调度程序可以将任务分配给管理节点。对于小型和非关键的 swarm，只要您使用 cpu 和内存的资源约束来调度服务，将任务分配给管理节点的风险相对较低。

但是，由于管理节点使用 Raft 共识算法以一致的方式复制数据，它们对资源匮乏很敏感。您应该将 swarm 中的管理节点与可能阻塞 swarm 操作（如 swarm 心跳或领导者选举）的进程隔离。

为了避免干扰管理节点的操作，您可以将管理节点设为 drain 状态，使其无法用作工作节点：

```console
$ docker node update --availability drain <NODE>
```

当您将节点设为 drain 状态时，调度程序会将该节点上运行的任何任务重新分配给 swarm 中的其他可用工作节点。它还会阻止调度程序将任务分配给该节点。

## 添加工作节点以实现负载均衡

[向 swarm 添加节点](join-nodes.md)以平衡您的 swarm 负载。复制服务任务会随着时间的推移尽可能均匀地分布在 swarm 中，只要工作节点符合服务的要求。当将服务限制为仅在特定类型的节点上运行时，例如具有特定数量 CPU 或内存量的节点，请记住不符合这些要求的工作节点无法运行这些任务。

## 监控 swarm 健康状况

您可以通过 `/nodes` HTTP 端点以 JSON 格式查询 docker `nodes` API 来监控管理节点的健康状况。有关更多信息，请参阅 [nodes API 文档](/reference/api/engine/v1.25/#tag/Node)。

从命令行运行 `docker node inspect <id-node>` 来查询节点。例如，要查询作为管理节点的节点可达性：

```console
$ docker node inspect manager1 --format "{{ .ManagerStatus.Reachability }}"
reachable
```

要查询作为接受任务的工作节点的状态：

```console
$ docker node inspect manager1 --format "{{ .Status.State }}"
ready
```

从这些命令中，我们可以看到 `manager1` 作为管理节点的状态为 `reachable`，作为工作节点的状态为 `ready`。

`unreachable` 健康状态表示此特定管理节点无法被其他管理节点访问。在这种情况下，您需要采取措施来恢复无法访问的管理节点：

- 重启守护进程，看看管理节点是否恢复为可达状态。
- 重启机器。
- 如果重启或重新启动都不起作用，您应该添加另一个管理节点或将工作节点提升为管理节点。您还需要使用 `docker node demote <NODE>` 和 `docker node rm <id-node>` 从管理节点集中干净地移除失败的节点条目。

或者，您也可以从管理节点使用 `docker node ls` 获得 swarm 健康状况的概览：

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

## 排查管理节点问题

您永远不应该通过从另一个节点复制 `raft` 目录来重启管理节点。数据目录对于节点 ID 是唯一的。一个节点只能使用一个节点 ID 加入 swarm。节点 ID 空间应该是全局唯一的。

要干净地将管理节点重新加入集群：

1. 使用 `docker node demote <NODE>` 将节点降级为工作节点。
2. 使用 `docker node rm <NODE>` 从 swarm 中移除节点。
3. 使用 `docker swarm join` 以全新状态将节点重新加入 swarm。

有关将管理节点加入 swarm 的更多信息，请参阅[将节点加入 swarm](join-nodes.md)。

## 强制移除节点

在大多数情况下，您应该在使用 `docker node rm` 命令从 swarm 中移除节点之前关闭该节点。如果节点变得无法访问、无响应或被入侵，您可以通过传递 `--force` 标志在不关闭节点的情况下强制移除该节点。例如，如果 `node9` 被入侵：

```none
$ docker node rm node9

Error response from daemon: rpc error: code = 9 desc = node node9 is not down and can't be removed

$ docker node rm --force node9

Node node9 removed from swarm
```

在强制移除管理节点之前，您必须先将其降级为工作节点角色。如果您降级或移除管理节点，请确保始终保持奇数个管理节点。

## 备份 swarm

Docker 管理节点将 swarm 状态和管理器日志存储在 `/var/lib/docker/swarm/` 目录中。此数据包括用于加密 Raft 日志的密钥。没有这些密钥，您将无法恢复 swarm。

您可以使用任何管理节点来备份 swarm。使用以下步骤。

1.  如果 swarm 启用了自动锁定，您需要解锁密钥来从备份恢复 swarm。如有必要，检索解锁密钥并将其存储在安全的地方。如果不确定，请阅读[锁定您的 swarm 以保护其加密密钥](swarm_manager_locking.md)。

2.  在备份数据之前停止管理节点上的 Docker，这样在备份期间不会有数据被更改。虽然可以在管理节点运行时进行备份（"热"备份），但不建议这样做，恢复时结果的可预测性较差。当管理节点关闭时，其他节点会继续生成不属于此备份的 swarm 数据。

    > [!NOTE]
    >
    > 请确保维持 swarm 管理节点的法定人数。在管理节点关闭期间，如果更多节点丢失，您的 swarm 更容易失去法定人数。您运行的管理节点数量是一个权衡。如果您经常关闭管理节点来进行备份，请考虑运行五个管理节点的 swarm，这样您可以在备份运行时再丢失一个管理节点，而不会中断您的服务。

3.  备份整个 `/var/lib/docker/swarm` 目录。

4.  重启管理节点。

要恢复，请参阅[从备份恢复](#restore-from-a-backup)。

## 从灾难中恢复

### 从备份恢复

按照[备份 swarm](#back-up-the-swarm)中的说明备份 swarm 后，使用以下步骤将数据恢复到新的 swarm。

1.  关闭恢复 swarm 的目标主机上的 Docker。

2.  移除新 swarm 上 `/var/lib/docker/swarm` 目录的内容。

3.  使用备份的内容恢复 `/var/lib/docker/swarm` 目录。

    > [!NOTE]
    >
    > 新节点使用与旧节点相同的磁盘存储加密密钥。目前无法更改磁盘存储加密密钥。
    >
    > 对于启用了自动锁定的 swarm，解锁密钥也与旧 swarm 相同，恢复 swarm 需要解锁密钥。

4.  在新节点上启动 Docker。如有必要，解锁 swarm。使用以下命令重新初始化 swarm，这样此节点就不会尝试连接到旧 swarm 中的节点（这些节点可能已不存在）。

    ```console
    $ docker swarm init --force-new-cluster
    ```

5.  验证 swarm 的状态是否符合预期。这可能包括特定于应用的测试，或者只是检查 `docker service ls` 的输出以确保所有预期的服务都存在。

6.  如果使用自动锁定，请[轮换解锁密钥](swarm_manager_locking.md#rotate-the-unlock-key)。

7.  添加管理节点和工作节点以使您的新 swarm 达到运行容量。

8.  在新 swarm 上恢复您之前的备份计划。

### 从失去法定人数中恢复

Swarm 对故障具有弹性，可以从任意数量的临时节点故障（机器重启或崩溃后重启）或其他瞬态错误中恢复。但是，如果 swarm 失去法定人数，它无法自动恢复。现有工作节点上的任务继续运行，但无法执行管理任务，包括扩展或更新服务以及将节点加入或从 swarm 移除。最佳恢复方式是将丢失的管理节点恢复上线。如果这不可能，请继续阅读以了解恢复 swarm 的一些选项。

在一个有 `N` 个管理节点的 swarm 中，必须始终有法定人数（大多数）的管理节点可用。例如，在有五个管理节点的 swarm 中，必须至少有三个管理节点处于运行状态并相互通信。换句话说，swarm 可以容忍最多 `(N-1)/2` 个永久性故障，超过这个数量，涉及 swarm 管理的请求将无法处理。这些类型的故障包括数据损坏或硬件故障。

如果您失去了管理节点的法定人数，您将无法管理 swarm。如果您失去了法定人数并尝试对 swarm 执行任何管理操作，会出现错误：

```none
Error response from daemon: rpc error: code = 4 desc = context deadline exceeded
```

从失去法定人数中恢复的最佳方法是将故障节点恢复上线。如果无法做到这一点，从这种状态恢复的唯一方法是从管理节点使用 `--force-new-cluster` 操作。这会移除除运行该命令的管理节点之外的所有管理节点。由于现在只有一个管理节点，因此达成了法定人数。将节点提升为管理节点，直到您拥有所需数量的管理节点。

从要恢复的节点上运行：

```console
$ docker swarm init --force-new-cluster --advertise-addr node01:2377
```

当您使用 `--force-new-cluster` 标志运行 `docker swarm init` 命令时，运行该命令的 Docker Engine 成为单节点 swarm 的管理节点，该 swarm 能够管理和运行服务。管理节点拥有所有关于服务和任务的先前信息，工作节点仍然是 swarm 的一部分，服务仍在运行。您需要添加或重新添加管理节点以实现您之前的任务分布，并确保您有足够的管理节点来维持高可用性并防止失去法定人数。

## 强制 swarm 重新平衡

通常，您不需要强制 swarm 重新平衡其任务。当您向 swarm 添加新节点，或者节点在一段时间不可用后重新连接到 swarm 时，swarm 不会自动将工作负载分配给空闲节点。这是一个设计决策。如果 swarm 定期为了平衡而将任务转移到不同的节点，使用这些任务的客户端将会受到干扰。目标是避免为了 swarm 的平衡而干扰正在运行的服务。当新任务启动，或者运行任务的节点变得不可用时，这些任务会被分配给较不繁忙的节点。目标是最终达到平衡，同时对最终用户的干扰最小。

您可以使用 `docker service update` 命令的 `--force` 或 `-f` 标志强制服务在可用工作节点之间重新分配其任务。这会导致服务任务重启。客户端应用可能会受到干扰。如果您已配置，您的服务将使用[滚动更新](swarm-tutorial/rolling-update.md)。

如果您使用较早的版本，并且想要实现工作节点之间负载的均匀平衡，并且不介意干扰正在运行的任务，您可以通过临时扩展服务来强制 swarm 重新平衡。使用 `docker service inspect --pretty <servicename>` 查看服务的配置规模。当您使用 `docker service scale` 时，任务数量最少的节点将被选中接收新的工作负载。您的 swarm 中可能有多个负载不足的节点。您可能需要多次以适度的增量扩展服务，以实现您想要的所有节点之间的平衡。

当负载平衡达到您的满意时，您可以将服务缩减回原来的规模。您可以使用 `docker service ps` 来评估服务在各节点之间的当前平衡。

另请参阅
[`docker service scale`](/reference/cli/docker/service/scale.md) 和
[`docker service ps`](/reference/cli/docker/service/ps.md)。
