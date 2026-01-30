---
title: 安装 Docker Engine
linkTitle: 安装
weight: 10
description: 了解如何选择最适合您的 Docker Engine 安装方法。此客户端-服务器应用程序可在 Linux、Mac、Windows 上使用，也可作为静态二进制文件使用。
keywords: 安装引擎, docker engine 安装, 安装 docker engine, docker engine 安装过程, 引擎安装, docker ce 安装, docker ce 安装过程, 引擎安装程序, 正在安装 docker engine, docker 服务器安装, docker desktop 与 docker engine 比较
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

本节介绍如何在 Linux 上安装 Docker Engine (也称为 Docker CE)。Docker Engine 也可以通过 Docker Desktop 在 Windows、macOS 和 Linux 上使用。有关如何安装 Docker Desktop 的说明，请参阅：[Docker Desktop 概览](/manuals/desktop/_index.md)。

## 支持的平台

| 平台                                           | x86_64 / amd64 | arm64 / aarch64 | arm (32-bit) | ppc64le | s390x |
| :--------------------------------------------- | :------------: | :-------------: | :----------: | :-----: | :---: |
| [CentOS](centos.md)                            |       ✅       |       ✅        |              |   ✅    |       |
| [Debian](debian.md)                            |       ✅       |       ✅        |      ✅      |   ✅    |       |
| [Fedora](fedora.md)                            |       ✅       |       ✅        |              |   ✅    |       |
| [Raspberry Pi OS (32-bit)](raspberry-pi-os.md) |                |                 |      ✅      |         |       |
| [RHEL](rhel.md)                                |       ✅       |       ✅        |              |         |  ✅   |
| [SLES](sles.md)                                |                |                 |              |         |  ✅   |
| [Ubuntu](ubuntu.md)                            |       ✅       |       ✅        |      ✅      |   ✅    |  ✅   |
| [二进制文件 (Binaries)](binaries.md)           |       ✅       |       ✅        |      ✅      |         |       |

### 其他 Linux 发行版

> [!NOTE]
>
> 尽管以下说明可能有效，但 Docker 不会测试或验证在发行版衍生版上的安装。

- 如果您使用 Debian 衍生版，如 "BunsenLabs Linux"、"Kali Linux" 或 "LMDE" (基于 Debian 的 Mint)，应遵循 [Debian](debian.md) 的安装说明，并将您的发行版版本替换为对应的 Debian 版本。请参考您的发行版文档以查找哪个 Debian 版本与您的衍生版本对应。
- 同样，如果您使用 Ubuntu 衍生版，如 "Kubuntu"、"Lubuntu" 或 "Xubuntu"，应遵循 [Ubuntu](ubuntu.md) 的安装说明，并将您的发行版版本替换为对应的 Ubuntu 版本。请参考您的发行版文档以查找哪个 Ubuntu 版本与您的衍生版本对应。
- 一些 Linux 发行版通过其软件包仓库提供 Docker Engine 软件包。这些软件包由 Linux 发行版的软件包维护者构建和维护，在配置上可能存在差异，或者是由修改后的源代码构建的。Docker 不参与这些软件包的发布，您应向您的 Linux 发行版的问题跟踪器报告涉及这些软件包的任何错误或问题。

Docker 提供用于手动安装 Docker Engine 的 [二进制文件](binaries.md)。这些二进制文件是静态链接的，您可以在任何 Linux 发行版上使用它们。

## 发布渠道

Docker Engine 有两种更新渠道：**stable** (稳定版) 和 **test** (测试版)：

* **stable** 渠道为您提供正式发布的最新版本。
* **test** 渠道为您提供在正式发布前准备好进行测试的预发布版本。

请谨慎使用测试渠道。预发布版本包含实验性和早期访问功能，可能会发生破坏性更改。

## 支持

Docker Engine 是一个开源项目，由 Moby 项目维护者和社区成员提供支持。Docker 不直接为 Docker Engine 提供支持。Docker 为其产品提供支持，包括 Docker Desktop，它将 Docker Engine 作为其组件之一。

有关开源项目的信息，请参阅 [Moby 项目网站](https://mobyproject.org/)。

### 升级路径

补丁版本始终与其主版本和次版本向后兼容。

### 许可

Docker Engine 根据 Apache License 2.0 版获得许可。有关完整的许可文本，请参阅 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。

## 报告安全问题

如果您发现了安全问题，我们请求您立即引起我们的注意。

请勿提交公开问题 (Issue)。相反，请私下将您的报告发送至 security@docker.com。

非常感谢安全报告，Docker 将对此公开致谢。

## 开始使用

设置好 Docker 后，您可以通过 [Docker 入门教程](/get-started/introduction/_index.md) 学习基础知识。
