---
description: 了解 Docker Desktop for Windows 的权限要求
keywords: Docker Desktop, Windows, security, install
title: 了解 Windows 的权限要求
linkTitle: Windows 权限要求
aliases:
- /desktop/windows/privileged-helper/
- /desktop/windows/permission-requirements/
- /desktop/install/windows-permission-requirements/
weight: 40
---

本页面包含有关在 Windows 上运行和安装 Docker Desktop 的权限要求、特权助手进程 `com.docker.service` 的功能以及这种方法背后的原因的信息。

它还阐明了以 `root` 身份运行容器与在主机上拥有 `Administrator`（管理员）访问权限之间的区别，以及 Windows Docker 引擎和 Windows 容器的权限。

Windows 上的 Docker Desktop 在设计时考虑了安全性。仅在绝对必要时才需要管理员权限。

## 权限要求

虽然 Windows 上的 Docker Desktop 可以在没有 `Administrator` 权限的情况下运行，但安装过程中需要这些权限。在安装时，您会收到一个 UAC 提示，允许安装特权助手服务。之后，Docker Desktop 可以在没有管理员权限的情况下运行。

在没有特权助手的情况下在 Windows 上运行 Docker Desktop 不要求用户是 `docker-users` 组的成员。但是，某些需要特权操作的功能会有此要求。

如果您执行了安装，您会自动被添加到此组，但其他用户必须手动添加。这允许管理员控制谁可以访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器。

当 Docker Desktop 启动时，所有非特权命名管道都会被创建，以便只有以下用户可以访问它们：
- 启动 Docker Desktop 的用户。
- 本地 `Administrators` 组的成员。
- `LOCALSYSTEM` 账户。

## 特权助手

Docker Desktop 需要执行一组有限的特权操作，这些操作由特权助手进程 `com.docker.service` 执行。这种方法遵循最小权限原则，只在绝对必要的操作中使用 `Administrator` 访问权限，同时仍然能够以非特权用户身份使用 Docker Desktop。

特权助手 `com.docker.service` 是一个以 `SYSTEM` 权限在后台运行的 Windows 服务。它监听命名管道 `//./pipe/dockerBackendV2`。开发者运行 Docker Desktop 应用程序，该应用程序连接到命名管道并向服务发送命令。此命名管道受保护，只有 `docker-users` 组的成员才能访问它。

该服务执行以下功能：
- 确保 `kubernetes.docker.internal` 在 Win32 hosts 文件中定义。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
- 确保 `host.docker.internal` 和 `gateway.docker.internal` 在 Win32 hosts 文件中定义。它们指向主机本地 IP 地址，允许应用程序从主机本身或容器使用相同的名称解析主机 IP。
- 安全缓存注册表访问管理策略，该策略对开发者是只读的。
- 创建 Hyper-V 虚拟机 `"DockerDesktopVM"` 并管理其生命周期——启动、停止和销毁它。虚拟机名称在服务代码中硬编码，因此该服务不能用于创建或操作任何其他虚拟机。
- 移动 VHDX 文件或文件夹。
- 启动和停止 Windows Docker 引擎并查询其是否正在运行。
- 删除所有 Windows 容器数据文件。
- 检查 Hyper-V 是否已启用。
- 检查引导加载程序是否激活 Hyper-V。
- 检查所需的 Windows 功能是否已安装并启用。
- 执行健康检查并检索服务本身的版本。

服务启动模式取决于选择的容器引擎，对于 WSL，取决于是否需要在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal`。这由设置页面中 `Use the WSL 2 based engine` 下的设置控制。当设置此选项时，WSL 引擎的行为与 Hyper-V 相同。因此：
- 使用 Windows 容器或 Hyper-V Linux 容器时，服务在系统启动时启动并一直运行，即使 Docker Desktop 未运行。这是必需的，以便您可以在没有管理员权限的情况下启动 Docker Desktop。
- 使用 WSL2 Linux 容器时，服务不是必需的，因此在系统启动时不会自动运行。当您切换到 Windows 容器或 Hyper-V Linux 容器，或选择在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal` 时，会出现 UAC 提示，要求您接受特权操作以启动服务。如果接受，服务将启动并设置为在下次 Windows 启动时自动启动。

## 在 Linux 虚拟机内以 root 身份运行容器

Linux Docker 守护进程和容器在 Docker 管理的最小化、专用 Linux 虚拟机中运行。它是不可变的，因此您无法扩展它或更改已安装的软件。这意味着虽然容器默认以 `root` 身份运行，但这不允许更改虚拟机，也不会授予对 Windows 主机的 `Administrator` 访问权限。Linux 虚拟机充当安全边界，限制可以从主机访问的资源。文件共享使用用户空间精心设计的文件服务器，从主机绑定挂载到 Docker 容器的任何目录仍保留其原始权限。容器无法访问除显式共享之外的任何主机文件。

## 增强容器隔离

此外，Docker Desktop 支持[增强容器隔离（Enhanced Container Isolation）模式](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)（ECI），仅适用于 Business 客户，它在不影响开发者工作流程的情况下进一步保护容器。

ECI 自动在 Linux 用户命名空间内运行所有容器，使得容器中的 root 被映射到 Docker Desktop 虚拟机内的非特权用户。ECI 使用这种和其他高级技术进一步保护 Docker Desktop Linux 虚拟机内的容器，使它们与 Docker 守护进程和虚拟机内运行的其他服务进一步隔离。

## Windows 容器

> [!WARNING]
>
> 启用 Windows 容器具有重要的安全影响。

与在虚拟机中运行的 Linux Docker 引擎和容器不同，Windows 容器使用操作系统功能实现，直接在 Windows 主机上运行。如果您在安装期间启用 Windows 容器，容器内用于管理的 `ContainerAdministrator` 用户是主机上的本地管理员。在安装期间启用 Windows 容器会使 `docker-users` 组的成员能够提升为主机上的管理员。对于不希望开发者运行 Windows 容器的组织，可以使用 `-–no-windows-containers` 安装程序标志来禁用其使用。

## 网络

对于网络连接，Docker Desktop 使用用户空间进程（`vpnkit`），它继承启动它的用户的约束，如防火墙规则、VPN、HTTP 代理属性等。
