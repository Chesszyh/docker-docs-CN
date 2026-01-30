---
description: Docker Engine Swarm 模式入门教程
keywords: tutorial, cluster management, swarm mode, docker engine, get started, 教程, 集群管理, 入门
title: Swarm 模式入门
toc_max: 4
---

本教程向您介绍 Docker Engine Swarm 模式的功能。在开始之前，您可能需要先熟悉一下 [核心概念](../key-concepts.md)。

本教程将引导您完成以下操作：

* 初始化一个以 Swarm 模式运行的 Docker Engine 集群
* 向 Swarm 添加节点
* 将应用程序服务部署到 Swarm
* 在一切运行起来后管理 Swarm

本教程使用在终端窗口命令行中输入的 Docker Engine CLI 命令。

如果您完全是 Docker 新手，请参阅 [关于 Docker Engine](../../_index.md)。

## 设置

要运行本教程，您需要：

* [三台可以进行网络通信且已安装 Docker 的 Linux 主机](#three-networked-host-machines)
* [管理节点机器的 IP 地址](#the-ip-address-of-the-manager-machine)
* [主机之间开放的端口](#open-protocols-and-ports-between-the-hosts)

### 三台联网的主机

本教程需要三台已安装 Docker 且可以通过网络通信的 Linux 主机。这些主机可以是物理机、虚拟机、Amazon EC2 实例或以其他方式托管的主机。查看 [部署到 Swarm](/guides/swarm-deploy.md#prerequisites) 以了解一种可能的主机设置方案。

其中一台机器是管理节点 (称为 `manager1`)，另外两台是工作节点 (`worker1` 和 `worker2`)。

> [!NOTE]
>
> 您也可以按照教程中的许多步骤来测试单节点 Swarm，在这种情况下您只需要一台主机。虽然多节点命令无法工作，但您可以初始化 Swarm、创建服务并对其进行扩展。

#### 在 Linux 机器上安装 Docker Engine

如果您使用基于 Linux 的物理机或云提供的计算机作为主机，只需按照适用于您平台的 [Linux 安装说明](../../install/_index.md) 操作即可。启动三台机器，您就准备好了。您可以在 Linux 机器上测试单节点和多节点 Swarm 场景。

### 管理节点机器的 IP 地址

IP 地址必须分配给主机操作系统可用的网络接口。Swarm 中的所有节点都需要通过该 IP 地址连接到管理节点。

由于其他节点通过管理节点的 IP 地址与其联系，因此您应该使用固定的 IP 地址。

您可以在 Linux 或 macOS 上运行 `ifconfig` 查看可用网络接口的列表。

本教程使用 `manager1` 的 IP 地址：`192.168.99.100`。

### 主机之间开放的协议和端口

以下端口必须可用。在某些系统上，这些端口默认是开放的。

* 端口 `2377` TCP：用于管理节点之间的通信
* 端口 `7946` TCP/UDP：用于 overlay 网络节点发现
* 端口 `4789` UDP (可配置)：用于 overlay 网络流量

如果您打算创建带有加密功能的 overlay 网络 (`--opt encrypted`)，还需要确保允许 IP 协议 50 (IPSec ESP) 流量。

端口 `4789` 是 Swarm 数据路径端口 (也称为 VXLAN 端口) 的默认值。防止任何不可信流量到达此端口非常重要，因为 VXLAN 不提供身份验证。此端口应仅对受信任的网络开放，绝不能在边界防火墙上开放。

如果 Swarm 流量经过的网络不是完全可信的，强烈建议使用加密的 overlay 网络。如果排他性地使用加密的 overlay 网络，建议进行一些额外的加固：

* [自定义默认 ingress 网络](../networking.md) 以使用加密
* 仅在数据路径端口上接受加密数据包：

```bash
# iptables 规则示例 (顺序和其他工具可能需要自定义)
iptables -I INPUT -m udp --dport 4789 -m policy --dir in --pol none -j DROP
```

## 下一步

接下来，您将创建一个 Swarm。

{{< button text="创建一个 Swarm" url="create-swarm.md" >}}
