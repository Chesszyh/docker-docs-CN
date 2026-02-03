---
title: 使用 Docker 进行持续集成 (CI)
linkTitle: 持续集成 (CI)
weight: 70
description: 使用 Docker 进行持续集成
keywords: ci, build, 构建
aliases:
  - /ci-cd/best-practices/
---

持续集成 (Continuous Integration, CI) 是开发过程中将代码更改合并到项目主分支的阶段。在这一阶段，开发团队会运行测试和构建，以验证代码更改不会导致任何不必要或非预期的行为。

![即将合并的 Git 分支](./images/continuous-integration.svg)

在开发的这一阶段，即使您最终并不打算将应用程序打包为容器镜像，Docker 也有多种用途。

## Docker 作为构建环境

容器是可重现的、隔离的环境，能产生可预测的结果。在 Docker 容器中构建并测试您的应用程序，可以更轻松地防止非预期行为的发生。通过 Dockerfile，您可以精确定义构建环境的要求，包括编程运行时、操作系统、二进制文件等。

使用 Docker 管理构建环境还简化了维护工作。例如，升级到新版本的编程运行时只需更改 Dockerfile 中的标签或摘要 (digest)。无需通过 SSH 进入某台“宠物”虚拟机来手动重新安装新版本并更新相关配置文件。

此外，正如您期望第三方开源包是安全的一样，您的构建环境也应如此。您可以像扫描任何其他容器化应用程序一样，对构建镜像进行扫描和索引。

以下链接提供了关于如何开始在 CI 中使用 Docker 构建应用程序的说明：

- [GitHub Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [GitLab](https://docs.gitlab.com/runner/executors/docker.html)
- [Circle CI](https://circleci.com/docs/using-docker/)
- [Render](https://render.com/docs/docker)

### Docker in Docker

您还可以使用容器化的构建环境来通过 Docker 构建容器镜像。也就是说，您的构建环境运行在容器内部，而该容器本身已装备了运行 Docker 构建的能力。这种方法被称为 "Docker in Docker"。

Docker 提供了一个官方 [Docker 镜像](https://hub.docker.com/_/docker)，您可以将其用于此目的。

## 下一步

Docker 维护了一套官方 GitHub Actions，您可以使用它们在 GitHub Actions 平台上构建、注解并推送容器镜像。请参阅 [GitHub Actions 简介](github-actions/_index.md) 了解更多信息并开始使用。