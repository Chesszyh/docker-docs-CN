---
title: Overlay 网络驱动程序
description: 关于使用 overlay 网络的一切
keywords: network, overlay, user-defined, swarm, service, 网络, 覆盖网络, 用户定义, 服务
alias:
- /config/containers/overlay/
- /engine/userguide/networking/overlay-security-model/
- /network/overlay/
- /network/drivers/overlay/
---

`overlay` 网络驱动程序在多个 Docker 守护进程主机之间创建一个分布式网络。该网络位于 (覆盖在) 特定于主机的网络之上，允许连接到它的容器在启用加密时进行安全通信。Docker 透明地处理每个数据包往返于正确的 Docker 守护进程主机和正确的目标容器的路由。

您可以使用 `docker network create` 创建用户定义的 `overlay` 网络，就像创建用户定义的 `bridge` 网络一样。服务或容器可以同时连接到多个网络。服务或容器只能在它们各自都连接到的网络之间进行通信。

Overlay 网络通常用于在 Swarm 服务之间创建连接，但您也可以使用它来连接运行在不同主机上的独立容器。使用独立容器时，仍然需要使用 Swarm 模式来在主机之间建立连接。

本页描述了通用的 overlay 网络，以及将其与独立容器配合使用的情况。有关 Swarm 服务的 overlay 信息，请参阅 [管理 Swarm 服务网络](/manuals/engine/swarm/networking.md)。

## 创建 overlay 网络

在开始之前，必须确保参与的节点可以通过网络进行通信。下表列出了参与 overlay 网络的主机需要开放的端口：

| 端口                   | 描述                                                                                                                                                          |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2377/tcp`             | 默认的 Swarm 控制面端口，可通过 [`docker swarm join --listen-addr`](/reference/cli/docker/swarm/join.md#--listen-addr-value) 进行配置。 |
| `4789/udp`             | 默认的 overlay 流量端口，可通过 [`docker swarm init --data-path-addr`](/reference/cli/docker/swarm/init.md#data-path-port) 进行配置。          |
| `7946/tcp`, `7946/udp` | 用于节点间通信，不可配置。                                                                                                                 |

要创建一个其他 Docker 主机上的容器可以连接的 overlay 网络，运行以下命令：

```console
$ docker network create -d overlay --attachable my-attachable-overlay
```

`--attachable` 选项使独立容器和 Swarm 服务都能连接到该 overlay 网络。如果没有 `--attachable`，则只有 Swarm 服务可以连接到该网络。

您可以指定 IP 地址范围、子网、网关和其他选项。有关详情，请参阅 `docker network create --help`。

## 加密 overlay 网络上的流量

使用 `--opt encrypted` 标志来加密在 overlay 网络上传输的应用程序数据：

```console
docker network create \
  --opt encrypted \
  --driver overlay \
  --attachable \
  my-attachable-multi-host-network
```

这会在虚拟可扩展局域网 (VXLAN) 级别启用 IPsec 加密。这种加密会带来不可忽视的性能开销，因此在生产环境中使用之前应测试此选项。

> [!WARNING]
>
> 请勿将 Windows 容器连接到加密的 overlay 网络。
>
> Windows 不支持 overlay 网络加密。当 Windows 主机尝试连接到加密的 overlay 网络时，Swarm 不会报错，但 Windows 容器的网络会受到以下影响：
>
> - Windows 容器无法与网络上的 Linux 容器通信
> - 网络上 Windows 容器之间的数据流量不会被加密

## 将容器连接到 overlay 网络

将容器添加到 overlay 网络使其能够与其他容器通信，而无需在各个 Docker 守护进程主机上设置路由。执行此操作的前提是这些主机已加入同一个 Swarm。

要让一个 `busybox` 容器加入名为 `multi-host-network` 的 overlay 网络：

```console
$ docker run --network multi-host-network busybox sh
```

> [!NOTE]
>
> 仅当 overlay 网络是可连接的 (使用 `--attachable` 标志创建) 时，此操作才有效。

## 容器发现

在 overlay 网络上发布容器端口会向同一网络上的其他容器开放这些端口。通过使用容器名称进行 DNS 查询可以发现容器。

| 标志值                          | 描述                                                                                                                                                 |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | 将容器中的 TCP 80 端口映射到 overlay 网络上的 `8080` 端口。                                                                                     |
| `-p 8080:80/udp`                | 将容器中的 UDP 80 端口映射到 overlay 网络上的 `8080` 端口。                                                                                     |
| `-p 8080:80/sctp`               | 将容器中的 SCTP 80 端口映射到 overlay 网络上的 `8080` 端口。                                                                                    |
| `-p 8080:80/tcp -p 8080:80/udp` | 将容器中的 TCP 80 端口映射到 overlay 网络上的 TCP `8080` 端口，并将容器中的 UDP 80 端口映射到 overlay 网络上的 UDP `8080` 端口。 |

## Overlay 网络的连接限制

由于 Linux 内核设置的限制，当 1000 个容器位于同一台主机上时，overlay 网络会变得不稳定，并且容器间通信可能会中断。

有关此限制的更多信息，请参阅 [moby/moby#44973](https://github.com/moby/moby/issues/44973#issuecomment-1543747718)。

## 后续步骤

- 学习 [overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- 了解 [从容器角度看的网络](../_index.md)
- 了解 [独立运行 bridge 网络](bridge.md)
- 了解 [Macvlan 网络](macvlan.md)
