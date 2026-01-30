---
description: 在 Swarm 模式下运行 Docker Engine
keywords: guide, swarm mode, node, Docker Engines, Swarm 模式, 节点
title: 在 Swarm 模式下运行 Docker Engine
---

当您第一次安装并开始使用 Docker Engine 时，Swarm 模式默认是禁用的。启用 Swarm 模式后，您将使用通过 `docker service` 命令管理的服务 (services) 概念。

运行 Swarm 模式下的 Engine 有两种方式：

* 创建一个新的 Swarm，本篇文章将涵盖此内容。
* [加入现有的 Swarm](join-nodes.md)。

当您在本地机器上以 Swarm 模式运行 Engine 时，您可以根据自己创建的镜像或其他可用镜像创建并测试服务。在生产环境中，Swarm 模式提供了一个具有集群管理功能的容错平台，以保持您的服务持续运行并可用。

这些说明假设您已在某台机器上安装了 Docker Engine，该机器将作为 Swarm 中的管理节点 (manager node)。

如果您还没有阅读过 [Swarm 模式核心概念](key-concepts.md)，请务必阅读，并尝试 [Swarm 模式教程](swarm-tutorial/_index.md)。

## 创建 Swarm

当您运行创建 Swarm 的命令时，Docker Engine 开始以 Swarm 模式运行。

运行 [`docker swarm init`](/reference/cli/docker/swarm/init.md) 在当前节点上创建一个单节点 Swarm。Engine 会按如下方式设置 Swarm：

* 将当前节点切换到 Swarm 模式。
* 创建一个名为 `default` 的 Swarm。
* 将当前节点指定为 Swarm 的 Leader 管理节点。
* 以机器的主机名命名该节点。
* 配置管理节点在活动网络接口的 `2377` 端口上进行监听。
* 将当前节点的可用性设置为 `Active`，这意味着它可以接收来自调度程序的任务。
* 为参与 Swarm 的 Engine 启动一个内部分布式数据存储，以维持对 Swarm 及其上运行的所有服务的一致视图。
* 默认情况下，为 Swarm 生成一个自签名根 CA。
* 默认情况下，生成用于工作节点和管理节点加入 Swarm 的令牌。
* 创建一个名为 `ingress` 的 overlay 网络，用于向 Swarm 外部发布服务端口。
* 为您的网络创建一个 overlay 默认 IP 地址和子网掩码。

`docker swarm init` 的输出提供了在向 Swarm 加入新工作节点时要使用的连接命令：

```console
$ docker swarm init
Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

### 配置默认地址池

默认情况下，Swarm 模式为全局作用域 (overlay) 网络使用默认地址池 `10.0.0.0/8`。每个未指定子网的网络都将按顺序从该池中分配一个子网。在某些情况下，可能希望为网络使用不同的默认 IP 地址池。

例如，如果默认的 `10.0.0.0/8` 范围与您网络中已分配的地址空间冲突，那么最好确保网络使用不同的范围，而无需 Swarm 用户使用 `--subnet` 命令指定每个子网。

要配置自定义默认地址池，必须在 Swarm 初始化时使用 `--default-addr-pool` 命令行选项定义池。此命令行选项使用 CIDR 表示法来定义子网掩码。
要为 Swarm 创建自定义地址池，必须至少定义一个默认地址池，以及一个可选的默认地址池子网掩码长度。例如，对于 `10.0.0.0/27`，使用值 `27`。

Docker 会从 `--default-addr-pool` 选项指定的地址范围中分配子网地址。例如，命令行选项 `--default-addr-pool 10.10.0.0/16` 表示 Docker 将从该 `/16` 地址范围分配子网。如果 `--default-addr-pool-mask-len` 未指定或显式设置为 24，这将产生 256 个格式为 `10.10.X.0/24` 的 `/24` 网络。

子网范围来自 `--default-addr-pool` (例如 `10.10.0.0/16`)。其中的 16 表示在该 `default-addr-pool` 范围内可以创建的网络数量。`--default-addr-pool` 选项可以出现多次，每个选项都为 Docker 提供额外的地址供 overlay 子网使用。

该命令的格式为：

```console
$ docker swarm init --default-addr-pool <CIDR 格式的 IP 范围> [--default-addr-pool <CIDR 格式的 IP 范围> --default-addr-pool-mask-length <CIDR 值>]
```

为 `10.20.0.0` 网络创建一个 /16 (B 类) 默认 IP 地址池的命令如下：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16
```

为 `10.20.0.0` 和 `10.30.0.0` 网络创建一个默认 IP 地址池，并为每个网络创建一个 `/26` 子网掩码的命令如下：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool 10.30.0.0/16 --default-addr-pool-mask-length 26
```

在此示例中，`docker network create -d overlay net1` 将导致 `10.20.0.0/26` 作为 `net1` 分配的子网，而 `docker network create -d overlay net2` 将导致 `10.20.0.64/26` 作为 `net2` 分配的子网。这一过程将持续到所有子网耗尽。

参考以下页面获取更多信息：
- [Swarm 联网](./networking.md) 了解关于默认地址池使用的更多信息
- `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md) 了解关于 `--default-addr-pool` 标志的更多细节。

### 配置通告地址 (Advertise address)

管理节点使用通告地址来允许 Swarm 中的其他节点访问 Swarmkit API 和 overlay 联网。Swarm 中的其他节点必须能够通过管理节点的通告地址访问该管理节点。

如果您不指定通告地址，Docker 会检查系统是否只有一个 IP 地址。如果是，Docker 默认使用该 IP 地址和监听端口 `2377`。如果系统有多个 IP 地址，您必须指定正确的 `--advertise-addr` 以启用管理节点间通信和 overlay 联网：

```console
$ docker swarm init --advertise-addr <管理节点 IP>
```

如果其他节点访问第一个管理节点的地址与管理节点看到的自身地址不同，您也必须指定 `--advertise-addr`。例如，在跨越不同区域的云设置中，主机既有用于区域内访问的内部地址，也有您用于从该区域外部访问的外部地址。在这种情况下，请使用 `--advertise-addr` 指定外部地址，以便该节点可以将该信息传播给随后连接到它的其他节点。

参考 `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md) 了解关于通告地址的更多细节。

### 查看 join 命令或更新 Swarm join 令牌

节点需要一个机密令牌才能加入 Swarm。工作节点的令牌与管理节点的令牌不同。节点仅在加入 Swarm 的时刻使用 join-token。在节点加入 Swarm 后轮换 join 令牌不会影响该节点的 Swarm 成员身份。令牌轮换可确保旧令牌无法被任何尝试加入 Swarm 的新节点使用。

要检索包含工作节点 join 令牌的 join 命令，请运行：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

This node joined a swarm as a worker.
```

要查看管理节点的 join 命令和令牌，请运行：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-59egwe8qangbzbqb3ryawxzk3jn97ifahlsrw01yar60pmkr90-bdjfnkcflhooyafetgjod97sz \
    192.168.99.100:2377
```

传递 `--quiet` 标志仅打印令牌：

```console
$ docker swarm join-token --quiet worker

SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c
```

请小心保管 join 令牌，因为它们是加入 Swarm 所需的机密。特别地，将机密提交到版本控制系统是一种坏习惯，因为这会允许任何有权访问应用程序源代码的人向 Swarm 添加新节点。管理令牌尤其敏感，因为它们允许新的管理节点加入并获得对整个 Swarm 的控制权。

我们建议在以下情况下轮换 join 令牌：

* 如果令牌意外被提交到版本控制系统、群聊或意外打印到您的日志中。
* 如果您怀疑某个节点已遭到破坏。
* 如果您希望保证没有任何新节点可以加入 Swarm。

此外，为任何机密 (包括 Swarm join 令牌) 实施定期的轮换计划是最佳实践。我们建议您至少每 6 个月轮换一次令牌。

运行 `swarm join-token --rotate` 以使旧令牌失效并生成新令牌。指定您想要轮换 `worker` 还是 `manager` 节点的令牌：

```console
$ docker swarm join-token  --rotate worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-2kscvs0zuymrsc9t0ocyy1rdns9dhaodvpl639j2bqx55uptag-ebmn5u927reawo27s3azntd44 \
    192.168.99.100:2377
```

## 了解更多

* [将节点加入 Swarm](join-nodes.md)
* `swarm init` [命令行参考](/reference/cli/docker/swarm/init.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)
