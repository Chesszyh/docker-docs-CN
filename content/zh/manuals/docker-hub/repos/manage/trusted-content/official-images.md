---
title: Docker 官方镜像
description: |
  本文介绍 Docker 官方镜像是如何创建的，
  以及您如何贡献或留下反馈。
keywords: docker official images, doi, contributing, upstream, open source
aliases:
- /trusted-content/official-images/contributing/
- /docker-hub/official_repos/
- /docker-hub/official_images/
---

Docker, Inc. 赞助一个专门的团队，负责审核和发布 Docker 官方镜像中的所有内容。该团队与上游软件维护者、安全专家以及更广泛的 Docker 社区协作工作。

虽然最好由上游软件作者维护其 Docker 官方镜像，但这不是一个严格的要求。为 Docker 官方镜像创建和维护镜像是一个协作过程。它在 [GitHub 上公开进行](https://github.com/docker-library/official-images)，鼓励参与。任何人都可以提供反馈、贡献代码、建议流程更改，甚至提议新的官方镜像。

## 创建 Docker 官方镜像

从高层次来看，官方镜像始于以一组 GitHub 拉取请求形式提交的提案。以下 GitHub 仓库详细说明了提案要求：

- [GitHub 上的 Docker 官方镜像仓库](https://github.com/docker-library/official-images#readme)
- [Docker 官方镜像文档](https://github.com/docker-library/docs#readme)

Docker 官方镜像团队在社区贡献者的帮助下，正式审核每个提案并向作者提供反馈。这个初始审核过程可能较长，通常需要一些来回沟通才能接受提案。

审核过程中有主观考量。这些主观关注归结为一个基本问题："这个镜像是否普遍有用？"例如，[Python](https://hub.docker.com/_/python/) Docker 官方镜像对于更大的 Python 开发者社区来说"普遍有用"，而上周用 Python 编写的一个晦涩的文字冒险游戏则不是。

一旦新提案被接受，作者有责任保持其镜像和文档的更新并响应用户反馈。Docker 负责在 Docker Hub 上构建和发布镜像。Docker 官方镜像的更新遵循与新镜像相同的拉取请求流程，尽管更新的审核过程更加精简。Docker 官方镜像团队最终充当所有更改的把关者，这有助于确保一致性、质量和安全性。

## 为 Docker 官方镜像提交反馈

所有 Docker 官方镜像在其文档中都包含一个 **User Feedback** 部分，涵盖该特定仓库的详细信息。在大多数情况下，包含官方镜像 Dockerfile 的 GitHub 仓库也有一个活跃的问题跟踪器。

关于 Docker 官方镜像的一般反馈和支持问题应发送到 [Docker 社区 Slack](https://dockr.ly/comm-slack) 的 `#general` 频道。

如果您是 Docker 官方镜像的维护者或贡献者，需要帮助或建议，请使用 [Libera.Chat IRC](https://libera.chat) 上的 `#docker-library` 频道。
