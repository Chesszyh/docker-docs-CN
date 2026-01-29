---
title: 最佳实践
description: 结合使用 Docker Desktop 和 WSL 2 的最佳实践
keywords: wsl, docker desktop, best practices
tags: [最佳实践]
aliases:
- /desktop/wsl/best-practices/
---

- 始终使用最新版本的 WSL。您必须至少使用 2.1.5 版本的 WSL，否则 Docker Desktop 可能无法按预期工作。测试、开发和文档均基于最新的内核版本。旧版本的 WSL 可能会导致：
    - Docker Desktop 定期挂起或在升级时挂起
    - 通过 SCCM 部署失败
    - `vmmem.exe` 进程耗尽所有内存 
    - 网络过滤策略被全局应用，而非针对特定对象
    - 容器中的 GPU 故障

- 为了在绑定挂载文件时获得最佳的文件系统性能，建议您将源代码和其他需要绑定挂载到 Linux 容器中的数据存储在 Linux 文件系统中。例如，在 Linux 文件系统中运行 `docker run -v <宿主机路径>:<容器路径>`，而不是在 Windows 文件系统中运行。您还可以参考微软的 [建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - 只有当原始文件存储在 Linux 文件系统中时，Linux 容器才能接收到文件更改事件（即 "inotify 事件"）。例如，某些 Web 开发工作流依赖 inotify 事件在文件更改时自动重载。
    - 当文件从 Linux 文件系统进行绑定挂载时，其性能要比从 Windows 宿主机远程挂载高得多。因此，请避免使用 `docker run -v /mnt/c/users:/users` 这样的命令，因为 `/mnt/c` 是从 Windows 挂载的。
    - 相反，请在 Linux shell 中使用类似 `docker run -v ~/my-project:/sources <镜像名称>` 的命令，其中 `~` 会被 Linux shell 展开为 `$HOME`。

- 如果您担心 `docker-desktop-data` 发行版的大小，请查看 [Windows 内置的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。 
    - Docker Desktop 4.30 及更高版本的安装不再依赖 `docker-desktop-data` 发行版；取而代之的是，Docker Desktop 创建并管理自己的虚拟硬盘 (VHDX) 进行存储。（但请注意，如果该发行版已由软件的早期版本创建，Docker Desktop 将继续使用它）。
    - 从 4.34 及更高版本开始，Docker Desktop 会自动管理受管 VHDX 的大小，并将未使用的空间返回给操作系统。

- 如果您担心 CPU 或内存使用情况，可以对分配给 [WSL 2 实用虚拟机](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 的内存、CPU 和交换文件（swap）大小配置限制。
