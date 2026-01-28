---
description: 如何启用嵌套虚拟化的说明
keywords: nested virtualization, Docker Desktop, windows, VM, VDI environment
title: 在虚拟机或 VDI 环境中运行 Docker Desktop for Windows
linkTitle: 虚拟机或 VDI 环境
aliases:
 - /desktop/nested-virtualization/
 - /desktop/vm-vdi/
weight: 30
---

Docker 建议在 Mac、Linux 或 Windows 上原生运行 Docker Desktop。但是，只要虚拟桌面配置正确，Docker Desktop for Windows 也可以在虚拟桌面内运行。

要在虚拟桌面环境中运行 Docker Desktop，您有两个选择，具体取决于是否支持嵌套虚拟化（nested virtualization）：

- 如果您的环境支持嵌套虚拟化，您可以使用 Docker Desktop 的默认本地 Linux 虚拟机运行。
- 如果不支持嵌套虚拟化，Docker 建议使用 Docker Cloud。要加入测试版，请通过 `docker-cloud@docker.com` 联系 Docker。

## 使用 Docker Cloud

{{< summary-bar feature_name="Docker Cloud" >}}

Docker Cloud 允许您将容器工作负载卸载到高性能、完全托管的云环境，实现无缝的混合体验。它包含一个洞察仪表板，提供性能指标和环境管理功能，帮助优化您的开发工作流程。

此模式在不支持嵌套虚拟化的虚拟桌面环境中非常有用。在这些环境中，Docker Desktop 默认使用云模式，以确保您仍然可以在不依赖本地虚拟化的情况下构建和运行容器。

Docker Cloud 将 Docker Desktop 客户端与 Docker Engine 解耦，允许 Docker CLI 和 Docker Desktop Dashboard 与云端资源交互，就像它们是本地资源一样。当您运行容器时，Docker 会配置一个安全、隔离且临时的云环境，通过 SSH 隧道连接到 Docker Desktop。尽管是远程运行，绑定挂载和端口转发等功能仍然可以无缝工作，提供类似本地的体验。要使用 Docker Cloud：

1. 通过 `docker-cloud@docker.com` 联系 Docker 以激活您账户的此功能。
2. 在您的 Windows 虚拟桌面上[安装 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#install-docker-desktop-on-windows) 4.42 或更高版本。
3. [启动 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#start-docker-desktop)。
4. 登录 Docker Desktop。

登录后，Docker Cloud 默认启用且无法禁用。启用后，Docker Desktop 的 Dashboard 标题栏显示为紫色，云模式切换按钮是一个云图标（{{< inline-image
src="./images/cloud-mode.png" alt="Cloud mode icon" >}}）。

在此模式下，Docker Desktop 镜像您的云环境，提供在 Docker Cloud 上运行的容器和资源的无缝视图。您可以通过运行一个简单的容器来验证 Docker Cloud 是否正常工作。在虚拟桌面的终端中，运行以下命令：

```console
$ docker run hello-world
```

如果一切正常工作，您将在终端中看到 `Hello from Docker!`。

### 查看洞察和管理 Docker Cloud

要获取洞察和进行管理，请使用 [Docker Cloud Dashboard](https://app.docker.com/cloud)。它提供构建、运行和云资源使用情况的可见性。主要功能包括：

- 概览：监控云使用量、构建缓存和构建量最多的仓库。
- 构建历史：查看过去的构建，支持筛选和排序选项。
- 运行历史：跟踪容器运行情况，并按各种选项排序。
- 集成：了解如何为您的 CI 流水线设置云构建器和运行器。
- 设置：管理云构建器、使用量和账户设置。

访问 Docker Cloud Dashboard：https://app.docker.com/cloud。

### 限制

使用 Docker Cloud 时存在以下限制：

- 持久性：容器在云引擎中启动，只要您与容器交互并消费容器输出，云引擎就会保持可用。关闭 Docker Desktop 后，或约 30 分钟不活动后，引擎将关闭并变得不可访问，其中存储的任何数据（包括镜像、容器和卷）也将不可访问。新的工作负载将配置新的引擎。
- 使用量和计费：在测试版期间，使用 Docker Cloud 资源不会产生费用。Docker 会强制执行使用上限，并保留随时禁用 Docker Cloud 访问的权利。

## 使用嵌套虚拟化时的虚拟桌面支持

> [!NOTE]
>
> 支持在虚拟桌面上运行 Docker Desktop 仅适用于 Docker Business 客户，且仅限于 VMware ESXi 或 Azure 虚拟机。

Docker 支持在虚拟机内安装和运行 Docker Desktop，前提是嵌套虚拟化已正确启用。唯一经过成功测试的虚拟化管理程序是 VMware ESXi 和 Azure，不支持其他虚拟机。有关 Docker Desktop 支持的更多信息，请参阅[获取支持](/manuals/desktop/troubleshoot-and-support/support.md)。

对于 Docker 控制范围之外的故障排除问题和间歇性故障，您应该联系您的虚拟化管理程序供应商。每个虚拟化管理程序供应商提供不同级别的支持。例如，Microsoft 支持在本地和 Azure 上运行嵌套 Hyper-V，但有一些版本限制。VMware ESXi 可能不是这种情况。

Docker 不支持在虚拟机或 VDI 环境中的同一台机器上运行多个 Docker Desktop 实例。

> [!TIP]
>
> 如果您在 Citrix VDI 内运行 Docker Desktop，请注意 Citrix 可以与多种底层虚拟化管理程序一起使用，例如 VMware、Hyper-V、Citrix Hypervisor/XenServer。Docker Desktop 需要嵌套虚拟化，而 Citrix Hypervisor/XenServer 不支持嵌套虚拟化。
>
> 请与您的 Citrix 管理员或 VDI 基础设施团队确认正在使用哪个虚拟化管理程序，以及是否启用了嵌套虚拟化。

## 开启嵌套虚拟化

在不使用 Docker Cloud 的虚拟机上安装 Docker Desktop 之前，您必须先开启嵌套虚拟化。

### 在 VMware ESXi 上开启嵌套虚拟化

在 vSphere 虚拟机内嵌套运行其他虚拟化管理程序（如 Hyper-V）[不是受支持的场景](https://kb.vmware.com/s/article/2009916)。但是，在 VMware ESXi 虚拟机中运行 Hyper-V 虚拟机在技术上是可行的，根据版本不同，ESXi 将硬件辅助虚拟化作为受支持的功能。内部测试使用了配置为 1 个 CPU、4 个核心和 12GB 内存的虚拟机。

有关如何向客户操作系统公开硬件辅助虚拟化的步骤，[请参阅 VMware 的文档](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-2A98801C-68E8-47AF-99ED-00C63E4857F6.html)。

### 在 Azure 虚拟机上开启嵌套虚拟化

Microsoft 支持在 Azure 虚拟机内运行 Hyper-V 的嵌套虚拟化。

对于 Azure 虚拟机，[请检查所选的虚拟机大小是否支持嵌套虚拟化](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)。Microsoft 提供了一份[关于 Azure 虚拟机大小的有用列表](https://docs.microsoft.com/en-us/azure/virtual-machines/acu)，并标注了当前支持嵌套虚拟化的大小。内部测试使用了 D4s_v5 机器。为了获得 Docker Desktop 的最佳性能，请使用此规格或更高配置。

## Nutanix 驱动的 VDI 上的 Docker Desktop 支持

只要底层 Windows 环境支持 WSL 2 或 Windows 容器模式，Docker Desktop 就可以在 Nutanix 驱动的 VDI 环境中使用。由于 Nutanix 官方支持 WSL 2，只要 WSL 2 在 VDI 环境中正常运行，Docker Desktop 应该可以按预期工作。

如果使用 Windows 容器模式，请确认 Nutanix 环境支持 Hyper-V 或其他 Windows 容器后端。

### 支持的配置

Docker Desktop 遵循[前文](#virtual-desktop-support-when-using-nested-virtualization)概述的 VDI 支持定义：

 - 持久性 VDI 环境（支持）：您在各个会话中获得相同的虚拟桌面实例，保留已安装的软件和配置。

 - 非持久性 VDI 环境（不支持）：Docker Desktop 不支持操作系统在会话之间重置的环境，这种环境每次都需要重新安装或重新配置。

### 支持范围和责任

对于 WSL 2 相关问题，请联系 Nutanix 支持。对于 Docker Desktop 特定问题，请联系 Docker 支持。

## 其他资源

- [在 Microsoft Dev Box 上使用 Docker Desktop](/manuals/desktop/setup/install/enterprise-deployment/dev-box.md)
