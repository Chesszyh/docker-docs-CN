---
description: 开启 Docker WSL 2 后端，并在本详尽指南中使用最佳实践、GPU 支持等功能开始工作。
keywords: wsl, wsl2, installing wsl2, wsl installation, docker wsl2, wsl docker, wsl2
  tech preview, wsl install docker, install docker wsl, how to install docker in wsl
title: Windows 上的 Docker Desktop WSL 2 后端
linkTitle: WSL
weight: 120
aliases:
- /docker-for-windows/wsl/
- /docker-for-windows/wsl-tech-preview/
- /desktop/windows/wsl/
- /desktop/wsl/
---

Windows Subsystem for Linux (WSL) 2 是由 Microsoft 构建的完整 Linux 内核，它允许 Linux 发行版在不管理虚拟机的情况下运行。通过在 WSL 2 上运行 Docker Desktop，用户可以利用 Linux 工作区并避免同时维护 Linux 和 Windows 构建脚本。此外，WSL 2 在文件系统共享和启动时间方面提供了改进。

Docker Desktop 使用 WSL 2 中的动态内存分配功能来改善资源消耗。这意味着 Docker Desktop 仅使用其所需的 CPU 和内存资源，同时允许构建容器等 CPU 和内存密集型任务运行得更快。

此外，使用 WSL 2，冷启动后启动 Docker 守护进程所需的时间显著加快。

## 前提条件

在开启 Docker Desktop WSL 2 功能之前，请确保您已：

- 至少使用 WSL 版本 2.1.5，但理想情况下使用最新版本的 WSL 以[避免 Docker Desktop 无法按预期工作](best-practices.md)。
- 满足 Windows 版 Docker Desktop 的[系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)。
- 在 Windows 上安装了 WSL 2 功能。有关详细说明，请参阅 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。

> [!TIP]
>
> 为了在 WSL 上获得更好的体验，请考虑启用自 WSL 1.3.10 起可用的 WSL
> [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings)
> 设置（实验性）。
>
> 此功能增强了 Windows 主机在 WSL 虚拟机内回收未使用内存的能力，确保为其他主机应用程序提供更好的内存可用性。此功能对 Docker Desktop 特别有益，因为它可以防止 WSL 虚拟机在 Docker 容器镜像构建期间在 Linux 内核的页面缓存中保留大量内存（以 GB 为单位），而在虚拟机中不再需要时不将其释放回主机。

## 开启 Docker Desktop WSL 2

> [!IMPORTANT]
>
> 为避免在 Docker Desktop 上使用 WSL 2 时出现任何潜在冲突，您必须在安装 Docker Desktop 之前卸载任何直接通过 Linux 发行版安装的早期版本的 Docker Engine 和 CLI。

1. 下载并安装最新版本的 [Windows 版 Docker Desktop](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)。
2. 按照常规安装说明安装 Docker Desktop。根据您使用的 Windows 版本，Docker Desktop 可能会在安装过程中提示您开启 WSL 2。阅读屏幕上显示的信息并开启 WSL 2 功能以继续。
3. 从 **Windows 开始**菜单启动 Docker Desktop。
4. 导航到 **Settings**。
5. 从 **General** 选项卡，选择 **Use WSL 2 based engine**。

    如果您在支持 WSL 2 的系统上安装了 Docker Desktop，此选项默认已开启。
6. 选择 **Apply**。

现在 `docker` 命令可以使用新的 WSL 2 引擎从 Windows 运行。

> [!TIP]
>
> 默认情况下，Docker Desktop 将 WSL 2 引擎的数据存储在 `C:\Users\[USERNAME]\AppData\Local\Docker\wsl`。
> 如果您想更改位置，例如更改到另一个驱动器，可以通过 Docker Dashboard 的 `Settings -> Resources -> Advanced` 页面进行。
> 在[更改设置](/manuals/desktop/settings-and-maintenance/settings.md)中阅读有关此设置和其他 Windows 设置的更多信息

## 在 WSL 2 发行版中启用 Docker 支持

WSL 2 为 Windows 添加了对"Linux 发行版"的支持，其中每个发行版的行为类似于虚拟机，只是它们都运行在单个共享 Linux 内核之上。

Docker Desktop 不需要安装任何特定的 Linux 发行版。`docker` CLI 和 UI 在没有任何额外 Linux 发行版的情况下从 Windows 运行良好。但是，为了获得最佳开发者体验，我们建议至少安装一个额外的发行版并启用 Docker 支持：

1. 确保发行版在 WSL 2 模式下运行。WSL 可以在 v1 或 v2 模式下运行发行版。

    要检查 WSL 模式，请运行：

     ```console
     $ wsl.exe -l -v
     ```

    要将 Linux 发行版升级到 v2，请运行：

    ```console
    $ wsl.exe --set-version (distribution name) 2
    ```

    要将 v2 设置为未来安装的默认版本，请运行：

    ```console
    $ wsl.exe --set-default-version 2
    ```

2. 当 Docker Desktop 启动时，转到 **Settings** > **Resources** > **WSL Integration**。

    Docker-WSL 集成在默认 WSL 发行版（即 [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install)）上启用。要更改默认 WSL 发行版，请运行：
     ```console
    $ wsl --set-default <distribution name>
    ```
   如果 **Resources** 下没有 **WSL integrations**，Docker 可能处于 Windows 容器模式。在任务栏中，选择 Docker 菜单，然后选择 **Switch to Linux containers**。

3. 选择 **Apply**。

> [!NOTE]
>
> 在 Docker Desktop 4.30 及更早版本中，Docker Desktop 安装了两个特殊用途的内部 Linux 发行版 `docker-desktop` 和 `docker-desktop-data`。`docker-desktop` 用于运行 Docker 引擎 `dockerd`，而 `docker-desktop-data` 存储容器和镜像。两者都不能用于一般开发。
>
> 在 Docker Desktop 4.30 及更高版本的全新安装中，不再创建 `docker-desktop-data`。相反，Docker Desktop 创建并管理自己的虚拟硬盘进行存储。`docker-desktop` 发行版仍然被创建并用于运行 Docker 引擎。
>
> 请注意，如果 `docker-desktop-data` 发行版已由早期版本的 Docker Desktop 创建且尚未进行全新安装或恢复出厂设置，则 Docker Desktop 4.30 及更高版本将继续使用它。

## Docker Desktop 中的 WSL 2 安全性

Docker Desktop 的 WSL 2 集成在 WSL 现有的安全模型内运行，不会引入超出标准 WSL 行为的额外安全风险。

Docker Desktop 在其自己的专用 WSL 发行版 `docker-desktop` 中运行，该发行版遵循与任何其他 WSL 发行版相同的隔离属性。Docker Desktop 与其他已安装 WSL 发行版之间的唯一交互发生在设置中启用 Docker Desktop **WSL integration** 功能时。此功能允许从集成的发行版轻松访问 Docker CLI。

WSL 旨在促进 Windows 和 Linux 环境之间的互操作性。其文件系统可从 Windows 主机 `\\wsl$` 访问，这意味着 Windows 进程可以读取和修改 WSL 中的文件。此行为不是 Docker Desktop 特有的，而是 WSL 本身的核心方面。

对于担心与 WSL 相关的安全风险并希望获得更严格隔离和安全控制的组织，请在 Hyper-V 模式而不是 WSL 2 中运行 Docker Desktop。或者，在启用[增强容器隔离](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)的情况下运行容器工作负载。

## 其他资源

- [探索最佳实践](best-practices.md)
- [了解如何使用 Docker 和 WSL 2 进行开发](use-wsl.md)
- [了解 WSL 2 的 GPU 支持](/manuals/desktop/features/gpu.md)
- [WSL 上的自定义内核](custom-kernels.md)
