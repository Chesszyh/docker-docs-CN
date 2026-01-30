---
description: 使用 Swarm 模式的 overlay 联网特性
keywords: swarm, networking, ingress, overlay, service discovery, 网络, 服务发现
title: 管理 Swarm 服务网络
toc_max: 3
---

本页介绍了 Swarm 服务的联网功能。

## Swarm 及其流量类型

Docker Swarm 会产生两种不同类型的流量：

- 控制和管理平面流量：这包括 Swarm 管理消息，例如加入或离开 Swarm 的请求。此类流量始终是加密的。

- 应用程序数据平面流量：这包括容器流量以及往返外部客户端的流量。

## 关键网络概念

以下三个网络概念对 Swarm 服务非常重要：

- Overlay 网络：管理参与 Swarm 的 Docker 守护进程之间的通信。您可以创建 overlay 网络，方式与为独立容器创建用户定义网络相同。您还可以将服务附加到一个或多个现有的 overlay 网络，以实现服务间通信。Overlay 网络是使用 `overlay` 网络驱动程序的 Docker 网络。

- Ingress 网络：是一个特殊的 overlay 网络，用于在服务节点之间进行负载均衡。当任何 Swarm 节点在发布端口上收到请求时，它会将该请求交给一个名为 `IPVS` 的模块。`IPVS` 跟踪参与该服务的所有 IP 地址，选择其中一个，并通过 `ingress` 网络将请求路由到它。

  `ingress` 网络在您初始化或加入 Swarm 时自动创建。大多数用户不需要自定义其配置，但 Docker 允许您这样做。

- docker_gwbridge：是一个 bridge 网络，它将 overlay 网络 (包括 `ingress` 网络) 连接到单个 Docker 守护进程的物理网络。默认情况下，服务运行的每个容器都连接到其本地 Docker 守护进程主机的 `docker_gwbridge` 网络。

  `docker_gwbridge` 网络在您初始化或加入 Swarm 时自动创建。大多数用户不需要自定义其配置，但 Docker 允许您这样做。

> [!TIP]
> 
> 另请参阅 [网络概览](/manuals/engine/network/_index.md) 以获取有关 Swarm 联网的更多常规细节。

## 防火墙注意事项

参与 Swarm 的 Docker 守护进程需要能够通过以下端口相互通信：

* 端口 `7946` TCP/UDP：用于容器网络发现。
* 端口 `4789` UDP (可配置)：用于 overlay 网络 (包括 ingress) 数据路径。

在 Swarm 中设置联网时应格外小心。参考 [教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts) 获取概览。

## Overlay 联网

当您初始化 Swarm 或将 Docker 主机加入现有 Swarm 时，该 Docker 主机上会创建两个新网络：

- 名为 `ingress` 的 overlay 网络，用于处理与 Swarm 服务相关的控制和数据流量。当您创建 Swarm 服务且未将其连接到用户定义的 overlay 网络时，它默认连接到 `ingress` 网络。
- 名为 `docker_gwbridge` 的 bridge 网络，用于将单个 Docker 守护进程连接到参与 Swarm 的其他守护进程。

### 创建 overlay 网络

要创建 overlay 网络，请在 `docker network create` 命令中指定 `overlay` 驱动程序：

```console
$ docker network create \
  --driver overlay \
  my-network
```

上述命令没有指定任何自定义选项，因此 Docker 会分配一个子网并使用默认选项。您可以使用 `docker network inspect` 查看有关该网络的信息。

当没有容器连接到该 overlay 网络时，其配置非常简单：

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "0001-01-01T00:00:00Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": null,
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": null
    }
]
```

在上述输出中，注意到驱动程序是 `overlay`，且作用域 (scope) 是 `swarm`，而不是您在其他类型的 Docker 网络中可能看到的 `local`、`host` 或 `global` 作用域。此作用域表示只有参与 Swarm 的主机才能访问此网络。

该网络的子网和网关在服务首次连接到网络时动态配置。以下示例显示了与上述相同的网络，但有三个 `redis` 服务的容器连接到它。

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "2017-05-31T18:35:58.877628262Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.0.0.0/24",
                    "Gateway": "10.0.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": {
            "0e08442918814c2275c31321f877a47569ba3447498db10e25d234e47773756d": {
                "Name": "my-redis.1.ka6oo5cfmxbe6mq8qat2djgyj",
                "EndpointID": "950ce63a3ace13fe7ef40724afbdb297a50642b6d47f83a5ca8636d44039e1dd",
                "MacAddress": "02:42:0a:00:00:03",
                "IPv4Address": "10.0.0.3/24",
                "IPv6Address": ""
            },
            "88d55505c2a02632c1e0e42930bcde7e2fa6e3cce074507908dc4b827016b833": {
                "Name": "my-redis.2.s7vlybipal9xlmjfqnt6qwz5e",
                "EndpointID": "dd822cb68bcd4ae172e29c321ced70b731b9994eee5a4ad1d807d9ae80ecc365",
                "MacAddress": "02:42:0a:00:00:05",
                "IPv4Address": "10.0.0.5/24",
                "IPv6Address": ""
            },
            "9ed165407384f1276e5cfb0e065e7914adbf2658794fd861cfb9b991eddca754": {
                "Name": "my-redis.3.hbz3uk3hi5gb61xhxol27hl7d",
                "EndpointID": "f62c686a34c9f4d70a47b869576c37dffe5200732e1dd6609b488581634cf5d2",
                "MacAddress": "02:42:0a:00:00:04",
                "IPv4Address": "10.0.0.4/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "moby-e57c567e25e2",
                "IP": "192.168.65.2"
            }
        ]
    }
]
```

### 自定义 overlay 网络

在某些情况下，您可能不想使用 overlay 网络的默认配置。要查看可配置选项的完整列表，请运行命令 `docker network create --help`。以下是一些最常更改的选项。

#### 配置子网和网关

默认情况下，该网络的子网和网关在第一个服务连接到网络时自动配置。您可以在创建网络时使用 `--subnet` 和 `--gateway` 标志来配置这些选项。以下示例通过配置子网和网关扩展了前一个示例。

```console
$ docker network create \
  --driver overlay \
  --subnet 10.0.9.0/24 \
  --gateway 10.0.9.99 \
  my-network
```

##### 使用自定义默认地址池

要自定义 Swarm 网络的子网分配，您可以在 `swarm init` 期间 [选择性地配置它们](swarm-mode.md)。

例如，在初始化 Swarm 时使用以下命令：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 26
```

每当用户创建一个网络，但未使用 `--subnet` 命令行选项时，该网络的子网将按顺序从地址池中下一个可用的子网中分配。如果指定的网络已被分配，则该网络将不被 Swarm 使用。

如果需要不连续的地址空间，可以配置多个池。但是，不支持从特定池进行分配。网络子网将按顺序从 IP 池空间中分配，且子网在从被删除网络中回收后将被重用。

可以配置默认的掩码长度，且所有网络都相同。默认设置为 `/24`。要更改默认子网掩码长度，请使用 `--default-addr-pool-mask-length` 命令行选项。

> [!NOTE]
> 
> 默认地址池只能在 `swarm init` 时配置，且在集群创建后无法更改。

##### Overlay 网络大小限制

Docker 建议使用 `/24` 块创建 overlay 网络。`/24` overlay 网络块将网络限制为 256 个 IP 地址。

此建议旨在解决 [Swarm 模式的局限性](https://github.com/moby/moby/issues/30820)。如果您需要超过 256 个 IP 地址，请不要增加 IP 块的大小。您可以将 `dnsrr` 端点模式与外部负载均衡器配合使用，或者使用多个较小的 overlay 网络。有关不同端点模式的更多信息，请参阅 [配置服务发现](#configure-service-discovery)。

#### 配置应用程序数据的加密 {#encryption}

与 Swarm 相关的管理和控制平面数据始终是加密的。有关加密机制的更多细节，请参阅 [Docker Swarm 模式 overlay 网络安全模型](/manuals/engine/network/drivers/overlay.md)。

Swarm 节点之间的应用程序数据默认不加密。要加密给定 overlay 网络上的此类流量，请在 `docker network create` 上使用 `--opt encrypted` 标志。这将在 vxlan 级别启用 IPSEC 加密。这种加密会带来不可忽视的性能损失，因此在将其用于生产环境之前，您应该测试此选项。

> [!NOTE]
> 
> 您必须 [自定义自动创建的 ingress](#customize-ingress) 才能启用加密。默认情况下，所有入口流量都是未加密的，因为加密是网络级别的选项。

## 将服务附加到 overlay 网络

要将服务附加到现有的 overlay 网络，请向 `docker service create` 传递 `--network` 标志，或向 `docker service update` 传递 `--network-add` 标志。

```console
$ docker service create \
  --replicas 3 \
  --name my-web \
  --network my-network \
  nginx
```

连接到同一个 overlay 网络的各服务容器可以相互通信。

要查看服务连接到了哪些网络，请使用 `docker service ls` 查找服务名称，然后使用 `docker service ps <service-name>` 列出网络。或者，要查看哪些服务的容器连接到了某个网络，请使用 `docker network inspect <network-name>`。您可以从任何已加入 Swarm 且处于 `running` 状态的 Swarm 节点运行这些命令。

### 配置服务发现

服务发现 (Service discovery) 是 Docker 用来将来自服务外部客户端的请求路由到单个 Swarm 节点的机制，客户端无需知道有多少个节点参与该服务，也不需要知道它们的 IP 地址或端口。您不需要发布在同一网络上的服务之间使用的端口。例如，如果您有一个 [在 MySQL 服务中存储数据的 WordPress 服务](https://training.play-with-docker.com/swarm-service-discovery/)，且它们连接到同一个 overlay 网络，则无需向客户端发布 MySQL 端口，只需发布 WordPress HTTP 端口。

服务发现有两种不同的工作方式：使用内嵌 DNS 和虚拟 IP (VIP) 的第 3 层和第 4 层内部基于连接的负载均衡，或者使用 DNS 轮询 (DNSRR) 的第 7 层外部且定制的基于请求的负载均衡。您可以按服务进行配置。

- 默认情况下，当您将服务附加到网络且该服务发布了一个或多个端口时，Docker 会为该服务分配一个虚拟 IP (VIP)，这是客户端访问该服务的“前端”。Docker 维护该服务中所有工作节点的列表，并在客户端和其中一个节点之间路由请求。来自客户端的每个请求可能会被路由到不同的节点。

- 如果您将服务配置为使用 DNS 轮询 (DNSRR) 服务发现，则不存在单一的虚拟 IP。相反，Docker 会为服务设置 DNS 条目，使得对服务名称的 DNS 查询返回一个 IP 地址列表，客户端直接连接到其中之一。

  DNS 轮询在您想要使用自己的负载均衡器 (如 HAProxy) 的情况下很有用。要配置服务使用 DNSRR，请在创建新服务或更新现有服务时使用 `--endpoint-mode dnsrr` 标志。

## 自定义 ingress 网络 {#customize-ingress}

大多数用户永远不需要配置 `ingress` 网络，但 Docker 允许您这样做。如果自动选择的子网与网络上已存在的子网发生冲突，或者您需要自定义其他低级网络设置 (如 MTU)，或者如果您想 [启用加密](#encryption)，这将非常有用。

自定义 `ingress` 网络涉及将其移除并重新创建。这通常在您在 Swarm 中创建任何服务之前完成。如果您已有发布端口的服务，则需要先移除这些服务，然后才能移除 `ingress` 网络。

在不存在 `ingress` 网络期间，现有的未发布端口的服务会继续运行，但不会进行负载均衡。这会影响发布端口的服务，例如发布 80 端口的 WordPress 服务。

1.  使用 `docker network inspect ingress` 检查 `ingress` 网络，并移除所有容器连接到它的服务。这些是发布端口的服务，如发布 80 端口的 WordPress 服务。如果所有此类服务均未停止，则下一步将失败。

2.  移除现有的 `ingress` 网络：

    ```console
    $ docker network rm ingress

    WARNING! Before removing the routing-mesh network, make sure all the nodes
    in your swarm run the same docker engine version. Otherwise, removal may not
    be effective and functionality of newly created ingress networks will be
    impaired.
    Are you sure you want to continue? [y/N]
    ```

3.  使用 `--ingress` 标志以及您想要设置的自定义选项创建一个新的 overlay 网络。本示例将 MTU 设置为 1200，子网设置为 `10.11.0.0/16`，网关设置为 `10.11.0.2`。

    ```console
    $ docker network create \
      --driver overlay \
      --ingress \
      --subnet=10.11.0.0/16 \
      --gateway=10.11.0.2 \
      --opt com.docker.network.driver.mtu=1200 \
      my-ingress
    ```

    > [!NOTE]
    > 
    > 您可以将 `ingress` 网络命名为 `ingress` 之外的其他名称，但只能有一个。尝试创建第二个将失败。

4.  重启您在第一步中停止的服务。

## 自定义 docker_gwbridge

`docker_gwbridge` 是一个虚拟网桥，它将 overlay 网络 (包括 `ingress` 网络) 连接到单个 Docker 守护进程的物理网络。Docker 在您初始化 Swarm 或将 Docker 主机加入 Swarm 时会自动创建它，但它不是 Docker 设备。它存在于 Docker 主机的内核中。如果您需要自定义其设置，必须在将 Docker 主机加入 Swarm 之前，或在临时将主机从 Swarm 中移除之后执行此操作。

您需要在操作系统上安装 `brctl` 应用程序才能删除现有的网桥。软件包名称为 `bridge-utils`。

1.  停止 Docker。

2.  使用 `brctl show docker_gwbridge` 命令检查是否存在名为 `docker_gwbridge` 的网桥设备。如果是，使用 `brctl delbr docker_gwbridge` 将其移除。

3.  启动 Docker。不要加入或初始化 Swarm。

4.  使用您的自定义设置创建或重新创建 `docker_gwbridge` 网桥。本示例使用子网 `10.11.0.0/16`。有关可自定义选项的完整列表，请参阅 [Bridge 驱动程序选项](/reference/cli/docker/network/create.md#bridge-driver-options)。

    ```console
    $ docker network create \
    --subnet 10.11.0.0/16 \
    --opt com.docker.network.bridge.name=docker_gwbridge \
    --opt com.docker.network.bridge.enable_icc=false \
    --opt com.docker.network.bridge.enable_ip_masquerade=true \
    docker_gwbridge
    ```

5.  初始化或加入 Swarm。

## 为控制和数据流量使用独立的接口

默认情况下，所有的 Swarm 流量都在同一个接口上发送，包括用于维护 Swarm 本身的控制和管理流量，以及往返服务容器的数据流量。

You can separate these traffic flows by passing the `--data-path-addr` flag when initializing or joining a Swarm. If you have multiple interfaces, you must explicitly specify `--advertise-addr`, and if it is not specified, `--data-path-addr` defaults to `--advertise-addr`. Traffic for joining, leaving, and managing the Swarm is sent over the `--advertise-addr` interface, while traffic between service containers is sent over the `--data-path-addr` interface. These flags can accept an IP address or a network device name (e.g., `eth0`).

This example initializes a Swarm using a separate `--data-path-addr`. It assumes your Docker host has two different network interfaces: 10.0.0.1 for control and management traffic, and 192.168.0.1 for service-related traffic.

```console
$ docker swarm init --advertise-addr 10.0.0.1 --data-path-addr 192.168.0.1
```

This example joins a Swarm managed by host `192.168.99.100:2377`, setting the `--advertise-addr` flag to `eth0` and the `--data-path-addr` flag to `eth1`.

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  --advertise-addr eth0 \
  --data-path-addr eth1 \
  192.168.99.100:2377
```

## 在 overlay 网络上发布端口

连接到同一个 overlay 网络的 Swarm 服务实际上向彼此暴露了所有端口。为了使端口在服务外部可访问，必须在 `docker service create` 或 `docker service update` 上使用 `-p` 或 `--publish` 标志 *发布* 该端口。同时支持传统的冒号分隔语法和较新的逗号分隔值语法。长语法由于具有一定的自文档性而受到推荐。

<table>
<thead>
<tr>
<th>标志值</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td><tt>-p 8080:80</tt> 或<br /><tt>-p published=8080,target=80</tt></td>
<td>将服务上的 TCP 80 端口映射到路由网格上的 8080 端口。</td>
</tr>
<tr>
<td><tt>-p 8080:80/udp</tt> 或<br /><tt>-p published=8080,target=80,protocol=udp</tt></td>
<td>将服务上的 UDP 80 端口映射到路由网格上的 8080 端口。</td>
</tr>
<tr>
<td><tt>-p 8080:80/tcp -p 8080:80/udp</tt> 或 <br /><tt>-p published=8080,target=80,protocol=tcp -p published=8080,target=80,protocol=udp</tt></td>
<td>将服务上的 TCP 80 端口映射到路由网格上的 TCP 8080 端口，并将服务上的 UDP 80 端口映射到路由网格上的 UDP 8080 端口。</td>
</tr>
</tbody>
</table>

## 了解更多

* [将服务部署到 Swarm](services.md)
* [Swarm 管理指南](admin_guide.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)
* [网络概览](/manuals/engine/network/_index.md)
* [Docker CLI 参考](/reference/cli/docker/)
