---
Title: Microsoft Dev Box 中的 Docker Desktop
linkTitle: Microsoft Dev Box
description: 了解在 Microsoft Dev Box 中设置 Docker Desktop 的优势和方法
keywords: desktop, docker, windows, microsoft dev box
aliases:
 - /desktop/features/dev-box/
---

Docker Desktop 作为预配置镜像在 Microsoft Azure Marketplace 中提供，可与 Microsoft Dev Box 配合使用，让开发人员能够在云端快速搭建一致的开发环境。

Microsoft Dev Box 提供基于云的预配置开发者工作站，让您无需配置本地开发环境即可编写代码、构建和测试应用程序。用于 Microsoft Dev Box 的 Docker Desktop 镜像预装了 Docker Desktop 及其依赖项，为您提供开箱即用的容器化开发环境。

## 主要优势

- 预配置环境：Docker Desktop、WSL2 及其他必要组件均已预装并配置完成
- 一致的开发体验：确保所有团队成员使用相同的 Docker 环境
- 强大的资源：获得比本地机器更多的计算能力和存储空间
- 状态持久化：Dev Box 在会话之间保持您的状态，类似于本地机器的休眠功能
- 无缝授权：使用您现有的 Docker 订阅或直接通过 Azure Marketplace 购买新订阅

## 设置

### 前提条件

- 一个 Azure 订阅
- 访问 Microsoft Dev Box 的权限
- Docker 订阅（Pro、Team 或 Business）。您可以通过以下任一订阅选项在 Microsoft Dev Box 中使用 Docker Desktop：
   - 现有或新的 Docker 订阅
   - 通过 Azure Marketplace 购买的新 Docker 订阅
   - 已为您的组织配置 SSO 的 Docker Business 订阅

### 在 Dev Box 中设置 Docker Desktop

1. 导航至 Azure Marketplace 中的 [Docker Desktop for Microsoft Dev Box](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/dockerinc1694120899427.devbox_azuremachine?tab=Overview) 列表页面。
2. 选择 **Get It Now** 将虚拟机镜像添加到您的订阅。
3. 按照 Azure 工作流完成设置。
4. 根据您组织的设置，使用该镜像创建虚拟机、分配到开发中心或创建 Dev Box 池。

### 激活 Docker Desktop

当您的 Dev Box 使用 Docker Desktop 镜像配置完成后：

1. 启动您的 Dev Box 实例。
2. 启动 Docker Desktop。
3. 使用您的 Docker ID 登录。

## 支持

如遇以下相关问题：

- Docker Desktop 配置、使用或授权问题：通过 [Docker Support](https://hub.docker.com/support) 创建支持工单。
- Dev Box 创建、Azure 门户配置或网络问题：联系 Azure 支持。

## 限制

- Microsoft Dev Box 目前仅适用于 Windows 10 和 11（不支持 Linux 虚拟机）。
- 性能可能因您的 Dev Box 配置和网络条件而异。
