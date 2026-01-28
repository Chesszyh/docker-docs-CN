---
description: 查找与网络和虚拟化相关的常见问题解答
keywords: Docker, Docker Hub, Docker Desktop security FAQs, security, platform, networks, vms
title: 网络和虚拟机常见问题
linkTitle: 网络和虚拟机
weight: 30
tags: [FAQ]
aliases:
- /faq/security/networking-and-vms/
---

### 当容器运行时，如何限制其允许的互联网访问类型，以防止其泄露数据或下载恶意代码？

没有内置机制来实现此目的，但可以通过主机上的进程级防火墙来解决。挂钩到 `com.docker.vpnkit` 用户空间进程，并应用规则限制其可以连接的位置（DNS URL 白名单；数据包/负载过滤器）以及允许使用的端口/协议。

### 我可以阻止用户在 0.0.0.0 上绑定端口吗？

没有直接的方法通过 Docker Desktop 强制执行此操作，但它会继承主机上强制执行的任何防火墙规则。

### 有哪些选项可以将容器化网络设置锁定到系统？如果不支持，操纵这些设置会有什么后果？

Docker 网络设置完全在 VM 内部是本地的，对系统没有影响。

### 我可以通过本地防火墙或 VPN 客户端对容器网络流量应用规则吗？

对于网络连接，Docker Desktop 使用用户空间进程（`com.docker.vpnkit`），它继承启动它的用户的防火墙规则、VPN、HTTP 代理属性等约束。

### 使用 Hyper-V 后端运行 Docker Desktop for Windows 是否允许用户创建任意虚拟机？

不允许。`DockerDesktopVM` 名称在服务代码中是硬编码的，因此您不能使用 Docker Desktop 创建或操作任何其他虚拟机。

### 在 Mac 上使用 Docker Desktop 时，我可以阻止用户创建其他虚拟机吗？

在 Mac 上启动虚拟机是非特权操作，因此 Docker Desktop 不会强制执行此限制。

### 当使用 Hyper-V 和/或 WSL2 时，Docker Desktop 如何实现网络级隔离？

VM 进程对于 WSL 2（在 `docker-desktop` 发行版内部运行）和 Hyper-V（在 `DockerDesktopVM` 内部运行）是相同的。主机/VM 通信使用 `AF_VSOCK` 虚拟机监控程序套接字（共享内存）。它不使用 Hyper-V 网络交换机或网络接口。所有主机网络都是使用 `com.docker.vpnkit.exe` 和 `com.docker.backend.exe` 进程的普通 TCP/IP 套接字执行的。有关更多信息，请参阅 [Docker Desktop 网络工作原理揭秘](https://www.docker.com/blog/how-docker-desktop-networking-works-under-the-hood/)。
