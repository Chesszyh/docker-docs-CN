---
title: 网络概览
linkTitle: 网络
weight: 30
description: 了解从容器角度来看网络是如何工作的
keywords: 网络, 容器, 独立运行, IP 地址, DNS 解析
aliases:
- /articles/networking/
- /config/containers/container-networking/
- /engine/tutorials/networkingcontainers/
- /engine/userguide/networking/
- /engine/userguide/networking/configure-dns/
- /engine/userguide/networking/default_network/binding/
- /engine/userguide/networking/default_network/configure-dns/
- /engine/userguide/networking/default_network/container-communication/
- /engine/userguide/networking/dockernetworks/
- /network/
---

容器网络是指容器能够相互连接和通信，或与非 Docker 工作负载连接和通信的能力。

容器默认启用网络功能，并可以进行出站连接。容器不知道自己连接到哪种类型的网络，也不知道其对等方是否也是 Docker 工作负载。容器只能看到一个带有 IP 地址、网关、路由表、DNS 服务和其他网络详细信息的网络接口。当然，除非容器使用 `none` 网络驱动程序。

本页从容器的角度描述了网络以及围绕容器网络的概念。本页不描述关于 Docker 网络如何工作的特定于操作系统的细节。有关 Docker 在 Linux 上如何操作 `iptables` 规则的信息，请参阅 [数据包过滤和防火墙](packet-filtering-firewalls.md)。

## 用户定义网络

您可以创建自定义的用户定义网络，并将多个容器连接到同一个网络。连接到用户定义网络后，容器可以使用容器 IP 地址或容器名称相互通信。

以下示例使用 `bridge` 网络驱动程序创建一个网络，并在该网络中运行一个容器：

```console
$ docker network create -d bridge my-net
$ docker run --network=my-net -itd --name=container3 busybox
```

### 驱动程序

默认情况下提供以下网络驱动程序，它们提供了核心网络功能：

| 驱动程序  | 描述                                                                 |
| :-------- | :------------------------------------------------------------------- |
| `bridge`  | 默认网络驱动程序。                                                   |
| `host`    | 移除容器与 Docker 主机之间的网络隔离。                               |
| `none`    | 将容器与主机及其他容器完全隔离。                                     |
| `overlay` | Overlay 网络将多个 Docker 守护进程连接在一起。                       |
| `ipvlan`  | IPvlan 网络提供对 IPv4 和 IPv6 地址的完全控制。                      |
| `macvlan` | 为容器分配 MAC 地址。                                                |

有关不同驱动程序的更多信息，请参阅 [网络驱动程序概览](./drivers/_index.md)。

### 连接到多个网络

一个容器可以连接到多个网络。

例如，一个前端容器可以连接到一个具有外部访问权限的 bridge 网络，以及一个用于与运行后端服务的容器通信的 [`--internal`](/reference/cli/docker/network/create/#internal) 网络 (该后端服务不需要外部网络访问)。

一个容器也可以连接到不同类型的网络。例如，一个提供互联网访问的 `ipvlan` 网络，以及一个用于访问本地服务的 `bridge` 网络。

发送数据包时，如果目的地是直接相连的网络中的地址，则数据包会发送到该网络。否则，数据包会发送到默认网关，由其路由到目的地。在上述示例中，`ipvlan` 网络的网关必须是默认网关。

默认网关由 Docker 选择，并在容器的网络连接发生变化时可能会随之改变。要让 Docker 在创建容器或连接新网络时选择特定的默认网关，请设置网关优先级。请参阅 [`docker run`](/reference/cli/docker/container/run.md) 和 [`docker network connect`](/reference/cli/docker/network/connect.md) 命令的 `gw-priority` 选项。

默认的 `gw-priority` 为 `0`，具有最高优先级的网络中的网关即为默认网关。因此，当一个网络应该始终作为默认网关时，只需将其 `gw-priority` 设置为 `1` 即可。

```console
$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr
```

## 容器网络 (Container networks)

除了用户定义网络外，您还可以使用 `--network container:<name|id>` 标志格式，直接将一个容器连接到另一个容器的网络栈。

对于使用 `container:` 网络模式的容器，不支持以下标志：

- `--add-host`
- `--hostname`
- `--dns`
- `--dns-search`
- `--dns-option`
- `--mac-address`
- `--publish`
- `--publish-all`
- `--expose`

以下示例运行一个 Redis 容器，Redis 绑定到 `localhost`，然后运行 `redis-cli` 命令并通过 `localhost` 接口连接到 Redis 服务器。

```console
$ docker run -d --name redis example/redis --bind 127.0.0.1
$ docker run --rm -it --network container:redis example/redis-cli -h 127.0.0.1
```

## 发布端口

默认情况下，当您使用 `docker create` 或 `docker run` 创建或运行容器时，bridge 网络上的容器不会向外界暴露任何端口。使用 `--publish` 或 `-p` 标志可使端口对 bridge 网络之外的服务可用。这会在主机中创建一条防火墙规则，将容器端口映射到 Docker 主机上的端口以面向外界。以下是一些示例：

| 标志值                          | 描述                                                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | 将 Docker 主机上的端口 `8080` 映射到容器中的 TCP 端口 `80`。                                                                                   |
| `-p 192.168.1.100:8080:80`      | 将 Docker 主机 IP `192.168.1.100` 上的端口 `8080` 映射到容器中的 TCP 端口 `80`。                                                                |
| `-p 8080:80/udp`                | 将 Docker 主机上的端口 `8080` 映射到容器中的 UDP 端口 `80`。                                                                                   |
| `-p 8080:80/tcp -p 8080:80/udp` | 将 Docker 主机上的 TCP 端口 `8080` 映射到容器中的 TCP 端口 `80`，并将 Docker 主机上的 UDP 端口 `8080` 映射到容器中的 UDP 端口 `80`。 |

> [!IMPORTANT]
>
> 发布容器端口默认是不安全的。这意味着当您发布容器端口时，它不仅对 Docker 主机可用，而且对外界也可用。
>
> 如果您在发布标志中包含 localhost IP 地址 (`127.0.0.1` 或 `::1`)，则只有 Docker 主机及其容器可以访问发布的容器端口。
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```
>
> > [!WARNING]
> >
> > 在 28.0.0 之前的版本中，同一 L2 网段内的主机 (例如连接到同一网络交换机的主机) 可以访问发布到 localhost 的端口。有关更多信息，请参阅 [moby/moby#45610](https://github.com/moby/moby/issues/45610)

如果您想让一个容器可以被其他容器访问，并不需要发布容器的端口。您可以通过将容器连接到同一个网络 (通常是 [bridge 网络](./drivers/bridge.md)) 来启用容器间通信。

如果在端口映射中未给出主机 IP，且 bridge 网络仅为 IPv4 且 `--userland-proxy=true` (默认值)，则主机 IPv6 地址上的端口将映射到容器的 IPv4 地址。

有关端口映射的更多信息 (包括如何禁用它以及如何使用到容器的直接路由)，请参阅 [数据包过滤和防火墙](./packet-filtering-firewalls.md)。

## IP 地址和主机名

创建网络时，默认启用 IPv4 地址分配，可以使用 `--ipv4=false` 禁用它。可以使用 `--ipv6` 启用 IPv6 地址分配。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

默认情况下，容器会为其连接的每个 Docker 网络获得一个 IP 地址。容器从网络的 IP 子网中接收一个 IP 地址。Docker 守护进程为容器执行动态子网划分和 IP 地址分配。每个网络还具有默认的子网掩码和网关。

您可以将运行中的容器连接到多个网络，方法是在创建容器时多次传递 `--network` 标志，或者对已经运行的容器使用 `docker network connect` 命令。在这两种情况下，您都可以使用 `--ip` 或 `--ip6` 标志指定容器在该特定网络上的 IP 地址。

同样，容器的主机名默认是 Docker 中的容器 ID。您可以使用 `--hostname` 覆盖主机名。使用 `docker network connect` 连接到现有网络时，可以使用 `--alias` 标志为容器在该网络上指定额外的网络别名。

## DNS 服务

默认情况下，容器使用与主机相同的 DNS 服务器，但您可以使用 `--dns` 覆盖此设置。

默认情况下，容器继承 `/etc/resolv.conf` 配置文件中定义的 DNS 设置。连接到默认 `bridge` 网络的容器会收到此文件的副本。连接到 [自定义网络](tutorials/standalone.md#use-user-defined-bridge-networks) 的容器使用 Docker 的内嵌 DNS 服务器。内嵌 DNS 服务器将外部 DNS 查询转发到主机上配置的 DNS 服务器。

您可以使用用于启动容器的 `docker run` 或 `docker create` 命令的标志，按容器配置 DNS 解析。下表描述了与 DNS 配置相关的可用 `docker run` 标志。

| 标志           | 描述                                                                                                                                                                                                                                           |
| -------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--dns`        | DNS 服务器的 IP 地址。要指定多个 DNS 服务器，请使用多个 `--dns` 标志。DNS 请求将从容器的网络命名空间转发，因此例如 `--dns=127.0.0.1` 指的是容器自己的回环地址。 |
| `--dns-search` | 用于搜索非完全限定主机名的 DNS 搜索域。要指定多个 DNS 搜索前缀，请使用多个 `--dns-search` 标志。                                                                                                              |
| `--dns-opt`    | 表示 DNS 选项及其值的键值对。请参阅您的操作系统中关于 `resolv.conf` 的文档以获取有效选项。                                                                                                              |
| `--hostname`   | 容器为自己使用的主机名。如果未指定，默认使用容器 ID。                                                                                                                                                            |

### 自定义 hosts

您的容器将在 `/etc/hosts` 中包含定义容器本身主机名、`localhost` 以及其他一些常见内容的行。在主机上的 `/etc/hosts` 中定义的自定义 hosts 不会被容器继承。要将额外的 hosts 传递到容器中，请参阅 `docker run` 参考文档中的 [向容器 hosts 文件添加条目](/reference/cli/docker/container/run.md#add-host)。

## 代理服务器

如果您的容器需要使用代理服务器，请参阅 [使用代理服务器](/manuals/engine/daemon/proxy.md)。
