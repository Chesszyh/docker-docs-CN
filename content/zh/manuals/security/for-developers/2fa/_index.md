---
description: 了解如何在您的 Docker 帐户上启用双重身份验证 (2FA)
keywords: Docker, docker, registry, security, Docker Hub, authentication, two-factor authentication, account security, 安全, 双重身份验证, 2FA
title: 为您的 Docker 帐户启用双重身份验证
linkTitle: 双重身份验证
aliases:
- /docker-hub/2fa/
---

双重身份验证 (Two-factor authentication, 2FA) 通过在登录帐户时要求输入唯一的安全码，为您的 Docker 帐户增加了一层额外的安全保护。安全码是除密码之外的额外要求。

当您启用双重身份验证时，系统还会为您提供一个恢复码（Recovery code）。每个恢复码都是唯一的，并特定于您的帐户。如果您无法访问身份验证器应用程序（Authenticator app），可以使用此代码来恢复您的帐户。请参阅[恢复您的 Docker 帐户](recover-hub-account/)。

## 前提条件

您需要一部安装了基于时间的一次性密码 (TOTP) 身份验证器应用程序的手机。常见的示例包括 Google Authenticator，或者配合已注册 YubiKey 使用的 Yubico Authenticator。

## 启用双重身份验证

1. 登录您的 [Docker 帐户](https://app.docker.com/login)。
2. 选择您的头像，然后从下拉菜单中选择 **Account settings（帐户设置）**。
3. 选择 **2FA**。
4. 输入您的帐户密码，然后选择 **Confirm（确认）**。
5. 保存您的恢复码并将其存放在安全的地方。如果您无法访问身份验证器应用程序，可以使用恢复码来恢复帐户。
6. 使用基于时间的一次性密码 (TOTP) 移动应用扫描 QR 码或输入文本代码。
7. 关联身份验证器应用后，在文本框中输入六位数字代码。
8. 选择 **Enable 2FA（启用 2FA）**。

双重身份验证现已启用。下次登录 Docker 帐户时，您将需要输入安全码。
