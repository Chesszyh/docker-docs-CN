---
description: 查找容器安全相关的常见问题解答
keywords: Docker, Docker Hub, Docker Desktop 安全 FAQ, 平台, Docker Scout, 管理员, 安全
title: 容器安全常见问题 (FAQ)
linkTitle: 容器
weight: 20
tags: [FAQ]
aliases:
- /faq/security/containers/
---

### 在 Docker Desktop 中，容器是如何与主机隔离的？

Docker Desktop 在一个定制化的最小 Linux 虚拟机内运行所有容器 (原生 Windows 容器除外)。即使容器以 root 权限运行，这也在容器与主机机器之间增加了一层强有力的隔离。

但请注意以下几点：

* 容器可以通过 **Settings** -> **Resources** -> **File Sharing** 访问配置为文件共享的主机文件 (有关更多信息，请参阅下方的下一个 FAQ 问题)。

* 默认情况下，容器在 Docker Desktop 虚拟机内部以具有有限能力 (limited capabilities) 的 root 用户身份运行。以提升权限运行的容器 (例如 `--privileged`、`--pid=host`、`--cap-add` 等) 在 Docker Desktop 虚拟机内部以具有提升权限的 root 用户身份运行，这使它们能够访问 Docker Desktop 虚拟机的内部，包括 Docker Engine。因此，用户必须谨慎对待以这些权限运行哪些容器，以避免恶意容器镜像造成安全破坏。

* 如果启用了 [增强型容器隔离 (Enhanced Container Isolation, ECI)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md) 模式，则每个容器都在 Docker Desktop 虚拟机内部的一个专用 Linux 用户命名空间 (User Namespace) 中运行，这意味着该容器在 Docker Desktop 虚拟机内部没有任何权限。即使使用 `--privileged` 标志或类似标志，容器进程也仅在容器的逻辑边界内拥有特权，但在其他情况下没有特权。此外，ECI 还使用了其他先进技术来确保它们无法轻易突破 Docker Desktop 虚拟机及其内部的 Docker Engine (更多信息请参阅 ECI 章节)。由于额外的保护是在后台添加的，因此无需对容器或用户工作流进行任何更改。

### 容器对主机文件系统的哪些部分具有读写权限？

容器只有在通过 **Settings** -> **Resources** -> **File Sharing** 共享主机文件，且这些文件被绑定挂载 (bind-mount) 到容器中 (例如 `docker run -v /path/to/host/file:/mnt ...`) 时，才能访问主机文件。

### 以 root 身份运行的容器能否获得对主机上管理员拥有的文件或目录的访问权限？

不能。主机文件共享 (从主机文件系统进行的绑定挂载) 使用了一个专门构建的用户空间文件服务器 (在 `com.docker.backend` 中以运行 Docker Desktop 的用户身份运行)，因此容器无法获得主机用户尚未拥有的任何访问权限。
