---
description: 了解如何安装 Docker Compose。Compose 原生包含在 Docker Desktop 中，也可作为 Docker Engine 插件和独立工具使用。
keywords: install docker compose, docker compose plugin, docker-compose-plugin linux, docker compose v2, docker compose manual install, linux docker compose
title: 安装 Docker Compose 概述
linkTitle: 安装
weight: 20
toc_max: 3
aliases:
- /compose/compose-desktop/
- /compose/install/other/
- /compose/install/compose-desktop/
---

本页面总结了根据您的平台和需求安装 Docker Compose 的不同方式。

## 安装场景

### Docker Desktop（推荐）

获取 Docker Compose 最简单和推荐的方式是安装 Docker Desktop。

Docker Desktop 包含 Docker Compose 以及 Docker Engine 和 Docker CLI，这些都是 Compose 的前提条件。

Docker Desktop 可用于：
- [Linux](/manuals/desktop/setup/install/linux/_index.md)
- [Mac](/manuals/desktop/setup/install/mac-install.md)
- [Windows](/manuals/desktop/setup/install/windows-install.md)

> [!TIP]
>
> 如果您已经安装了 Docker Desktop，可以从 Docker 菜单 {{< inline-image src="../../desktop/images/whale-x.svg" alt="whale menu" >}} 选择**关于 Docker Desktop** 来检查您安装的 Compose 版本。

### 插件（仅限 Linux）

> [!IMPORTANT]
>
> 此方法仅适用于 Linux。

如果您已经安装了 Docker Engine 和 Docker CLI，可以从命令行安装 Docker Compose 插件，方法是：
- [使用 Docker 的仓库](linux.md#install-using-the-repository)
- [手动下载和安装](linux.md#install-the-plugin-manually)

### 独立版（旧版）

> [!WARNING]
>
> 不推荐此安装场景，仅为向后兼容目的提供支持。

您可以在 Linux 或 Windows Server 上[安装 Docker Compose 独立版](standalone.md)。
