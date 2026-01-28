---
title: 扩展镜像标签
linkTitle: 添加标签
description: Docker 扩展标签
keywords: Docker, extensions, sdk, labels
aliases:
 - /desktop/extensions-sdk/extensions/labels/
weight: 10
---

扩展使用镜像标签来提供额外信息，如标题、描述、截图等。

这些信息随后作为扩展的概述显示，以便用户选择是否安装它。

![从标签生成的扩展概述](images/marketplace-details.png)

您可以在扩展的 `Dockerfile` 中定义[镜像标签](/reference/dockerfile.md#label)。

> [!IMPORTANT]
>
> 如果 `Dockerfile` 中缺少任何**必需**标签，Docker Desktop 会将该扩展视为无效，不会在 Marketplace 中列出。


以下是构建扩展时可以或需要指定的标签列表：

| 标签                                       | 必需 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 示例                                                                                                                                                                                                                                                         |
| ------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `org.opencontainers.image.title`            | 是      | 镜像的人类可读标题（字符串）。这将显示在 Docker Desktop 的 UI 中。                                                                                                                                                                                                                                                                                                                                                                                                                | my-extension                                                                                                                                                                                                                                                    |
| `org.opencontainers.image.description`      | 是      | 镜像中打包软件的人类可读描述（字符串）                                                                                                                                                                                                                                                                                                                                                                                                                             | This extension is cool.                                                                                                                                                                                                                                         |
| `org.opencontainers.image.vendor`           | 是      | 分发实体、组织或个人的名称。                                                                                                                                                                                                                                                                                                                                         | Acme, Inc.                                                                                                                                                                                                                                                      |
| `com.docker.desktop.extension.api.version`  | 是      | 扩展兼容的 Docker Extension manager 版本。必须遵循[语义化版本控制](https://semver.org/)。                                                                                                                                                                                                                                                             | 特定版本如 `0.1.0` 或约束表达式：`>= 0.1.0`、`>= 1.4.7, < 2.0`。对于您的第一个扩展，可以使用 `docker extension version` 来了解 SDK API 版本并指定 `>= <SDK_API_VERSION>`。                                   |
| `com.docker.desktop.extension.icon`         | 是      | 扩展图标（格式：.svg .png .jpg）                                                                                                                                                                                                                                                                                                                                                           | `https://example.com/assets/image.svg`                                                                                                                                                                                                                          |
| `com.docker.extension.screenshots`          | 是      | 图片 URL 和备用文本的 JSON 数组，按在元数据中出现的顺序显示给用户，显示在扩展详情页面。**注意：**截图的推荐尺寸为 2400x1600 像素。                                                                                                                                                                               | `[{"alt":"alternative text for image 1",` `"url":"https://example.com/image1.png"},` `{"alt":"alternative text for image2",` `"url":"https://example.com/image2.jpg"}]`                                                                                         |
| `com.docker.extension.detailed-description` | 是      | 以纯文本或 HTML 格式提供的关于扩展的附加信息，显示在详情对话框中。                                                                                                                                                                                                                                                    | `My detailed description` 或 `<h1>My detailed description</h1>`                                                                                                                                                 |
| `com.docker.extension.publisher-url`        | 是      | 发布者网站 URL，显示在详情对话框中。                                                                                                                                                                                                                                                           | `https://example.com`                                                                                                                                                                                                                                           |
| `com.docker.extension.additional-urls`      | 否       | 标题和附加 URL 的 JSON 数组，按在元数据中出现的顺序显示给用户，显示在扩展详情页面。Docker 建议您显示以下链接（如适用）：文档、支持、服务条款和隐私政策链接。                                                                                                                                      | `[{"title":"Documentation","url":"https://example.com/docs"},` `{"title":"Support","url":"https://example.com/bar/support"},` `{"title":"Terms of Service","url":"https://example.com/tos"},` `{"title":"Privacy policy","url":"https://example.com/privacy"}]` |
| `com.docker.extension.changelog`            | 是      | 以纯文本或 HTML 格式的变更日志，仅包含当前版本的更改。                                                                                                                                                                                                                                                   | `Extension changelog` 或 `<p>Extension changelog<ul>` `<li>New feature A</li>` `<li>Bug fix on feature B</li></ul></p>`                                                                                                                                         |
| `com.docker.extension.account-info`         | 否       | 用户是否需要注册 SaaS 平台才能使用扩展的某些功能。                                                                                                                                                                                                                                                          | 如果需要则填 `required`，否则留空。                                                                                                                                                                                                           |
| `com.docker.extension.categories`           | 否       | 扩展所属的 Marketplace 类别列表：`ci-cd`、`container-orchestration`、`cloud-deployment`、`cloud-development`、`database`、`kubernetes`、`networking`、`image-registry`、`security`、`testing-tools`、`utility-tools`、`volumes`。如果您未指定此标签，用户在按类别筛选时将无法在扩展 Marketplace 中找到您的扩展。2022 年 9 月 22 日之前发布到 Marketplace 的扩展已由 Docker 自动分类。 | 如果有多个类别，以逗号分隔的值指定，例如：`kubernetes,security` 或单个值，例如 `kubernetes`。                                                                                   |

> [!TIP]
>
> Docker Desktop 会对提供的 HTML 内容应用 CSS 样式。您可以确保它
> [在 Marketplace 中](#preview-the-extension-in-the-marketplace)正确渲染。建议您遵循
> [样式指南](../design/_index.md)。

## 在 Marketplace 中预览扩展

您可以验证镜像标签是否按预期渲染。

当您创建并安装未发布的扩展时，可以在 Marketplace 的**管理**选项卡中预览扩展。您可以看到扩展标签在列表中和扩展详情页面中的渲染效果。

> 预览已在 Marketplace 中列出的扩展
>
> 当您安装已发布到 Marketplace 的扩展的本地镜像时，例如使用 `latest` 标签，您的本地镜像不会被检测为"未发布"。
>
> 您可以重新标记镜像以获得不同的镜像名称，该名称不会被列为已发布的扩展。
> 使用 `docker tag org/published-extension unpublished-extension`，然后使用 `docker extension install unpublished-extension`。

![列表预览](images/list-preview.png)
