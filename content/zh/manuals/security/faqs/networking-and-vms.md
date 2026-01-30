---
description: 查找与网络和虚拟化相关的常见问题解答
keywords: Docker, Docker Hub, Docker Desktop 安全 FAQ, 安全, 平台, 网络, 虚拟机
title: 网络和虚拟机常见问题 (FAQ)
linkTitle: 网络和虚拟机
weight: 30
tags: [FAQ]
aliases:
- /faq/security/networking-and-vms/
---

### 容器运行时，我该如何限制其允许的互联网访问类型，以防止其外泄数据或下载恶意代码？

目前没有内置机制可以实现这一点，但可以通过主机上的进程级防火墙来解决。挂钩到 `com.docker.vpnkit` 用户空间进程，并应用有关其可以连接到何处 (DNS URL 白名单；数据包/负载过滤器) 以及允许使用哪些端口/协议的规则。

### 我能否阻止用户将端口绑定到 0.0.0.0？

没有直接的方法可以通过 Docker Desktop 强制执行此操作，但它会继承主机上强制执行的任何防火墙规则。

### 有哪些选项可以将容器化的网络设置锁定到系统中？如果不支持，操作这些设置会有什么后果吗？

Docker 网络设置完全在虚拟机内部本地化，对系统没有影响。

### 我能否通过本地防火墙或 VPN 客户端对容器网络流量应用规则？

对于网络连接，Docker Desktop 使用一个用户空间进程 (`com.docker.vpnkit`)，该进程继承了启动它的用户的约束条件，如防火墙规则、VPN、HTTP 代理属性等。

### 在使用 Hyper-V 后端的 Windows 版 Docker Desktop 运行时，是否允许用户创建任意虚拟机？

不允许。`DockerDesktopVM` 名称在服务代码中是硬编码的，因此您无法使用 Docker Desktop 来创建或操作任何其他虚拟机。

### 我在使用 Mac 版 Docker Desktop 时，能否防止我们的用户创建其他虚拟机？

在 Mac 上启动虚拟机是非特权操作，因此 Docker Desktop 不对此进行强制限制。

### 当使用 Hyper-V 和/或 WSL2 时，Docker Desktop 是如何实现网络级隔离的？

WSL 2 (在 `docker-desktop` 发行版内部运行) 和 Hyper-V (在 `DockerDesktopVM` 内部运行) 的虚拟机进程是相同的。主机/虚拟机通信使用 `AF_VSOCK` 管理程序套接字 (共享内存)。它不使用 Hyper-V 网络交换机或网络接口。所有主机联网都是使用来自 `com.docker.vpnkit.exe` 和 `com.docker.backend.exe` 进程的普通 TCP/IP 套接字执行的。更多信息请参阅 [Docker Desktop 联网底层原理 (英文)](https://www.docker.com/blog/how-docker-desktop-networking-works-under-the-hood/)。
