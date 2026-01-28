---
linktitle: 镜像类型
title: 可用的 Docker 强化镜像类型
description: 了解 Docker 强化镜像目录中提供的不同镜像类型、发行版和变体。
keywords: docker hardened images, distroless containers, distroless images, docker distroless, alpine base image, debian base image, development containers, runtime containers, secure base image, multi-stage builds
weight: 20
---

Docker 强化镜像（DHI）是一个全面的安全强化容器镜像目录，旨在满足多样化的开发和生产需求。

## 框架和应用镜像

DHI 包含一系列流行的框架和应用镜像，每个镜像都经过强化和维护以确保安全性和合规性。这些镜像可无缝集成到现有工作流程中，使开发人员能够专注于构建应用程序而不影响安全性。

例如，您可能会在 DHI 目录中找到以下仓库：

- `node`：用于 Node.js 应用程序的框架
- `python`：用于 Python 应用程序的框架
- `nginx`：Web 服务器镜像

## 兼容性选项

Docker 强化镜像提供不同的基础镜像选项，让您可以灵活选择最适合您的环境和工作负载需求的选项：

- 基于 Debian 的镜像：如果您已经在基于 glibc 的环境中工作，这是一个很好的选择。Debian 被广泛使用，在许多语言生态系统和企业系统中提供强大的兼容性。

- 基于 Alpine 的镜像：使用 musl libc 的更小、更轻量的选项。这些镜像往往很小，因此拉取速度更快，占用空间更少。

每个镜像通过移除非必要组件（如 shell、包管理器和调试工具）来维护最小化和安全的运行时层。这有助于减少攻击面，同时保持与常见运行时环境的兼容性。

示例标签包括：

- `3.9.23-alpine3.21`：Python 3.9.23 的基于 Alpine 的镜像
- `3.9.23-debian12`：Python 3.9.23 的基于 Debian 的镜像

如果您不确定选择哪个，请从您已经熟悉的基础开始。Debian 往往提供最广泛的兼容性。

## 开发和运行时变体

为了适应应用程序生命周期的不同阶段，DHI 为所有语言框架镜像和部分应用镜像提供两种变体：

- 开发（dev）镜像：配备必要的开发工具和库，这些镜像有助于在安全环境中构建和测试应用程序。它们包括 shell、包管理器、root 用户和其他开发所需的工具。

- 运行时镜像：这些镜像去除了开发工具，仅包含运行应用程序所需的基本组件，确保在生产环境中具有最小的攻击面。

这种分离支持多阶段构建，使开发人员能够在安全的构建环境中编译代码，并使用精简的运行时镜像进行部署。

例如，您可能会在 DHI 仓库中找到以下标签：

- `3.9.23-debian12`：Python 3.9.23 的运行时镜像
- `3.9.23-debian12-dev`：Python 3.9.23 的开发镜像

## FIPS 变体

一些 Docker 强化镜像包含 `-fips` 变体。这些变体使用经过 [FIPS 140](../core-concepts/fips.md) 验证的加密模块，这是美国政府关于安全加密操作的标准。

FIPS 变体旨在帮助组织满足与敏感或受监管环境中加密使用相关的法规和合规要求。

您可以通过标签中包含 `-fips` 来识别 FIPS 变体。

例如：
- `3.13-fips`：Python 3.13 镜像的 FIPS 变体
- `3.9.23-debian12-fips`：基于 Debian 的 Python 3.9.23 镜像的 FIPS 变体

FIPS 变体可以像任何其他 Docker 强化镜像一样使用，非常适合在受监管行业运营或需要加密验证的合规框架下的团队。
