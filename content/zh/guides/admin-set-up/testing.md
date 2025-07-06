---
title: 测试
description: 测试你的 Docker 设置。
weight: 30
---

## SSO 和 SCIM 测试

你可以通过使用与已验证域的 Docker 帐户关联的电子邮件地址登录 Docker Desktop 或 Docker Hub 来测试 SSO 和 SCIM。使用其 Docker 用户名登录的开发人员将不受 SSO 和/或 SCIM 设置的影响。

> [!IMPORTANT] 
>
> 一些用户可能需要基于 CLI 的登录到 Docker Hub，为此他们将需要一个[个人访问令牌 (PAT)](/manuals/security/for-developers/access-tokens.md)。

## 测试 RAM 和 IAM

> [!WARNING]
> 在继续之前，请务必与你的用户进行沟通，因为此步骤将影响所有登录到你的 Docker 组织的现有用户

如果你计划使用[注册表访问管理 (RAM)](/manuals/security/for-admins/hardened-desktop/registry-access-management.md) 和/或[镜像访问管理 (IAM)](/manuals/security/for-admins/hardened-desktop/image-access-management.md)，请确保你的测试开发人员使用其组织凭据登录到 Docker Desktop。经过身份验证后，让他们尝试通过 Docker CLI 拉取未经授权的镜像或来自不允许的注册表的镜像。他们应该会收到一条错误消息，指示该注册表受组织限制。

## 向测试组部署设置并强制登录

通过 MDM 向一小部分测试用户部署 Docker 设置并强制登录。让该组使用 Docker Desktop 和 Docker Hub 上的容器测试其开发工作流程，以确保所有设置和登录强制功能都按预期工作。

## 测试 Docker Build Cloud 功能

让你的一位 Docker Desktop 测试人员[连接到你创建的云构建器并使用它进行构建](/manuals/build-cloud/usage.md)。

## 验证 Docker Scout 对存储库的监控

检查 [Docker Scout 仪表板](https://scout.docker.com/)以确认已启用 Docker Scout 的存储库正在正确接收数据。
