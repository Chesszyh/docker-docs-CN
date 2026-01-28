---
title: Docker 扩展的设计指南
linkTitle: 指南
description: Docker 扩展设计
keywords: Docker, extensions, design
aliases:
 - /desktop/extensions-sdk/design/design-guidelines/
weight: 10
---

在 Docker，我们的目标是构建能够融入用户现有工作流程的工具，而不是要求他们采用新的工作流程。我们强烈建议您在创建扩展时遵循这些指南。我们根据这些要求审核并批准您的市场发布。

以下是创建扩展时需要检查的简单清单：
- 是否容易上手？
- 是否易于使用？
- 在需要时是否容易获得帮助？


## 创建与 Docker Desktop 一致的体验

使用 [Docker Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme)和 [Docker 扩展样式指南](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771)确保您的扩展感觉像是 Docker Desktop 的一部分，为用户创造无缝体验。

- 确保扩展同时具有浅色和深色主题。按照 Docker 样式指南使用组件和样式可确保您的扩展符合 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。

  ![浅色和深色模式](images/light_dark_mode.webp)

- 确保您的扩展图标在浅色和深色模式下都可见。

  ![浅色和深色模式下的图标颜色](images/icon_colors.webp)

- 确保导航行为与 Docker Desktop 的其余部分一致。添加标题以设置扩展的上下文。

  ![设置上下文的标题](images/header.webp)

- 避免嵌入终端窗口。与 CLI 相比，Docker Desktop 的优势在于我们有机会向用户提供丰富的信息。尽可能充分利用这个界面。

  ![终端窗口的错误使用](images/terminal_window_dont.webp)

  ![终端窗口的正确使用](images/terminal_window_do.webp)

## 原生构建功能

- 为了不打断用户的流程，避免用户必须导航到 Docker Desktop 之外（例如到 CLI 或网页）才能执行某些功能的场景。相反，构建 Docker Desktop 原生的功能。

  ![切换上下文的错误方式](images/switch_context_dont.webp)

  ![切换上下文的正确方式](images/switch_context_do.webp)

## 分解复杂的用户流程

- 如果流程太复杂或概念太抽象，将流程分解为多个步骤，每个步骤只有一个简单的行动号召。这有助于新用户入门您的扩展

  ![复杂流程](images/complicated_flows.webp)

- 当有多个行动号召时，确保使用主按钮（填充按钮样式）和次按钮（轮廓按钮样式）来传达每个操作的重要性。

  ![行动号召](images/cta.webp)

## 新用户入门

在创建扩展时，确保扩展和您产品的首次用户能够理解其附加价值并轻松采用它。确保在扩展中包含上下文帮助。

- 确保将所有必要信息添加到扩展市场以及扩展详情页面。这应包括：
  - 扩展的截图。请注意，截图的推荐尺寸为 2400x1600 像素。
  - 详细描述，涵盖扩展的目的是什么、谁会发现它有用以及它如何工作。
  - 链接到必要的资源，如文档。
- 如果您的扩展具有特别复杂的功能，请在起始页面添加演示或视频。这有助于首次用户快速入门。

  ![起始页面](images/start_page.webp)

## 下一步

- 探索我们的[设计原则](design-principles.md)。
- 查看我们的 [UI 样式指南](index.md)。
- 了解如何[发布您的扩展](../extensions/_index.md)。
