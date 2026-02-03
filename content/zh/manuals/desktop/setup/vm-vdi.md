---
description: 关于如何启用嵌套虚拟化的说明
keywords: 嵌套虚拟化, nested virtualization, Docker Desktop, windows, VM, VDI 环境
title: 在 VM 或 VDI 环境中运行 Docker Desktop for Windows
linkTitle: VM 或 VDI 环境
aliases:
 - /desktop/nested-virtualization/
 - /desktop/vm-vdi/
weight: 30
---

Docker 建议在 Mac、Linux 或 Windows 上原生运行 Docker Desktop。但是，只要虚拟桌面配置正确，Docker Desktop for Windows 也可以在虚拟桌面中运行。

在虚拟桌面环境中运行 Docker Desktop，您有两个选择，具体取决于是否支持嵌套虚拟化：

- 如果您的环境支持嵌套虚拟化，您可以运行带有默认本地 Linux VM 的 Docker Desktop。
- 如果不支持嵌套虚拟化，Docker 建议使用 Docker Cloud。要加入 Beta 测试，请通过 `docker-cloud@docker.com` 联系 Docker。

## 使用 Docker Cloud

{{< summary-bar feature_name="Docker Cloud" >}}

Docker Cloud 让您可以将容器工作负载卸载到高性能、全托管的云环境中，从而实现无缝的混合体验。它包含一个洞察控制面板（Insights dashboard），提供性能指标和环境管理，帮助优化您的开发工作流。

此模式在不支持嵌套虚拟化的虚拟桌面环境中非常有用。在这些环境中，Docker Desktop 默认使用云模式（Cloud mode），以确保您仍能构建和运行容器，而无需依赖本地虚拟化。

Docker Cloud 将 Docker Desktop 客户端与 Docker Engine 解耦，允许 Docker CLI 和 Docker Desktop 控制面板像与本地资源交互一样与云端资源进行交互。当您运行容器时，Docker 会通过 SSH 隧道连接到 Docker Desktop，预配一个安全、隔离且临时的云环境。尽管是在远程运行，但绑定挂载（Bind mounts）和端口转发等功能仍能无缝工作，提供类似于本地的体验。要使用 Docker Cloud：

1. 联系 Docker（邮箱：`docker-cloud@docker.com`）为您的帐户激活此功能。
2. 在您的 Windows 虚拟桌面中[安装 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#install-docker-desktop-on-windows) 4.42 或更高版本。
3. [启动 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#start-docker-desktop)。
4. 登录 Docker Desktop。

登录后，Docker Cloud 默认启用且无法禁用。启用后，Docker Desktop 的控制面板标题栏会显示为紫色，且云模式切换开关是一个云图标（{{< inline-image src="./images/cloud-mode.png" alt="云模式图标" >}}）。

在此模式下，Docker Desktop 会映射您的云环境，提供在 Docker Cloud 上运行的容器和资源的无缝视图。您可以通过运行一个简单的容器来验证 Docker Cloud 是否工作正常。在虚拟桌面的终端中运行以下命令：

```console
$ docker run hello-world
```

如果一切正常，您将在终端中看到 `Hello from Docker!`。

### 查看洞察并管理 Docker Cloud

如需查看洞察和进行管理，请使用 [Docker Cloud 控制面板](https://app.docker.com/cloud)。它可以让您直观地了解构建、运行情况以及云资源使用情况。关键特性包括：

- 概览 (Overview)：监控云使用情况、构建缓存和构建次数最多的存储库。
- 构建历史 (Build history)：查看过去的构建，支持过滤和排序选项。
- 运行历史 (Run history)：跟踪容器运行情况，并支持多种排序选项。
- 集成 (Integrations)：了解如何为您的 CI 流水线设置云构建器（Builders）和运行器（Runners）。
- 设置 (Settings)：管理云构建器、使用情况和帐户设置。

访问 Docker Cloud 控制面板：https://app.docker.com/cloud。

### 限制

使用 Docker Cloud 时存在以下限制：

- 持久性 (Persistence)：容器在云引擎中启动，只要您与容器交互并消费其输出，该引擎就会一直可用。关闭 Docker Desktop 或在不活动约 30 分钟后，引擎将关闭并变得不可访问，其中存储的所有数据（包括镜像、容器和卷）也将一并消失。任何新的工作负载都将预配一个新的引擎。
- 使用与计费 (Usage and billing)：在 Beta 测试期间，使用 Docker Cloud 资源不会产生费用。Docker 会强制执行使用上限，并保留随时禁用 Docker Cloud 访问权限的权利。

## 使用嵌套虚拟化时的虚拟桌面支持

> [!NOTE]
>
> 在 VMware ESXi 或 Azure VM 上运行 Docker Desktop 的虚拟桌面支持仅提供给 Docker Business 客户。

Docker 的支持范围包括在 VM 中安装和运行 Docker Desktop，前提是已正确启用嵌套虚拟化。目前仅在 VMware ESXi 和 Azure 上成功测试过，不支持其他虚拟机（VM）。有关 Docker Desktop 支持的更多信息，请参阅[获取支持](/manuals/desktop/troubleshoot-and-support/support.md)。

对于超出 Docker 控制范围的故障排查问题和间歇性错误，您应联系您的虚拟机管理程序（Hypervisor）供应商。每个供应商提供的支持级别各不相同。例如，Microsoft 支持在本地和 Azure 上运行嵌套 Hyper-V，但有一些版本限制。对于 VMware ESXi，情况可能有所不同。

Docker 不支持在 VM 或 VDI 环境中的同一台机器上运行多个 Docker Desktop 实例。

> [!TIP]
>
> 如果您在 Citrix VDI 中运行 Docker Desktop，请注意 Citrix 可以与多种底层虚拟机管理程序配合使用，例如 VMware、Hyper-V、Citrix Hypervisor/XenServer。Docker Desktop 需要嵌套虚拟化，而 Citrix Hypervisor/XenServer 不支持此功能。
>
> 请咨询您的 Citrix 管理员或 VDI 基础设施团队，以确认正在使用哪种虚拟机管理程序，以及是否启用了嵌套虚拟化。

## 开启嵌套虚拟化

在不使用 Docker Cloud 的虚拟机上安装 Docker Desktop 之前，必须先开启嵌套虚拟化。

### 在 VMware ESXi 上开启嵌套虚拟化

在 vSphere VM 内部运行像 Hyper-V 这样的其他虚拟机管理程序的嵌套虚拟化 [不是一个受支持的场景](https://kb.vmware.com/s/article/2009916)。但是，在 VMware ESXi VM 中运行 Hyper-V VM 在技术上是可行的，并且根据版本的不同，ESXi 包含硬件辅助虚拟化这一受支持的功能。内部测试使用的是一台拥有 1 个 CPU（4 核）和 12GB 内存的 VM。

有关如何向客户机操作系统开放硬件辅助虚拟化的步骤，[请参阅 VMware 文档](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-2A98801C-68E8-47AF-99ED-00C63E4857F6.html)。

### 在 Azure 虚拟机上开启嵌套虚拟化

Microsoft 支持在 Azure VM 内部运行 Hyper-V。

对于 Azure 虚拟机，[请检查所选的 VM 大小是否支持嵌套虚拟化](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)。Microsoft 提供了一份[关于 Azure VM 大小的有用列表](https://docs.microsoft.com/en-us/azure/virtual-machines/acu)，并强调了当前支持嵌套虚拟化的尺寸。内部测试使用的是 D4s_v5 机器。请使用此规格或更高规格以获得 Docker Desktop 的最佳性能。

## Nutanix 驱动的 VDI 上的 Docker Desktop 支持

Docker Desktop 可以在 Nutanix 驱动的 VDI 环境中使用，前提是底层 Windows 环境支持 WSL 2 或 Windows 容器模式。由于 Nutanix 官方支持 WSL 2，只要 WSL 2 在 VDI 环境中正常运行，Docker Desktop 应该就能按预期工作。

如果使用 Windows 容器模式，请确认 Nutanix 环境支持 Hyper-V 或其他 Windows 容器后端。

### 受支持的配置

Docker Desktop 遵循[前面](#使用嵌套虚拟化时的虚拟桌面支持)概述的 VDI 支持定义：

 - 持久性 VDI 环境 (受支持)：您在不同会话中获得的是同一个虚拟桌面实例，从而保留了已安装的软件和配置。

 - 非持久性 VDI 环境 (不受支持)：Docker Desktop 不支持 OS 在会话之间重置的环境，因为这需要每次都重新安装或重新配置。

### 支持范围和责任

对于与 WSL 2 相关的问题，请联系 Nutanix 支持。对于 Docker Desktop 特定问题，请联系 Docker 支持。

## 额外资源

- [Microsoft Dev Box 上的 Docker Desktop](/manuals/desktop/setup/install/enterprise-deployment/dev-box.md)