---
description: 了解创建扩展的流程。
title: 构建和发布流程
keyword: Docker Extensions, sdk, build, create, publish
aliases:
 - /desktop/extensions-sdk/process/
weight: 10
---

本文档的结构与创建扩展时需要采取的步骤相匹配。

创建 Docker 扩展主要有两个部分：

1. 构建基础
2. 发布扩展

> [!NOTE]
>
> 创建 Docker 扩展不需要付费。[Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) 采用 Apache 2.0 许可证，可免费使用。任何人都可以创建新扩展并无限制地分享。
>
> 对于每个扩展应该如何授权也没有限制，这由您在创建新扩展时自行决定。

## 第一部分：构建基础

构建流程包括：

- 安装最新版本的 Docker Desktop。
- 设置包含文件的目录，包括扩展的源代码和所需的扩展特定文件。
- 创建 `Dockerfile` 以在 Docker Desktop 中构建、发布和运行您的扩展。
- 配置元数据文件，这是镜像文件系统根目录所必需的。
- 构建和安装扩展。

如需更多灵感，请参阅 [samples 文件夹](https://github.com/docker/extensions-sdk/tree/main/samples)中的其他示例。

> [!TIP]
>
> 在创建扩展时，请确保遵循[设计](design/design-guidelines.md)和 [UI 样式](design/_index.md)指南，以确保视觉一致性和 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。

## 第二部分：发布和分发您的扩展

Docker Desktop 在扩展市场中显示已发布的扩展。扩展市场是一个精选空间，开发者可以在这里发现改善开发体验的扩展，并上传自己的扩展与全世界分享。

如果您想将扩展发布到市场，请阅读[发布文档](extensions/publish.md)。

{{% include "extensions-form.md" %}}

## 下一步

如果您想快速开始创建 Docker 扩展，请参阅[快速入门指南](quickstart.md)。

或者，从阅读"第一部分：构建"部分开始，获取有关扩展创建过程每个步骤的更深入信息。

有关完整构建过程的深入教程，我们推荐以下来自 DockerCon 2022 的视频演示。

<iframe width="560" height="315" src="https://www.youtube.com/embed/Yv7OG-EGJsg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
