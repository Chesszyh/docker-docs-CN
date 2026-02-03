---
description: 了解如何排查常见的用户预配问题。
keywords: scim, jit, provision, troubleshoot, group mapping, 预配, 排查
title: 排查预配故障
linkTitle: 排查预配故障
tags: [Troubleshooting]
toc_max: 2
---

如果您在使用用户预配时遇到用户角色、属性问题或意外的帐户行为，本指南提供了解决冲突的排查建议。

## SCIM 属性值被覆盖或忽略

### 错误信息

通常，这种情况在 Docker 或您的 IdP 中不会产生错误消息。此问题通常表现为角色或团队分配不正确。

### 可能的原因

- 启用了 JIT 预配，且 Docker 正在使用来自 IdP 的 SSO 登录流程中的值来预配用户，这会覆盖 SCIM 提供的属性。
- SCIM 是在用户已经通过 JIT 预配后才启用的，因此 SCIM 更新未生效。

### 受影响的环境

- 同时使用 SCIM 和 SSO 的 Docker 组织
- 在设置 SCIM 之前已通过 JIT 预配的用户

### 复现步骤

1. 为您的 Docker 组织启用 JIT 和 SSO。
1. 用户通过 SSO 登录 Docker。
1. 启用 SCIM 并为该用户设置角色/团队属性。
1. SCIM 尝试更新用户的属性，但角色或团队分配未反映更改。

### 解决方案

#### 禁用 JIT 预配（推荐）

1. 登录 [Docker Home](https://app.docker.com/)。
1. 选择 **Admin Console（管理控制台）**，然后选择 **SSO and SCIM**。
1. 找到相关的 SSO 连接。
1. 选择 **操作菜单 (actions menu)** 并选择 **Edit（编辑）**。
1. 禁用 **Just-in-Time provisioning（即时预配）**。
1. 保存更改。

禁用 JIT 后，Docker 将使用 SCIM 作为用户创建和角色分配的唯一事实来源。

#### 保持 JIT 启用并匹配属性

如果您希望保持 JIT 启用：

- 确保您的 IdP 的 SSO 属性映射与 SCIM 发送的值一致。
- 避免将 SCIM 配置为覆盖已通过 JIT 设置的属性。

此选项要求在您的 IdP 配置中严格协调 SSO 和 SCIM 属性。

## SCIM 更新不适用于现有用户

### 可能的原因

用户帐户最初是手动创建或通过 JIT 创建的，SCIM 未被链接来管理它们。

### 解决方案

SCIM 仅管理由其预配的用户。要允许 SCIM 管理现有用户：

1. 从 Docker [管理控制台 (Admin Console)](https://app.docker.com/admin) 中手动移除该用户。
2. 从您的 IdP 触发预配。
3. SCIM 将使用正确的属性重新创建该用户。

> [!WARNING]
>
> 删除用户会移除其资源所有权（例如存储库）。在移除用户之前，请先转移所有权。
