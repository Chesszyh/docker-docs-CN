---
description: 了解如何使用 Docker Desktop 控制面板，包括快速搜索、Docker 菜单等
keywords: Docker Desktop Dashboard, 管理, 容器, gui, 控制面板, 仪表板, images, 镜像, 用户手册, 鲸鱼菜单
title: 探索 Docker Desktop
weight: 30
aliases:
- /desktop/dashboard/
---

当您打开 Docker Desktop 时，会显示 Docker Desktop 控制面板（Dashboard）。

![Docker Desktop 控制面板容器视图](../images/dashboard.png)

它提供了一个集中式的界面，用于管理您的 [容器 (Containers)](container.md)、[镜像 (Images)](images.md)、[卷 (Volumes)](volumes.md) 和 [构建 (Builds)](builds.md)。

此外，Docker Desktop 控制面板还允许您：

- 使用 [Ask Gordon](/manuals/ai/gordon/_index.md)：一个嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，帮助您充分利用 Docker 生态系统。
- 导航到 **Settings（设置）** 菜单以配置您的 Docker Desktop 设置。点击控制面板头部的 **Settings** 图标。
- 访问 **Troubleshoot（故障排除）** 菜单以进行调试和执行重启操作。点击控制面板头部的 **Troubleshoot** 图标（小虫子图标）。
- 在 **通知中心 (Notifications center)** 中接收新版本发布、安装进度更新等通知。点击 Docker Desktop 控制面板右下角的铃铛图标即可访问通知中心。
- 从控制面板头部访问 **学习中心 (Learning center)**。它通过快速的应用内演练帮助您入门，并提供学习 Docker 的其他资源。有关更详细的入门指南，请参阅 [入门教程](/get-started/introduction/_index.md)。
- 访问 [Docker Hub](/manuals/docker-hub/_index.md) 以搜索、浏览、拉取、运行或查看镜像详情。
- 进入 [Docker Scout](../../scout/_index.md) 控制面板。
- 导航到 [Docker 扩展 (Docker Extensions)](/manuals/extensions/_index.md)。

## Docker 终端 (Docker terminal)

通过 Docker 控制面板的页脚，您可以直接在 Docker Desktop 中使用集成终端。

集成终端具有以下特点：

- **会话持久化**：如果您导航到控制面板的其他部分后再返回，会话仍会保留。
- **功能支持**：支持复制、粘贴、搜索以及清除会话。

#### 打开集成终端

要打开集成终端，可以采取以下任一方式：

- 将鼠标悬停在运行中的容器上，在 **Actions（操作）** 列中，点击 **Show container actions** 菜单。从下拉菜单中选择 **Open in terminal**。
- 或者，点击右下角版本号旁边的 **Terminal** 图标。

若要使用外部终端，请前往 **Settings** 中的 **General** 选项卡，并在 **Choose your terminal** 下选择 **System default** 选项。

## 快速搜索 (Quick search)

使用位于 Docker 控制面板头部的“快速搜索”功能，可以搜索：

- 您本地系统上的任何容器或 Compose 应用程序。您可以查看相关环境变量的概览，或执行快速操作，如启动、停止或删除。

- 公共 Docker Hub 镜像、本地镜像以及来自远程存储库的镜像（即您在 Hub 中所属组织的私有存储库）。根据所选镜像的类型，您可以按标签拉取镜像、查看文档、转到 Docker Hub 获取更多详情，或使用该镜像运行新容器。

- 扩展 (Extensions)。您可以从中了解有关扩展的更多信息并一键安装。或者，如果您已经安装了某个扩展，可以直接从搜索结果中将其打开。

- 任何卷 (Volumes)。您可以从中查看关联的容器。

- 文档 (Docs)。直接从 Docker Desktop 中查找来自 Docker 官方文档的帮助。

## Docker 菜单 (The Docker menu)

Docker Desktop 还在系统托盘中包含一个图标，即 Docker 菜单 {{< inline-image src="../../assets/images/whale-x.svg" alt="鲸鱼菜单" >}}，以便快速访问。

点击任务栏中的 {{< inline-image src="../../assets/images/whale-x.svg" alt="鲸鱼菜单" >}} 图标，可打开如下选项：

- **Dashboard（控制面板）**：转到 Docker Desktop 控制面板。
- **Sign in/Sign up（登录/注册）**
- **Settings（设置）**
- **Check for updates（检查更新）**
- **Troubleshoot（故障排除）**
- **Give feedback（提供反馈）**
- **Switch to Windows containers（切换到 Windows 容器）**（如果您使用的是 Windows）
- **About Docker Desktop（关于 Docker Desktop）**：包含您正在运行的版本信息，以及订阅服务协议的链接等。
- **Docker Hub**
- **Documentation（文档）**
- **Extensions（扩展）**
- **Kubernetes**
- **Restart（重启）**
- **Quit Docker Desktop（退出 Docker Desktop）**
