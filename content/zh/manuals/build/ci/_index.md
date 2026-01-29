---
title: 使用 Docker 进行持续集成
linkTitle: CI
weight: 70
description: 使用 Docker 进行持续集成
keywords: ci, build
aliases:
  - /ci-cd/best-practices/
---

持续集成 (Continuous Integration, CI) 是开发过程中的一个环节，旨在将您的代码更改合并到项目的主分支中。在此阶段，开发团队会运行测试和构建，以审查代码更改是否会导致任何不必要的或意外的行为。

![即将合并的 Git 分支](./images/continuous-integration.svg)

在开发的这个阶段，Docker 有多种用途，即使您最终并不打算将应用程序打包为容器镜像。

## Docker 作为构建环境

容器是可重现的、隔离的环境，能产生可预测的结果。在 Docker 容器中构建和测试应用程序可以更轻松地防止发生意外行为。通过 Dockerfile，您可以定义构建环境的确切要求，包括编程运行时、操作系统、二进制文件等。

使用 Docker 管理您的构建环境还可以简化维护工作。例如，更新到新版本的编程运行时可以像更改 Dockerfile 中的标签或摘要一样简单。无需 SSH 登录到特定的虚拟机来手动重新安装较新版本并更新相关的配置文件。

此外，正如您期望第三方开源包是安全的一样，您的构建环境也应该如此。您可以扫描并索引构建器镜像，就像对任何其他容器化应用程序所做的那样。

以下链接提供了关于如何在 CI 中开始使用 Docker 构建应用程序的说明：

- [GitHub Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [GitLab](https://docs.gitlab.com/runner/executors/docker.html)
- [Circle CI](https://circleci.com/docs/using-docker/)
- [Render](https://render.com/docs/docker)

### Docker in Docker

您还可以使用容器化的构建环境，通过 Docker 构建容器镜像。也就是说，您的构建环境运行在一个容器内部，而该容器本身具备运行 Docker 构建的能力。这种方法被称为 "Docker in Docker"。

Docker 提供了一个官方 [Docker 镜像](https://hub.docker.com/_/docker)，您可以将其用于此目的。

## 下一步

Docker 维护了一组官方 GitHub Actions，您可以使用它们在 GitHub Actions 平台上构建、标注和推送容器镜像。请参阅 [GitHub Actions 简介](github-actions/_index.md) 了解更多信息并开始使用。
