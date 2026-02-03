---
description: 在 Debian 上安装 Docker Desktop 的说明
keywords: debian, 安装, 卸载, 升级, 更新, linux, desktop, docker desktop, docker desktop for linux, dd4l
title: 在 Debian 上安装 Docker Desktop
linkTitle: Debian
weight: 20
toc_max: 4
aliases:
- /desktop/linux/install/debian/
- /desktop/install/debian/
- /desktop/install/linux/debian/
---

{{< summary-bar feature_name="Docker Desktop Debian" >}}

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关如何在 Debian 发行版上安装、启动和升级 Docker Desktop 的信息。

## 前提条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#通用系统要求)。
- 拥有 64 位版本的 Debian 12。
- 对于 Gnome 桌面环境，您还必须安装 AppIndicator 和 KStatusNotifierItem [Gnome 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 如果您不使用 GNOME，则必须安装 `gnome-terminal` 以便从 Docker Desktop 访问终端：

  ```console
  $ sudo apt install gnome-terminal
  ```

## 安装 Docker Desktop

在 Debian 上安装 Docker Desktop 的推荐方法：

1. 设置 Docker 的 `apt` 存储库。
   请参阅 [使用 apt 存储库安装](/manuals/engine/install/debian.md#install-using-the-repository) 的第一步。

2. 下载最新的 [DEB 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。有关校验和（Checksums），请参阅[发行说明](/manuals/desktop/release-notes.md)。

3. 使用 `apt` 安装软件包：

  ```console
  $ sudo apt-get update
  $ sudo apt-get install ./docker-desktop-amd64.deb
  ```

  > [!NOTE]
  >
  > 在安装过程结束时，由于安装的是手动下载的软件包，`apt` 会显示一个错误。您可以忽略此错误消息。
  >
  > ```text
  > N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
  > ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

软件包包含一个安装后脚本，可自动完成额外的设置步骤。

安装后脚本会执行以下操作：

- 在 Docker Desktop 二进制文件上设置功能位（capability），以便映射特权端口和设置资源限制。
- 将 Kubernetes 的 DNS 名称添加到 `/etc/hosts`。
- 创建从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典的 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会在 `/usr/local/bin/com.docker.cli` 安装一个包含云集成功能的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器。符号链接确保该包装器可以访问经典的 Docker CLI。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 升级 Docker Desktop

发布新版本的 Docker Desktop 后，Docker UI 会显示通知。每次升级 Docker Desktop 时，您需要下载新软件包并运行：

```console
$ sudo apt-get install ./docker-desktop-amd64.deb
```

## 下一步

- 探索 [Docker 订阅方案](https://www.docker.com/pricing/)，了解 Docker 还能为您提供什么。
- 参加 [Docker 工作坊](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有特性。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 介绍了常见问题、解决方案、如何运行并提交诊断以及提交问题。
- [常见问题解答 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的解答。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发行版相关的组件更新、新功能和改进。
- [备份与还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和还原 Docker 相关数据的说明。
