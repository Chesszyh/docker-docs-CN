---
title: 扩展 SDK 概述
linkTitle: 扩展 SDK
description: Docker 扩展 SDK 文档总索引
keywords: Docker, Extensions, sdk
aliases:
 - /desktop/extensions-sdk/dev/overview/
 - /desktop/extensions-sdk/
grid:
  - title: "构建和发布流程"
    description: 了解构建和发布扩展的流程。
    icon: "checklist"
    link: "/extensions/extensions-sdk/process/"
  - title: "快速入门指南"
    description: 按照快速入门指南快速创建基本的 Docker 扩展。
    icon: "explore"
    link: "/extensions/extensions-sdk/quickstart/"
  - title: "查看设计指南"
    description: 确保您的扩展符合 Docker 的设计指南和原则。
    icon: "design_services"
    link: "/extensions/extensions-sdk/design/design-guidelines/"
  - title: "发布您的扩展"
    description: 了解如何将扩展发布到市场。
    icon: "publish"
    link: "/extensions/extensions-sdk/extensions/"
  - title: "与 Kubernetes 交互"
    description: 了解如何从 Docker 扩展间接与 Kubernetes 集群交互。
    icon: "multiple_stop"
    link: "/extensions/extensions-sdk/guides/kubernetes/"
  - title: "多架构扩展"
    description: 为多种架构构建您的扩展。
    icon: "content_copy"
    link: "/extensions/extensions-sdk/extensions/multi-arch/"
---

本节中的资源帮助您创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令来帮助您构建和发布扩展，扩展被打包为特殊格式的 Docker 镜像。

在镜像文件系统的根目录下有一个 `metadata.json` 文件，用于描述扩展的内容。它是 Docker 扩展的基本元素。

扩展可以包含 UI 部分和后端部分，后端部分可以在主机上或在 Desktop 虚拟机中运行。有关更多信息，请参阅[架构](architecture/_index.md)。

您通过 Docker Hub 分发扩展。但是，您可以在本地开发扩展，无需将扩展推送到 Docker Hub。有关更多详细信息，请参阅[扩展分发](extensions/DISTRIBUTION.md)。

{{% include "extensions-form.md" %}}

{{< grid >}}
