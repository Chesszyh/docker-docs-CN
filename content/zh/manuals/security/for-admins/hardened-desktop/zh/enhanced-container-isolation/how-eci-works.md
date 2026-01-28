---
description: 增强容器隔离的工作原理
title: 工作原理
keywords: set up, enhanced container isolation, rootless, security
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/how-eci-works/
weight: 10
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

Docker 通过使用 [Sysbox 容器运行时](https://github.com/nestybox/sysbox)来实现增强容器隔离。Sysbox 是标准 OCI runc 运行时的一个分支，经过修改以增强标准容器隔离和工作负载。有关更多详情，请参阅[底层实现](#底层实现)。

当[启用增强容器隔离](index.md#如何启用增强容器隔离)后，用户通过 `docker run` 或 `docker create` 创建的容器会自动使用 Sysbox 而不是标准 OCI runc 运行时启动。用户无需做任何其他事情，可以继续像往常一样使用容器。有关例外情况，请参阅[常见问题](faq.md)。

即使是使用不安全的 `--privileged` 标志的容器，现在也可以通过增强容器隔离安全地运行，使它们不能再用于突破 Docker Desktop 虚拟机（VM）或其他容器。

> [!NOTE]
>
> 在 Docker Desktop 中启用增强容器隔离后，Docker CLI 的 `--runtime` 标志会被忽略。Docker 的默认运行时继续是 `runc`，但所有用户容器都隐式使用 Sysbox 启动。

增强容器隔离与 [Docker Engine 的 userns-remap 模式或 Rootless Docker](#增强容器隔离与用户命名空间重映射) 不同。

### 底层实现

Sysbox 通过以下技术增强容器隔离：

* 在所有容器上启用 Linux 用户命名空间（容器中的 root 用户映射到 Linux 虚拟机中的非特权用户）。
* 限制容器挂载敏感的虚拟机目录。
* 审查容器和 Linux 内核之间的敏感系统调用。
* 在容器的用户命名空间和 Linux 虚拟机之间映射文件系统用户/组 ID。
* 在容器内模拟 `/proc` 和 `/sys` 文件系统的部分内容。

其中一些是由 Docker Desktop 现已整合的 Linux 内核的最新进展实现的。Sysbox 应用这些技术时对容器的功能或性能影响最小。

这些技术补充了 Docker 的传统容器安全机制，如使用其他 Linux 命名空间、cgroups、受限的 Linux Capabilities、Seccomp 和 AppArmor。它们在容器和 Docker Desktop 虚拟机内的 Linux 内核之间添加了一层强大的隔离。

有关更多信息，请参阅[主要功能和优势](features-benefits.md)。

### 增强容器隔离与用户命名空间重映射

Docker Engine 包含一个称为 [userns-remap 模式](/engine/security/userns-remap/)的功能，它在所有容器中启用用户命名空间。但是它存在一些[限制](/engine/security/userns-remap/)，并且在 Docker Desktop 中不受支持。

userns-remap 模式与增强容器隔离类似，因为两者都通过利用 Linux 用户命名空间来改善容器隔离。

但是，增强容器隔离更加先进，因为它自动为每个容器分配独占的用户命名空间映射，并添加了几个其他[容器隔离功能](#底层实现)，旨在保护对安全有严格要求的组织中的 Docker Desktop。

### 增强容器隔离与 Rootless Docker

[Rootless Docker](/engine/security/rootless/) 允许 Docker Engine 以及扩展的容器在 Linux 主机上无需 root 权限原生运行。这允许非 root 用户在 Linux 上原生安装和运行 Docker。

Rootless Docker 在 Docker Desktop 中不受支持。虽然它在 Linux 上原生运行 Docker 时是一个有价值的功能，但它在 Docker Desktop 中的价值降低了，因为 Docker Desktop 在 Linux 虚拟机中运行 Docker Engine。也就是说，Docker Desktop 已经允许非 root 主机用户运行 Docker，并使用虚拟机将 Docker Engine 与主机隔离。

与 Rootless Docker 不同，增强容器隔离不在 Linux 用户命名空间内运行 Docker Engine。相反，它在用户命名空间内运行由该引擎生成的容器。这样做的优势是绑过 [Rootless Docker 的限制](/engine/security/rootless/#known-limitations)，并在容器和 Docker Engine 之间创建更强的边界。

增强容器隔离旨在确保使用 Docker Desktop 启动的容器不能轻易突破 Docker Desktop Linux 虚拟机，因此不能修改其中的安全设置。
