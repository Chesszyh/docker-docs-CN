---
description: Instructions for installing Docker Desktop Arch package. Mostly meant
  for hackers who want to try out Docker Desktop on a variety of Arch-based distributions.
keywords: Arch Linux, install, uninstall, upgrade, update, linux, desktop, docker
  desktop, docker desktop for linux, dd4l
title: 在基于 Arch 的发行版上安装 Docker Desktop
linkTitle: Arch
aliases:
- /desktop/linux/install/archlinux/
- /desktop/install/archlinux/
- /desktop/install/linux/archlinux/
---

{{< summary-bar feature_name="Docker Desktop Archlinux" >}}

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面包含有关如何在基于 Arch 的发行版上安装、启动和升级 Docker Desktop 的信息。



## 前提条件

要成功安装 Docker Desktop，您必须满足[通用系统要求](_index.md#general-system-requirements)。

## 安装 Docker Desktop

1. [在 Linux 上安装 Docker 客户端二进制文件](/manuals/engine/install/binaries.md#install-daemon-and-client-binaries-on-linux)。Docker 客户端的静态二进制文件以 `docker` 形式提供给 Linux。您可以使用：

   ```console
   $ wget https://download.docker.com/linux/static/stable/x86_64/docker-{{% param "docker_ce_version" %}}.tgz -qO- | tar xvfz - docker/docker --strip-components=1
   $ mv ./docker /usr/local/bin
   ```

2. 从[发行说明](/manuals/desktop/release-notes.md)下载最新的 Arch 软件包。

3. 安装软件包：

   ```console
   $ sudo pacman -U ./docker-desktop-x86_64.pkg.tar.zst
   ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 下一步

- 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，了解 Docker 能为您提供什么。
- 查看 [Docker 研讨会](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md)提供了常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md)列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)提供了有关备份和恢复 Docker 相关数据的说明。
