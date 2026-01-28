---
title: 安装 Docker Engine
linkTitle: 安装
weight: 10
description: 了解如何选择最适合您的 Docker Engine 安装方法。这个客户端-服务器
  应用程序可在 Linux、Mac、Windows 上使用，也可作为静态二进制文件使用。
keywords: install engine, docker engine install, install docker engine, docker engine
  installation, engine install, docker ce installation, docker ce install, engine
  installer, installing docker engine, docker server install, docker desktop vs docker engine
aliases:
- /cs-engine/
- /cs-engine/1.12/
- /cs-engine/1.12/upgrade/
- /cs-engine/1.13/
- /cs-engine/1.13/upgrade/
- /ee/docker-ee/oracle/
- /ee/supported-platforms/
- /en/latest/installation/
- /engine/installation/
- /engine/installation/frugalware/
- /engine/installation/linux/
- /engine/installation/linux/archlinux/
- /engine/installation/linux/cruxlinux/
- /engine/installation/linux/docker-ce/
- /engine/installation/linux/docker-ee/
- /engine/installation/linux/docker-ee/oracle/
- /engine/installation/linux/frugalware/
- /engine/installation/linux/gentoolinux/
- /engine/installation/linux/oracle/
- /engine/installation/linux/other/
- /engine/installation/oracle/
- /enterprise/supported-platforms/
- /install/linux/docker-ee/oracle/
---

本节介绍如何在 Linux 上安装 Docker Engine（Docker 引擎），也称为
Docker CE。Docker Engine 也可通过 Docker Desktop 在 Windows、macOS 和 Linux 上使用。有关如何安装 Docker Desktop 的说明，
请参阅：[Docker Desktop 概述](/manuals/desktop/_index.md)。

## 支持的平台

| 平台                                           | x86_64 / amd64 | arm64 / aarch64 | arm (32位) | ppc64le | s390x |
| :--------------------------------------------- | :------------: | :-------------: | :--------: | :-----: | :---: |
| [CentOS](centos.md)                            |       ✅       |       ✅        |            |   ✅    |       |
| [Debian](debian.md)                            |       ✅       |       ✅        |     ✅     |   ✅    |       |
| [Fedora](fedora.md)                            |       ✅       |       ✅        |            |   ✅    |       |
| [Raspberry Pi OS (32位)](raspberry-pi-os.md)   |                |                 |     ✅     |         |       |
| [RHEL](rhel.md)                                |       ✅       |       ✅        |            |         |  ✅   |
| [SLES](sles.md)                                |                |                 |            |         |  ✅   |
| [Ubuntu](ubuntu.md)                            |       ✅       |       ✅        |     ✅     |   ✅    |  ✅   |
| [二进制文件](binaries.md)                       |       ✅       |       ✅        |     ✅     |         |       |

### 其他 Linux 发行版

> [!NOTE]
>
> 虽然以下说明可能有效，但 Docker 不会在衍生发行版上测试或验证
> 安装。

- 如果您使用 Debian 衍生发行版，例如 "BunsenLabs Linux"、"Kali Linux" 或
  "LMDE"（基于 Debian 的 Mint），应按照
  [Debian](debian.md) 的安装说明进行操作，将您发行版的版本替换为
  相应的 Debian 版本。请参阅您发行版的文档以了解
  哪个 Debian 版本与您的衍生版本对应。
- 同样，如果您使用 Ubuntu 衍生发行版，例如 "Kubuntu"、"Lubuntu" 或 "Xubuntu"，
  应按照 [Ubuntu](ubuntu.md) 的安装说明进行操作，
  将您发行版的版本替换为相应的 Ubuntu 版本。
  请参阅您发行版的文档以了解哪个 Ubuntu 版本
  与您的衍生版本对应。
- 一些 Linux 发行版通过其软件包仓库提供 Docker Engine 软件包。这些软件包由 Linux
  发行版的软件包维护者构建和维护，可能在配置上有所不同
  或从修改过的源代码构建。Docker 不参与这些
  软件包的发布，您应该向您的 Linux 发行版的问题跟踪器报告任何涉及这些软件包的错误或问题。

Docker 提供用于手动安装 Docker Engine 的[二进制文件](binaries.md)。
这些二进制文件是静态链接的，您可以在任何 Linux 发行版上使用它们。

## 发布渠道

Docker Engine 有两种类型的更新渠道，**stable（稳定版）** 和 **test（测试版）**：

* **stable** 渠道为您提供正式发布的最新版本。
* **test** 渠道为您提供在正式发布前可供测试的预发布版本。

请谨慎使用 test 渠道。预发布版本包含实验性和
早期访问功能，这些功能可能会发生破坏性变更。

## 支持

Docker Engine 是一个开源项目，由 Moby 项目维护者
和社区成员支持。Docker 不为 Docker Engine 提供支持。
Docker 为 Docker 产品提供支持，包括 Docker Desktop，它使用
Docker Engine 作为其组件之一。

有关开源项目的信息，请参阅
[Moby 项目网站](https://mobyproject.org/)。

### 升级路径

补丁版本始终与其主版本和次版本向后兼容。

### 许可

Docker Engine 根据 Apache License, Version 2.0 许可。请参阅
[LICENSE](https://github.com/moby/moby/blob/master/LICENSE) 获取完整的
许可文本。

## 报告安全问题

如果您发现安全问题，我们请求您立即引起我们的注意。

请勿提交公开问题。而是将您的报告私下提交至 security@docker.com。

我们非常感谢安全报告，Docker 将公开感谢您。

## 开始使用

设置好 Docker 后，您可以通过
[Docker 入门](/get-started/introduction/_index.md)学习基础知识。
