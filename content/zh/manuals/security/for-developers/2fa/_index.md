---
description: 了解如何为您的 Docker 账户启用双因素认证
keywords: Docker, docker, registry, security, Docker Hub, authentication, two-factor
  authentication, account security
title: 为您的 Docker 账户启用双因素认证
linkTitle: 双因素认证
aliases:
- /docker-hub/2fa/
---

双因素认证（Two-factor authentication）为您的 Docker 账户增加了一层额外的安全保护，要求您在登录账户时提供唯一的安全码。除了密码之外，还需要此安全码。

当您启用双因素认证时，还会获得一个恢复码。每个恢复码都是唯一的，专属于您的账户。如果您无法访问身份验证器应用，可以使用此恢复码来恢复您的账户。请参阅[恢复您的 Docker 账户](recover-hub-account/)。

## 前提条件

您需要一部安装了基于时间的一次性密码（Time-based One-Time Password，TOTP）身份验证器应用的手机。常见的示例包括 Google Authenticator 或带有已注册 YubiKey 的 Yubico Authenticator。

## 启用双因素认证

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 选择您的头像，然后从下拉菜单中选择 **Account settings**。
3. 选择 **2FA**。
4. 输入您的账户密码，然后选择 **Confirm**。
5. 保存您的恢复码并将其存放在安全的地方。如果您无法访问身份验证器应用，可以使用恢复码来恢复账户。
6. 使用基于时间的一次性密码（TOTP）移动应用扫描二维码或输入文本验证码。
7. 关联身份验证器应用后，在文本框中输入六位数验证码。
8. 选择 **Enable 2FA**。

双因素认证现已启用。下次登录 Docker 账户时，您需要输入安全码。
