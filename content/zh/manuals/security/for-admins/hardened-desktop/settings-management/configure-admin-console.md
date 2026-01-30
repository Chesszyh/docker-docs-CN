---
description: 如何使用 Docker 管理控制台为 Docker Desktop 配置设置管理
keywords: admin, 管理, 控制, rootless, 增强型容器隔离
title: 使用管理控制台配置设置管理
linkTitle: 使用管理控制台
weight: 20
---

{{< summary-bar feature_name="管理控制台" >}}

本页介绍了管理员如何使用 Docker 管理控制台（Admin Console）为 Docker Desktop 创建并应用设置策略。这些策略有助于在您的组织内实现 Docker Desktop 环境的标准化和安全性。

## 前提条件

- [安装 Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)。
- [验证您的域名](/manuals/security/for-admins/single-sign-on/configure.md#step-one-add-and-verify-your-domain)。
- [强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)以确保用户使用您的组织身份进行身份验证。
- 需要 Docker Business 订阅。

> [!IMPORTANT]
>
> 您必须将用户添加到已验证的域名中，设置才能生效。

## 创建设置策略

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **Desktop Settings Management（Desktop 设置管理）**。
3. 选择 **Create a settings policy（创建设置策略）**。
4. 提供名称和可选描述。

      > [!TIP]
      >
      > 您可以上传现有的 `admin-settings.json` 文件来预填表单。管理控制台策略会覆盖本地的 `admin-settings.json` 文件。

1. 选择策略适用的对象：
   - 所有用户（All users）
   - 特定用户（Specific users）

      > [!NOTE]
      >
      > 特定用户的策略会覆盖全局默认策略。在全局推行之前，请先对少数用户测试您的策略。

1. 配置每个设置的状态：
   - **User-defined（用户定义）**：用户可以更改设置。
   - **Always enabled（始终启用）**：设置已开启且已锁定。
   - **Enabled（已启用）**：设置已开启，但可以更改。
   - **Always disabled（始终禁用）**：设置已关闭且已锁定。
   - **Disabled（已禁用）**：设置已关闭，但可以更改。

      > [!TIP]
      >
      > 有关可用设置的完整列表、支持的平台以及它们适用的配置方法，请参阅[设置参考](settings-reference.md)。

1. 选择 **Create（创建）**。

应用策略：

- 新安装：启动 Docker Desktop 并登录。
- 现有安装：完全退出并重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 仅从 Docker Desktop 菜单中选择“Restart”（重新启动）是不够的。用户必须完全退出并重新启动 Docker Desktop。

Docker Desktop 会在启动时以及每隔 60 分钟检查一次策略更新。要回滚策略，可以将其删除或将单个设置设为 **User-defined（用户定义）**。

## 管理策略

在 **Settings Management** 页面的 **Actions（操作）** 菜单中，您可以：

- 编辑或删除现有的设置策略
- 将设置策略导出为 `admin-settings.json` 文件
- 将特定用户的策略提升为新的全局默认策略

## 了解更多

要查看每个 Docker Desktop 设置如何在 Docker 控制面板（Dashboard）、`admin-settings.json` 文件和管理控制台中进行映射，请参阅[设置参考](settings-reference.md)。
