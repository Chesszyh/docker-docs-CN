---
title: 最佳实践
description: 使用 Docker Desktop 与 WSL 2 的最佳实践
keywords: wsl, docker desktop, best practices
tags: [Best practices]
aliases:
- /desktop/wsl/best-practices/
---

- 始终使用最新版本的 WSL。至少必须使用 WSL 版本 2.1.5，否则 Docker Desktop 可能无法按预期工作。测试、开发和文档基于最新的内核版本。旧版本的 WSL 可能导致：
    - Docker Desktop 周期性挂起或在升级时挂起
    - 通过 SCCM 部署失败
    - `vmmem.exe` 消耗所有内存
    - 网络过滤策略被全局应用，而不是应用于特定对象
    - 容器的 GPU 故障

- 为了在绑定挂载文件时获得最佳的文件系统性能，建议您将源代码和其他绑定挂载到 Linux 容器的数据存储在 Linux 文件系统中。例如，使用 `docker run -v <host-path>:<container-path>` 时使用 Linux 文件系统，而不是 Windows 文件系统。您也可以参考 Microsoft 的[建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - 只有当原始文件存储在 Linux 文件系统中时，Linux 容器才会接收文件更改事件（"inotify events"）。例如，一些 Web 开发工作流程依赖 inotify 事件在文件更改时自动重新加载。
    - 当文件从 Linux 文件系统绑定挂载时，性能要高得多，而不是从 Windows 主机远程挂载。因此，避免使用 `docker run -v /mnt/c/users:/users`，其中 `/mnt/c` 是从 Windows 挂载的。
    - 相反，从 Linux shell 使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 由 Linux shell 展开为 `$HOME`。

- 如果您担心 `docker-desktop-data` 发行版的大小，请查看[内置于 Windows 中的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。
    - Docker Desktop 4.30 及更高版本的安装不再依赖 `docker-desktop-data` 发行版；相反，Docker Desktop 创建并管理自己的虚拟硬盘（VHDX）进行存储。（但请注意，如果 `docker-desktop-data` 发行版已由早期版本的软件创建，Docker Desktop 将继续使用它）。
    - 从 4.34 及更高版本开始，Docker Desktop 自动管理托管 VHDX 的大小，并将未使用的空间返回给操作系统。

- 如果您担心 CPU 或内存使用，可以配置分配给 [WSL 2 实用程序虚拟机](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig)的内存、CPU 和交换空间大小的限制。
