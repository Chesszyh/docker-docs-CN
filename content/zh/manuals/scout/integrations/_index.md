---
description: 如何将 Docker Scout 与其他系统集成。
keywords: supply chain, security, integrations, registries, ci, environments
title: 将 Docker Scout 与其他系统集成
linkTitle: 集成
weight: 80
---

默认情况下，Docker Scout 与您的 Docker 组织以及 Docker Hub 上启用了 Docker Scout 的仓库集成。您可以将 Docker Scout 与其他第三方系统集成，以获得更多洞察，包括有关运行中工作负载的实时信息。

## 集成类别

根据您选择集成 Docker Scout 的位置和方式，您将获得不同的洞察。

### 容器镜像仓库

将 Docker Scout 与第三方容器镜像仓库集成，使 Docker Scout 能够对这些仓库运行镜像分析，这样即使镜像不托管在 Docker Hub 上，您也可以获得这些镜像组成的洞察。

以下容器镜像仓库集成可用：

- [Amazon Elastic Container Registry](./registry/ecr.md)
- [Azure Container Registry](./registry/acr.md)

### 持续集成

将 Docker Scout 与持续集成（CI）系统集成是在内部循环中获得即时、自动安全态势反馈的好方法。在 CI 中运行的分析还可以获得额外上下文的好处，这对于获得更多洞察非常有用。

以下 CI 集成可用：

- [GitHub Actions](./ci/gha.md)
- [GitLab](./ci/gitlab.md)
- [Microsoft Azure DevOps Pipelines](./ci/azure.md)
- [Circle CI](./ci/circle-ci.md)
- [Jenkins](./ci/jenkins.md)

### 环境监控

环境监控是指将 Docker Scout 与您的部署集成。这可以为您提供有关运行中容器工作负载的实时信息。

与环境集成可让您将生产工作负载与镜像仓库中或其他环境中的其他版本进行比较。

以下环境监控集成可用：

- [Sysdig](./environment/sysdig.md)

有关环境集成的更多信息，请参阅[环境](./environment/_index.md)。

### 代码质量

将 Docker Scout 与代码分析工具集成，可以直接对源代码进行质量检查，帮助您跟踪错误、安全问题、测试覆盖率等。除了镜像分析和环境监控外，代码质量门禁可让您使用 Docker Scout 将供应链管理左移。

启用代码质量集成后，Docker Scout 会将代码质量评估作为策略评估结果包含在您启用集成的仓库中。

以下代码质量集成可用：

- [SonarQube](sonarqube.md)

### 源代码管理

将 Docker Scout 与您的版本控制系统集成，可以直接在您的仓库中获得关于如何解决 Docker Scout 镜像分析检测到的问题的指导性修复建议。

以下源代码管理集成可用：

- [GitHub](source-code-management/github.md) {{< badge color=blue text=Beta >}}

### 团队协作

此类别中的集成可让您将 Docker Scout 与协作平台集成，用于将软件供应链相关的通知实时广播到团队通信平台。

以下团队协作集成可用：

- [Slack](./team-collaboration/slack.md)
