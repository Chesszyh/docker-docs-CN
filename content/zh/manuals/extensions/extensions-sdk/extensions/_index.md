---
title: "第二部分：发布"
description: 如何发布扩展的一般步骤
keywords: Docker, Extensions, sdk, publish
aliases:
 - /desktop/extensions-sdk/extensions/
weight: 40
---

本节描述如何使您的扩展可用且更容易被发现，以便用户可以一键发现并安装它。

## 发布您的扩展

在您开发并在本地测试了扩展之后，您就可以发布扩展，让其他人安装和使用（无论是在团队内部还是更广泛的公开使用）。

发布您的扩展包括：

- 提供有关扩展的信息：描述、截图等，以便用户决定是否安装您的扩展
- [验证](validate.md)扩展是否以正确的格式构建并包含所需的信息
- 在 [Docker Hub](https://hub.docker.com/) 上提供扩展镜像

有关发布流程的更多详细信息，请参阅[打包和发布您的扩展](DISTRIBUTION.md)。

## 推广您的扩展

一旦您的扩展在 Docker Hub 上可用，有权访问扩展镜像的用户可以使用 Docker CLI 安装它。

### 使用分享扩展链接

您还可以[生成分享 URL](share.md)，以便在团队内分享您的扩展，或在互联网上推广您的扩展。分享链接允许用户查看扩展描述和截图。

### 在 Marketplace 中发布您的扩展

您可以在扩展 Marketplace（扩展市场）中发布您的扩展，使其更容易被发现。如果您希望将扩展发布到 Marketplace，必须[提交您的扩展](publish.md)。

## 接下来会发生什么

### 新版本发布

一旦您发布了扩展，您只需推送带有递增标签的新版本扩展镜像即可发布新版本（仍使用 `semver` 约定）。
在 Marketplace 中发布的扩展可以向所有安装了该扩展的 Desktop 用户发送更新通知。有关更多详细信息，请参阅[新版本和更新](DISTRIBUTION.md#new-releases-and-updates)。

### 扩展支持和用户反馈

除了提供扩展功能描述和截图外，您还应该使用[扩展标签](labels.md)指定额外的 URL。这将引导用户访问您的网站以报告错误和反馈，以及获取文档和支持。

{{% include "extensions-form.md" %}}
