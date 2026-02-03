---
description: 安装 Docker Desktop for Mac 以开始使用。本指南涵盖了系统要求、下载地址以及如何安装和更新的说明。
keywords: docker for mac, 安装 docker macos, docker mac, docker mac install, docker install macos, install docker on mac, install docker macbook, docker desktop for mac, 如何在 mac 上安装 docker, 在 mac 上设置 docker
title: 在 Mac 上安装 Docker Desktop
linkTitle: Mac
weight: 10
aliases:
- /desktop/mac/install/
- /docker-for-mac/install/
- /engine/installation/mac/
- /installation/mac/
- /docker-for-mac/apple-m1/
- /docker-for-mac/apple-silicon/
- /desktop/mac/apple-silicon/
- /desktop/install/mac-install/
---

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页提供了 Docker Desktop for Mac 的下载链接、系统要求和详细的安装说明。

{{< button text="Docker Desktop for Mac (Apple 芯片)" url="https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64" >}}
{{< button text="Docker Desktop for Mac (Intel 芯片)" url="https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64" >}}

*有关校验和（Checksums），请参阅[发行说明](/manuals/desktop/release-notes.md)。*

> [!WARNING]
>
> 如果您遇到恶意软件检测问题，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 系统要求

{{< tabs >}}
{{< tab name="搭载 Intel 芯片的 Mac" >}}

- 受支持的 macOS 版本。

  > [!IMPORTANT]
  >
  > Docker Desktop 支持当前版本以及前两个主要版本的 macOS。随着 macOS 新主版本的发布，Docker 将停止支持最旧的版本，转而支持最新版本（以及之前的两个版本）。

- 至少 4 GB 内存。

{{< /tab >}}
{{< tab name="搭载 Apple 芯片的 Mac" >}}

- 受支持的 macOS 版本。

  > [!IMPORTANT]
  >
  > Docker Desktop 支持当前版本以及前两个主要版本的 macOS。随着 macOS 新主版本的发布，Docker 将停止支持最旧的版本，转而支持最新版本（以及之前的两个版本）。

- 至少 4 GB 内存。
- 为了获得最佳体验，建议您安装 Rosetta 2。虽然 Rosetta 2 不再是严格必须的，但在使用 Darwin/AMD64 时，仍有少数可选的命令行工具需要 Rosetta 2。请参阅[已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)。要通过命令行手动安装 Rosetta 2，请运行以下命令：

   ```console
   $ softwareupdate --install-rosetta
   ```
{{< /tab >}}
{{< /tabs >}}

## 在 Mac 上安装并运行 Docker Desktop

> [!TIP]
>
> 有关如何在不需要管理员权限的情况下安装和运行 Docker Desktop，请参阅 [常见问题解答 (FAQs)](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-I-run-docker-desktop-without-administrator-privileges)。

### 交互式安装

1. 使用页面顶部的下载按钮或从[发行说明](/manuals/desktop/release-notes.md)下载安装程序。

2. 双击 `Docker.dmg` 打开安装程序，然后将 Docker 图标拖动到 **Applications**（应用程序）文件夹。默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。

3. 在 **Applications** 文件夹中双击 `Docker.app` 以启动 Docker。

4. Docker 菜单将显示 Docker 订阅服务协议。

    以下是关键点的总结：
    - Docker Desktop 对小型企业（员工少于 250 人且年收入少于 1000 万美元）、个人使用、教育和非商业开源项目是免费的。
    - 否则，专业用途需要付费订阅。
    - 政府实体也需要付费订阅。
    - Docker Pro、Team 和 Business 订阅包含 Docker Desktop 的商业使用权。

5. 选择 **Accept（接受）** 继续。

   请注意，如果您不同意这些条款，Docker Desktop 将无法运行。您可以稍后通过打开 Docker Desktop 来选择接受条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读 [常见问题解答 (FAQs)](https://www.docker.com/pricing/faq)。

6. 在安装窗口中，选择以下之一：
   - **Use recommended settings (Requires password)**（使用推荐设置，需要密码）。这允许 Docker Desktop 自动设置必要的配置。
   - **Use advanced settings**（使用高级设置）。您可以设置 Docker CLI 工具在系统或用户目录中的位置、启用默认的 Docker 套接字，以及启用特权端口映射。有关更多信息以及如何设置 Docker CLI 工具的位置，请参阅[设置](/manuals/desktop/settings-and-maintenance/settings.md#advanced)。
7. 选择 **Finish（完成）**。如果您在步骤 6 中应用了任何需要密码的配置，请输入密码以确认您的选择。

### 通过命令行安装

从页面顶部的下载按钮或[发行说明](/manuals/desktop/release-notes.md)下载 `Docker.dmg` 后，在终端中运行以下命令，将 Docker Desktop 安装到 **Applications** 文件夹中：

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
$ sudo hdiutil detach /Volumes/Docker
```

默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。由于 macOS 通常在首次使用应用程序时执行安全检查，因此 `install` 命令可能需要几分钟才能完成。

#### 安装程序标志

`install` 命令接受以下标志：

##### 安装行为

- `--accept-license`：立即接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不需要在首次运行应用程序时接受。
- `--user=<username>`：在安装期间执行一次特权配置。这免去了用户在首次运行时授予 root 权限的需要。有关更多信息，请参阅[特权辅助工具权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#permission-requirements)。要查找用户名，请在 CLI 中输入 `ls /Users`。

##### 安全与访问

- `--allowed-org=<org name>`：要求用户在运行应用程序时登录并属于指定的 Docker Hub 组织。
- `--admin-settings`：自动创建一个 `admin-settings.json` 文件，管理员可以使用该文件来控制其组织内客户机上的某些 Docker Desktop 设置。有关更多信息，请参阅[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。
  - 该标志必须与 `--allowed-org=<org name>` 标志配合使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`

##### 代理配置

- `--proxy-http-mode=<mode>`：设置 HTTP 代理模式。两种模式为 `system`（默认）或 `manual`。
- `--override-proxy-http=<URL>`：设置用于传出 HTTP 请求的 HTTP 代理 URL。要求 `--proxy-http-mode` 设置为 `manual`。
- `--override-proxy-https=<URL>`：设置用于传出 HTTPS 请求的 HTTP 代理 URL。要求 `--proxy-http-mode` 设置为 `manual`。
- `--override-proxy-exclude=<hosts/domains>`：为指定的主机和域名绕过代理设置。这是一个以逗号分隔的列表。

> [!TIP]
>
> 作为 IT 管理员，您可以使用终端管理 (MDM) 软件来识别环境中的 Docker Desktop 实例数量及其版本。这可以提供准确的许可报告，帮助确保您的机器使用最新版本的 Docker Desktop，并允许您[强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 下一步

- 探索 [Docker 订阅方案](https://www.docker.com/pricing/)，了解 Docker 还能为您提供什么。
- [Docker 入门教程](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有特性。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 介绍了常见问题、解决方案、如何运行并提交诊断以及提交问题。
- [常见问题解答 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的解答。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发行版相关的组件更新、新功能和改进。
- [备份与还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和还原 Docker 相关数据的说明。