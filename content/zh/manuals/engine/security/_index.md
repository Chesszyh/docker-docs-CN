---
description: Docker 守护进程攻击面评估
keywords: Docker, Docker documentation, security, 安全
title: Docker Engine 安全
linkTitle: 安全
weight: 80
aliases:
- /articles/security/
- /engine/articles/security/
- /engine/security/security/
- /security/security/
---

在评估 Docker 安全时，有四个主要领域需要考虑：

 - 内核的内在安全及其对命名空间 (namespaces) 和控制组 (cgroups) 的支持
 - Docker 守护进程本身的攻击面
 - 默认或由用户自定义的容器配置文件的漏洞。
 - 内核的“加固”安全特性及其与容器的交互。

## 内核命名空间 (Kernel namespaces)

Docker 容器与 LXC 容器非常相似，它们具有相似的安全特性。当您使用 `docker run` 启动容器时，Docker 在后台为该容器创建了一组命名空间和控制组。

命名空间提供了第一种也是最直接的隔离形式。在容器内运行的进程无法看到，更不用说影响运行在另一个容器中或宿主机系统中的进程。

每个容器还拥有自己的网络栈，这意味着一个容器无法获得对另一个容器套接字或接口的特权访问。当然，如果宿主机系统配置得当，容器可以通过各自的网络接口相互交互 —— 就像它们可以与外部主机交互一样。当您为容器指定公共端口或使用 [链接 (links)](/manuals/engine/network/links.md) 时，容器之间允许 IP 流量。它们可以互相 ping、发送/接收 UDP 数据包并建立 TCP 连接，但如有必要，可以对其进行限制。从网络架构的角度来看，给定 Docker 主机上的所有容器都位于网桥接口上。这意味着它们就像通过公共以太网交换机连接的物理机一样；不多不少。

提供内核命名空间和私有网络的代码有多成熟？内核命名空间是在 [内核版本 2.6.15 到 2.6.26 之间](https://man7.org/linux/man-pages/man7/namespaces.7.html) 引入的。这意味着自 2008 年 7 月 (2.6.26 版本发布日期) 以来，命名空间代码已在大量生产系统中得到了实践和审视。而且还不止于此：命名空间代码的设计和灵感甚至更久远。命名空间实际上是努力以一种可以合并到主流内核中的方式重新实现 [OpenVZ](https://en.wikipedia.org/wiki/OpenVZ) 的功能。而 OpenVZ 最初发布于 2005 年，因此设计和实现都相当成熟。

## 控制组 (Control groups)

控制组 (cgroups) 是 Linux 容器的另一个关键组件。它们实现了资源核算和限制。它们提供了许多有用的指标，但也帮助确保每个容器都能获得公平份额的内存、CPU、磁盘 I/O；更重要的是，确保单个容器不会通过耗尽其中一种资源而导致系统崩溃。

因此，虽然它们在防止一个容器访问或影响另一个容器的数据和进程方面不起作用，但它们对于抵御某些拒绝服务攻击至关重要。它们在多租户平台 (如公共和私有 PaaS) 上尤为重要，即使某些应用程序开始出现异常行为，也能保证一致的运行时间 (和性能)。

控制组也已经存在了一段时间：代码始于 2006 年，最初合并在内核 2.6.24 中。

## Docker 守护进程攻击面

使用 Docker 运行容器 (和应用程序) 意味着运行 Docker 守护进程。除非您选择使用 [无根模式 (Rootless mode)](rootless.md)，否则该守护进程需要 `root` 特权，因此您应该意识到一些重要的细节。

首先，只有受信任的用户才应被允许控制您的 Docker 守护进程。这是一些强大的 Docker 特性的直接结果。具体来说，Docker 允许您在 Docker 主机和客户机容器之间共享目录；并且允许您在不限制容器访问权限的情况下这样做。这意味着您可以启动一个容器，其中的 `/host` 目录是您主机上的 `/` 目录；容器可以不受任何限制地更改您的主机文件系统。这类似于虚拟化系统允许文件系统资源共享。没有什么能阻止您与虚拟机共享根文件系统 (甚至根块设备)。

这具有很强的安全影响：例如，如果您通过 Web 服务器控制 Docker 以通过 API 预配容器，您应该比平时更加小心参数检查，以确保恶意用户无法传递精心构造的参数导致 Docker 创建任意容器。

出于这个原因，REST API 端点 (Docker CLI 用来与 Docker 守护进程通信) 在 Docker 0.5.2 中发生了变化，现在使用 Unix 套接字而不是绑定在 127.0.0.1 上的 TCP 套接字 (如果恰好在虚拟机之外的本地机器上直接运行 Docker，后者容易受到跨站请求伪造攻击)。然后，您可以使用传统的 Unix 权限检查来限制对控制套接字的访问。

如果您明确决定这样做，也可以通过 HTTP 暴露 REST API。但是，如果这样做，请注意上述安全影响。请注意，即使您有防火墙来限制来自网络中其他主机的 REST API 端点访问，该端点仍可能从容器中访问，并且很容易导致特权提升。因此，**必须** 使用 [HTTPS 和证书](protect-access.md) 来保护 API 端点。不允许在没有 TLS 的情况下通过 HTTP 暴露守护进程 API，这种配置会导致守护进程在启动早期失败，参见 [未经过身份验证的 TCP 连接](../deprecated.md#unauthenticated-tcp-connections)。还建议确保只能从受信任的网络或 VPN 访问它。

如果您更喜欢 SSH 而不是 TLS，也可以使用 `DOCKER_HOST=ssh://USER@HOST` 或 `ssh -L /path/to/docker.sock:/var/run/docker.sock`。

守护进程也可能容易受到其他输入的影响，例如通过 `docker load` 从磁盘加载镜像，或通过 `docker pull` 从网络加载镜像。从 Docker 1.3.2 开始，镜像现在在 Linux/Unix 平台上通过 chroot 的子进程进行提取，这是朝着权限分离迈出的更广泛努力的第一步。从 Docker 1.10.0 开始，所有镜像都通过其内容的加密校验和进行存储和访问，限制了攻击者导致与现有镜像冲突的可能性。

最后，如果您在服务器上运行 Docker，建议在服务器上仅运行 Docker，并将所有其他服务移至 Docker 控制的容器内。当然，保留您喜欢的管理工具 (可能至少是一个 SSH 服务器) 以及现有的监控/监督进程 (如 NRPE 和 collectd) 是可以的。

## Linux 内核能力 (Capabilities)

默认情况下，Docker 启动容器时带有一组受限的能力。这意味着什么？

能力 (Capabilities) 将二进制的“root/非 root”二分法转变为精细的访问控制系统。仅需要在 1024 以下端口绑定的进程 (如 Web 服务器) 不需要以 root 身份运行：它们可以被授予 `net_bind_service` 能力。此外还有许多其他能力，涵盖了几乎所有通常需要 root 特权的特定领域。这对容器安全意义重大。

典型的服务器以 `root` 身份运行多个进程，包括 SSH 守护进程、`cron` 守护进程、日志守护进程、内核模块、网络配置工具等。容器则不同，因为几乎所有这些任务都由容器周围的基础设施处理：

 - SSH 访问通常由运行在 Docker 主机上的单个服务器管理
 - `cron` 在必要时应作为用户进程运行，专为需要其调度服务的应用定制，而不是作为平台范围的设施
 - 日志管理也通常交给 Docker，或交给 Loggly 或 Splunk 等第三方服务
 - 硬件管理是无关的，这意味着您永远不需要在容器内运行 `udevd` 或等效的守护进程
 - 网络管理发生在容器外部，尽可能强制执行关注点分离，这意味着容器永远不需要执行 `ifconfig`、`route` 或 ip 命令 (当然，除非容器是专门设计为充当路由器或防火墙的)

这意味着在大多数情况下，容器根本不需要“真正的” root 特权。因此，容器可以运行在减少的能力集下；这意味着容器内的 "root" 拥有的特权远少于真正的 "root"。例如，可以：

 - 拒绝所有 "mount" 操作
 - 拒绝访问原始套接字 (以防止数据包欺骗)
 - 拒绝访问某些文件系统操作，如创建新设备节点、更改文件所有者或更改属性 (包括不可变标志)
 - 拒绝模块加载

这意味着即使入侵者设法在容器内提升到 root 权限，也很难造成严重破坏，或提升到宿主机。

这不会影响常规的 Web 应用，但大大减少了恶意用户的攻击媒介。默认情况下，Docker 会丢弃除 [所需能力](https://github.com/moby/moby/blob/master/oci/caps/defaults.go#L6-L19) 之外的所有能力，这是一种白名单而非黑名单的方法。您可以在 [Linux 手册页](https://man7.org/linux/man-pages/man7/capabilities.7.html) 中查看可用能力的完整列表。

运行 Docker 容器的一个主要风险是，分配给容器的默认能力集和挂载可能无法提供完全的隔离，无论是独立存在还是与内核漏洞结合使用。

Docker 支持添加和移除能力，允许使用非默认配置文件。这可能通过移除能力使 Docker 更安全，或者通过添加能力使其安全性降低。用户的最佳实践是移除除进程显式需要的能力之外的所有能力。

## Docker 内容信托 (Content Trust) 签名验证

Docker Engine 可以配置为仅运行签名的镜像。Docker 内容信托签名验证功能直接内置在 `dockerd` 二进制文件中。这在 Dockerd 配置文件中进行配置。

要启用此功能，可以在 `daemon.json` 中配置 trustpinning，从而只能拉取和运行使用用户指定的根密钥签名的仓库。
  
此功能为管理员提供了比以前通过 CLI 执行镜像签名验证更多的见解。

有关配置 Docker 内容信托签名验证的更多信息，请参阅 [Docker 中的内容信托](trust/_index.md)。

## 其他内核安全特性

能力只是现代 Linux 内核提供的众多安全特性之一。在 Docker 中也可以利用现有的知名系统，如 TOMOYO、AppArmor、SELinux、GRSEC 等。

虽然 Docker 目前仅启用能力，但它不会干扰其他系统。这意味着有很多不同的方法可以加固 Docker 主机。以下是几个示例。

 - 您可以运行带有 GRSEC 和 PAX 的内核。这增加了许多编译时和运行时的安全检查；由于地址随机化等技术，它还挫败了许多漏洞利用。它不需要 Docker 特定的配置，因为这些安全特性适用于整个系统，独立于容器。
 - 如果您的发行版附带了适用于 Docker 容器的安全模型模板，您可以直接使用它们。例如，我们提供了一个适用于 AppArmor 的模板，而 Red Hat 则为 Docker 提供了 SELinux 策略。这些模板提供了一层额外的安全网 (即使它与能力有很大重叠)。
 - 您可以使用自己喜欢的访问控制机制定义自己的策略。

正如您可以使用第三方工具来增强 Docker 容器 (包括特殊的网络拓扑或共享文件系统) 一样，也存在无需修改 Docker 本身即可加固 Docker 容器的工具。

自 Docker 1.10 起，Docker 守护进程直接支持用户命名空间 (User Namespaces)。此特性允许将容器中的 root 用户映射到容器外部的非 uid-0 用户，这有助于减轻容器逃逸的风险。此设施可用但默认未启用。

有关此特性的更多信息，请参阅命令行参考中的 [daemon 命令](/reference/cli/dockerd.md#daemon-user-namespace-options)。有关 Docker 中用户命名空间实现的更多信息，可以在 [这篇博文](https://integratedcode.us/2015/10/13/user-namespaces-have-arrived-in-docker/) 中找到。

## 结论

Docker 容器默认情况下是相当安全的；特别是如果您在容器内以非特权用户身份运行进程。

您可以通过启用 AppArmor、SELinux、GRSEC 或其他适当的加固系统来增加额外的安全层。

如果您想到使 Docker 变得更安全的方法，我们欢迎在 Docker 社区论坛上提出功能请求、拉取请求或评论。

## 相关信息

* [使用受信任的镜像](trust/_index.md)
* [适用于 Docker 的 Seccomp 安全配置文件](seccomp.md)
* [适用于 Docker 的 AppArmor 安全配置文件](apparmor.md)
* [On the Security of Containers (2014)](https://medium.com/@ewindisch/on-the-security-of-containers-2c60ffe25a9e)
* [Docker swarm 模式 overlay 网络安全模型](/manuals/engine/network/drivers/overlay.md)
