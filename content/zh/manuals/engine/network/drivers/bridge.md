--- 
title: Bridge 网络驱动程序
description: 关于使用用户定义 bridge 网络和默认 bridge 网络的一切
keywords: network, bridge, user-defined, standalone, 网络, 桥接, 用户定义, 独立运行
---

在网络术语中，bridge (网桥) 网络是一个在网络段之间转发流量的链路层 (Link Layer) 设备。网桥可以是硬件设备，也可以是运行在主机内核中的软件设备。

在 Docker 术语中，bridge 网络使用软件网桥，允许连接到同一个 bridge 网络的容器相互通信，同时提供与未连接到该 bridge 网络的容器的隔离。Docker bridge 驱动程序会自动在主机中安装规则，使得不同 bridge 网络上的容器无法直接相互通信。

Bridge 网络适用于运行在同一个 Docker 守护进程主机上的容器。对于运行在不同 Docker 守护进程主机上的容器之间的通信，您可以选择在操作系统级别管理路由，也可以使用 [overlay 网络](./overlay.md)。

当您启动 Docker 时，会自动创建一个 [默认 bridge 网络](#use-the-default-bridge-network) (也称为 `bridge`)，除非另有指定，否则新启动的容器都会连接到它。您还可以创建用户定义的自定义 bridge 网络。**用户定义 bridge 网络优于默认 `bridge` 网络。**

## 用户定义 bridge 网络与默认 bridge 网络之间的区别

- **用户定义 bridge 网络在容器之间提供自动 DNS 解析**。

  默认 bridge 网络上的容器只能通过 IP 地址互相访问，除非您使用被视为传统功能的 [`--link` 选项](../links.md)。在用户定义 bridge 网络上，容器可以通过名称或别名相互解析。

  想象一个具有 Web 前端和数据库后端的应用程序。如果您将容器命名为 `web` 和 `db`，那么无论应用程序栈运行在哪个 Docker 主机上，web 容器都可以通过 `db` 连接到 db 容器。

  如果您在默认 bridge 网络上运行相同的应用程序栈，则需要手动在容器之间创建 link (使用传统的 `--link` 标志)。这些 link 需要在两个方向上都创建，因此当有超过两个容器需要通信时，您会发现这变得非常复杂。或者，您可以操纵容器内的 `/etc/hosts` 文件，但这会产生难以调试的问题。

- **用户定义 bridge 网络提供更好的隔离**。

  所有未指定 `--network` 的容器都会连接到默认 bridge 网络。这可能存在风险，因为无关的栈/服务/容器随后能够相互通信。

  使用用户定义网络提供了一个作用域网络，在该网络中只有连接到该网络的容器才能进行通信。

- **容器可以随时在用户定义网络上进行连接和断开**。

  在容器的生命周期内，您可以随时将其从用户定义网络中连接或断开。要从默认 bridge 网络中移除容器，您需要停止容器并使用不同的网络选项重新创建它。

- **每个用户定义网络都会创建一个可配置的网桥**。

  如果您的容器使用默认 bridge 网络，您可以对其进行配置，但所有容器都使用相同的设置，例如 MTU 和 `iptables` 规则。此外，配置默认 bridge 网络发生在 Docker 本身之外，并且需要重启 Docker。

  用户定义 bridge 网络使用 `docker network create` 创建和配置。如果不同的应用程序组有不同的网络需求，您可以在创建每个用户定义网桥时单独配置它们。

- **默认 bridge 网络上的链接容器共享环境变量**。

  最初，在两个容器之间共享环境变量的唯一方法是使用 [`--link` 标志](../links.md) 链接它们。这种类型的变量共享在用户定义网络中是不可能的。但是，有更好的方法来共享环境变量。一些建议：

  - 多个容器可以使用 Docker 卷挂载包含共享信息的文件或目录。

  - 多个容器可以使用 `docker-compose` 一起启动，并且 compose 文件可以定义共享变量。

  - 您可以使用 swarm 服务代替独立容器，并利用共享的 [机密 (secrets)](/manuals/engine/swarm/secrets.md) 和 [配置 (configs)](/manuals/engine/swarm/configs.md)。

连接到同一个用户定义 bridge 网络的容器实际上向彼此暴露了所有端口。为了使端口对不同网络上的容器或非 Docker 主机可用，必须使用 `-p` 或 `--publish` 标志 *发布* 该端口。

## 选项 (Options)

下表描述了在使用 `bridge` 驱动程序创建自定义网络时可以传递给 `--opt` 的特定于驱动程序的选项。

| 选项                                                                                            | 默认值                      | 描述                                                                                         |
|-------------------------------------------------------------------------------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------|
| `com.docker.network.bridge.name`                                                                |                             | 创建 Linux 网桥时使用的接口名称。                                               |
| `com.docker.network.bridge.enable_ip_masquerade`                                                | `true`                      | 启用 IP 伪装。                                                                             |
| `com.docker.network.bridge.gateway_mode_ipv4`<br/>`com.docker.network.bridge.gateway_mode_ipv6` | `nat`                       | 控制外部连接。参见 [数据包过滤和防火墙](./packet-filtering-firewalls.md)。 | 
| `com.docker.network.bridge.enable_icc`                                                          | `true`                      | 启用或禁用容器间连接 (inter-container connectivity)。                                                     |
| `com.docker.network.bridge.host_binding_ipv4`                                                   | 所有 IPv4 和 IPv6 地址 | 绑定容器端口时的默认 IP。                                                            |
| `com.docker.network.driver.mtu`                                                                 | `0` (无限制)              | 设置容器网络最大传输单元 (MTU)。                                         |
| `com.docker.network.container_iface_prefix`                                                     | `eth`                       | 为容器接口设置自定义前缀。                                                       |
| `com.docker.network.bridge.inhibit_ipv4`                                                        | `false`                     | 防止 Docker 向网桥 [分配 IP 地址](#skip-bridge-ip-address-configuration)。 | 

其中一些选项也可以作为 `dockerd` CLI 的标志，您可以在启动 Docker 守护进程时使用它们来配置默认的 `docker0` 网桥。下表显示了哪些选项在 `dockerd` CLI 中具有等效标志。

| 选项                                             | 标志        | 
|------------------------------------------------ | ----------- | 
| `com.docker.network.bridge.name`                 | -           | 
| `com.docker.network.bridge.enable_ip_masquerade` | `--ip-masq` | 
| `com.docker.network.bridge.enable_icc`           | `--icc`     | 
| `com.docker.network.bridge.host_binding_ipv4`    | `--ip`      | 
| `com.docker.network.driver.mtu`                  | `--mtu`     | 
| `com.docker.network.container_iface_prefix`      | -           | 

Docker 守护进程支持 `--bridge` 标志，您可以使用该标志定义自己的 `docker0` 网桥。如果您想在同一台主机上运行多个守护进程实例，请使用此选项。有关详情，请参阅 [运行多个守护进程](./reference/cli/dockerd.md#run-multiple-daemons)。

### 默认主机绑定地址

当端口发布选项 (如 `-p 80` 或 `-p 8080:80`) 中没有给出主机地址时，默认是在所有主机地址 (IPv4 和 IPv6) 上提供容器的 80 端口。

bridge 网络驱动程序选项 `com.docker.network.bridge.host_binding_ipv4` 可用于修改已发布端口的默认地址。

尽管该选项名为 IPv4，但也可以指定 IPv6 地址。

当默认绑定地址是分配给特定接口的地址时，容器的端口将只能通过该地址访问。

将默认绑定地址设置为 `::` 意味着发布的端口将仅在主机的 IPv6 地址上可用。但是，将其设置为 `0.0.0.0` 意味着它将在主机的 IPv4 和 IPv6 地址上可用。

要将发布的端口限制为仅 IPv4，必须在容器的发布选项中包含该地址。例如，`-p 0.0.0.0:8080:80`。

## 管理用户定义 bridge 网络

使用 `docker network create` 命令创建用户定义 bridge 网络。

```console
$ docker network create my-net
```

您可以指定子网、IP 地址范围、网关和其他选项。有关详情，请参阅 [docker network create](./reference/cli/docker/network/create.md#specify-advanced-options) 参考或 `docker network create --help` 的输出。

使用 `docker network rm` 命令移除用户定义 bridge 网络。如果当前有容器连接到该网络，请先 [断开它们的连接](#disconnect-a-container-from-a-user-defined-bridge)。

```console
$ docker network rm my-net
```

> **究竟发生了什么？**
> 
> 当您创建或移除用户定义 bridge 网络，或者将容器连接到用户定义 bridge 网络或从中断开连接时，Docker 会使用操作系统特定的工具来管理底层的网络基础设施 (例如在 Linux 上添加或移除网桥设备或配置 `iptables` 规则)。这些细节应被视为实现细节。让 Docker 为您管理用户定义网络。

## 将容器连接到用户定义 bridge 网络

创建新容器时，可以指定一个或多个 `--network` 标志。此示例将一个 Nginx 容器连接到 `my-net` 网络。它还将容器中的 80 端口发布到 Docker 主机上的 8080 端口，以便外部客户端可以访问该端口。任何其他连接到 `my-net`网络的容器都可以访问 `my-nginx` 容器上的所有端口，反之亦然。

```console
$ docker create --name my-nginx \
  --network my-net \
  --publish 8080:80 \
  nginx:latest
```

要将 **正在运行** 的容器连接到现有的用户定义 bridge 网络，请使用 `docker network connect` 命令。以下命令将一个已经在运行的 `my-nginx` 容器连接到一个已经存在的 `my-net` 网络：

```console
$ docker network connect my-net my-nginx
```

## 从用户定义 bridge 网络断开容器连接

要将正在运行的容器从用户定义 bridge 网络中断开连接，请使用 `docker network disconnect` 命令。以下命令将 `my-nginx` 容器从 `my-net` 网络中移除。

```console
$ docker network disconnect my-net my-nginx
```

## 在用户定义 bridge 网络中使用 IPv6

创建网络时，可以指定 `--ipv6` 标志以启用 IPv6。

```console
$ docker network create --ipv6 --subnet 2001:db8:1234::/64 my-net
```

如果您不提供 `--subnet` 选项，将自动选择一个唯一本地地址 (Unique Local Address, ULA) 前缀。

## 仅限 IPv6 的 bridge 网络

要跳过网桥及其容器上的 IPv4 地址配置，请使用选项 `--ipv4=false` 创建网络，并使用 `--ipv6` 启用 IPv6。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

在默认 bridge 网络中无法禁用 IPv4 地址配置。

## 使用默认 bridge 网络

默认 `bridge` 网络被认为是 Docker 的一个传统细节，不建议在生产环境中使用。配置它需要手动操作，并且存在 [技术缺陷](#differences-between-user-defined-bridges-and-the-default-bridge)。

### 将容器连接到默认 bridge 网络

如果您没有使用 `--network` 标志指定网络，但指定了网络驱动程序，则您的容器默认连接到默认 `bridge` 网络。连接到默认 `bridge`网络的容器可以通信，但只能通过 IP 地址进行通信，除非它们使用 [传统 `--link` 标志](../links.md) 进行链接。

### 配置默认 bridge 网络

要配置默认 `bridge` 网络，您可以在 `daemon.json` 中指定选项。下面是一个指定了几个选项的 `daemon.json` 示例。请仅指定您需要自定义的设置。

```json
{
  "bip": "192.168.1.1/24",
  "fixed-cidr": "192.168.1.0/25",
  "mtu": 1500,
  "default-gateway": "192.168.1.254",
  "dns": ["10.20.1.2","10.20.1.3"]
}
```

在此示例中：

- 网桥的地址是 "192.168.1.1/24" (源自 `bip`)。
- bridge 网络的子网是 "192.168.1.0/24" (源自 `bip`)。
- 容器地址将从 "192.168.1.0/25" 分配 (源自 `fixed-cidr`)。

### 在默认 bridge 网络中使用 IPv6

可以通过 `daemon.json` 中的以下选项或其等效的命令行参数为默认 bridge 启用 IPv6。

这三个选项仅影响默认网桥，用户定义网络不使用它们。以下地址是 IPv6 文档范围内的示例。

- 必须使用 `ipv6` 选项。
- `bip6` 选项是可选的，它指定默认网桥的地址，该地址将由容器用作默认网关。它还指定 bridge 网络的子网。
- `fixed-cidr-v6` 选项是可选的，它指定 Docker 可以自动分配给容器的地址范围。
  - 前缀通常应为 `/64` 或更短。
  - 对于本地网络上的实验，最好使用唯一本地地址 (ULA) 前缀 (匹配 `fd00::/8`) 而不是链路本地 (Link Local) 前缀 (匹配 `fe80::/10`)。
- `default-gateway-v6` 选项是可选的。如果未指定，默认值为 `fixed-cidr-v6` 子网中的第一个地址。

```json
{
  "ipv6": true,
  "bip6": "2001:db8::1111/64",
  "fixed-cidr-v6": "2001:db8::/64",
  "default-gateway-v6": "2001:db8:abcd::89"
}
```

如果未指定 `bip6`，则 `fixed-cidr-v6` 定义 bridge 网络的子网。如果未指定 `bip6` 或 `fixed-cidr-v6`，将选择一个 ULA 前缀。

重启 Docker 以使更改生效。

## Bridge 网络的连接限制

由于 Linux 内核设置的限制，当 1000 个或更多容器连接到单个网络时，bridge 网络会变得不稳定，容器间通信可能会中断。

有关此限制的更多信息，请参阅 [moby/moby#44973](https://github.com/moby/moby/issues/44973#issuecomment-1543747718)。

## 跳过网桥 IP 地址配置

网桥通常被分配网络的 `--gateway` 地址，该地址被用作从 bridge 网络到其他网络的默认路由。

`com.docker.network.bridge.inhibit_ipv4` 选项允许您在创建网络时不将 IPv4 网关地址分配给网桥。如果您想手动配置网桥的网关 IP 地址，这很有用。例如，如果您向网桥添加了一个物理接口，并需要它拥有该网关地址。

使用此配置后，南北流量 (往返 bridge 网络) 将无法工作，除非您手动在网桥或其连接的设备上配置了网关地址。

此选项只能与用户定义 bridge 网络一起使用。

## 后续步骤

- 学习 [独立运行网络教程](./manuals/engine/network/tutorials/standalone.md)
- 了解 [从容器角度看的网络](../_index.md)
- 了解 [overlay 网络](./overlay.md)
- 了解 [Macvlan 网络](./macvlan.md)
