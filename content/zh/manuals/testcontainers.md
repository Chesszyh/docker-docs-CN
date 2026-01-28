---
title: Testcontainers
description: 学习如何使用 Testcontainers 在您首选的编程语言中以编程方式运行容器。
keywords: docker APIs, docker, testcontainers documentation, testcontainers, testcontainers oss, testcontainers oss documentation,
  docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: Open source
intro:
- title: 什么是 Testcontainers？
  description: 了解 Testcontainers 的功能及其主要优势
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流程
  description: 理解 Testcontainers 的工作流程
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Testcontainers for Go
  description: 一个 Go 包，可以简单地为自动化集成/冒烟测试创建和清理基于容器的依赖项。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Testcontainers for Java
  description: 一个支持 JUnit 测试的 Java 库，提供轻量级、一次性的 Docker 容器实例。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一组开源库，提供简单轻量的 API，用于使用封装在 Docker 容器中的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于与生产环境相同服务的测试，无需模拟或内存服务。

{{< grid items=intro >}}

## 快速入门

### 支持的语言

Testcontainers 为最流行的语言提供支持，Docker 赞助以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余的由社区驱动，由独立贡献者维护。

### 先决条件

Testcontainers 需要与 Docker API 兼容的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新 Docker 版本以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。
Testcontainers 会自动检测并使用这些 Docker 环境，无需任何额外配置。

可以配置 Testcontainers 以支持其他 Docker 设置，例如远程 Docker 主机或 Docker 替代方案。
但是，这些不在主要开发工作流程中进行积极测试，因此可能不是所有 Testcontainers 功能都可用，
可能需要额外的手动配置。

如果您对您的设置的配置详情或是否支持运行基于 Testcontainers 的测试有进一步的问题，
请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队和 Testcontainers 社区的其他用户。

 {{< grid items=quickstart >}}
