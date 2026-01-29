---
description: 了解如何安装 Docker Compose。Compose 原生内置于 Docker Desktop 中，也可以作为 Docker Engine 插件或独立工具使用。
keywords: 安装 docker compose, docker compose 插件, linux 安装 compose, 安装 docker desktop, windows docker compose, 独立版 docker compose, 找不到 docker compose
title: 安装 Docker Compose 概览
linkTitle: 安装
weight: 20
toc_max: 3
aliases:
- /compose/compose-desktop/
- /compose/install/other/
- /compose/install/compose-desktop/
---

本页总结了根据您的平台和需求安装 Docker Compose 的不同方式。

## 安装方案 

### Docker Desktop（推荐）

获取 Docker Compose 最简单且推荐的方法是安装 Docker Desktop。 

Docker Desktop 包含了 Docker Compose，以及作为其前提条件的 Docker Engine 和 Docker CLI。 

Docker Desktop 适用于：
- [Linux](/manuals/desktop/setup/install/linux/_index.md)
- [Mac](/manuals/desktop/setup/install/mac-install.md)
- [Windows](/manuals/desktop/setup/install/windows-install.md)

> [!TIP]
> 
> 如果您已经安装了 Docker Desktop，可以通过从 Docker 菜单 {{< inline-image src="../../desktop/images/whale-x.svg" alt="鲸鱼菜单" >}} 中选择 **关于 Docker Desktop (About Docker Desktop)** 来检查您拥有的 Compose 版本。

### 插件（仅限 Linux）

> [!IMPORTANT]
>
> 此方法仅适用于 Linux。

如果您已经安装了 Docker Engine 和 Docker CLI，可以通过命令行安装 Docker Compose 插件，方式如下：
- [使用 Docker 的仓库](linux.md#install-using-the-repository)
- [手动下载并安装](linux.md#install-the-plugin-manually)

### 独立版（旧版）

> [!WARNING]
>
> 这种安装方案不被推荐，仅出于向后兼容的目的而提供支持。

您可以在 Linux 或 Windows Server 上 [安装独立版 Docker Compose](standalone.md)。
