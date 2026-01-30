---
description: 如何将 Docker Scout 与其他系统进行设置。
keywords: 供应链, 安全, 集成, 注册表, ci, 环境
title: 将 Docker Scout 与其他系统集成
linkTitle: 集成
weight: 80
---

默认情况下，Docker Scout 会与您的 Docker 组织以及您在 Docker Hub 上启用 Scout 的仓库集成。您可以将 Docker Scout 与其他第三方系统集成，以获得更多见解，包括有关正在运行的工作负载的实时信息。

## 集成类别

根据您选择集成 Docker Scout 的位置和方式，您将获得不同的见解。

### 容器注册表

将 Docker Scout 与第三方容器注册表集成，使 Docker Scout 能够对这些仓库运行镜像分析，以便即使镜像不托管在 Docker Hub 上，您也能了解这些镜像的组成。

提供以下容器注册表集成：

- [Amazon Elastic Container Registry](./registry/ecr.md)
- [Azure Container Registry](./registry/acr.md)

### 持续集成

将 Docker Scout 与持续集成 (CI) 系统集成是在内部循环中即时、自动获得安全状况反馈的好方法。在 CI 中运行的分析还可以受益于额外的上下文，这对于获得更多见解非常有用。

提供以下 CI 集成：

- [GitHub Actions](./ci/gha.md)
- [GitLab](./ci/gitlab.md)
- [Microsoft Azure DevOps Pipelines](./ci/azure.md)
- [Circle CI](./ci/circle-ci.md)
- [Jenkins](./ci/jenkins.md)

### 环境监控

环境监控是指将 Docker Scout 与您的部署集成。这可以为您提供有关正在运行的容器工作负载的实时信息。

通过与环境集成，您可以将生产工作负载与镜像仓库或其他环境中的其他版本进行比较。

提供以下环境监控集成：

- [Sysdig](./environment/sysdig.md)

有关环境集成的更多信息，请参阅 [环境 (Environments)](./environment/_index.md)。

### 代码质量

将 Docker Scout 与代码分析工具集成，可以直接对源代码进行质量检查，帮助您跟踪错误、安全问题、测试覆盖率等。除了镜像分析和环境监控外，代码质量门禁还允许您通过 Docker Scout 将供应链管理向左移动。

启用代码质量集成后，对于已启用该集成的仓库，Docker Scout 会将代码质量评估作为策略评估结果包含在内。

提供以下代码质量集成：

- [SonarQube](sonarqube.md)

### 源代码管理

将 Docker Scout 与您的版本控制系统集成，可以直接在您的仓库中获得有关如何解决 Docker Scout 镜像分析检测到的问题的指导修复建议。

提供以下源代码管理集成：

- [GitHub](source-code-management/github.md) {{< badge color=blue text=Beta >}}

### 团队协作

此类集成允许您将 Docker Scout 与协作平台集成，以便将有关软件供应链的实时通知广播到团队沟通平台。

提供以下团队协作集成：

- [Slack](./team-collaboration/slack.md)
