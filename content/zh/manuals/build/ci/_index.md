---
title: 使用 Docker 进行持续集成
linkTitle: CI
weight: 70
description: 使用 Docker 进行持续集成
keywords: ci, build
aliases:
  - /ci-cd/best-practices/
---

持续集成（Continuous Integration，CI）是开发过程中将代码变更合并到项目主分支的环节。在这个阶段，开发团队会运行测试和构建，以验证代码变更不会引起任何意外或预期外的行为。

![即将合并的 Git 分支](./images/continuous-integration.svg)

在开发的这个阶段，Docker 有多种用途，即使您最终不会将应用程序打包为容器镜像。

## Docker 作为构建环境

容器是可重现的、隔离的环境，能够产生可预测的结果。在 Docker 容器中构建和测试您的应用程序可以更容易地防止意外行为的发生。使用 Dockerfile，您可以定义构建环境的确切需求，包括编程运行时、操作系统、二进制文件等。

使用 Docker 来管理您的构建环境也简化了维护工作。例如，更新到新版本的编程运行时可以像更改 Dockerfile 中的标签或摘要一样简单。无需通过 SSH 连接到宠物虚拟机（pet VM）来手动重新安装新版本并更新相关配置文件。

此外，正如您期望第三方开源软件包是安全的一样，您的构建环境也应该如此。您可以扫描和索引构建器镜像，就像对待任何其他容器化应用程序一样。

以下链接提供了如何开始在 CI 中使用 Docker 构建应用程序的说明：

- [GitHub Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [GitLab](https://docs.gitlab.com/runner/executors/docker.html)
- [Circle CI](https://circleci.com/docs/using-docker/)
- [Render](https://render.com/docs/docker)

### Docker in Docker

您还可以使用 Docker 化的构建环境来使用 Docker 构建容器镜像。也就是说，您的构建环境运行在一个容器内，而该容器本身具备运行 Docker 构建的能力。这种方法被称为"Docker in Docker"。

Docker 提供了一个官方的 [Docker 镜像](https://hub.docker.com/_/docker)，您可以用于此目的。

## 下一步

Docker 维护了一套官方的 GitHub Actions，您可以使用它们在 GitHub Actions 平台上构建、注释和推送容器镜像。请参阅 [GitHub Actions 简介](github-actions/_index.md) 了解更多信息并开始使用。
