---
title: 使用 Intune 进行部署
description: 使用 Microsoft 的云端设备管理工具 Intune 来部署 Docker Desktop
keywords: microsoft, windows, docker desktop, 部署, deploy, mdm, 企业, 管理员, administrator, mac, pkg, dmg
tags: [admin]
weight: 40
aliases:
- /desktop/install/msi/use-intune/
- /desktop/setup/install/msi/use-intune/
---

{{< summary-bar feature_name="Intune" >}}

了解如何使用 Microsoft Intune 在 Windows 和 macOS 设备上部署 Docker Desktop。内容涵盖应用创建、安装程序配置以及向用户或设备分配应用。

{{< tabs >}}
{{< tab name="Windows" >}}

1. 登录您的 Intune 管理中心。
2. 添加新应用。依次选择 **Apps（应用）** > **Windows** > **Add（添加）**。
3. 应用类型选择 **Windows app (Win32)**。
4. 选择 `intunewin` 软件包。
5. 填写所需详细信息，如描述、发布者或应用版本，然后选择 **Next（下一步）**。
6. （可选）在 **Program（程序）** 选项卡上，您可以根据需要更新 **Install command（安装命令）** 字段。该字段预填为 `msiexec /i "DockerDesktop.msi" /qn`。有关您可以进行的更改示例，请参阅[常用安装场景](msi-install-and-configure.md)。

   > [!TIP]
   >
   > 建议您配置 Intune 部署，在安装成功后安排机器重启。
   >
   > 这是因为 Docker Desktop 安装程序会根据您的引擎选择安装 Windows 功能，并更新 `docker-users` 本地组的成员身份。
   >
   > 您可能还希望设置 Intune 根据返回代码来决定行为，并关注返回代码 `3010`。返回代码 3010 表示安装成功但需要重启。

7. 完成其余选项卡，然后查看并创建应用。

{{< /tab >}}
{{< tab name="Mac" >}}

首先，上传软件包：

1. 登录您的 Intune 管理中心。
2. 添加新应用。依次选择 **Apps（应用）** > **macOS** > **Add（添加）**。
3. 选择 **Line-of-business app（业务线应用）**，然后选择 **Select（选择）**。
4. 上传 `Docker.pkg` 文件并填写所需详细信息。

接下来，分配应用：

1. 添加应用后，在 Intune 中导航到 **Assignments（分配）**。
2. 选择 **Add group（添加组）**，并选择您要分配应用的用户组或设备组。
3. 选择 **Save（保存）**。

{{< /tab >}}
{{< /tabs >}}

## 额外资源

- [浏览常见问题解答 (FAQ)](faq.md)。
- 了解如何为您的用户[强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
