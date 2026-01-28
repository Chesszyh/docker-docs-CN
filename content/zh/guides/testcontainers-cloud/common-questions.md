---
title: 常见挑战和问题
description: 探索与 Docker Testcontainers Cloud 相关的常见挑战和问题。
weight: 40
---

<!-- vale Docker.HeadingLength = NO -->

### Testcontainers Cloud 与开源 Testcontainers 框架有什么不同？

开源 Testcontainers 是一个库，提供轻量级 API，用于使用封装在 Docker 容器中的真实服务来引导本地开发和测试依赖项。而 Testcontainers Cloud 为这些容器提供云端运行时。这减少了本地环境的资源压力，并提供了更好的可扩展性，特别是在 CI/CD 工作流中，使组织内的 Testcontainers 体验保持一致。

### Testcontainers Cloud 可以运行哪些类型的容器？

Testcontainers Cloud 支持您通常使用 Testcontainers 框架运行的任何容器，包括数据库（PostgreSQL、MySQL、MongoDB）、消息代理（Kafka、RabbitMQ）以及集成测试所需的其他服务。

### 使用 Testcontainers Cloud 需要修改现有的测试代码吗？

不需要，您无需修改现有的测试代码。Testcontainers Cloud 与开源 Testcontainers 框架无缝集成。一旦完成云端配置，它会自动在云中管理容器，无需更改代码。

### 如何将 Testcontainers Cloud 集成到我的项目中？

要集成 Testcontainers Cloud，您需要安装 Testcontainers Desktop 应用程序，并在菜单中选择"使用 Testcontainers Cloud 运行"选项。在 CI 环境中，您需要添加一个下载 Testcontainers Cloud 代理的工作流步骤。除了在本地通过 Testcontainers Desktop 应用程序启用 Cloud 运行时或在 CI 中安装 Testcontainers Cloud 代理外，无需更改代码。

### Testcontainers Cloud 可以在 CI/CD 流水线中使用吗？

是的，Testcontainers Cloud 专为在 CI/CD 流水线中高效运行而设计。它通过将使用 Testcontainers 库启动的容器卸载到云端，帮助减少构建时间和资源瓶颈，使其成为持续测试环境的理想选择。

### 使用 Testcontainers Cloud 有哪些好处？

主要好处包括：减少本地机器和 CI 服务器的资源使用、可扩展性（可以同时运行更多容器而不会降低性能）、一致的测试环境、集中监控，以及简化 CI 配置并消除运行 Docker-in-Docker 或特权守护进程的安全顾虑。

### Testcontainers Cloud 支持所有编程语言吗？

Testcontainers Cloud 支持任何与开源 Testcontainers 库兼容的语言，包括 Java、Python、Node.js、Go 等。只要您的项目使用 Testcontainers，就可以卸载到 Testcontainers Cloud。

### Testcontainers Cloud 如何处理容器清理？

Testcontainers 库会自动处理容器生命周期管理，而 Testcontainers Cloud 管理分配的云工作节点的生命周期。这意味着容器由 Testcontainers 库启动、监控并在测试完成后清理，而运行这些容器的工作节点将在约 35 分钟空闲期后由 Testcontainers Cloud 自动删除。这种方法使开发者无需手动管理容器和相关的云资源。

### Testcontainers Cloud 有免费层级或定价模式吗？

Testcontainers Cloud 的定价详情可在[定价页面](https://testcontainers.com/cloud/pricing/)找到。
