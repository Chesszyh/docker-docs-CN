---
description: Getting Started tutorial for Docker Engine Swarm mode
keywords: tutorial, cluster management, swarm mode, docker engine, get started
title: Swarm 模式入门
toc_max: 4
---

本教程向你介绍 Docker 引擎 Swarm 模式的功能。在开始之前，你可能需要先熟悉[关键概念](../key-concepts.md)。

本教程将指导你完成：

* 以 swarm 模式初始化 Docker 引擎集群
* 向 swarm 添加节点
* 将应用程序服务部署到 swarm
* 在一切运行后管理 swarm

本教程使用在终端窗口命令行中输入的 Docker 引擎 CLI 命令。

如果你对 Docker 完全陌生，请参阅[关于 Docker 引擎](../../_index.md)。

## 设置

要运行本教程，你需要：

* [三台可以通过网络通信且已安装 Docker 的 Linux 主机](#three-networked-host-machines)
* [管理节点机器的 IP 地址](#the-ip-address-of-the-manager-machine)
* [主机之间开放的端口](#open-protocols-and-ports-between-the-hosts)

### 三台联网的主机

本教程需要三台已安装 Docker 且可以通过网络通信的 Linux 主机。这些可以是物理机、虚拟机、Amazon EC2 实例，或以其他方式托管。查看[部署到 Swarm](/guides/swarm-deploy.md#prerequisites) 了解主机的一种可能设置方式。

其中一台机器是管理节点（称为 `manager1`），另外两台是工作节点（`worker1` 和 `worker2`）。

> [!NOTE]
>
> 你也可以按照许多教程步骤来测试单节点 swarm，在这种情况下你只需要一台主机。多节点命令将无法工作，但你可以初始化 swarm、创建服务并扩展它们。

#### 在 Linux 机器上安装 Docker 引擎

如果你使用基于 Linux 的物理计算机或云提供的计算机作为主机，只需按照你的平台的 [Linux 安装说明](../../install/_index.md)进行操作。启动三台机器，然后你就准备好了。你可以在 Linux 机器上测试单节点和多节点 swarm 场景。

### 管理节点机器的 IP 地址

IP 地址必须分配给主机操作系统可用的网络接口。swarm 中的所有节点都需要通过该 IP 地址连接到管理节点。

因为其他节点通过管理节点的 IP 地址联系管理节点，所以你应该使用固定 IP 地址。

你可以在 Linux 或 macOS 上运行 `ifconfig` 来查看可用网络接口的列表。

本教程使用 `manager1`：`192.168.99.100`。

### 主机之间开放的协议和端口

以下端口必须可用。在某些系统上，这些端口默认是开放的。

* 端口 `2377` TCP 用于与管理节点之间以及管理节点之间的通信
* 端口 `7946` TCP/UDP 用于覆盖网络节点发现
* 端口 `4789` UDP（可配置）用于覆盖网络流量

如果你计划创建加密的覆盖网络（`--opt encrypted`），你还需要确保允许 IP 协议 50（IPSec ESP）流量。

端口 `4789` 是 Swarm 数据路径端口的默认值，也称为 VXLAN 端口。重要的是要防止任何不受信任的流量到达此端口，因为 VXLAN 不提供身份验证。此端口应该只对受信任的网络开放，永远不要在边界防火墙上开放。

如果 Swarm 流量经过的网络不是完全受信任的，强烈建议使用加密的覆盖网络。如果专门使用加密的覆盖网络，建议进行一些额外的加固：

* [自定义默认入口网络](../networking.md)以使用加密
* 仅在数据路径端口上接受加密数据包：

```bash
# Example iptables rule (order and other tools may require customization)
iptables -I INPUT -m udp --dport 4789 -m policy --dir in --pol none -j DROP
```

## 下一步

接下来，你将创建一个 swarm。

{{< button text="创建 swarm" url="create-swarm.md" >}}
