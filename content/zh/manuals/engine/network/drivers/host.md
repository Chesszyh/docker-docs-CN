---
title: Host 网络驱动程序
description: 关于在 Docker 主机网络上暴露容器的一切
keywords: network, host, standalone, host mode networking, 网络, 主机模式, 独立运行
---

如果您为容器使用 `host` 网络模式，该容器的网络栈将不会与 Docker 主机隔离 (容器共享主机的网络命名空间)，并且容器不会获得分配给它的 IP 地址。例如，如果您运行一个绑定到 80 端口的容器并使用 `host` 网络，该容器的应用程序将可在主机的 IP 地址的 80 端口上访问。

> [!NOTE]
>
> 鉴于使用 `host` 模式网络时容器没有自己的 IP 地址，[端口映射 (port-mapping)](overlay.md#publish-ports) 不会生效，并且 `-p`、`--publish`、`-P` 和 `--publish-all` 选项会被忽略，并产生警告：
>
> ```console
> WARNING: Published ports are discarded when using host network mode
> ```

主机模式网络在以下用例中非常有用：

- 优化性能
- 容器需要处理大量端口的情况

这是因为它不需要网络地址转换 (NAT)，并且不会为每个端口创建 "userland-proxy"。

Docker Engine (仅限 Linux) 和 Docker Desktop 4.34 及更高版本支持 host 网络驱动程序。

您也可以通过向 `docker service create` 命令传递 `--network host`，为 swarm 服务使用 `host` 网络。在这种情况下，控制流量 (与管理 swarm 和服务相关的流量) 仍通过 overlay 网络发送，但各个 swarm 服务容器使用 Docker 守护进程的主机网络和端口发送数据。这会产生一些额外的限制。例如，如果服务容器绑定到 80 端口，则给定的 swarm 节点上只能运行一个服务容器。

## Docker Desktop

Docker Desktop 4.34 及更高版本支持主机网络。要启用此功能：

1. 在 Docker Desktop 中登录您的 Docker 帐户。
2. 导航到 **Settings** (设置)。
3. 在 **Resources** (资源) 选项卡下，选择 **Network** (网络)。
4. 勾选 **Enable host networking** (启用主机网络) 选项。
5. 选择 **Apply and restart** (应用并重启)。

此功能是双向工作的。这意味着您可以从主机访问运行在容器中的服务器，也可以从启用主机网络启动的任何容器访问运行在主机上的服务器。支持 TCP 和 UDP 通信协议。

### 示例

以下命令启动容器中的 netcat，监听 `8000` 端口：

```console
$ docker run --rm -it --net=host nicolaka/netshoot nc -lkv 0.0.0.0 8000
```

`8000` 端口将在主机上可用，您可以从另一个终端使用以下命令连接到它：

```console
$ nc localhost 8000
```

您在此处输入的内容将出现在运行容器的终端上。

要从容器访问运行在主机上的服务，您可以使用此命令启动启用主机网络的容器：

```console
$ docker run --rm -it --net=host nicolaka/netshoot
```

如果您随后想从容器访问主机上的服务 (在此示例中是运行在 `80` 端口上的 Web 服务器)，您可以这样做：

```console
$ nc localhost 80
```

### 限制

- 容器内的进程无法绑定到主机的 IP 地址，因为容器无法直接访问主机的接口。
- Docker Desktop 的主机网络功能工作在第 4 层。这意味着与 Linux 上的 Docker 不同，不支持在 TCP 或 UDP 之下的网络协议。
- 此功能在启用增强容器隔离 (Enhanced Container Isolation) 时不起作用，因为将容器与主机隔离并允许它们访问主机网络是相互矛盾的。
- 仅支持 Linux 容器。主机网络不适用于 Windows 容器。

## 后续步骤

- 学习 [host 网络教程](/manuals/engine/network/tutorials/host.md)
- 了解 [从容器角度看的网络](../_index.md)
- 了解 [bridge 网络](./bridge.md)
- 了解 [overlay 网络](./overlay.md)
- 了解 [Macvlan 网络](./macvlan.md)
