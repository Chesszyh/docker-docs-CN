---
description: 了解当您强制用户登录 Docker Desktop 时会发生什么
toc_max: 2
keywords: authentication, registry.json, configure, enforce sign-in, docker desktop, security, .plist, registry key, mac, windows, 身份验证, 配置, 强制登录, 安全
title: 强制执行 Docker Desktop 登录
linkTitle: 强制登录
tags: [admin]
aliases:
 - /security/for-admins/configure-sign-in/
 - /docker-hub/configure-sign-in/
weight: 30
---

{{< summary-bar feature_name="Enforce sign-in" >}}

默认情况下，您组织的成员可以在不登录的情况下使用 Docker Desktop。当用户不以组织成员身份登录时，他们无法享受 [组织订阅的权益](../../../subscription/details.md)，并且可以规避为您组织设置的 [Docker 安全功能](/manuals/security/for-admins/hardened-desktop/_index.md)。

根据您公司的设置和偏好，有多种强制登录的方法：
- [注册表键方法 (仅限 Windows)](methods.md#registry-key-method-windows-only){{< badge color=green text="新" >}}
- [配置描述文件方法 (仅限 Mac)](methods.md#configuration-profiles-method-mac-only){{< badge color=green text="新" >}}
- [`.plist` 方法 (仅限 Mac)](methods.md#plist-method-mac-only){{< badge color=green text="新" >}}
- [`registry.json` 方法 (所有平台)](methods.md#registryjson-method-all)

## 如何强制执行登录？

当 Docker Desktop 启动并检测到注册表键、`.plist` 文件或 `registry.json` 文件时，会发生以下情况：

- 出现 **Sign in required!** (需要登录！) 提示，要求用户以您组织成员的身份登录才能使用 Docker Desktop。 ![强制登录提示](../../images/enforce-sign-in.png?w=400)
- 当用户登录的帐户不是您组织的成员时，他们会被自动注销且无法使用 Docker Desktop。用户可以选择 **Sign in** (登录) 并重试。
- 当用户登录的帐户是您组织的成员时，他们可以使用 Docker Desktop。
- 当用户注销时，会出现 **Sign in required!** 提示，他们将无法再使用 Docker Desktop。

> [!NOTE]
>
> 强制执行 Docker Desktop 登录不会影响访问 Docker CLI。只有强制执行单点登录 (SSO) 的组织才会影响 CLI 访问。

## 强制登录与强制单点登录 (SSO) 的对比

[强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md#optional-enforce-sso) 和强制登录是不同的功能。下表提供了使用每个功能的描述和好处。

| 强制执行方式                      | 描述                                                     | 好处                                                                                                                                                                                                                                                   |
|:----------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 仅强制登录              | 用户必须先登录才能使用 Docker Desktop。                 | 确保用户获得订阅权益并确保应用安全功能。此外，您还可以深入了解用户的活动。                                                                                                    |
| 仅强制单点登录 (SSO) | 如果用户登录，必须使用 SSO 登录。                  | 集中身份验证并强制执行由身份提供者设置的统一策略。                                                                                                                                                                     |
| 两者都强制执行                      | 用户在使用 Docker Desktop 前必须使用 SSO 登录。       | 确保用户获得订阅权益并确保应用安全功能。此外，您还可以深入了解用户的活动。最后，它实现了身份验证的集中化，并强制执行由身份提供者设置的统一策略。 |
| 两者都不强制执行                   | 如果用户登录，可以使用 SSO 或其 Docker 凭据。 | 让用户无障碍地访问 Docker Desktop，但代价是安全性和洞察力的降低。                                                                                                                                                  |

## 下一步

- 要强制登录，请参阅 [方法 (Methods)](/manuals/security/for-admins/enforce-sign-in/methods.md) 指南。
- 要强制执行 SSO，请参阅 [强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md) 步骤。
