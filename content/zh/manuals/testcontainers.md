---
title: Testcontainers
description: 了解如何使用 Testcontainers 在您偏好的编程语言中以编程方式运行容器。
keywords: docker API, docker, testcontainers 文档, testcontainers, testcontainers oss, testcontainers oss 文档,
  docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: 开源
intro:
- title: 什么是 Testcontainers？
  description: 了解 Testcontainers 的功能及其主要优点
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流程
  description: 了解 Testcontainers 工作流程
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Testcontainers for Go
  description: 一个 Go 包，可简化为自动化集成/冒烟测试创建和清理基于容器的依赖项。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Testcontainers for Java
  description: 一个 Java 库，支持 JUnit 测试，提供可在 Docker 容器中运行的任何东西的轻量级、一次性实例。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一组开源库，提供简单轻量的 API，用于通过包裹在 Docker 容器中的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于您在生产中使用的相同服务的测试，而无需模拟或内存服务。

{{< grid items=intro >}}

## 快速入门

### 支持的语言

Testcontainers 为最流行的语言提供支持，Docker 赞助以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余的由社区驱动并由独立贡献者维护。

### 先决条件

Testcontainers 需要一个与 Docker-API 兼容的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新版 Docker 以及 Mac 和 Windows 上的 Docker Desktop 进行主动测试。
这些 Docker 环境会被 Testcontainers 自动检测和使用，无需任何额外配置。

可以配置 Testcontainers 以适用于其他 Docker 设置，例如远程 Docker 主机或 Docker 替代方案。
但是，这些并未在主要开发工作流程中进行主动测试，因此并非所有 Testcontainers 功能都可用
并且可能需要额外的手动配置。

如果您对您的设置的配置详细信息或它是否支持运行基于 Testcontainers 的测试有其他问题，
请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队和 Testcontainers 社区的其他用户。

 {{< grid items=quickstart >}}
