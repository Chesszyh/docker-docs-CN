---
description: 了解如何在 Docker Desktop 中使用 Docker Desktop Dashboard（Docker Desktop 仪表板），包括快速搜索、Docker 菜单等功能
keywords: Docker Desktop Dashboard, manage, containers, gui, dashboard, images, user manual,
  whale menu
title: 探索 Docker Desktop
weight: 30
aliases:
- /desktop/dashboard/
---

当您打开 Docker Desktop 时，会显示 Docker Desktop Dashboard（Docker Desktop 仪表板）。

![Docker Desktop Dashboard 容器视图](../images/dashboard.png)

它提供了一个集中的界面来管理您的[容器](container.md)、[镜像](images.md)、[卷](volumes.md)和[构建](builds.md)。

此外，Docker Desktop Dashboard 还允许您：

- 使用 [Ask Gordon](/manuals/ai/gordon/_index.md)，这是一个嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，帮助您充分利用 Docker 生态系统。
- 导航到 **Settings**（设置）菜单来配置您的 Docker Desktop 设置。选择 Dashboard 标题栏中的 **Settings** 图标。
- 访问 **Troubleshoot**（故障排除）菜单来调试和执行重启操作。选择 Dashboard 标题栏中的 **Troubleshoot** 图标。
- 在 **Notifications center**（通知中心）接收新版本发布、安装进度更新等通知。选择 Docker Desktop Dashboard 右下角的铃铛图标即可访问通知中心。
- 从 Dashboard 标题栏访问 **Learning center**（学习中心）。它通过快速的应用内引导帮助您入门，并提供其他学习 Docker 的资源。

  如需更详细的入门指南，请参阅[入门](/get-started/introduction/_index.md)。
- 访问 [Docker Hub](/manuals/docker-hub/_index.md) 来搜索、浏览、拉取、运行或查看镜像详情。
- 进入 [Docker Scout](../../scout/_index.md) 仪表板。
- 导航到 [Docker Extensions（Docker 扩展）](/manuals/extensions/_index.md)。

## Docker 终端

从 Docker Dashboard 底部，您可以直接在 Docker Desktop 中使用集成终端。

集成终端：

- 如果您导航到 Docker Desktop Dashboard 的其他部分然后返回，会话会被保留。
- 支持复制、粘贴、搜索和清除会话。

#### 打开集成终端

要打开集成终端，可以：

- 将鼠标悬停在正在运行的容器上，在 **Actions**（操作）列下选择 **Show container actions**（显示容器操作）菜单。从下拉菜单中选择 **Open in terminal**（在终端中打开）。
- 或者，选择位于右下角版本号旁边的 **Terminal**（终端）图标。

要使用外部终端，请导航到 **Settings** 中的 **General**（常规）选项卡，然后在 **Choose your terminal**（选择您的终端）下选择 **System default**（系统默认）选项。

## 快速搜索

使用位于 Docker Dashboard 标题栏中的 Quick Search（快速搜索）来搜索：

- 本地系统上的任何容器或 Compose 应用程序。您可以查看相关环境变量的概览，或执行快速操作，如启动、停止或删除。

- 公共 Docker Hub 镜像、本地镜像以及来自远程仓库的镜像（来自您在 Hub 中所属组织的私有仓库）。根据您选择的镜像类型，您可以按标签拉取镜像、查看文档、前往 Docker Hub 获取更多详情，或使用该镜像运行新容器。

- 扩展。在这里，您可以了解更多关于扩展的信息，并一键安装。或者，如果您已经安装了扩展，可以直接从搜索结果中打开它。

- 任何卷。在这里您可以查看关联的容器。

- 文档。直接从 Docker Desktop 查找 Docker 官方文档中的帮助。

## Docker 菜单

Docker Desktop 还包含一个托盘图标，称为 Docker 菜单 {{< inline-image src="../../assets/images/whale-x.svg" alt="whale menu" >}}，用于快速访问。

选择任务栏中的 {{< inline-image src="../../assets/images/whale-x.svg" alt="whale menu" >}} 图标可打开以下选项：

- **Dashboard**。跳转到 Docker Desktop Dashboard。
- **Sign in/Sign up**（登录/注册）
- **Settings**（设置）
- **Check for updates**（检查更新）
- **Troubleshoot**（故障排除）
- **Give feedback**（提供反馈）
- **Switch to Windows containers**（切换到 Windows 容器，如果您在 Windows 上）
- **About Docker Desktop**（关于 Docker Desktop）。包含您正在运行的版本信息，以及订阅服务协议等链接。
- **Docker Hub**
- **Documentation**（文档）
- **Extensions**（扩展）
- **Kubernetes**
- **Restart**（重启）
- **Quit Docker Desktop**（退出 Docker Desktop）
