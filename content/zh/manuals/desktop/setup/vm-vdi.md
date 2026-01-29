---
description: 关于如何开启嵌套虚拟化的说明
keywords: 嵌套虚拟化, Docker Desktop, windows, 虚拟机, VDI 环境
title: 在虚拟机 (VM) 或 VDI 环境中运行 Windows 版 Docker Desktop
linkTitle: 虚拟机或 VDI 环境
aliases:
 - /desktop/nested-virtualization/
 - /desktop/vm-vdi/
weight: 30
---

Docker 建议在 Mac、Linux 或 Windows 上原生运行 Docker Desktop。然而，只要虚拟机进行了正确配置，Windows 版 Docker Desktop 也可以在虚拟桌面内运行。

要在虚拟桌面环境中运行 Docker Desktop，根据是否支持嵌套虚拟化，您有两种选择：

- 如果您的环境支持嵌套虚拟化，您可以使用默认的本地 Linux 虚拟机运行 Docker Desktop。
- 如果不支持嵌套虚拟化，Docker 建议使用 Docker Cloud。要加入 Beta 测试，请通过 `docker-cloud@docker.com` 联系 Docker。

## 使用 Docker Cloud 

{{< summary-bar feature_name="Docker Cloud" >}}

Docker Cloud 让您可以将容器工作负载卸载到高性能、全托管的云环境中，从而实现无缝的混合体验。它包含一个洞察（insights）控制面板，提供性能指标和环境管理，帮助优化您的开发工作流。

这种模式在不支持嵌套虚拟化的虚拟桌面环境中非常有用。在这些环境中，Docker Desktop 默认使用云模式，以确保您在不依赖本地虚拟化的情况下仍能构建和运行容器。

Docker Cloud 将 Docker Desktop 客户端与 Docker 引擎解耦，允许 Docker CLI 和 Docker Desktop 控制面板像操作本地资源一样与云端资源进行交互。当您运行容器时，Docker 会配置一个安全、隔离且临时的云环境，并通过 SSH 隧道连接到 Docker Desktop。尽管是在远程运行，但绑定挂载（bind mounts）和端口转发等功能仍能无缝工作，提供类似本地的体验。要使用 Docker Cloud：

1. 联系 Docker（邮箱：`docker-cloud@docker.com`）以为您的账户激活该功能。
2. 在您的 Windows 虚拟桌面上 [安装 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#在-Windows-上安装-Docker-Desktop) 4.42 或更高版本。
3. [启动 Docker Desktop](/manuals/desktop/setup/install/windows-install.md#启动-Docker-Desktop)。
4. 登录 Docker Desktop。

登录后，Docker Cloud 默认启用且无法禁用。启用时，Docker Desktop 控制面板的页眉显示为紫色，云模式切换开关是一个云图标 ({{< inline-image src="./images/cloud-mode.png" alt="云模式图标" >}})。

在这种模式下，Docker Desktop 会镜像您的云环境，提供对运行在 Docker Cloud 上的容器和资源的无缝查看。您可以通过运行一个简单的容器来验证 Docker Cloud 是否正在工作。在虚拟桌面的终端中运行以下命令：

```console
$ docker run hello-world
```

如果一切正常，您将在终端中看到 `Hello from Docker!`。

### 查看洞察并管理 Docker Cloud

如需查看洞察和进行管理，请使用 [Docker Cloud 控制面板](https://app.docker.com/cloud)。它可以让您直观地查看构建、运行情况以及云资源使用情况。关键功能包括：

- 概览 (Overview)：监控云使用情况、构建缓存以及构建最多的前几名仓库。
- 构建历史 (Build history)：通过过滤和排序选项查看过去的构建记录。
- 运行历史 (Run history)：跟踪容器运行情况，并按各种选项进行排序。
- 集成 (Integrations)：了解如何为您的 CI 流水线设置云构建器（builders）和运行器（runners）。
- 设置 (Settings)：管理云构建器、使用情况和账户设置。

访问 Docker Cloud 控制面板：https://app.docker.com/cloud。

### 局限性

使用 Docker Cloud 时存在以下局限性：

- 持久性：容器在云引擎中启动，只要您与容器交互并消耗其输出，该引擎就一直可用。关闭 Docker Desktop 或在空闲约 30 分钟后，引擎将关闭并变得无法访问，其中存储的任何数据（包括镜像、容器和卷）也将随之消失。任何新的工作负载都会重新配置一个新的引擎。
- 使用与计费：在 Beta 期间，使用 Docker Cloud 资源不收取费用。Docker 强制执行使用上限，并保留随时禁用 Docker Cloud 访问的权利。

## 使用嵌套虚拟化时的虚拟桌面支持

> [!NOTE]
>
> 对在虚拟桌面上运行 Docker Desktop 的支持仅提供给 Docker Business 客户，且仅限于 VMware ESXi 或 Azure 虚拟机。

Docker 的支持范围包括在虚拟机内安装和运行 Docker Desktop，前提是已正确启用嵌套虚拟化。目前仅在 VMware ESXi 和 Azure 虚拟机监控程序上成功测试过，不支持其他虚拟机。有关 Docker Desktop 支持的更多信息，请参阅 [获取支持](/manuals/desktop/troubleshoot-and-support/support.md)。

对于 Docker 无法控制的故障排除问题和间歇性故障，您应联系您的虚拟机监控程序供应商。每个供应商提供的支持级别不同。例如，微软支持在本地和 Azure 上运行嵌套的 Hyper-V（有一些版本限制）。VMware ESXi 的情况可能并非如此。

Docker 不支持在虚拟机或 VDI 环境中的同一台机器上运行多个 Docker Desktop 实例。 

> [!TIP]
>
> 如果您是在 Citrix VDI 中运行 Docker Desktop，请注意 Citrix 可以与多种底层虚拟机监控程序（如 VMware、Hyper-V、Citrix Hypervisor/XenServer）配合使用。Docker Desktop 需要嵌套虚拟化，而 Citrix Hypervisor/XenServer 并不支持。
>
> 请向您的 Citrix 管理员或 VDI 基础设施团队确认正在使用的是哪种虚拟机监控程序，以及是否启用了嵌套虚拟化。

## 开启嵌套虚拟化

在不使用 Docker Cloud 的虚拟机上安装 Docker Desktop 之前，您必须先开启嵌套虚拟化。

### 在 VMware ESXi 上开启嵌套虚拟化

在 vSphere 虚拟机内嵌套虚拟化其他虚拟机监控程序（如 Hyper-V）[不是一个受支持的场景](https://kb.vmware.com/s/article/2009916)。然而，在 VMware ESXi 虚拟机中运行 Hyper-V 虚拟机在技术上是可行的，并且根据版本的不同，ESXi 包含硬件辅助虚拟化作为一项受支持的功能。内部测试使用的是一台拥有 1 个 CPU（4 核）和 12GB 内存的虚拟机。

有关如何向客户机操作系统暴露硬件辅助虚拟化的步骤，[请参阅 VMware 的文档](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-2A98801C-68E8-47AF-99ED-00C63E4857F6.html)。

### 在 Azure 虚拟机上开启嵌套虚拟化

微软支持在 Azure 虚拟机内部运行 Hyper-V 进行嵌套虚拟化。

对于 Azure 虚拟机，请 [检查所选的虚拟机大小是否支持嵌套虚拟化](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)。微软提供了一个 [Azure 虚拟机大小列表](https://docs.microsoft.com/en-us/azure/virtual-machines/acu)，并重点标出了当前支持嵌套虚拟化的大小。内部测试使用的是 D4s_v5 机器。为了获得 Docker Desktop 的最佳性能，请使用此规格或更高规格。

## 在 Nutanix 驱动的 VDI 上获得 Docker Desktop 支持

只要底层的 Windows 环境支持 WSL 2 或 Windows 容器模式，Docker Desktop 就可以在 Nutanix 驱动的 VDI 环境中使用。由于 Nutanix 官方支持 WSL 2，只要 WSL 2 在 VDI 环境中正常运行，Docker Desktop 就应该能按预期工作。

如果使用 Windows 容器模式，请确认 Nutanix 环境支持 Hyper-V 或备选的 Windows 容器后端。

### 受支持的配置

Docker Desktop 遵循 [此前](#使用嵌套虚拟化时的虚拟桌面支持) 概述的 VDI 支持定义：

 - 持久性 VDI 环境（受支持）：您在不同会话中获得的是同一个虚拟桌面实例，保留了已安装的软件和配置。

 - 非持久性 VDI 环境（不受支持）：Docker Desktop 不支持操作系统在会话间重置的环境，因为这需要每次都重新安装或重新配置。 

### 支持范围与责任

对于 WSL 2 相关问题，请联系 Nutanix 支持。对于 Docker Desktop 特定问题，请联系 Docker 支持。

## 更多资源

- [Microsoft Dev Box 上的 Docker Desktop](/manuals/desktop/setup/install/enterprise-deployment/dev-box.md)
