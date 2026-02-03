---
description: 开启 Docker WSL 2 后端，并通过本详尽指南开始使用最佳实践、GPU 支持等功能。
keywords: wsl, wsl2, 安装 wsl2, wsl 安装, docker wsl2, wsl docker, wsl2 技术预览, wsl 安装 docker, 在 wsl 中安装 docker
title: Windows 上的 Docker Desktop WSL 2 后端
linkTitle: WSL
weight: 120
aliases:
- /docker-for-windows/wsl/
- /docker-for-windows/wsl-tech-preview/
- /desktop/windows/wsl/
- /desktop/wsl/
---

Windows Subsystem for Linux (WSL) 2 是由 Microsoft 构建的完整 Linux 内核，它允许 Linux 发行版在无需管理虚拟机的情况下运行。通过在 WSL 2 上运行 Docker Desktop，用户可以利用 Linux 工作区，并避免同时维护 Linux 和 Windows 的构建脚本。此外，WSL 2 在文件系统共享和启动时间方面也提供了改进。

Docker Desktop 利用 WSL 2 中的动态内存分配功能来优化资源消耗。这意味着 Docker Desktop 仅使用其所需的 CPU 和内存资源量，同时允许 CPU 和内存密集型任务（如构建容器）运行得更快。

此外，使用 WSL 2 后，在冷启动后启动 Docker 守护进程所需的时间也显著缩短。

## 前提条件

在开启 Docker Desktop WSL 2 功能之前，请确保您：

- 至少拥有 WSL 2.1.5 版本，但最好使用最新版本的 WSL，以 [避免 Docker Desktop 运行不符合预期](best-practices.md)。
- 满足 Windows 版 Docker Desktop 的 [系统要求](/manuals/desktop/setup/install/windows-install.md#系统要求)。
- 在 Windows 上安装了 WSL 2 功能。详细说明请参考 [Microsoft 官方文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。

> [!TIP]
>
> 为了在 WSL 上获得更好的体验，请考虑启用 WSL 的 [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings) 设置，该设置自 WSL 1.3.10（实验性）起可用。
>
> 此功能增强了 Windows 宿主机回收 WSL 虚拟机内未使用的内存的能力，确保为其他宿主机应用程序提供更好的内存可用性。此功能对 Docker Desktop 特别有益，因为它可以防止 WSL 虚拟机在 Docker 镜像构建过程中在 Linux 内核的页面缓存（Page cache）中保留大量内存（以 GB 为单位），而是在虚拟机不再需要时将其释放回宿主机。

## 开启 Docker Desktop WSL 2

> [!IMPORTANT]
>
> 为了避免在 Docker Desktop 上使用 WSL 2 时产生任何潜在冲突，在安装 Docker Desktop 之前，您必须卸载之前通过 Linux 发行版直接安装的所有版本的 Docker Engine 和 CLI。

1. 下载并安装最新版本的 [Windows 版 Docker Desktop](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)。
2. 按照常规安装说明安装 Docker Desktop。根据您使用的 Windows 版本，Docker Desktop 可能会在安装过程中提示您开启 WSL 2。阅读屏幕上显示的信息并开启 WSL 2 功能以继续。
3. 从 **Windows 开始** 菜单启动 Docker Desktop。
4. 导航到 **Settings（设置）**。
5. 在 **General（常规）** 选项卡中，勾选 **Use WSL 2 based engine（使用基于 WSL 2 的引擎）**。
    如果您是在支持 WSL 2 的系统上安装的 Docker Desktop，此选项通常默认开启。
6. 选择 **Apply（应用）**。

现在，`docker` 命令可以在 Windows 中通过新的 WSL 2 引擎工作了。

> [!TIP]
>
> 默认情况下，Docker Desktop 将 WSL 2 引擎的数据存储在 `C:\Users\[用户名]\AppData\Local\Docker\wsl`。
> 如果您想更改位置（例如更改到另一个驱动器），可以通过 Docker 控制面板的 `Settings -> Resources -> Advanced` 页面进行操作。
> 欲了解更多关于此设置及其他 Windows 设置的信息，请参阅 [更改设置](/manuals/desktop/settings-and-maintenance/settings.md)。

## 在 WSL 2 发行版中启用 Docker 支持

WSL 2 为 Windows 增加了对“Linux 发行版”的支持，其中每个发行版的行为都类似于 VM，但它们都运行在单个共享的 Linux 内核之上。

Docker Desktop 不需要安装任何特定的 Linux 发行版。`docker` CLI 和 UI 在 Windows 中无需任何额外的 Linux 发行版即可正常工作。然而，为了获得最佳的开发体验，我们建议至少安装一个额外的发行版并启用 Docker 支持：

1. 确保发行版运行在 WSL 2 模式下。WSL 可以运行在 v1 或 v2 模式下的发行版。
    要检查 WSL 模式，请运行：
     ```console
     $ wsl.exe -l -v
     ```
    要将 Linux 发行版升级到 v2，请运行：
    ```console
    $ wsl.exe --set-version (发行版名称) 2
    ```
    要将 v2 设置为未来安装的默认版本，请运行：
    ```console
    $ wsl.exe --set-default-version 2
    ```

2. 当 Docker Desktop 启动后，前往 **Settings** > **Resources** > **WSL Integration**。
    Docker-WSL 集成已在默认的 WSL 发行版（通常是 [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install)）上启用。要更改您的默认 WSL 发行版，请运行：
     ```console
    $ wsl --set-default <发行版名称>
    ```
   如果 **Resources** 下没有 **WSL Integration**，可能是因为 Docker 处于 Windows 容器模式。在任务栏中选择 Docker 菜单，然后选择 **Switch to Linux containers**。

3. 选择 **Apply（应用）**。

> [!NOTE]
>
> 在 Docker Desktop 4.30 及更早版本中，Docker Desktop 会安装两个专用内部 Linux 发行版：`docker-desktop` 和 `docker-desktop-data`。`docker-desktop` 用于运行 Docker 引擎 `dockerd`，而 `docker-desktop-data` 用于存储容器和镜像。这两者都不能用于通用开发。
>
> 对于 Docker Desktop 4.30 及更高版本的全新安装，不再创建 `docker-desktop-data`。相反，Docker Desktop 创建并管理其自己的虚拟硬盘用于存储。`docker-desktop` 发行版仍会被创建并用于运行 Docker 引擎。
>
> 请注意，如果是由旧版本 Docker Desktop 创建且尚未全新安装或恢复出厂设置，Docker Desktop 4.30 及更高版本将继续使用 `docker-desktop-data` 发行版。

## Docker Desktop 中的 WSL 2 安全性

Docker Desktop 的 WSL 2 集成运行在 WSL 现有的安全模型内，除了标准的 WSL 行为外，不会引入额外的安全风险。

Docker Desktop 运行在其专用的 WSL 发行版 `docker-desktop` 中，该发行版遵循与其他任何 WSL 发行版相同的隔离属性。Docker Desktop 与其他已安装的 WSL 发行版之间的唯一交互发生在设置中启用了 **WSL integration** 功能时。此功能允许从集成的发行版中轻松访问 Docker CLI。

WSL 的设计初衷是促进 Windows 和 Linux 环境之间的互操作性。其文件系统可以从 Windows 宿主机的 `\\wsl$\\` 路径访问，这意味着 Windows 进程可以读取并修改 WSL 内部的文件。这种行为并不是 Docker Desktop 特有的，而是 WSL 本身的核心特性。

对于担心 WSL 相关安全风险并希望进行更严格隔离和安全控制的组织，请在 Hyper-V 模式下运行 Docker Desktop 而不是 WSL 2 模式。或者，在启用 [增强型容器隔离 (Enhanced Container Isolation)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md) 的情况下运行您的容器工作负载。

## 额外资源

- [探索最佳实践](best-practices.md)
- [了解如何配合 Docker 和 WSL 2 进行开发](use-wsl.md)
- [了解 WSL 2 的 GPU 支持](/manuals/desktop/features/gpu.md)
- [WSL 上的自定义内核](custom-kernels.md)