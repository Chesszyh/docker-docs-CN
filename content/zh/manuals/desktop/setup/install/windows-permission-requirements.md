---
description: 了解 Windows 版 Docker Desktop 的权限要求
keywords: Docker Desktop, Windows, security, 安全, install, 安装
title: 了解 Windows 版权限要求
linkTitle: Windows 权限要求
aliases:
- /desktop/windows/privileged-helper/
- /desktop/windows/permission-requirements/
- /desktop/install/windows-permission-requirements/
weight: 40
---

本页包含有关在 Windows 上运行和安装 Docker Desktop 的权限要求、特权辅助进程 `com.docker.service` 的功能以及采取此方法的原因等信息。

它还说明了在容器中以 `root` 运行与在宿主机上拥有 `Administrator` 权限之间的区别，以及 Windows Docker 引擎和 Windows 容器的权限。

Windows 版 Docker Desktop 在设计时充分考虑了安全性。仅在绝对必要时才需要管理权限。

## 权限要求

虽然 Windows 版 Docker Desktop 可以在没有 `Administrator` 权限的情况下运行，但在安装期间确实需要这些权限。安装时，您会收到一个 UAC 提示，允许安装特权辅助服务。之后，Docker Desktop 就可以在没有管理员权限的情况下运行了。

在没有特权辅助程序的情况下运行 Windows 版 Docker Desktop 不要求用户必须属于 `docker-users` 组。然而，某些需要特权操作的功能仍会有此要求。

如果您执行了安装操作，您会自动被添加到该组中，但其他用户必须手动添加。这允许管理员控制谁有权访问需要更高权限的功能，例如创建和管理 Hyper-V VM，或使用 Windows 容器。

当 Docker Desktop 启动时，会创建所有非特权命名管道 (Named pipes)，以便仅允许以下用户访问：
- 启动 Docker Desktop 的用户。
- 本地 `Administrators` 组的成员。
- `LOCALSYSTEM` 帐户。

## 特权辅助程序 (Privileged helper)

Docker Desktop 需要执行一组有限的特权操作，这些操作由特权辅助进程 `com.docker.service` 完成。根据最小特权原则，这种方法允许仅在绝对必要的操作中使用 `Administrator` 访问权限，同时仍能以非特权用户身份使用 Docker Desktop。

特权辅助程序 `com.docker.service` 是一个以 `SYSTEM` 权限在后台运行的 Windows 服务。它监听命名管道 `//./pipe/dockerBackendV2`。开发人员运行 Docker Desktop 应用程序，该程序连接到命名管道并向服务发送命令。此命名管道受到保护，只有属于 `docker-users` 组的用户才能访问它。

该服务执行以下功能：
- 确保在 Win32 hosts 文件中定义了 `kubernetes.docker.internal`。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
- 确保在 Win32 hosts 文件中定义了 `host.docker.internal` 和 `gateway.docker.internal`。它们指向宿主机本地 IP 地址，并允许应用程序无论是在宿主机本身还是在容器中，都能使用相同的名称解析宿主机 IP。
- 安全地缓存注册表访问管理（Registry Access Management）策略，该策略对开发人员是只读的。
- 创建名为 `"DockerDesktopVM"` 的 Hyper-V VM 并管理其生命周期——启动、停止和销毁。VM 名称硬编码在服务代码中，因此该服务不能用于创建或操作任何其他 VM。
- 移动 VHDX 文件或文件夹。
- 启动和停止 Windows Docker 引擎，并查询其运行状态。
- 删除所有 Windows 容器数据文件。
- 检查是否启用了 Hyper-V。
- 检查引导加载程序是否激活了 Hyper-V。
- 检查所需的 Windows 功能是否已安装并启用。
- 执行健康检查并检索服务自身的版本。

服务的启动模式取决于选择的容器引擎，以及（对于 WSL）是否需要维护 Win32 hosts 文件中的 `host.docker.internal` 和 `gateway.docker.internal`。这由设置页面中 `Use the WSL 2 based engine` 下的一个设置控制。设置此项后，WSL 引擎的行为与 Hyper-V 相同。因此：
- 对于 Windows 容器或 Hyper-V Linux 容器，服务在系统启动时启动并一直运行，即使 Docker Desktop 未运行也是如此。这是为了让您无需管理员权限即可启动 Docker Desktop。
- 对于 WSL 2 Linux 容器，该服务不是必需的，因此在系统启动时不会自动运行。当您切换到 Windows 容器或 Hyper-V Linux 容器，或者选择维护 Win32 hosts 文件中的 `host.docker.internal` 和 `gateway.docker.internal` 时，会出现 UAC 提示，要求您接受启动服务的特权操作。如果接受，服务将启动并被设置为在下次 Windows 启动时自动运行。

## Linux VM 中以 root 运行的容器

Linux Docker 守护进程和容器运行在一个由 Docker 管理的极简专用 Linux VM 中。它是不可变的，因此您无法扩展它或更改已安装的软件。这意味着虽然容器默认以 `root` 身份运行，但这并不允许更改 VM，也不会授予 Windows 宿主机的 `Administrator` 访问权限。Linux VM 充当了安全边界，并限制了可以访问的宿主机资源。文件共享使用了一个在用户空间构建的文件服务器，任何从宿主机绑定挂载到 Docker 容器中的目录仍保留其原始权限。容器无法访问除了显式共享的文件以外的任何宿主机文件。

## 增强型容器隔离 (Enhanced Container Isolation)

此外，Docker Desktop 支持 [增强型容器隔离模式](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md) (ECI)，该模式仅供 Business 客户使用，可在不影响开发人员工作流的情况下进一步提高容器的安全性。

ECI 自动在 Linux 用户命名空间中运行所有容器，从而使容器中的 root 映射到 Docker Desktop VM 内部的一个非特权用户。ECI 使用此技术和其他先进技术来进一步保障 Docker Desktop Linux VM 内部容器的安全，使它们进一步与 VM 内部运行的 Docker 守护进程和其他服务隔离。

## Windows 容器

> [!WARNING]
>
> 启用 Windows 容器具有重要的安全影响。

与运行在 VM 中的 Linux Docker 引擎和容器不同，Windows 容器是使用操作系统功能实现的，并直接在 Windows 宿主机上运行。如果您在安装期间启用 Windows 容器，则容器内部用于管理的 `ContainerAdministrator` 用户就是宿主机上的本地管理员。在安装期间启用 Windows 容器意味着 `docker-users` 组的成员能够提升为宿主机的管理员。对于不希望其开发人员运行 Windows 容器的组织，可以使用 `-–no-windows-containers` 安装程序标志来禁用该功能。

## 网络 (Networking)

对于网络连接，Docker Desktop 使用一个用户空间进程 (`vpnkit`)，该进程继承了启动它的用户的约束（如防火墙规则、VPN、HTTP 代理属性等）。
