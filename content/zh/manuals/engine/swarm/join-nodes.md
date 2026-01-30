---
description: 向 Swarm 添加工作节点和管理节点
keywords: guide, swarm mode, node, 节点, 添加
title: 将节点加入 Swarm
---

当您第一次创建 Swarm 时，您是将单个 Docker Engine 置于 Swarm 模式。为了充分利用 Swarm 模式，您可以向 Swarm 添加节点：

* 添加工作节点 (worker nodes) 会增加容量。当您将服务部署到 Swarm 时，Engine 会在可用节点上调度任务，无论是工作节点还是管理节点。当您向 Swarm 添加工作节点时，您增加了 Swarm 处理任务的规模，而不会影响管理节点的 Raft 共识。
* 管理节点 (manager nodes) 会提高容错能力。管理节点负责 Swarm 的编排和集群管理功能。在管理节点中，由单个 Leader 节点执行编排任务。如果 Leader 节点宕机，剩余的管理节点会选举出新的 Leader 并恢复 Swarm 状态的编排和维护。默认情况下，管理节点也会运行任务。

Docker Engine 加入 Swarm 取决于您提供给 `docker swarm join` 命令的 **join-token**。节点仅在加入时使用该令牌。如果您随后轮换 (rotate) 了令牌，它不会影响现有的 Swarm 节点。参考 [在 Swarm 模式下运行 Docker Engine](swarm-mode.md#view-the-join-command-or-update-a-swarm-join-token)。

## 以工作节点身份加入

要检索包含工作节点 join 令牌的 join 命令，请在管理节点上运行以下命令：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

在工作节点上运行输出中的命令以加入 Swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

This node joined a swarm as a worker.
```

`docker swarm join` 命令会执行以下操作：

* 将当前节点上的 Docker Engine 切换到 Swarm 模式。
* 向管理节点请求 TLS 证书。
* 以机器的主机名命名该节点。
* 根据 Swarm 令牌，在管理节点监听地址处将当前节点加入 Swarm。
* 将当前节点的可用性设置为 `Active`，这意味着它可以接收来自调度程序的任务。
* 将 `ingress` overlay 网络扩展到当前节点。

## 以管理节点身份加入

当您运行 `docker swarm join` 并传递管理节点令牌时，Docker Engine 切换到 Swarm 模式的过程与工作节点相同。管理节点也会参与 Raft 共识。新节点应处于 `Reachable` (可达) 状态，但现有的管理节点仍保持为 Swarm 的 `Leader`。

Docker 建议每个集群部署三个或五个管理节点以实现高可用性。由于 Swarm 模式下的管理节点使用 Raft 共享数据，因此必须有奇数个管理节点。只要有超过一半的管理节点 (即法定人数 quorum) 可用，Swarm 就能继续运行。

有关 Swarm 管理节点和管理 Swarm 的更多细节，请参阅 [管理和维护 Docker Engine Swarm](admin_guide.md)。

要检索包含管理节点 join 令牌的 join 命令，请在管理节点上运行以下命令：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
    192.168.99.100:2377
```

在新的管理节点上运行输出中的命令以将其加入 Swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
  192.168.99.100:2377

This node joined a swarm as a manager.
```

## 了解更多

* `swarm join` [命令行参考](/reference/cli/docker/swarm/join.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)
