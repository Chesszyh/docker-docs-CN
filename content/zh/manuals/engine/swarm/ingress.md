---
description: 使用路由网格 (routing mesh) 向 Swarm 外部发布服务
keywords: guide, swarm mode, swarm, network, ingress, routing mesh, 路由网格
title: 使用 Swarm 模式路由网格
---

Docker Engine Swarm 模式可以轻松发布服务端口，使其对 Swarm 外部的资源可用。所有节点都参与入口路由网格 (ingress routing mesh)。路由网格使 Swarm 中的每个节点能够为 Swarm 中运行的任何服务接受已发布端口上的连接，即使该节点上没有运行任何任务。路由网格会将所有指向可用节点上已发布端口的入站请求路由到一个活动的容器。

要使用 Swarm 中的入口网络，在启用 Swarm 模式之前，您需要在 Swarm 节点之间开放以下端口：

* 端口 `7946` TCP/UDP：用于容器网络发现。
* 端口 `4789` UDP (可配置)：用于容器入口网络。

在 Swarm 中设置联网时应格外小心。参考 [教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts) 获取概览。

您还必须在 Swarm 节点与任何需要访问该端口的外部资源 (如外部负载均衡器) 之间开放已发布的端口。

您还可以为给定服务 [绕过路由网格](#bypass-the-routing-mesh)。

## 为服务发布端口

创建服务时，使用 `--publish` 标志发布端口。`target` 用于指定容器内部的端口，而 `published` 用于指定在路由网格上绑定的端口。如果您不指定 `published` 端口，则会为每个服务任务绑定一个随机的高端口号。您需要检查任务才能确定该端口。

```console
$ docker service create \
  --name <SERVICE-NAME> \
  --publish published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  <IMAGE>
```

> [!NOTE]
> 
> 这种语法的旧形式是冒号分隔的字符串，其中已发布端口在前，目标端口在后，例如 `-p 8080:80`。新语法由于更易读且更具灵活性而受到推荐。

`<PUBLISHED-PORT>` 是 Swarm 使服务可用的端口。如果省略，将绑定一个随机的高端口号。`<CONTAINER-PORT>` 是容器监听的端口。此参数是必填的。

例如，以下命令将 nginx 容器中的 80 端口发布到 Swarm 中任何节点的 8080 端口：

```console
$ docker service create \
  --name my-web \
  --publish published=8080,target=80 \
  --replicas 2 \
  nginx
```

当您访问任何节点上的 8080 端口时，Docker 会将您的请求路由到一个活动的容器。在 Swarm 节点本身上，8080 端口可能并没有被实际绑定，但路由网格知道如何路由流量并防止发生任何端口冲突。

路由网格会在分配给节点的任何 IP 地址上的已发布端口上进行监听。对于外部可路由的 IP 地址，该端口可从主机外部访问。对于所有其他 IP 地址，只能从主机内部访问。

![服务入口镜像](images/ingress-routing-mesh.webp)

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


输出显示了容器的 `<CONTAINER-PORT>` (标记为 `TargetPort`) 和节点监听服务请求的 `<PUBLISHED-PORT>` (标记为 `PublishedPort`)。

### 仅为 TCP 或仅为 UDP 发布端口

默认情况下，当您发布端口时，它是一个 TCP 端口。您可以专门发布一个 UDP 端口来代替 TCP 端口，或者与其并存。当您同时发布 TCP 和 UDP 端口时，如果您省略协议说明符，端口将作为 TCP 端口发布。如果您使用长语法 (推荐)，请将 `protocol` 键设置为 `tcp` 或 `udp`。

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

## 绕过路由网格 (Bypass the routing mesh)

默认情况下，发布端口的 Swarm 服务都使用路由网格。当您连接到任何 Swarm 节点上的已发布端口时 (无论它是否正在运行该服务)，您都会被透明地重定向到正在运行该服务的工作节点。实际上，Docker 充当了您 Swarm 服务的负载均衡器。

您可以绕过路由网格，这样当您访问给定节点上的绑定端口时，您始终是在访问运行在该节点上的服务实例。这被称为 `host` 模式。有几点需要注意：

- 如果您访问一个未运行该服务任务的节点，该服务将不会在该端口上监听。可能没有任何东西在监听，或者完全是另一个应用程序在监听。

- 如果您期望在每个节点上运行多个服务任务 (例如当您有 5 个节点但运行 10 个副本时)，您不能指定一个静态的目标端口。要么允许 Docker 分配一个随机的高端口号 (通过省去 `published` 部分)，要么通过使用全局服务 (global service) 而不是复制服务 (replicated service)，或者通过使用放置约束 (placement constraints) 来确保在给定节点上只运行一个服务实例。

要绕过路由网格，您必须使用长格式的 `--publish` 选项并将 `mode` 设置为 `host`。如果您省略 `mode` 键或将其设置为 `ingress`，则会使用路由网格。以下命令使用 `host` 模式并绕过路由网格创建一个全局服务。

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp,mode=host \
  --mode global \
  dns-cache
```

## 配置外部负载均衡器

您可以为 Swarm 服务配置外部负载均衡器，可以结合路由网格使用，也可以完全不使用路由网格。

### 使用路由网格

您可以配置外部负载均衡器来将请求路由到 Swarm 服务。例如，您可以配置 [HAProxy](https://www.haproxy.org) 来对发布在 8080 端口上的 nginx 服务进行负载均衡。

![带有外部负载均衡器的入口镜像](images/ingress-lb.webp)

在这种情况下，负载均衡器与 Swarm 中的节点之间必须开放 8080 端口。Swarm 节点可以位于代理服务器可访问的私有网络中，但不一定需要公开访问。

您可以配置负载均衡器在 Swarm 中的每个节点之间平衡请求，即使该节点上没有调度任务。例如，您可以在 `/etc/haproxy/haproxy.cfg` 中使用以下 HAProxy 配置：

```bash
global
        log /dev/log    local0
        log /dev/log    local1 notice
...snip...

# 配置 HAProxy 监听 80 端口
frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

# 配置 HAProxy 将请求路由到 8080 端口上的 Swarm 节点
backend http_back
   balance roundrobin
   server node1 192.168.99.100:8080 check
   server node2 192.168.99.101:8080 check
   server node3 192.168.99.102:8080 check
```

当您访问 HAProxy 负载均衡器的 80 端口时，它会将请求转发到 Swarm 中的节点。Swarm 路由网格随后将请求路由到一个活动任务。如果出于任何原因 Swarm 调度程序将任务分发到了不同的节点，您无需重新配置负载均衡器。

您可以配置任何类型的负载均衡器来将请求路由到 Swarm 节点。要了解有关 HAProxy 的更多信息，请参阅 [HAProxy 文档](https://cbonte.github.io/haproxy-dconv/)。

### 不使用路由网格

要使用不带路由网格的外部负载均衡器，请将 `--endpoint-mode` 设置为 `dnsrr` 而不是默认值 `vip`。在这种情况下，没有单一的虚拟 IP。相反，Docker 为服务设置 DNS 条目，使得对服务名称的 DNS 查询会返回一组 IP 地址列表，客户端直接连接到其中之一。

您不能将 `--endpoint-mode dnsrr` 与 `--publish mode=ingress` 同时使用。您必须在服务前端运行自己的负载均衡器。在 Docker 主机上对服务名称进行 DNS 查询会返回运行该服务的所有节点的 IP 地址列表。配置您的负载均衡器以消费此列表并在节点之间平衡流量。参见 [配置服务发现](networking.md#configure-service-discovery)。

## 了解更多

* [将服务部署到 Swarm](services.md)
