---
description: 如何使用 Docker Admin Console 为 Docker Desktop 配置设置管理
keywords: admin, controls, rootless, enhanced container isolation
title: 使用 Admin Console 配置设置管理
linkTitle: 使用 Admin Console
weight: 20
---

{{< summary-bar feature_name="Admin Console" >}}

本页说明管理员如何使用 Docker Admin Console 创建
和应用 Docker Desktop 的设置策略。这些策略有助于在组织内标准化
和保护 Docker Desktop 环境。

## 前提条件

- [安装 Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)。
- [验证您的域](/manuals/security/for-admins/single-sign-on/configure.md#step-one-add-and-verify-your-domain)。
- [强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)以
确保用户向您的组织进行身份验证。
- 需要 Docker Business 订阅。

> [!IMPORTANT]
>
> 您必须将用户添加到已验证的域才能使设置生效。

## 创建设置策略

1. 登录 [Docker Home](https://app.docker.com/) 并选择
您的组织。
1. 选择 **Admin Console**，然后选择 **Desktop Settings Management**。
1. 选择 **Create a settings policy**。
1. 提供名称和可选描述。

      > [!TIP]
      >
      > 您可以上传现有的 `admin-settings.json` 文件来预填表单。
      Admin Console 策略会覆盖本地 `admin-settings.json` 文件。

1. 选择策略适用对象：
   - All users（所有用户）
   - Specific users（特定用户）

      > [!NOTE]
      >
      > 用户特定策略会覆盖全局默认值。在全局推出之前，
      先用少数用户测试您的策略。

1. 为每个设置配置状态：
   - **User-defined**：用户可以更改该设置。
   - **Always enabled**：设置已开启且锁定。
   - **Enabled**：设置已开启但可以更改。
   - **Always disabled**：设置已关闭且锁定。
   - **Disabled**：设置已关闭但可以更改。

      > [!TIP]
      >
      > 有关可用设置的完整列表、支持的平台以及它们适用的配置方法，请参阅[设置参考](settings-reference.md)。

1. 选择 **Create**。

要应用策略：

- 新安装：启动 Docker Desktop 并登录。
- 现有安装：完全退出并重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 从 Docker Desktop 菜单重启是不够的。用户必须完全退出
并重新启动 Docker Desktop。

Docker Desktop 在启动时和每 60 分钟检查一次策略更新。要回滚
策略，可以删除它或将单个设置设为 **User-defined**。

## 管理策略

从 **Settings Management** 页面的 **Actions** 菜单，您可以：

- 编辑或删除现有设置策略
- 将设置策略导出为 `admin-settings.json` 文件
- 将用户特定策略提升为新的全局默认值

## 了解更多

要了解每个 Docker Desktop 设置如何在 Docker Dashboard、`admin-settings.json` 文件和 Admin Console 之间映射，请参阅[设置参考](settings-reference.md)。
