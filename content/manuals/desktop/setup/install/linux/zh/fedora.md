---
description: Instructions for installing Docker Desktop on Fedora
keywords: fedora, rpm, update install, uninstall, upgrade, update, linux, desktop,
  docker desktop, docker desktop for linux, dd4l
title: 在 Fedora 上安装 Docker Desktop
linkTitle: Fedora
weight: 30
toc_max: 4
aliases:
- /desktop/linux/install/fedora/
- /desktop/install/fedora/
- /desktop/install/linux/fedora/
---

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面包含有关如何在 Fedora 发行版上安装、启动和升级 Docker Desktop 的信息。

## 前提条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有 64 位版本的 Fedora 41 或 Fedora 42。
- 对于 GNOME 桌面环境，您必须安装 AppIndicator 和 KStatusNotifierItem [GNOME 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 如果您不使用 GNOME，您必须安装 `gnome-terminal` 以启用从 Docker Desktop 访问终端：

   ```console
   $ sudo dnf install gnome-terminal
   ```

## 安装 Docker Desktop

在 Fedora 上安装 Docker Desktop：

1. 设置 [Docker 的软件包仓库](/manuals/engine/install/fedora.md#set-up-the-repository)。

2. 下载最新的 [RPM 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。有关校验和，请参阅[发行说明](/manuals/desktop/release-notes.md)。

3. 使用 dnf 安装软件包，如下所示：

   ```console
   $ sudo dnf install ./docker-desktop-x86_64.rpm
   ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

RPM 软件包包含一个安装后脚本，可自动完成额外的设置步骤。

安装后脚本：

- 在 Docker Desktop 二进制文件上设置功能，以映射特权端口和设置资源限制。
- 将 Kubernetes 的 DNS 名称添加到 `/etc/hosts`。
- 创建从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还安装了一个包含云集成功能的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器，位于 `/usr/local/bin/com.docker.cli`。该符号链接确保包装器可以访问经典 Docker CLI。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 升级 Docker Desktop

一旦 Docker Desktop 发布新版本，Docker UI 会显示通知。
每次您想升级 Docker Desktop 时，都需要先删除之前的版本，然后下载新软件包。运行：

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-x86_64.rpm
```

## 下一步

- 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，了解 Docker 能为您提供什么。
- 查看 [Docker 研讨会](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md)提供了常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md)列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)提供了有关备份和恢复 Docker 相关数据的说明。
