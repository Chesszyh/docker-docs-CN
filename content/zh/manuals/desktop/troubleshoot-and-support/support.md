---
description: 了解 Docker Desktop 提供哪些支持
keywords: 支持, Support, Docker Desktop, Linux, Mac, Windows
title: 获取 Docker Desktop 支持
weight: 20
aliases:
 - /desktop/support/
 - /support/
---

> [!NOTE]
> 
> Docker Desktop 为拥有 [Pro、Team 或 Business 订阅](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade_desktop_support) 的开发人员提供支持。

### 如何获取 Docker Desktop 支持？

> [!TIP]
>
> 在寻求支持之前，请先按照故障排除文档中相应的 [诊断步骤](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#诊断) 进行操作。

如果您拥有付费的 Docker 订阅，可以 [联系支持团队](https://hub.docker.com/support/contact/)。

所有 Docker 用户都可以通过以下资源寻求支持，Docker 官方或社区将尽力提供帮助：
- [Docker Desktop for Windows GitHub 仓库](https://github.com/docker/for-win) 
- [Docker Desktop for Mac GitHub 仓库](https://github.com/docker/for-mac)
- [Docker Desktop for Linux GitHub 仓库](https://github.com/docker/desktop-linux)
- [Docker 社区论坛](https://forums.docker.com/)
- [Docker 社区 Slack](http://dockr.ly/comm-slack)


### 我可以获得哪些支持？

- 帐户管理相关问题
- 自动构建 (Automated builds)
- 基础产品的“如何操作”类问题
- 账单或订阅问题
- 配置问题
- Desktop 安装问题
   - 安装过程崩溃
   - 首次运行时无法启动 Docker Desktop
- Desktop 更新问题
- 命令行界面 (CLI) 和 Docker Hub 用户界面的登录问题
- 推送或拉取问题，包括速率限制 (Rate limiting)
- 使用问题
   - 软件关闭时崩溃
   - Docker Desktop 运行不符合预期

对于 Windows 用户，您还可以就以下方面请求支持：
- 在 BIOS 中开启虚拟化
- 开启 Windows 功能
- 在 [特定的 VM 或 VDI 环境](/manuals/desktop/setup/vm-vdi.md) 中运行（仅限 Docker Business 客户）

### 哪些内容不在支持范围内？

Docker Desktop 的支持不包括以下类型的问题：

- 在适用文档指定之外的硬件或软件上使用，或与其配合使用
- 在不受支持的操作系统上运行，包括操作系统的 Beta/预览版本
- 使用模拟技术运行不同架构的容器
- 对 Docker Engine、Docker CLI 或其他捆绑的 Linux 组件的直接支持
- 对 Kubernetes 的支持
- 标记为实验性 (Experimental) 的功能
- 系统/服务器管理活动
- 将 Desktop 作为生产环境运行的支持
- Desktop 的大规模部署/多机安装
- 日常产品维护（数据备份、清理磁盘空间和配置日志轮转）
- 非 Docker 提供的第三方应用程序
- 经改动或修改的 Docker 软件
- 由于硬件故障、滥用或不当使用导致的 Docker 软件缺陷
- 除最新版本外的任何 Docker 软件版本
- 报销非 Docker 提供的第三方服务的费用
- Docker 支持不包括培训、定制和集成
- 在单台机器上运行多个 Docker Desktop 实例

> [!NOTE]
>
> [在 VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md) 的支持仅提供给 Docker Business 客户。

### 支持哪些版本？

对于 Docker Business 客户，Docker 提供对比最新版本早最多六个月的版本支持，但任何修复都将应用在最新版本上。

对于 Pro 和 Team 客户，Docker 仅提供对最新版本 Docker Desktop 的支持。如果您运行的是旧版本，Docker 可能会要求您在调查您的支持请求之前先进行更新。

### 我可以在多少台机器上获得 Docker Desktop 支持？

作为 Pro 用户，您可以在单台机器上获得 Docker Desktop 支持。
作为 Team 用户，您可以按照订阅方案中的席位数量，在相应数量的机器上获得 Docker Desktop 支持。

### 支持哪些操作系统？

Docker Desktop 适用于 Mac、Linux 和 Windows。受支持的版本信息可以在以下页面找到：

- [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#系统要求)
- [Windows 系统要求](/manuals/desktop/setup/install/windows-install.md#系统要求)
- [Linux 系统要求](/manuals/desktop/setup/install/linux/_index.md#系统要求)

### 在获取支持时，Docker Desktop 如何处理个人诊断数据？

在上传诊断信息以帮助 Docker 调查问题时，上传的诊断包可能包含用户名和 IP 地址等个人数据。诊断包仅供直接参与诊断 Docker Desktop 问题的 Docker, Inc. 员工访问。

默认情况下，Docker, Inc. 会在 30 天后删除上传的诊断包。您也可以通过指定诊断 ID 或通过您的 GitHub ID（如果诊断 ID 在 GitHub issue 中被提及）请求删除诊断包。Docker, Inc. 仅将诊断包中的数据用于调查特定的用户问题，但可能会从中提取高级别的（非个人）指标，如问题发生率。

有关更多信息，请参阅 [Docker 数据处理协议 (Docker Data Processing Agreement)](https://www.docker.com/legal/data-processing-agreement)。
