---
description: 了解设置管理（Settings Management）的工作原理、适用对象及其优势
keywords: 设置管理, Settings Management, rootless, docker desktop, hardened desktop
tags: [admin]
title: 什么是设置管理？
linkTitle: 设置管理
aliases:
 - /desktop/hardened-desktop/settings-management/
weight: 10
---

{{< summary-bar feature_name="强化版 Docker Desktop" >}}

设置管理允许管理员在最终用户机器上配置并强制执行 Docker Desktop 设置。它有助于保持配置的一致性，并增强组织内部的安全性。

## 适用对象

设置管理专为以下组织设计：

- 需要对 Docker Desktop 配置进行集中控制。
- 旨在跨团队标准化 Docker Desktop 环境。
- 在受监管的环境中运行，并需要强制执行合规性。

此功能随 Docker Business 订阅提供。

## 工作原理

管理员可以使用以下方法之一来定义设置：

- [管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)：通过 Docker 管理控制台创建并分配设置策略。
- [`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)：在用户的机器上放置配置文件以强制执行设置。

强制执行的设置会覆盖用户定义的配置，且开发人员无法修改。

## 可配置设置

设置管理支持广泛的 Docker Desktop 功能，包括代理、网络配置和容器隔离。

有关可以强制执行的设置完整列表，请参阅[设置参考](/manuals/security/for-admins/hardened-desktop/settings-management/settings-reference.md)。

## 设置设置管理

1. [强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)以确保所有开发人员都使用您的组织身份进行身份验证。
2. 选择一种配置方法：
    - 在 [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 或 [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 上使用 `--admin-settings` 安装程序标志，以自动创建 `admin-settings.json`。
    - 手动创建并配置 [`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)。
    - 在 [Docker 管理控制台](configure-admin-console.md)中创建设置策略。

配置完成后，开发人员在以下情况时会收到强制设置：

- 退出并重新启动 Docker Desktop，然后登录。
- 首次启动并登录 Docker Desktop。

> [!NOTE]
>
> 设置更改后，Docker Desktop 不会自动提示用户重新启动或重新进行身份验证。

## 开发人员体验

当设置被强制执行时：

- Docker Desktop 中的选项将显示为灰色，且无法通过控制面板（Dashboard）、CLI 或配置文件进行修改。
- 如果启用了增强型容器隔离（Enhanced Container Isolation），开发人员将无法使用特权容器或类似方法来更改 Docker Desktop Linux VM 中强制执行的设置。

## 下一步

- [使用 `admin-settings.json` 文件配置设置管理](configure-json-file.md)
- [使用 Docker 管理控制台配置设置管理](configure-admin-console.md)

## 了解更多

- 要查看每个 Docker Desktop 设置如何在 Docker 控制面板、`admin-settings.json` 文件和管理控制台中进行映射，请参阅[设置参考](settings-reference.md)。
- 阅读 [设置管理博客文章](https://www.docker.com/blog/settings-management-for-docker-desktop-now-generally-available-in-the-admin-console/)。
