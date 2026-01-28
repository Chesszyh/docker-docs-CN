---
description: Use the routing mesh to publish services externally to a swarm
keywords: guide, swarm mode, swarm, network, ingress, routing mesh
title: 使用 Swarm 模式路由网格
---

Docker Engine Swarm 模式使得将服务端口发布到 swarm 外部资源变得容易。所有节点都参与 ingress 路由网格。路由网格使 swarm 中的每个节点都能在已发布端口上接受 swarm 中任何服务的连接，即使该节点上没有运行任务。路由网格将所有传入请求路由到可用节点上的活动容器上的已发布端口。

要在 swarm 中使用 ingress 网络，您需要在启用 Swarm 模式之前在 swarm 节点之间打开以下端口：

* 端口 `7946` TCP/UDP，用于容器网络发现。
* 端口 `4789` UDP（可配置），用于容器 ingress 网络。

在 Swarm 中设置网络时，应特别注意。请参阅[教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts)以获取概述。

您还必须在 swarm 节点和任何需要访问该端口的外部资源（如外部负载均衡器）之间打开已发布的端口。

您还可以为给定服务[绕过路由网格](#bypass-the-routing-mesh)。

## 为服务发布端口

创建服务时使用 `--publish` 标志来发布端口。`target` 用于指定容器内的端口，`published` 用于指定要绑定到路由网格上的端口。如果省略 `published` 端口，则会为每个服务任务绑定一个随机的高端口号。您需要检查任务以确定端口。

```console
$ docker service create \
  --name <SERVICE-NAME> \
  --publish published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  <IMAGE>
```

> [!NOTE]
>
> 此语法的旧形式是用冒号分隔的字符串，其中已发布端口在前，目标端口在后，例如 `-p 8080:80`。新语法更受推荐，因为它更易于阅读并允许更大的灵活性。

`<PUBLISHED-PORT>` 是 swarm 使服务可用的端口。如果省略它，则会绑定一个随机的高端口号。`<CONTAINER-PORT>` 是容器监听的端口。此参数是必需的。

例如，以下命令将 nginx 容器中的端口 80 发布到 swarm 中任何节点的端口 8080：

```console
$ docker service create \
  --name my-web \
  --publish published=8080,target=80 \
  --replicas 2 \
  nginx
```

当您访问任何节点上的端口 8080 时，Docker 会将您的请求路由到活动容器。在 swarm 节点本身上，端口 8080 实际上可能没有被绑定，但路由网格知道如何路由流量并防止任何端口冲突发生。

路由网格在分配给节点的任何 IP 地址上的已发布端口上监听。对于外部可路由的 IP 地址，该端口可从主机外部访问。对于所有其他 IP 地址，访问仅在主机内可用。

![Service ingress image](images/ingress-routing-mesh.webp)

您可以使用以下命令为现有服务发布端口：

```console
$ docker service update \
  --publish-add published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  <SERVICE>
```

您可以使用 `docker service inspect` 查看服务的已发布端口。例如：

```console
$ docker service inspect --format="{{json .Endpoint.Spec.Ports}}" my-web

[{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080}]
```

输出显示容器的 `<CONTAINER-PORT>`（标记为 `TargetPort`）和节点为服务监听请求的 `<PUBLISHED-PORT>`（标记为 `PublishedPort`）。

### 仅发布 TCP 端口或仅发布 UDP 端口

默认情况下，当您发布端口时，它是 TCP 端口。您可以专门发布 UDP 端口，而不是或除了 TCP 端口。当您同时发布 TCP 和 UDP 端口时，如果省略协议说明符，端口将作为 TCP 端口发布。如果使用较长的语法（推荐），请将 `protocol` 键设置为 `tcp` 或 `udp`。

#### 仅 TCP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  dns-cache
```

#### TCP 和 UDP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  -p 53:53/udp \
  dns-cache
```

#### 仅 UDP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53/udp \
  dns-cache
```

## 绕过路由网格

默认情况下，发布端口的 swarm 服务使用路由网格来实现。当您连接到任何 swarm 节点上的已发布端口时（无论它是否运行给定服务），您都会被透明地重定向到运行该服务的工作节点。实际上，Docker 充当 swarm 服务的负载均衡器。

您可以绕过路由网格，这样当您访问给定节点上的绑定端口时，您始终访问该节点上运行的服务实例。这称为 `host` 模式。有几点需要注意。

- 如果您访问未运行服务任务的节点，则该服务不会在该端口上监听。可能什么都没有监听，或者完全不同的应用程序在监听。

- 如果您期望在每个节点上运行多个服务任务（例如，当您有 5 个节点但运行 10 个副本时），则无法指定静态目标端口。要么让 Docker 分配一个随机的高端口号（通过省略 `published`），要么通过使用全局服务而不是复制服务或使用放置约束来确保每个给定节点上只运行一个服务实例。

要绕过路由网格，您必须使用长 `--publish` 服务并将 `mode` 设置为 `host`。如果省略 `mode` 键或将其设置为 `ingress`，则使用路由网格。以下命令使用 `host` 模式创建全局服务并绕过路由网格。

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp,mode=host \
  --mode global \
  dns-cache
```

## 配置外部负载均衡器

您可以为 swarm 服务配置外部负载均衡器，可以与路由网格结合使用，也可以完全不使用路由网格。

### 使用路由网格

您可以配置外部负载均衡器将请求路由到 swarm 服务。例如，您可以配置 [HAProxy](https://www.haproxy.org) 来平衡发布到端口 8080 的 nginx 服务的请求。

![Ingress with external load balancer image](images/ingress-lb.webp)

在这种情况下，负载均衡器和 swarm 中的节点之间必须打开端口 8080。swarm 节点可以位于代理服务器可访问但公共不可访问的私有网络上。

您可以将负载均衡器配置为在 swarm 中的每个节点之间平衡请求，即使该节点上没有调度任务。例如，您可以在 `/etc/haproxy/haproxy.cfg` 中有以下 HAProxy 配置：

```bash
global
        log /dev/log    local0
        log /dev/log    local1 notice
...snip...

# Configure HAProxy to listen on port 80
frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

# Configure HAProxy to route requests to swarm nodes on port 8080
backend http_back
   balance roundrobin
   server node1 192.168.99.100:8080 check
   server node2 192.168.99.101:8080 check
   server node3 192.168.99.102:8080 check
```

当您在端口 80 访问 HAProxy 负载均衡器时，它会将请求转发到 swarm 中的节点。swarm 路由网格将请求路由到活动任务。如果由于任何原因 swarm 调度程序将任务分派到不同的节点，您不需要重新配置负载均衡器。

您可以配置任何类型的负载均衡器将请求路由到 swarm 节点。要了解有关 HAProxy 的更多信息，请参阅 [HAProxy 文档](https://cbonte.github.io/haproxy-dconv/)。

### 不使用路由网格

要使用外部负载均衡器而不使用路由网格，请将 `--endpoint-mode` 设置为 `dnsrr` 而不是默认值 `vip`。在这种情况下，没有单个虚拟 IP。相反，Docker 为服务设置 DNS 条目，以便对服务名称的 DNS 查询返回 IP 地址列表，客户端直接连接到其中一个。

您不能将 `--endpoint-mode dnsrr` 与 `--publish mode=ingress` 一起使用。您必须在服务前面运行自己的负载均衡器。Docker 主机上对服务名称的 DNS 查询返回运行服务的节点的 IP 地址列表。配置您的负载均衡器使用此列表并在节点之间平衡流量。请参阅[配置服务发现](networking.md#configure-service-discovery)。

## 了解更多

* [将服务部署到 swarm](services.md)
