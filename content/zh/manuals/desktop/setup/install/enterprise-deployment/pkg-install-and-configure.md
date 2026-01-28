---
title: PKG 安装程序
description: 了解如何使用 PKG 安装程序。同时探索其他配置选项。
keywords: pkg, mac, docker desktop, install, deploy, configure, admin, mdm
tags: [admin]
weight: 20
---

{{< summary-bar feature_name="PKG installer" >}}

PKG 软件包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，无需个人用户手动设置。借助此软件包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，提高其组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 从 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 下载完成后，双击 `Docker.pkg` 运行安装程序。
5. 按照安装向导上的说明授权安装程序并继续安装。
   - **Introduction**：选择 **Continue**。
   - **License**：查看许可协议并选择 **Agree**。
   - **Destination Select**：此步骤是可选的。建议您保留默认安装目标（通常是 `Macintosh HD`）。选择 **Continue**。
   - **Installation Type**：选择 **Install**。
   - **Installation**：使用管理员密码或 Touch ID 进行身份验证。
   - **Summary**：安装完成后，选择 **Close**。

> [!NOTE]
>
> 使用 PKG 安装 Docker Desktop 时，应用内更新会自动禁用。这确保组织可以保持版本一致性并防止未经批准的更新。对于使用 `.dmg` 安装程序安装的 Docker Desktop，应用内更新仍然受支持。
>
> Docker Desktop 会在有更新可用时通知您。要更新 Docker Desktop，请从 Docker Admin Console 下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本，请查看[发行说明](/manuals/desktop/release-notes.md)页面。

## 从命令行安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 从 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 在终端中，运行以下命令：

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## 其他资源

- 了解如何使用 [Intune](use-intune.md) 或 [Jamf Pro](use-jamf-pro.md) 部署 Docker Desktop for Mac
- 探索如何为您的用户[强制登录](/manuals/security/for-admins/enforce-sign-in/methods.md#plist-method-mac-only)。
