---
title: 发布到 Marketplace
description: Docker 扩展分发
keywords: Docker, extensions, publish
aliases:
 - /desktop/extensions-sdk/extensions/publish/
weight: 50
---

## 将您的扩展提交到 Marketplace

Docker Desktop 在 [Docker Desktop](https://open.docker.com/extensions/marketplace) 和 [Docker Hub](https://hub.docker.com/search?q=&type=extension) 上的扩展 Marketplace（扩展市场）中显示已发布的扩展。
扩展 Marketplace 是一个空间，开发者可以在此发现扩展以改善其开发体验，并提交自己的扩展以供所有 Desktop 用户使用。

当您[准备好发布](DISTRIBUTION.md)您的扩展到 Marketplace 时，可以[自助发布您的扩展](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)

> [!NOTE]
>
> 随着扩展 Marketplace 继续为扩展用户和发布者添加新功能，您需要
> 随时间维护您的扩展以确保它在 Marketplace 中保持可用。

> [!IMPORTANT]
>
> Docker 对扩展的人工审核流程目前已暂停。请通过[自动提交流程](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)提交您的扩展

### 提交前须知

在提交扩展之前，它必须通过[验证](validate.md)检查。

强烈建议您的扩展在提交前遵循本节中概述的指南。如果您在未遵循这些指南的情况下请求 Docker Extensions 团队进行审核，审核过程可能需要更长时间。

这些指南不能取代 Docker 的服务条款，也不保证获得批准：
- 查看[设计指南](../design/design-guidelines.md)
- 确保 [UI 样式](../design/_index.md)符合 Docker Desktop 指南
- 确保您的扩展同时支持浅色和深色模式
- 考虑扩展的新用户和现有用户的需求
- 与潜在用户一起测试您的扩展
- 测试您的扩展是否存在崩溃、错误和性能问题
- 在各种平台（Mac、Windows、Linux）上测试您的扩展
- 阅读[服务条款](https://www.docker.com/legal/extensions_marketplace_developer_agreement/)

#### 验证流程

提交的扩展会经过自动验证流程。如果所有验证检查都成功通过，扩展将在几小时内发布到 Marketplace 并可供所有用户访问。
这是让开发者获得所需工具并在您改进/完善扩展时获得反馈的最快方式。

> [!IMPORTANT]
>
> Docker Desktop 会缓存 Marketplace 中可用扩展的列表 12 小时。如果您没有在
> Marketplace 中看到您的扩展，可以重新启动 Docker Desktop 以强制刷新缓存。
