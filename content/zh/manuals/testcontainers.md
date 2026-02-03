---
title: Testcontainers
description: 了解如何使用 Testcontainers 以您偏好的编程语言以编程方式运行容器。
keywords: docker APIs, docker, testcontainers 文档, testcontainers, testcontainers oss, testcontainers oss 文档, docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: 开源 (Open source)
intro:
- title: 什么是 Testcontainers？
  description: 了解 Testcontainers 的功能及其核心优势
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流
  description: 理解 Testcontainers 的工作流程
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Testcontainers for Go
  description: 一个 Go 语言包，能够轻松地为自动化集成测试/冒烟测试创建并清理基于容器的依赖项。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Testcontainers for Java
  description: 一个支持 JUnit 测试的 Java 库，为任何可以在 Docker 容器中运行的对象提供轻量级、即用即弃的实例。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一套开源库，提供了简单且轻量级的 API，用于通过封装在 Docker 容器中的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于与生产环境相同的服务的测试，而无需使用模拟 (Mocks) 或内存服务。

{{< grid items=intro >}}

## 快速入门

### 支持的语言

Testcontainers 支持大多数热门编程语言，Docker 赞助了以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其他的实现由社区驱动并由独立贡献者维护。

### 前提条件

Testcontainers 需要一个兼容 Docker-API 的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新版本 Docker 以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。
Testcontainers 会自动检测并使用这些 Docker 环境，无需任何额外配置。

也可以将 Testcontainers 配置为在其他 Docker 设置中工作，例如远程 Docker 宿主机或 Docker 替代方案。
然而，这些设置在主开发流程中并未经过积极测试，因此可能无法使用 Testcontainers 的所有特性，并且可能需要额外的手动配置。

如果您对特定设置的配置细节或是否支持运行基于 Testcontainers 的测试有进一步疑问，请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队及 Testcontainers 社区的其他用户。

 {{< grid items=quickstart >}}