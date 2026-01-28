---
title: 使用 Jamf Pro 部署
description: 使用 Jamf Pro 部署 Docker Desktop for Mac
keywords: jamf, mac, docker desktop, deploy, mdm, enterprise, administrator, pkg
tags: [admin]
weight: 50
---

{{< summary-bar feature_name="Jamf Pro" >}}

了解如何使用 Jamf Pro 部署 Docker Desktop for Mac，包括上传安装程序和创建部署策略。

首先，上传软件包：

1. 从 Jamf Pro 控制台，导航到 **Computers** > **Management Settings** > **Computer Management** > **Packages**。
2. 选择 **New** 添加新软件包。
3. 上传 `Docker.pkg` 文件。

接下来，创建部署策略：

1. 导航到 **Computers** > **Policies**。
2. 选择 **New** 创建新策略。
3. 输入策略名称，例如 "Deploy Docker Desktop"。
4. 在 **Packages** 选项卡下，添加您上传的 Docker 软件包。
5. 配置范围以定位要安装 Docker 的设备或设备组。
6. 保存策略并部署。

有关更多信息，请参阅 [Jamf Pro 官方文档](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html)。

## 其他资源

- 了解如何为您的用户[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
