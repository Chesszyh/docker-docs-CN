---
title: 使用 Jamf Pro 进行部署
description: 使用 Jamf Pro 部署 Mac 版 Docker Desktop
keywords: jamf, mac, macos, docker desktop, 部署, deploy, mdm, 企业, 管理员, administrator, pkg
tags: [admin]
weight: 50
---

{{< summary-bar feature_name="Jamf Pro" >}}

了解如何使用 Jamf Pro 部署 Mac 版 Docker Desktop，包括上传安装程序和创建部署策略。

首先，上传软件包：

1. 在 Jamf Pro 控制台中，导航到 **Computers（计算机）** > **Management Settings（管理设置）** > **Computer Management（计算机管理）** > **Packages（软件包）**。
2. 选择 **New（新建）** 以添加新软件包。
3. 上传 `Docker.pkg` 文件。

接下来，创建一个部署策略：

1. 导航到 **Computers（计算机）** > **Policies（策略）**。
2. 选择 **New（新建）** 以创建新策略。
3. 为策略输入一个名称，例如 "Deploy Docker Desktop"。
4. 在 **Packages（软件包）** 选项卡下，添加您刚刚上传的 Docker 软件包。
5. 配置 **Scope（范围）**，以定位您想要安装 Docker 的设备或设备组。
6. 保存策略并进行部署。

有关更多信息，请参阅 [Jamf Pro 官方文档](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html)。

## 额外资源

- 了解如何为您的用户[强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
