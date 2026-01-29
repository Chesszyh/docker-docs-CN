---
description: 安装 Docker Desktop for Mac 以开始使用。本指南涵盖了系统要求、下载位置以及安装和更新说明。
keywords: docker for mac, 安装 docker macos, docker mac, docker mac 安装, docker 安装 macos, 在 mac 上安装 docker, install docker macbook, docker desktop for mac, 如何在 mac 上安装 docker, mac 设置 docker
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
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要 [付费订阅](https://www.docker.com/pricing/)。

本页提供了 Docker Desktop for Mac 的下载链接、系统要求和分步安装说明。

{{< button text="适用于 Apple 芯片的 Docker Desktop for Mac" url="https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64" >}}
{{< button text="适用于 Intel 芯片的 Docker Desktop for Mac" url="https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64" >}}

*有关校验和，请参阅 [发行说明](/manuals/desktop/release-notes.md)。*

> [!WARNING]
>
> 如果您遇到恶意软件检测问题，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 系统要求

{{< tabs >}}
{{< tab name="搭载 Intel 芯片的 Mac" >}}

- 受支持的 macOS 版本。

  > [!IMPORTANT]
  >
  > Docker Desktop 支持当前版本及前两个主要的 macOS 版本。随着新的 macOS 主要版本正式发布，Docker 将停止支持最旧的版本，并转而支持最新的 macOS 版本（以及之前的两个版本）。

- 至少 4 GB 的 RAM。

{{< /tab >}}
{{< tab name="搭载 Apple 芯片的 Mac" >}}

- 受支持的 macOS 版本。

  > [!IMPORTANT]
  >
  > Docker Desktop 支持当前版本及前两个主要的 macOS 版本。随着新的 macOS 主要版本正式发布，Docker 将停止支持最旧的版本，并转而支持最新的 macOS 版本（以及之前的两个版本）。

- 至少 4 GB 的 RAM。
- 为了获得最佳体验，建议您安装 Rosetta 2。虽然 Rosetta 2 不再是严格必需的，但在使用 Darwin/AMD64 时，仍有少数可选的命令行工具需要 Rosetta 2。请参阅 [已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)。要从命令行手动安装 Rosetta 2，请运行以下命令：

   ```console
   $ softwareupdate --install-rosetta
   ```
{{< /tab >}}
{{< /tabs >}}

## 在 Mac 上安装并运行 Docker Desktop

> [!TIP]
>
> 请参阅 [FAQ](/manuals/desktop/troubleshoot-and-support/faqs/general.md#如何在没有管理员权限的情况下运行-docker-desktop) 了解如何在无需管理员权限的情况下安装和运行 Docker Desktop。

### 交互式安装

1. 使用页面顶部的下载按钮或从 [发行说明](/manuals/desktop/release-notes.md) 下载安装程序。

2. 双击 `Docker.dmg` 打开安装程序，然后将 Docker 图标拖动到 **Applications**（应用程序）文件夹。默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。

3. 双击 **Applications** 文件夹中的 `Docker.app` 以启动 Docker。

4. Docker 菜单将显示 Docker 订阅服务协议（Docker Subscription Service Agreement）。

    以下是关键要点摘要： 
    - 对于小型企业（少于 250 名员工且年收入少于 1000 万美元）、个人使用、教育和非商业开源项目，Docker Desktop 是免费的。
    - 否则，专业用途需要付费订阅。
    - 政府实体也需要付费订阅。
    - Docker Pro、Team 和 Business 订阅包含 Docker Desktop 的商业使用。

5. 选择 **Accept**（接受）以继续。 

   请注意，如果您不同意这些条款，Docker Desktop 将无法运行。您可以稍后通过打开 Docker Desktop 来选择接受这些条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读 [常见问题解答 (FAQ)](https://www.docker.com/pricing/faq)。

6. 在安装窗口中，选择以下之一： 
   - **Use recommended settings (Requires password)**（使用推荐设置，需要密码）。这允许 Docker Desktop 自动设置必要的配置设置。 
   - **Use advanced settings**（使用高级设置）。然后您可以设置 Docker CLI 工具在系统或用户目录中的位置，启用默认的 Docker 套接字，并启用特权端口映射。有关更多信息以及如何设置 Docker CLI 工具的位置，请参阅 [设置](/manuals/desktop/settings-and-maintenance/settings.md#高级-advanced)。
7. 选择 **Finish**（完成）。如果您在第 6 步中应用了任何需要密码的配置，请输入密码以确认您的选择。  

### 从命令行安装

从页面顶部的下载按钮或 [发行说明](/manuals/desktop/release-notes.md) 下载 `Docker.dmg` 后，在终端中运行以下命令将 Docker Desktop 安装到 **Applications** 文件夹中：

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
$ sudo hdiutil detach /Volumes/Docker
```

默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。由于 macOS 通常在第一次使用应用程序时执行安全检查，`install` 命令可能需要几分钟才能运行完毕。

#### 安装程序标志

`install` 命令接受以下标志：

##### 安装行为

- `--accept-license`：现在就接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不是在应用程序首次运行时才要求接受。
- `--user=<用户名>`：在安装过程中执行一次特权配置。这免除了用户在首次运行时授予 root 权限的需要。有关更多信息，请参阅 [特权助手权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#权限要求-permission-requirements)。要查找用户名，请在 CLI 中输入 `ls /Users`。

##### 安全与访问

- `--allowed-org=<组织名称>`：要求用户在运行应用程序时登录并属于指定的 Docker Hub 组织。
- `--admin-settings`：自动创建一个 `admin-settings.json` 文件，管理员使用该文件来控制其组织内客户端机器上的某些 Docker Desktop 设置。有关更多信息，请参阅 [设置管理 (Settings Management)](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。
  - 它必须与 `--allowed-org=<组织名称>` 标志一起使用。 
  - 例如：`--allowed-org=<组织名称> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`

##### 代理配置

- `--proxy-http-mode=<模式>`：设置 HTTP 代理模式。两种模式分别为 `system`（系统，默认）或 `manual`（手动）。
- `--override-proxy-http=<URL>`：设置必须用于传出 HTTP 请求的 HTTP 代理 URL。它要求 `--proxy-http-mode` 设置为 `manual`。
- `--override-proxy-https=<URL>`：设置必须用于传出 HTTPS 请求的 HTTP 代理 URL，要求 `--proxy-http-mode` 设置为 `manual`。
- `--override-proxy-exclude=<主机/域名>`：为这些主机和域名绕过代理设置。这是一个以逗号分隔的列表。

> [!TIP]
>
> 作为 IT 管理员，您可以使用终端管理 (MDM) 软件来识别您环境中的 Docker Desktop 实例数量及其版本。这可以提供准确的许可报告，帮助确保您的机器使用最新版本的 Docker Desktop，并允许您 [强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 下一步

- 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，看看 Docker 能为您提供什么。
- [Docker 入门](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 介绍了常见问题、变通方法、如何运行和提交诊断信息以及提交 issue。
- [FAQ](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发布相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了备份和恢复 Docker 相关数据的说明。
