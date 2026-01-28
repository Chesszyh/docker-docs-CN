---
title: 网络概述
linkTitle: 网络
weight: 30
description: 从容器的角度了解网络是如何工作的
keywords: networking, container, standalone, IP address, DNS resolution
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

容器网络是指容器连接到其他容器
或非 Docker 工作负载并与之通信的能力。

容器默认启用网络，它们可以进行出站
连接。容器不知道它连接到什么类型的网络，
也不知道它的对等端是否也是 Docker 工作负载。容器
只能看到一个具有 IP 地址、网关、
路由表、DNS 服务和其他网络详细信息的网络接口。也就是说，除非
容器使用 `none` 网络驱动程序。

本页从容器的角度描述网络，
以及容器网络相关的概念。
本页不描述 Docker 网络工作原理的操作系统特定细节。
有关 Docker 如何在 Linux 上操作 `iptables` 规则的信息，
请参阅[数据包过滤和防火墙](packet-filtering-firewalls.md)。

## 用户定义网络

你可以创建自定义的用户定义网络，并将多个容器
连接到同一网络。一旦连接到用户定义网络，容器就可以
使用容器 IP 地址或容器名称相互通信。

以下示例使用 `bridge` 网络驱动程序创建网络并
在创建的网络中运行容器：

```console
$ docker network create -d bridge my-net
$ docker run --network=my-net -itd --name=container3 busybox
```

### 驱动程序

以下网络驱动程序默认可用，并提供核心
网络功能：

| 驱动程序    | 描述                                                              |
| :-------- | :----------------------------------------------------------------------- |
| `bridge`  | 默认网络驱动程序。                                              |
| `host`    | 移除容器和 Docker 主机之间的网络隔离。      |
| `none`    | 将容器与主机和其他容器完全隔离。       |
| `overlay` | Overlay 网络将多个 Docker 守护进程连接在一起。               |
| `ipvlan`  | IPvlan 网络提供对 IPv4 和 IPv6 地址的完全控制。 |
| `macvlan` | 为容器分配 MAC 地址。                                     |

有关不同驱动程序的更多信息，请参阅[网络驱动程序
概述](./drivers/_index.md)。

### 连接到多个网络

一个容器可以连接到多个网络。

例如，一个前端容器可能连接到一个具有外部访问权限的桥接网络，
以及一个
[`--internal`](/reference/cli/docker/network/create/#internal) 网络
用于与运行不需要外部网络访问的后端服务的容器通信。

容器也可以连接到不同类型的网络。例如，
一个 `ipvlan` 网络用于提供互联网访问，一个 `bridge` 网络用于
访问本地服务。

发送数据包时，如果目的地是直接连接网络中的地址，
数据包会发送到该网络。否则，数据包会发送到
默认网关进行路由到目的地。在上面的示例中，
`ipvlan` 网络的网关必须是默认网关。

默认网关由 Docker 选择，并且可能在
容器的网络连接发生变化时改变。
要让 Docker 在创建容器或连接新网络时选择特定的默认网关，
可以设置网关优先级。参见 [`docker run`](/reference/cli/docker/container/run.md) 和
[`docker network connect`](/reference/cli/docker/network/connect.md) 命令的 `gw-priority` 选项。

默认的 `gw-priority` 是 `0`，具有最高优先级的网络中的网关
是默认网关。因此，当一个网络应该始终
是默认网关时，将其 `gw-priority` 设置为 `1` 就足够了。

```console
$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr
```

## 容器网络

除了用户定义网络之外，你还可以使用 `--network
container:<name|id>` 标志格式直接将容器附加到另一个
容器的网络栈。

以下标志不支持使用 `container:`
网络模式的容器：

- `--add-host`
- `--hostname`
- `--dns`
- `--dns-search`
- `--dns-option`
- `--mac-address`
- `--publish`
- `--publish-all`
- `--expose`

以下示例运行一个 Redis 容器，Redis 绑定到
`localhost`，然后运行 `redis-cli` 命令并通过 `localhost` 接口连接到 Redis
服务器。

```console
$ docker run -d --name redis example/redis --bind 127.0.0.1
$ docker run --rm -it --network container:redis example/redis-cli -h 127.0.0.1
```

## 发布端口

默认情况下，当你使用 `docker create` 或 `docker run` 创建或运行容器时，
桥接网络上的容器不会向外部世界暴露任何端口。
使用 `--publish` 或 `-p` 标志使端口可用于
桥接网络之外的服务。
这会在主机上创建一条防火墙规则，
将容器端口映射到 Docker 主机上的端口以供外部访问。
以下是一些示例：

| 标志值                      | 描述                                                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | 将 Docker 主机上的端口 `8080` 映射到容器中的 TCP 端口 `80`。                                                                                   |
| `-p 192.168.1.100:8080:80`      | 将 Docker 主机 IP `192.168.1.100` 上的端口 `8080` 映射到容器中的 TCP 端口 `80`。                                                                |
| `-p 8080:80/udp`                | 将 Docker 主机上的端口 `8080` 映射到容器中的 UDP 端口 `80`。                                                                                   |
| `-p 8080:80/tcp -p 8080:80/udp` | 将 Docker 主机上的 TCP 端口 `8080` 映射到容器中的 TCP 端口 `80`，并将 Docker 主机上的 UDP 端口 `8080` 映射到容器中的 UDP 端口 `80`。 |

> [!IMPORTANT]
>
> 发布容器端口默认是不安全的。意思是，当你发布
> 容器的端口时，它不仅对 Docker 主机可用，而且对
> 外部世界也可用。
>
> 如果你在 publish 标志中包含 localhost IP 地址（`127.0.0.1` 或 `::1`），
> 只有 Docker 主机及其容器可以访问
> 发布的容器端口。
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```
>
> > [!WARNING]
> >
> > 在 28.0.0 之前的版本中，同一 L2 网段内的主机（例如，
> > 连接到同一网络交换机的主机）可以访问发布到 localhost 的端口。
> > 有关更多信息，请参阅
> > [moby/moby#45610](https://github.com/moby/moby/issues/45610)

如果你想让一个容器对其他容器可访问，
没有必要发布容器的端口。
你可以通过将容器连接到
同一网络（通常是[桥接网络](./drivers/bridge.md)）来启用容器间通信。

如果端口映射中没有给出主机 IP，桥接网络仅支持 IPv4，
并且 `--userland-proxy=true`（默认），主机 IPv6 地址上的端口将映射到容器的 IPv4 地址。

有关端口映射的更多信息，包括如何禁用它并使用
直接路由到容器，请参阅
[数据包过滤和防火墙](./packet-filtering-firewalls.md)。

## IP 地址和主机名

创建网络时，默认启用 IPv4 地址分配，可以使用 `--ipv4=false` 禁用。
可以使用 `--ipv6` 启用 IPv6 地址分配。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

默认情况下，容器为其连接的每个 Docker 网络获取一个 IP 地址。
容器从网络的 IP 子网中接收 IP 地址。
Docker 守护进程为容器执行动态子网划分和 IP 地址分配。
每个网络还有一个默认子网掩码和网关。

你可以将正在运行的容器连接到多个网络，
在创建容器时多次传递 `--network` 标志，
或者对已经运行的容器使用 `docker network connect` 命令。
在这两种情况下，你都可以使用 `--ip` 或 `--ip6` 标志指定容器在特定网络上的 IP 地址。

同样，容器的主机名默认为 Docker 中的容器 ID。
你可以使用 `--hostname` 覆盖主机名。
使用 `docker network connect` 连接到现有网络时，
你可以使用 `--alias` 标志为容器在该网络上指定一个额外的网络别名。

## DNS 服务

容器默认使用与主机相同的 DNS 服务器，但你可以
使用 `--dns` 覆盖。

默认情况下，容器继承
`/etc/resolv.conf` 配置文件中定义的 DNS 设置。
连接到默认 `bridge` 网络的容器会收到该文件的副本。
连接到
[自定义网络](tutorials/standalone.md#use-user-defined-bridge-networks)
的容器使用 Docker 的内置 DNS 服务器。
内置 DNS 服务器将外部 DNS 查询转发到主机上配置的 DNS 服务器。

你可以在每个容器的基础上配置 DNS 解析，使用
`docker run` 或 `docker create` 命令启动容器时使用的标志。
下表描述了与 DNS 配置相关的可用 `docker run` 标志。

| 标志           | 描述                                                                                                                                                                                                                                           |
| -------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--dns`        | DNS 服务器的 IP 地址。要指定多个 DNS 服务器，使用多个 `--dns` 标志。DNS 请求将从容器的网络命名空间转发，因此，例如，`--dns=127.0.0.1` 指的是容器自己的回环地址。 |
| `--dns-search` | 用于搜索非完全限定主机名的 DNS 搜索域。要指定多个 DNS 搜索前缀，使用多个 `--dns-search` 标志。                                                                                                              |
| `--dns-opt`    | 表示 DNS 选项及其值的键值对。有关有效选项，请参阅操作系统的 `resolv.conf` 文档。                                                                                                              |
| `--hostname`   | 容器用于自身的主机名。如果未指定，默认为容器的 ID。                                                                                                                                            |

### 自定义主机

你的容器将在 `/etc/hosts` 中包含定义
容器本身主机名的行，以及 `localhost` 和一些其他常见内容。在主机机器的 `/etc/hosts` 中定义的自定义
主机不会被容器继承。要向容器传递额外的主机，请参阅 `docker run` 参考文档中的[向容器 hosts 文件添加条目](/reference/cli/docker/container/run.md#add-host)。

## 代理服务器

如果你的容器需要使用代理服务器，请参阅
[使用代理服务器](/manuals/engine/daemon/proxy.md)。
