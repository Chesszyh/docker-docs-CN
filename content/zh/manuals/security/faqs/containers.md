---
description: 查找容器安全相关常见问题的解答
keywords: Docker, Docker Hub, Docker Desktop security FAQs, platform, Docker Scout, admin, security
title: 容器安全常见问题
linkTitle: 容器
weight: 20
tags: [FAQ]
aliases:
- /faq/security/containers/
---

### Docker Desktop 中容器是如何与主机隔离的？

Docker Desktop 在定制/最小化的 Linux 虚拟机内运行所有容器（原生 Windows 容器除外）。这在容器和主机机器之间添加了强大的隔离层，即使容器以 root 身份运行也是如此。

但是请注意以下几点：

* 容器可以访问通过 Settings（设置）-> Resources（资源）-> File Sharing（文件共享）配置用于文件共享的主机文件（有关更多信息，请参阅下面的常见问题）。

* 默认情况下，容器在 Docker Desktop VM 内以 root 身份运行，但具有有限的能力。以提升权限运行的容器（例如 `--privileged`、`--pid=host`、`--cap-add` 等）在 Docker Desktop VM 内以提升权限的 root 身份运行，这使它们可以访问 Docker Desktop VM 内部，包括 Docker Engine。因此，用户必须小心哪些容器以这些权限运行，以避免恶意容器镜像造成的安全漏洞。

* 如果启用了 [Enhanced Container Isolation (ECI)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)（增强容器隔离）模式，则每个容器在 Docker Desktop VM 内的专用 Linux 用户命名空间中运行，这意味着容器在 Docker Desktop VM 中没有权限。即使使用 `--privileged` 标志或类似选项，容器进程也只在容器的逻辑边界内拥有特权，而在其他情况下则没有特权。此外，ECI 使用其他高级技术保护容器，确保它们无法轻易突破 Docker Desktop VM 和其中的 Docker Engine（有关更多信息，请参阅 ECI 部分）。不需要对容器或用户工作流程进行任何更改，因为额外的保护是在底层添加的。

### 容器对主机文件系统的哪些部分具有读写访问权限？

容器只有在通过 Settings（设置）-> Resources（资源）-> File Sharing（文件共享）共享这些文件，并且将这些文件绑定挂载到容器中时（例如 `docker run -v /path/to/host/file:/mnt ...`），才能访问主机文件。

### 以 root 身份运行的容器能否获取主机上管理员拥有的文件或目录的访问权限？

不能；主机文件共享（从主机文件系统的绑定挂载）使用用户空间构建的文件服务器（在 `com.docker.backend` 中以运行 Docker Desktop 的用户身份运行），因此容器无法获得主机上用户尚未拥有的任何访问权限。
