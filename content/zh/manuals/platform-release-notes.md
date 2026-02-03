---
title: Docker Home、管理控制台、计费、安全及订阅功能发行说明
linkTitle: 发行说明
description: 了解 Docker Home、Docker 管理控制台、计费、订阅及安全功能的最新特性、错误修复和重大变更
keywords: Docker Home, Docker 管理控制台, Admin Console, 计费, 订阅, 安全, admin, releases, 发行说明, 更新内容
weight: 60
params:
  sidebar:
    group: 平台 (Platform)
tags: [Release notes, admin]
---

本页提供了关于 Docker Home、管理控制台、计费、安全及订阅功能的最新特性、改进、已知问题以及错误修复的详细信息。

## 2025-01-30

### 新特性

- 通过 PKG 安装程序安装 Docker Desktop 现已正式发布 (GA)。
- 通过配置配置文件 (Configuration Profiles) 强制执行登录现已正式发布 (GA)。

## 2024-12-10

### 新特性

- 新的 Docker 订阅方案现已上线。更多信息请参阅 [Docker 订阅与特性](/manuals/subscription/details.md) 以及 [宣布升级的 Docker 方案：更简单、更高价值、更优的开发体验与效率](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 2024-11-18

### 新特性

- 管理员现在可以：
  - 通过 [配置配置文件](/manuals/security/for-admins/enforce-sign-in/methods.md#配置配置文件方法仅限-mac) 强制执行登录（早期体验）。
  - 同时为多个组织强制执行登录（早期体验）。
  - 使用 [PKG 安装程序](/manuals/desktop/setup/install/enterprise-deployment/pkg-install-and-configure.md) 批量部署 Mac 版 Docker Desktop（早期体验）。
  - [通过 Docker 管理控制台使用 Desktop 设置管理功能](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)（早期体验）。

### 错误修复与增强

- 增强型容器隔离 (ECI) 已改进：
  - 允许管理员 [关闭 Docker 套接字挂载限制](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/config.md#允许所有容器挂载-docker-套接字)。
  - 在使用 [`allowedDerivedImages` 设置](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/config.md#派生镜像的-docker-套接字挂载权限) 时支持通配符标签。

## 2024-11-11

### 新特性

- [个人访问令牌 (Personal access tokens)](/security/for-developers/access-tokens/) (PATs) 现在支持设置过期日期。

## 2024-10-15

### 新特性

- Beta：您现在可以创建 [组织访问令牌 (Organization access tokens)](/security/for-admins/access-tokens/) (OATs)，以增强组织安全性并简化 Docker 管理控制台中的组织访问管理。

## 2024-08-29

### 新特性

- 通过 [MSI 安装程序](/manuals/desktop/setup/install/enterprise-deployment/msi-install-and-configure.md) 部署 Docker Desktop 现已正式发布 (GA)。
- 两种新的 [强制执行登录](/manuals/security/for-admins/enforce-sign-in/_index.md) 方法（Windows 注册表项和 `.plist` 文件）现已正式发布 (GA)。

## 2024-08-24

### 新特性

- 管理员现在可以查看 [组织洞察 (Organization Insights)](/manuals/admin/organization/insights.md)。

## 2024-07-17

### 新特性

- 您现在可以在 [Docker Home](https://app.docker.com) 中集中访问并管理 Docker 产品。