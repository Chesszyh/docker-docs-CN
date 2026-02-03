---
title: 最佳实践
description: 在 WSL 2 中使用 Docker Desktop 的最佳实践
keywords: wsl, docker desktop, best practices, 最佳实践
tags: [Best practices]
aliases:
- /desktop/wsl/best-practices/
---

- **始终使用最新版本的 WSL**：您必须至少使用 WSL 2.1.5 版本，否则 Docker Desktop 可能无法按预期工作。测试、开发和文档均基于最新的内核版本。较旧版本的 WSL 可能导致：
    - Docker Desktop 定期挂起或在升级时挂起
    - 通过 SCCM 进行的部署失败
    - `vmmem.exe` 消耗所有内存
    - 网络过滤策略被全局应用，而非针对特定对象
    - 容器中的 GPU 运行故障

- **优化文件系统性能**：为了在绑定挂载（bind-mount）文件时获得最佳性能，建议您将源码和其他数据存储在 Linux 发行版的文件系统中，然后再挂载到 Linux 容器中。例如，在 Linux 文件系统中执行 `docker run -v <host-path>:<container-path>`，而不是在 Windows 文件系统中。您也可以参考 Microsoft 的[建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - **文件更改事件**：只有当原始文件存储在 Linux 文件系统中时，Linux 容器才能接收到文件更改事件（即 "inotify 事件"）。例如，某些 Web 开发工作流依赖 inotify 事件在文件更改时自动重新加载。
    - **读写性能**：当文件从 Linux 文件系统绑定挂载时，性能远高于从 Windows 宿主机远程挂载。因此，应避免使用 `docker run -v /mnt/c/users:/users`（其中 `/mnt/c` 是从 Windows 挂载的）。
    - **推荐做法**：在 Linux shell 中使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 会被 Linux shell 扩展为 `$HOME`。

- **存储管理**：如果您担心 `docker-desktop-data` 发行版的大小，请查看 [Windows 内置的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。
    - **版本差异**：Docker Desktop 4.30 及更高版本的全新安装不再依赖 `docker-desktop-data` 发行版；相反，Docker Desktop 创建并管理其自己的虚拟硬盘 (VHDX) 用于存储。（注意：如果是由较早版本的软件创建的，Docker Desktop 会继续使用 `docker-desktop-data`）。
    - **自动回收**：从 4.34 版本开始，Docker Desktop 会自动管理该 VHDX 的大小，并将未使用的空间归还给操作系统。

- **资源限制**：如果您担心 CPU 或内存占用，可以为 [WSL 2 实用程序 VM（Utility VM）](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 配置分配的内存、CPU 和交换空间限制。