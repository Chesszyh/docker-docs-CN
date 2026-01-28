---
description: 如何配置和使用 Docker 扩展的私有市场
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, Marketplace, private, security, admin
title: 为扩展配置私有市场
tags: [admin]
linkTitle: 配置私有市场
weight: 30
aliases:
 - /desktop/extensions/private-marketplace/
---

{{< summary-bar feature_name="Private marketplace" >}}

了解如何为您的 Docker Desktop 用户配置和设置一个包含精选扩展列表的私有市场。

Docker 扩展的私有市场（Private Marketplace）专为不给开发者提供机器 root 访问权限的组织设计。它利用[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)功能，使管理员能够完全控制私有市场。

## 前提条件

- [下载并安装 Docker Desktop 4.26.0 或更高版本](https://docs.docker.com/desktop/release-notes/)。
- 您必须是组织的管理员。
- 您能够通过设备管理软件（如 [Jamf](https://www.jamf.com/)）将 `extension-marketplace` 文件夹和 `admin-settings.json` 文件推送到下面指定的位置。

## 第一步：初始化私有市场

1. 在本地为将部署到开发者机器的内容创建一个文件夹：

   ```console
   $ mkdir my-marketplace
   $ cd my-marketplace
   ```

2. 初始化市场的配置文件：

   {{< tabs group="os_version" >}}
   {{< tab name="Mac" >}}

   ```console
   $ /Applications/Docker.app/Contents/Resources/bin/extension-admin init
   ```

   {{< /tab >}}
   {{< tab name="Windows" >}}

   ```console
   $ C:\Program Files\Docker\Docker\resources\bin\extension-admin init
   ```

   {{< /tab >}}
   {{< tab name="Linux" >}}

   ```console
   $ /opt/docker-desktop/extension-admin init
   ```

   {{< /tab >}}
   {{< /tabs >}}

这会创建 2 个文件：

- `admin-settings.json`，一旦应用到开发者机器上的 Docker Desktop，它将激活私有市场功能。
- `extensions.txt`，确定在私有市场中列出哪些扩展。

## 第二步：设置行为

生成的 `admin-settings.json` 文件包含各种可以修改的设置。

每个设置都有一个可以设置的 `value`，还有一个 `locked` 字段，允许您锁定设置并使开发者无法更改。

- `extensionsEnabled` 启用 Docker 扩展。
- `extensionsPrivateMarketplace` 激活私有市场，确保 Docker Desktop 连接到管理员定义和控制的内容，而不是公共 Docker 市场。
- `onlyMarketplaceExtensions` 允许或阻止开发者通过命令行安装其他扩展。开发新扩展的团队必须将此设置解锁（`"locked": false`）才能安装和测试正在开发的扩展。
- `extensionsPrivateMarketplaceAdminContactURL` 定义一个联系链接，供开发者在私有市场中请求新扩展。如果 `value` 为空，则不会在 Docker Desktop 上向开发者显示任何链接，否则可以是 HTTP 链接或 "mailto:" 链接。例如，

  ```json
  "extensionsPrivateMarketplaceAdminContactURL": {
    "locked": true,
    "value": "mailto:admin@acme.com"
  }
  ```

要了解更多关于 `admin-settings.json` 文件的信息，请参阅[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)。

## 第三步：列出允许的扩展

生成的 `extensions.txt` 文件定义了私有市场中可用的扩展列表。

文件中的每一行都是一个允许的扩展，格式为 `org/repo:tag`。

例如，如果您想允许 Disk Usage 扩展，您需要在 `extensions.txt` 文件中输入以下内容：

```console
docker/disk-usage-extension:0.2.8
```

如果不提供标签，将使用镜像的最新可用标签。您也可以用 `#` 注释掉行，这样该扩展将被忽略。

此列表可以包含不同类型的扩展镜像：

- 来自公共市场的扩展或存储在 Docker Hub 中的任何公共镜像。
- 作为私有镜像存储在 Docker Hub 中的扩展镜像。开发者需要登录并拥有这些镜像的拉取权限。
- 存储在私有仓库中的扩展镜像。开发者需要登录并拥有这些镜像的拉取权限。

> [!IMPORTANT]
>
> 您的开发者只能安装您列出的扩展版本。

## 第四步：生成私有市场

一旦 `extensions.txt` 中的列表准备好，您就可以生成市场：

{{< tabs group="os_version" >}}
{{< tab name="Mac" >}}

```console
$ /Applications/Docker.app/Contents/Resources/bin/extension-admin generate
```

{{< /tab >}}
{{< tab name="Windows" >}}

```console
$ C:\Program Files\Docker\Docker\resources\bin\extension-admin generate
```

{{< /tab >}}
{{< tab name="Linux" >}}

```console
$ /opt/docker-desktop/extension-admin generate
```

{{< /tab >}}
{{< /tabs >}}

这会创建一个 `extension-marketplace` 目录，并下载所有允许扩展的市场元数据。

市场内容是从扩展镜像信息（如镜像标签）生成的，这与[公共扩展的格式相同](extensions-sdk/extensions/labels.md)。它包括扩展标题、描述、截图、链接等。

## 第五步：测试私有市场设置

建议您在自己的 Docker Desktop 安装中试用私有市场。

1. 在终端中运行以下命令。此命令会自动将生成的文件复制到 Docker Desktop 读取配置文件的位置。根据您的操作系统，位置为：

    - Mac: `/Library/Application\ Support/com.docker.docker`
    - Windows: `C:\ProgramData\DockerDesktop`
    - Linux: `/usr/share/docker-desktop`

   {{< tabs group="os_version" >}}
   {{< tab name="Mac" >}}

   ```console
   $ sudo /Applications/Docker.app/Contents/Resources/bin/extension-admin apply
   ```

   {{< /tab >}}
   {{< tab name="Windows (run as admin)" >}}

   ```console
   $ C:\Program Files\Docker\Docker\resources\bin\extension-admin apply
   ```

   {{< /tab >}}
   {{< tab name="Linux" >}}

   ```console
   $ sudo /opt/docker-desktop/extension-admin apply
   ```

   {{< /tab >}}
   {{< /tabs >}}

2. 退出并重新打开 Docker Desktop。
3. 使用 Docker 账户登录。

当您选择 **Extensions** 选项卡时，您应该会看到私有市场仅列出您在 `extensions.txt` 中允许的扩展。

![Extensions Private Marketplace](/assets/images/extensions-private-marketplace.webp)

## 第六步：分发私有市场

确认私有市场配置正常工作后，最后一步是使用您组织使用的 MDM 软件将文件分发到开发者的机器。例如，[Jamf](https://www.jamf.com/)。

需要分发的文件有：
* `admin-settings.json`
* 整个 `extension-marketplace` 文件夹及其子文件夹

这些文件必须放置在开发者的机器上。根据您的操作系统，目标位置为（如上所述）：

- Mac: `/Library/Application\ Support/com.docker.docker`
- Windows: `C:\ProgramData\DockerDesktop`
- Linux: `/usr/share/docker-desktop`

确保您的开发者已登录 Docker Desktop，以便私有市场配置生效。作为管理员，您应该[强制要求登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。

## 反馈

如有反馈或发现任何错误，请发送邮件至 `extensions@docker.com`。
