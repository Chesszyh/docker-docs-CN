---
title: 使用 Intune 部署
description: 使用 Microsoft 基于云的设备管理工具 Intune 部署 Docker Desktop
keywords: microsoft, windows, docker desktop, deploy, mdm, enterprise, administrator, mac, pkg, dmg
tags: [admin]
weight: 40
aliases:
- /desktop/install/msi/use-intune/
- /desktop/setup/install/msi/use-intune/
---

{{< summary-bar feature_name="Intune" >}}

了解如何使用 Microsoft Intune 在 Windows 和 macOS 设备上部署 Docker Desktop。本文涵盖应用创建、安装程序配置以及分配给用户或设备。

{{< tabs >}}
{{< tab name="Windows" >}}

1. 登录您的 Intune 管理中心。
2. 添加新应用。选择 **Apps**，然后选择 **Windows**，再选择 **Add**。
3. 对于应用类型，选择 **Windows app (Win32)**
4. 选择 `intunewin` 软件包。
5. 填写必要的详细信息，如描述、发布者或应用版本，然后选择 **Next**。
6. 可选：在 **Program** 选项卡上，您可以更新 **Install command** 字段以满足您的需求。该字段预填充为 `msiexec /i "DockerDesktop.msi" /qn`。有关可以进行的更改示例，请参阅[常见安装场景](msi-install-and-configure.md)。

   > [!TIP]
   >
   > 建议您将 Intune 部署配置为在成功安装后安排机器重启。
   >
   > 这是因为 Docker Desktop 安装程序会根据您的引擎选择安装 Windows 功能，并更新 `docker-users` 本地组的成员资格。
   >
   > 您可能还希望设置 Intune 根据返回代码确定行为，并监视返回代码 `3010`。返回代码 3010 表示安装成功但需要重启。

7. 完成其余选项卡，然后审核并创建应用。

{{< /tab >}}
{{< tab name="Mac" >}}

首先，上传软件包：

1. 登录您的 Intune 管理中心。
2. 添加新应用。选择 **Apps**，然后选择 **macOS**，再选择 **Add**。
3. 选择 **Line-of-business app**，然后选择 **Select**。
4. 上传 `Docker.pkg` 文件并填写必要的详细信息。

接下来，分配应用：

1. 添加应用后，在 Intune 中导航到 **Assignments**。
2. 选择 **Add group** 并选择要将应用分配到的用户或设备组。
3. 选择 **Save**。

{{< /tab >}}
{{< /tabs >}}

## 其他资源

- [探索常见问题](faq.md)。
- 了解如何为您的用户[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)。
