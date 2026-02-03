---
Title: Microsoft Dev Box 中的 Docker Desktop
linkTitle: Microsoft Dev Box
description: 了解在 Microsoft Dev Box 中设置 Docker Desktop 的好处及方法
keywords: desktop, docker, windows, microsoft dev box, 开发机
aliases:
 - /desktop/features/dev-box/
---

Docker Desktop 在 Microsoft Azure Marketplace 中以预配置镜像的形式提供，可用于 Microsoft Dev Box，使开发人员能够在云端快速设置一致的开发环境。

Microsoft Dev Box 提供基于云的、预配置的开发人员工作站，让您可以无需配置本地开发环境即可编写代码、构建和测试应用程序。面向 Microsoft Dev Box 的 Docker Desktop 镜像已预安装 Docker Desktop 及其依赖项，为您提供开箱即用的容器化开发环境。

## 核心优势

- **预配置环境**：Docker Desktop、WSL2 和其他必要组件均已预安装并配置完成。
- **一致的开发体验**：确保所有团队成员在相同的 Docker 环境下工作。
- **强大的资源**：访问比本地机器更强大的计算能力和存储空间。
- **状态持久化**：Dev Box 在不同会话之间保持您的状态，类似于本地机器的休眠。
- **无缝许可**：使用您现有的 Docker 订阅，或直接通过 Azure Marketplace 购买新订阅。

## 设置

### 前提条件

- 一个 Azure 订阅
- 拥有 Microsoft Dev Box 的访问权限
- 一个 Docker 订阅（Pro、Team 或 Business）。您可以通过以下任一订阅选项在 Microsoft Dev Box 中使用 Docker Desktop：
   - 现有的或新的 Docker 订阅
   - 通过 Azure Marketplace 购买的新 Docker 订阅
   - 为您的组织配置了 SSO 的 Docker Business 订阅

### 在 Dev Box 中设置 Docker Desktop

1. 导航到 Azure Marketplace 中的 [Docker Desktop for Microsoft Dev Box](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/dockerinc1694120899427.devbox_azuremachine?tab=Overview) 详情页。
2. 选择 **立即获取 (Get It Now)**，将该虚拟机镜像添加到您的订阅中。
3. 按照 Azure 的工作流完成设置。
4. 根据您的组织设置，使用该镜像创建 VM、分配给 Dev Centers 或创建 Dev Box Pools。

### 激活 Docker Desktop

当您的 Dev Box 使用 Docker Desktop 镜像预配完成后：

1. 启动您的 Dev Box 实例。
2. 运行 Docker Desktop。
3. 使用您的 Docker ID 登录。

## 支持

针对以下相关问题：

- Docker Desktop 的配置、使用或许可：请通过 [Docker 支持 (Docker Support)](https://hub.docker.com/support) 创建支持工单。
- Dev Box 的创建、Azure 门户配置或网络问题：请联系 Azure 支持。

## 限制

- Microsoft Dev Box 目前仅适用于 Windows 10 和 11（暂不支持 Linux VM）。
- 性能可能因您的 Dev Box 配置和网络状况而异。
