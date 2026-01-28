---
title: Testcontainers
description: 了解如何使用 Testcontainers 以您偏好的编程语言以编程方式运行容器。
keywords: docker APIs, docker, testcontainers documentation, testcontainers, testcontainers oss, testcontainers oss documentation,
  docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: 开源
intro:
- title: 什么是 Testcontainers？
  description: 了解 Testcontainers 的作用及其主要优势
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流
  description: 了解 Testcontainers 的工作流
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Testcontainers for Go
  description: 一个 Go 软件包，可以轻松创建和清理用于自动化集成/冒烟测试的基于容器的依赖项。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Testcontainers for Java
  description: 一个支持 JUnit 测试的 Java 库，提供可在 Docker 容器中运行的任何内容的轻量级、一次性实例。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一套开源库，提供了简单且轻量级的 API，用于通过包装在 Docker 容器中的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于与生产环境中相同服务的测试，而无需使用 Mock 或内存服务。

{{< grid items=intro >}}

## 快速入门

### 受支持的语言

Testcontainers 支持大多数流行的语言，Docker 赞助了以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余部分由社区驱动并由独立贡献者维护。

### 前提条件

Testcontainers 需要兼容 Docker-API 的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新 Docker 版本以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。
这些 Docker 环境会自动检测并由 Testcontainers 使用，无需进行任何额外配置。

可以将 Testcontainers 配置为在其他 Docker 设置下工作，例如远程 Docker 主机或 Docker 替代方案。
但是，这些并未在主开发工作流中进行积极测试，因此并非所有 Testcontainers 功能都可用，并且可能需要额外的手动配置。

如果您对您的设置的配置细节或它是否支持运行基于 Testcontainers 的测试有进一步的疑问，请通过 [Slack](https://slack.testcontainers.org/) 联系 Testcontainers 团队和 Testcontainers 社区的其他用户。

 {{< grid items=quickstart >}}
