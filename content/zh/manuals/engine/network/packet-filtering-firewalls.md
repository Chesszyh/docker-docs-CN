---
title: 数据包过滤和防火墙
weight: 10
description: Docker 如何与数据包过滤、iptables 和防火墙配合工作
keywords: network, iptables, firewall, 网络, 防火墙
---

在 Linux 上，Docker 创建 `iptables` 和 `ip6tables` 规则来实现网络隔离、端口发布和过滤。

由于这些规则是 Docker bridge 网络正常运行所必需的，因此您不应修改 Docker 创建的规则。

但是，如果您在暴露于互联网的主机上运行 Docker，您可能希望添加 iptables 策略，以防止未经授权访问容器或主机上运行的其他服务。本页介绍如何实现这一点，以及您需要注意的注意事项。

> [!NOTE]
> 
> Docker 为 bridge 网络创建 `iptables` 规则。
> 
> 不会为 `ipvlan`、`macvlan` 或 `host` 网络创建 `iptables` 规则。

## Docker 和 iptables 链

在 `filter` 表中，Docker 将默认策略设置为 `DROP`，并创建以下自定义 `iptables` 链：

* `DOCKER-USER`
  * 用户定义规则的占位符，这些规则将在 `DOCKER-FORWARD` 和 `DOCKER` 链中的规则之前处理。
* `DOCKER-FORWARD`
  * Docker 网络处理的第一阶段。将与已建立连接无关的数据包传递到其他 Docker 链的规则，以及接受属于已建立连接一部分的数据包的规则。
* `DOCKER`
  * 根据运行中容器的端口转发配置，确定是否应接受不属于已建立连接一部分的数据包的规则。
* `DOCKER-ISOLATION-STAGE-1` 和 `DOCKER-ISOLATION-STAGE-2`
  * 将 Docker 网络彼此隔离的规则。
* `DOCKER-INGRESS`
  * 与 Swarm 网络相关的规则。

在 `FORWARD` 链中，Docker 添加了无条件跳转到 `DOCKER-USER`、`DOCKER-FORWARD` 和 `DOCKER-INGRESS` 链的规则。

在 `nat` 表中，Docker 创建 `DOCKER` 链并添加规则来实现伪装 (masquerading) 和端口映射。

### 在 Docker 规则之前添加 iptables 策略

被这些自定义链中的规则接受或拒绝的数据包将不会被附加到 `FORWARD` 链的用户定义规则看到。因此，要添加额外的规则来过滤这些数据包，请使用 `DOCKER-USER` 链。

附加到 `FORWARD` 链的规则将在 Docker 规则之后处理。

### 匹配请求的原始 IP 和端口

当数据包到达 `DOCKER-USER` 链时，它们已经通过了目的网络地址转换 (DNAT) 过滤器。这意味着您使用的 `iptables` 标志只能匹配容器的内部 IP 地址和端口。

如果您想根据网络请求中的原始 IP 和端口匹配流量，则必须使用 [`conntrack` iptables 扩展](https://ipset.netfilter.org/iptables-extensions.man.html#lbAO)。例如：

```console
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctorigdst 198.51.100.2 --ctorigdstport 80 -j ACCEPT
```

> [!IMPORTANT]
> 
> 使用 `conntrack` 扩展可能会导致性能下降。

## 端口发布和映射

默认情况下，对于 IPv4 和 IPv6，守护进程都会阻止对未发布的端口的访问。发布的容器端口会映射到主机 IP 地址。为此，它使用 iptables 执行网络地址转换 (NAT)、端口地址转换 (PAT) 和伪装。

例如，`docker run -p 8080:80 [...]` 在 Docker 主机上的任何地址的 8080 端口与容器的 80 端口之间创建映射。来自容器的出站连接将使用 Docker 主机的 IP 地址进行伪装。

### 限制对容器的外部连接

默认情况下，允许所有外部源 IP 连接到已发布到 Docker 主机地址的端口。

要仅允许特定 IP 或网络访问容器，请在 `DOCKER-USER` 过滤链的顶部插入一条否定规则。例如，以下规则丢弃来自除 `192.0.2.2` 之外的所有 IP 地址的数据包：

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.2 -j DROP
```

您需要将 `ext_if` 更改为对应您主机的实际外部接口。您也可以允许来自源子网的连接。以下规则仅允许来自子网 `192.0.2.0/24` 的访问：

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.0/24 -j DROP
```

最后，您可以使用 `--src-range` 指定要接受的 IP 地址范围 (记住在使用 `--src-range` 或 `--dst-range` 时也要添加 `-m iprange`)：

```console
$ iptables -I DOCKER-USER -m iprange -i ext_if ! --src-range 192.0.2.1-192.0.2.3 -j DROP
```

您可以将 `-s` 或 `--src-range` 与 `-d` 或 `--dst-range` 结合使用来同时控制源和目的。例如，如果 Docker 主机具有地址 `2001:db8:1111::2` 和 `2001:db8:2222::2`，您可以制定针对 `2001:db8:1111::2` 的规则，并保持 `2001:db8:2222::2` 开放。

您可能需要允许来自允许的外部地址范围之外的服务器的响应。例如，容器可能会向不允许访问容器服务的向主机发送 DNS 或 HTTP 请求。以下规则接受属于已由其他规则接受的流的任何入站或出站数据包。它必须放置在限制外部地址范围访问的 `DROP` 规则之前。

```console
$ iptables -I DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT
```

`iptables` 很复杂。在 [Netfilter.org HOWTO](https://www.netfilter.org/documentation/HOWTO/NAT-HOWTO.html) 有更多信息。

### 直接路由 (Direct routing)

端口映射确保已发布的端口在主机的网络地址上可访问，这些地址对于任何外部客户端来说很可能是可路由的。通常不会在主机网络中为存在于主机内的容器地址设置路由。

但是，特别是在使用 IPv6 时，您可能更倾向于避免使用 NAT，而是安排到容器地址的外部路由 (“直接路由”)。

要从 Docker 主机外部访问 bridge 网络上的容器，您必须首先通过 Docker 主机上的地址设置到 bridge 网络的路由。这可以通过静态路由、边界网关协议 (BGP) 或任何适用于您网络的其他方式来实现。例如，在本地第 2 层网络中，远程主机可以通过本地网络上 Docker 守护进程主机的地址设置到容器网络的静态路由。

#### bridge 网络中容器的直接路由

默认情况下，远程主机不允许直接访问 Docker 的 Linux bridge 网络中的容器 IP 地址。它们只能访问发布到主机 IP 地址的端口。

要允许直接访问任何 Linux bridge 网络中任何容器的任何发布端口，请在 `/etc/docker/daemon.json` 中使用守护进程选项 `"allow-direct-routing": true` 或等效的 `--allow-direct-routing`。

要允许从任何地方直接路由到特定 bridge 网络中的容器，请参阅 [网关模式](#gateway-modes)。

或者，要允许通过特定的主机接口直接路由到特定的 bridge 网络，请在创建网络时使用以下选项：
- `com.docker.network.bridge.trusted_host_interfaces`

#### 示例

创建一个网络，其中容器 IP 地址上的发布端口可以从接口 `vxlan.1` 和 `eth3` 直接访问：

```console
$ docker network create --subnet 192.0.2.0/24 --ip-range 192.0.2.0/29 -o com.docker.network.bridge.trusted_host_interfaces="vxlan.1:eth3" mynet
```

在该网络中运行一个容器，将其 80 端口发布到主机回环接口的 8080 端口：

```console
$ docker run -d --ip 192.0.2.100 -p 127.0.0.1:8080:80 nginx
```

现在可以从 Docker 主机通过 `http://127.0.0.1:8080` 访问运行在容器 80 端口上的 Web 服务器，也可以直接通过 `http://192.0.2.100:80` 访问。如果连接到接口 `vxlan.1` 和 `eth3` 的网络上的远程主机具有到 Docker 主机内 `192.0.2.0/24` 网络的路由，它们也可以通过 `http://192.0.2.100:80` 访问 Web 服务器。

#### 网关模式 (Gateway modes)

bridge 网络驱动程序具有以下选项：
- `com.docker.network.bridge.gateway_mode_ipv6`
- `com.docker.network.bridge.gateway_mode_ipv4`

其中每一个都可以设置为以下网关模式之一：
- `nat`
- `nat-unprotected`
- `routed`
- `isolated`

默认值为 `nat`，会为每个发布的容器端口设置 NAT 和伪装规则。离开主机的数据包将使用主机地址。

使用 `routed` 模式，不会设置 NAT 或伪装规则，但仍会设置 `iptables` 以便仅允许访问发布的容器端口。来自容器的出站数据包将使用容器的地址，而不是主机地址。

在 `nat` 模式下，当端口发布到特定的主机地址时，该端口只能通过具有该地址的主机接口访问。因此，例如，将端口发布到回环接口上的地址意味着远程主机无法访问它。

但是，使用直接路由，发布的容器端口始终可以从远程主机访问，除非 Docker 主机的防火墙有额外的限制。本地第 2 层网络上的主机可以设置直接路由，而不需要任何额外的网络配置。本地网络之外的主机只有在网络路由器配置为启用直接路由的情况下才能使用到容器的直接路由。

在 `nat-unprotected` 模式下，未发布的容器端口也可以使用直接路由访问，不设置端口过滤规则。此模式是为了与传统的默认行为兼容而包含的。

网关模式还会影响连接到同一主机上不同 Docker 网络容器之间的通信。
- 在 `nat` 和 `nat-unprotected` 模式下，其他 bridge 网络中的容器只能通过发布的端口所发布到的主机地址来访问它们。不允许从其他网络进行直接路由。
- 在 `routed` 模式下，其他网络中的容器可以使用直接路由访问端口，而无需经过主机地址。

在 `routed` 模式下，`-p` 或 `--publish` 端口映射中的主机端口不会被使用，主机地址仅用于决定是否将映射应用于 IPv4 或 IPv6。因此，当映射仅应用于 `routed` 模式时，应仅使用地址 `0.0.0.0` 或 `::`，且不应给出主机端口。如果给出了特定的地址或端口，它将对发布的端口没有影响，并会记录一条警告消息。

只有当网络也是使用 CLI 标志 `--internal` 或等效标志创建时，才能使用 `isolated` 模式。通常在 `internal` 网络中会为 bridge 设备分配一个地址。因此，docker 主机上的进程可以访问该网络，并且该网络中的容器可以访问在该 bridge 地址上监听的主机服务 (包括在“任何”主机地址 `0.0.0.0` 或 `::` 上监听的服务)。当使用网关模式 `isolated` 创建网络时，不会为 bridge 分配地址。

#### 示例

创建一个适用于 IPv6 直接路由且 IPv4 启用 NAT 的网络：
```console
$ docker network create --ipv6 --subnet 2001:db8::/64 -o com.docker.network.bridge.gateway_mode_ipv6=routed mynet
```

创建一个带有发布端口的容器：
```console
$ docker run --network=mynet -p 8080:80 myimage
```

结果如下：
- 对于 IPv4 和 IPv6，仅容器端口 80 会开放。
- 对于 IPv6，使用 `routed` 模式，端口 80 将在容器的 IP 地址上开放。主机 IP 地址上的 8080 端口将不会被打开，且出站数据包将使用容器的 IP 地址。
- 对于 IPv4，使用默认的 `nat` 模式，容器的 80 端口将通过主机 IP 地址上的 8080 端口访问，也可直接从 Docker 主机内部访问。但是，无法直接从主机外部访问容器端口 80。源自容器的连接将使用主机的 IP 地址进行伪装。

在 `docker inspect` 中，此端口映射将如下显示。请注意，IPv6 没有 `HostPort`，因为它使用的是 `routed` 模式：
```console
$ docker container inspect <id> --format "{{json .NetworkSettings.Ports}}"
{"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"8080"},{"HostIp":"::","HostPort":""}]}
```

或者，要使映射仅针对 IPv6，从而禁用对容器 80 端口的 IPv4 访问，请使用未指定的 IPv6 地址 `[::]` 且不要包含主机端口号：
```console
$ docker run --network mynet -p '[::]::80'
```

### 为容器设置默认绑定地址

默认情况下，当容器端口映射没有指定任何特定主机地址时，Docker 守护进程会将发布的容器端口绑定到所有主机地址 (`0.0.0.0` 和 `[::]`)。

例如，以下命令将 8080 端口发布到主机上的所有网络接口 (包括 IPv4 和 IPv6 地址)，这可能会使它们对外界可用。

```console
docker run -p 8080:80 nginx
```

您可以更改发布容器端口的默认绑定地址，以便它们默认仅对 Docker 主机可用。为此，您可以配置守护进程使用回环地址 (`127.0.0.1`)。

> [!WARNING]
> 
> 在 28.0.0 之前的版本中，同一 L2 网段内的主机 (例如连接到同一网络交换机的主机) 可以访问发布到 localhost 的端口。有关更多信息，请参阅 [moby/moby#45610](https://github.com/moby/moby/issues/45610)

要为用户定义的 bridge 网络配置此设置，请在创建网络时使用 `com.docker.network.bridge.host_binding_ipv4` [驱动程序选项](./drivers/bridge.md#options)。

```console
$ docker network create mybridge \
  -o "com.docker.network.bridge.host_binding_ipv4=127.0.0.1"
```

> [!NOTE]
> 
> - 将默认绑定地址设置为 `::` 意味着未指定主机地址的端口绑定将适用于主机上的任何 IPv6 地址。但是，`0.0.0.0` 表示任何 IPv4 或 IPv6 地址。
> - 更改默认绑定地址对 Swarm 服务没有任何影响。Swarm 服务始终暴露在 `0.0.0.0` 网络接口上。

#### 默认 bridge (Default bridge)

要为默认 bridge 网络设置默认绑定，请在 `daemon.json` 配置文件中配置 `"ip"` 键：

```json
{
  "ip": "127.0.0.1"
}
```

这会将默认 bridge 网络上发布容器端口的默认绑定地址更改为 `127.0.0.1`。重启守护进程以使此更改生效。或者，您可以在启动守护进程时使用 `dockerd --ip` 标志。

## 在路由器上的 Docker

在 Linux 上，Docker 需要在主机上启用 "IP Forwarding" (IP 转发)。因此，如果它在启动时未启用，它会启用 `sysctl` 设置 `net.ipv4.ip_forward` 和 `net.ipv6.conf.all.forwarding`。当它这样做时，它还会将 iptables `FORWARD` 链的策略设置为 `DROP`。

如果 Docker 将 `FORWARD` 链的策略设置为 `DROP`。这将阻止您的 Docker 主机充当路由器，这是启用 IP 转发时的推荐设置。

要阻止 Docker 将 `FORWARD` 链的策略设置为 `DROP`，请在 `/etc/docker/daemon.json` 中包含 `"ip-forward-no-drop": true`，或者在 `dockerd` 命令行中添加选项 `--ip-forward-no-drop`。

或者，您可以为要转发的数据包向 `DOCKER-USER` 链添加 `ACCEPT` 规则。例如：

```console
$ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```

> [!WARNING]
> 
> 在 28.0.0 之前的版本中，Docker 始终将 IPv6 `FORWARD` 链的默认策略设置为 `DROP`。在 28.0.0 及更高版本中，它只有在自身启用 IPv6 转发时才会设置该策略。这一直是 IPv4 转发的行为。
> 
> 如果您的主机在 Docker 启动之前已启用 IPv6 转发，请检查您的主机配置以确保其仍然安全。

## 防止 Docker 操作系统操作 iptables

可以在 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/) 中将 `iptables` 或 `ip6tables` 键设置为 `false`，但此选项对大多数用户来说不合适。它可能会破坏 Docker Engine 的容器网络。

所有容器的所有端口都将可以从网络访问，并且没有任何端口会从 Docker 主机 IP 地址进行映射。

不可能完全防止 Docker 创建 `iptables` 规则，而事后创建规则非常复杂且超出了这些说明的范围。

## 与 firewalld 集成

如果您在运行 Docker 时将 `iptables` 选项设置为 `true`，并且系统中启用了 [firewalld](https://firewalld.org)，Docker 会自动创建一个名为 `docker` 的 `firewalld` 区域，目标为 `ACCEPT`。

所有由 Docker 创建的网络接口 (例如 `docker0`) 都会被插入到 `docker` 区域中。

Docker 还创建了一个名为 `docker-forwarding` 的转发策略，允许从 `ANY` (任何) 区域转发到 `docker` 区域。

## Docker 和 ufw

[Uncomplicated Firewall](https://launchpad.net/ufw) (ufw) 是 Debian 和 Ubuntu 附带的前端，它允许您管理防火墙规则。Docker 和 ufw 使用 iptables 的方式使得它们彼此不兼容。

当您使用 Docker 发布容器端口时，往返该容器的流量在通过 ufw 防火墙设置之前就被转移了。Docker 在 `nat` 表中路由容器流量，这意味着数据包在到达 ufw 使用的 `INPUT` 和 `OUTPUT` 链之前就被转移了。数据包在防火墙规则应用之前就被路由了，从而有效地忽略了您的防火墙配置。
