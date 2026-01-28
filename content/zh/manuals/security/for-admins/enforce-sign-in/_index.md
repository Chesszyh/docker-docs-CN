---
description: 了解强制用户登录 Docker Desktop 时会发生什么
toc_max: 2
keywords: authentication, registry.json, configure, enforce sign-in, docker desktop, security, .plist, registry key, mac, windows
title: 强制 Docker Desktop 登录
linkTitle: 强制登录
tags: [admin]
aliases:
 - /security/for-admins/configure-sign-in/
 - /docker-hub/configure-sign-in/
weight: 30
---

{{< summary-bar feature_name="Enforce sign-in" >}}

默认情况下，您组织的成员可以在不登录的情况下使用 Docker Desktop。当用户不以组织成员身份登录时，他们无法获得[组织订阅的权益](../../../subscription/details.md)，并且可以绕过您组织的 [Docker 安全功能](/manuals/security/for-admins/hardened-desktop/_index.md)。

根据您公司的设置和偏好，有多种方法可以强制登录：
- [注册表键方法（仅限 Windows）](methods.md#registry-key-method-windows-only){{< badge color=green text="New" >}}
- [配置描述文件方法（仅限 Mac）](methods.md#configuration-profiles-method-mac-only){{< badge color=green text="New" >}}
- [`.plist` 方法（仅限 Mac）](methods.md#plist-method-mac-only){{< badge color=green text="New" >}}
- [`registry.json` 方法（全平台）](methods.md#registryjson-method-all)

## 如何强制登录？

当 Docker Desktop 启动并检测到注册表键、`.plist` 文件或 `registry.json` 文件时，会发生以下情况：

- 出现 **Sign in required!** 提示，要求用户以组织成员身份登录才能使用 Docker Desktop。![强制登录提示](../../images/enforce-sign-in.png?w=400)
- 当用户登录的账户不是组织成员时，他们会自动退出登录且无法使用 Docker Desktop。用户可以选择 **Sign in** 重试。
- 当用户登录的账户是组织成员时，他们可以使用 Docker Desktop。
- 当用户退出登录时，会出现 **Sign in required!** 提示，他们将无法继续使用 Docker Desktop。

> [!NOTE]
>
> 强制 Docker Desktop 登录不会影响 Docker CLI 的访问。CLI 访问仅对强制单点登录的组织有影响。

## 强制登录与强制单点登录（SSO）的区别

[强制 SSO](/manuals/security/for-admins/single-sign-on/connect.md#optional-enforce-sso) 和强制登录是不同的功能。下表提供了使用每种功能时的描述和优势。

| 强制类型               | 描述                                                     | 优势                                                                                                                                                                                                                                                 |
|:----------------------|:--------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 仅强制登录             | 用户必须在使用 Docker Desktop 之前登录。                  | 确保用户获得订阅权益并确保应用安全功能。此外，您可以获得用户活动的洞察。                                                                                                                                                                               |
| 仅强制单点登录（SSO）  | 如果用户登录，则必须使用 SSO 登录。                       | 集中身份验证并强制执行身份提供商设置的统一策略。                                                                                                                                                                                                       |
| 同时强制两者           | 用户必须使用 SSO 登录后才能使用 Docker Desktop。          | 确保用户获得订阅权益并确保应用安全功能。此外，您可以获得用户活动的洞察。最后，它集中身份验证并强制执行身份提供商设置的统一策略。                                                                                                                        |
| 两者都不强制           | 如果用户登录，可以使用 SSO 或其 Docker 凭据。             | 让用户无障碍访问 Docker Desktop，但代价是降低了安全性和洞察能力。                                                                                                                                                                                      |

## 下一步

- 要强制登录，请查看[方法](/manuals/security/for-admins/enforce-sign-in/methods.md)指南。
- 要强制 SSO，请查看[强制 SSO](/manuals/security/for-admins/single-sign-on/connect.md) 步骤。
