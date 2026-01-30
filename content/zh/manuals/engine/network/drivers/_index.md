---
title: 网络驱动程序
weight: 20
description: 了解 Docker 网络驱动程序的基础知识
keywords: networking, drivers, bridge, routing, routing mesh, overlay, ports, 网络, 驱动程序
---

Docker 的网络子系统是可插拔的，通过驱动程序实现。默认情况下存在几个驱动程序，它们提供了核心网络功能：

- `bridge`: 默认网络驱动程序。如果您不指定驱动程序，这就是您正在创建的网络类型。当您的应用程序运行在需要与同一主机上的其他容器通信的容器中时，通常使用 Bridge 网络。
  参见 [Bridge 网络驱动程序](bridge.md)。

- `host`: 移除容器与 Docker 主机之间的网络隔离，直接使用主机的网络。
  参见 [Host 网络驱动程序](host.md)。

- `overlay`: Overlay 网络将多个 Docker 守护进程连接在一起，使 Swarm 服务和容器能够跨节点通信。这种策略消除了执行操作系统级路由的需要。
  参见 [Overlay 网络驱动程序](overlay.md)。

- `ipvlan`: IPvlan 网络让用户完全控制 IPv4 和 IPv6 地址。VLAN 驱动程序在此基础上构建，为对底层网络集成感兴趣的用户提供对第 2 层 VLAN 标记甚至 IPvlan L3 路由的完全控制。
  参见 [IPvlan 网络驱动程序](ipvlan.md)。

- `macvlan`: Macvlan 网络允许您为容器分配 MAC 地址，使其在网络上显示为物理设备。Docker 守护进程通过 MAC 地址将流量路由到容器。在处理期望直接连接到物理网络而非通过 Docker 主机网络栈路由的遗留应用程序时，使用 `macvlan` 驱动程序有时是最佳选择。
  参见 [Macvlan 网络驱动程序](macvlan.md)。

- `none`: 将容器与主机及其他容器完全隔离。`none` 不适用于 Swarm 服务。
  参见 [None 网络驱动程序](none.md)。

- [网络插件](/engine/extend/plugins_network/): 您可以在 Docker 中安装和使用第三方网络插件。

### 网络驱动程序摘要

- 默认 bridge 网络适用于运行不需要特殊网络能力的容器。
- 用户定义 bridge 网络使同一 Docker 主机上的容器能够相互通信。用户定义网络通常为属于共同项目或组件的多个容器定义一个隔离网络。
- Host 网络与容器共享主机的网络。当您使用此驱动程序时，容器的网络不会与主机隔离。
- 当您需要运行在不同 Docker 主机上的容器进行通信，或者当多个应用程序使用 Swarm 服务协作时，Overlay 网络是最佳选择。
- 当您从虚拟机设置迁移，或需要容器在网络上看起来像物理主机 (每个都有唯一的 MAC 地址) 时，Macvlan 网络是最佳选择。
- IPvlan 与 Macvlan 类似，但不为容器分配唯一的 MAC 地址。当对可以分配给网络接口或端口的 MAC 地址数量有限制时，请考虑使用 IPvlan。
- 第三方网络插件允许您将 Docker 与专门的网络栈集成。

## 网络教程

现在您已经了解了有关 Docker 网络的基础知识，请通过以下教程深入了解：

- [独立运行网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Host 网络教程](/manuals/engine/network/tutorials/host.md)
- [Overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md)
