---
description: 了解如何排查常见的用户配置问题。
keywords: scim, jit, provision, troubleshoot, group mapping
title: 用户配置故障排除
linkTitle: 用户配置故障排除
tags: [Troubleshooting]
toc_max: 2
---

如果您在用户配置（user provisioning）过程中遇到用户角色、属性或意外账户行为的问题，本指南提供故障排除建议以解决冲突。

## SCIM 属性值被覆盖或忽略

### 错误消息

通常，此场景不会在 Docker 或您的 IdP 中产生错误消息。此问题通常表现为角色或团队分配不正确。

### 可能的原因

- JIT 配置已启用，Docker 正在使用您的 IdP 的 SSO 登录流程中的值来配置用户，这会覆盖 SCIM 提供的属性。
- SCIM 是在用户已通过 JIT 配置之后才启用的，因此 SCIM 更新不会生效。

### 受影响的环境

- 同时使用 SCIM 和 SSO 的 Docker 组织
- 在 SCIM 设置之前通过 JIT 配置的用户

### 复现步骤

1. 为您的 Docker 组织启用 JIT 和 SSO。
1. 作为用户通过 SSO 登录 Docker。
1. 启用 SCIM 并为该用户设置角色/团队属性。
1. SCIM 尝试更新用户的属性，但角色或团队分配未反映更改。

### 解决方案

#### 禁用 JIT 配置（推荐）

1. 登录 [Docker Home](https://app.docker.com/)。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 找到相关的 SSO 连接。
1. 选择**操作菜单**并选择 **Edit**。
1. 禁用 **Just-in-Time provisioning**。
1. 保存更改。

禁用 JIT 后，Docker 将 SCIM 作为用户创建和角色分配的唯一数据源。

**保持 JIT 启用并匹配属性**

如果您希望保持 JIT 启用：

- 确保您的 IdP 的 SSO 属性映射与 SCIM 发送的值匹配。
- 避免配置 SCIM 覆盖已通过 JIT 设置的属性。

此选项需要在 IdP 配置中严格协调 SSO 和 SCIM 属性。

## SCIM 更新不适用于现有用户

### 可能的原因

用户账户最初是手动创建或通过 JIT 创建的，SCIM 未关联来管理它们。

### 解决方案

SCIM 仅管理它配置的用户。要允许 SCIM 管理现有用户：

1. 从 Docker [Admin Console](https://app.docker.com/admin) 手动删除该用户。
1. 从您的 IdP 触发配置。
1. SCIM 将使用正确的属性重新创建该用户。

> [!WARNING]
>
> 删除用户会移除其资源所有权（例如，仓库）。在删除用户之前请转移所有权。
