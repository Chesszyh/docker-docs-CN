---
title: 常见挑战与问题
description: 探索与 Docker Build Cloud 相关的常见挑战和问题。
weight: 40
---

### Docker Build Cloud 是独立产品还是 Docker Desktop 的一部分？

Docker Build Cloud 是一项服务，既可以与 Docker Desktop 配合使用，也可以独立使用。它能让您更快地构建容器镜像，无论是在本地还是在 CI 中，构建都在云端基础设施上运行。该服务使用远程构建缓存，确保在任何地方以及所有团队成员都能快速构建。

与 Docker Desktop 配合使用时，[构建视图](/desktop/use-desktop/builds/)可以开箱即用地与 Docker Build Cloud 配合工作。它会显示您的构建信息以及使用同一构建器的团队成员发起的构建信息，支持协作排查问题。

如果要在没有 Docker Desktop 的情况下使用 Docker Build Cloud，您必须[下载并安装](/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop)支持 Docker Build Cloud（`cloud` 驱动程序）的 Buildx 版本。如果您计划使用 `docker compose build` 命令通过 Docker Build Cloud 进行构建，还需要安装支持 Docker Build Cloud 的 Docker Compose 版本。

### Docker Build Cloud 如何与 Docker Compose 配合使用？

Docker Compose 可以开箱即用地与 Docker Build Cloud 配合工作。安装兼容 Docker Build Cloud 的客户端（buildx），它就可以与两个命令配合使用。

### Docker Build Cloud 团队版计划包含多少分钟？

Docker Build Cloud 的定价详情可在[定价页面](https://www.docker.com/pricing/)查看。

### 我是 Docker 个人用户。我可以试用 Docker Build Cloud 吗？

Docker 订阅用户（Pro、Team、Business）每月可获得一定数量的分钟数，在账户范围内共享，用于使用 Build Cloud。

如果您没有 Docker 订阅，可以注册免费的个人账户并开始试用 Docker Build Cloud。个人账户仅限单个用户使用。

团队要获得共享缓存的优势，必须订阅 Docker Team 或 Docker Business。

### Docker Build Cloud 是否支持 CI 平台？它是否与 GitHub Actions 兼容？

是的，Docker Build Cloud 可以与各种 CI 平台配合使用，包括 GitHub Actions、CircleCI、Jenkins 等。它可以加速您的构建流水线，这意味着更少的等待时间和上下文切换。

Docker Build Cloud 可以与 GitHub Actions 配合使用，自动化您的构建、测试和部署流水线。Docker 提供了一套官方 GitHub Actions，您可以在工作流中使用。

将 GitHub Actions 与 Docker Build Cloud 配合使用非常简单。只需在 GitHub Actions 配置中修改一行代码，其他所有内容保持不变。您无需创建新的流水线。在 Docker Build Cloud 的 [CI 文档](/build-cloud/ci/)中了解更多信息。

<div id="dbc-lp-survey-anchor"></div>
