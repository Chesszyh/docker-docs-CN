---
title: PKG 安装程序
description: 了解如何使用 PKG 安装程序，并探索其他配置选项。
keywords: pkg, mac, macos, docker desktop, 安装, 部署, 配置, 管理员, admin, mdm
tags: [admin]
weight: 20
---

{{< summary-bar feature_name="PKG 安装程序" >}}

PKG 软件包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，并消除了单个用户手动设置的需要。通过此软件包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，从而提高整个组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Enterprise deployment（企业级部署）**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer（下载 PKG 安装程序）** 按钮。
4. 下载完成后，双击 `Docker.pkg` 运行安装程序。
5. 按照安装向导的说明授权安装程序并继续安装。
   - **Introduction (简介)**：选择 **继续 (Continue)**。
   - **License (许可)**：查看许可协议并选择 **同意 (Agree)**。
   - **Destination Select (目标选择)**：此步骤为可选。建议保留默认安装目标（通常为 `Macintosh HD`）。选择 **继续 (Continue)**。
   - **Installation Type (安装类型)**：选择 **安装 (Install)**。
   - **Installation (安装)**：使用管理员密码或 Touch ID 进行身份验证。
   - **Summary (摘要)**：安装完成后，选择 **关闭 (Close)**。

> [!NOTE]
>
> 使用 PKG 安装 Docker Desktop 时，应用内更新会自动禁用。这确保了组织可以保持版本一致性并防止未经批准的更新。对于使用 `.dmg` 安装程序安装的 Docker Desktop，仍支持应用内更新。
>
> 当有更新可用时，Docker Desktop 会通知您。要更新 Docker Desktop，请从 Docker 管理控制台下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本信息，请查看 [发行说明](/manuals/desktop/release-notes.md) 页面。

## 通过命令行安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Enterprise deployment（企业级部署）**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer（下载 PKG 安装程序）** 按钮。
4. 在终端中运行以下命令：

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## 额外资源

- 了解如何使用 [Intune](use-intune.md) 或 [Jamf Pro](use-jamf-pro.md) 部署 Mac 版 Docker Desktop。
- 探索如何为您的用户[强制执行登录](/manuals/security/for-admins/enforce-sign-in/methods.md#plist-方法仅限-mac)。
