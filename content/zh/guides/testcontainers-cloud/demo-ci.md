---
title: 在 CI 流水线中配置 Testcontainers Cloud
description: 使用 Testcontainers Cloud 与 GitHub Workflows 在 CI 流水线中自动化测试。
weight: 30
---

{{< youtube-embed "NlZY9aumKJU" >}}

此演示展示了如何将 Testcontainers Cloud 无缝集成到使用 GitHub Workflows 的持续集成（CI）流水线中，为运行容器化集成测试提供强大的解决方案，而不会使本地或 CI 运行器资源过载。通过利用 GitHub Actions，开发者可以自动化在云中启动和管理用于测试的容器的过程，确保更快、更可靠的测试执行。只需几个配置步骤，包括设置 Testcontainers Cloud 身份验证并将其添加到您的工作流中，您就可以将容器编排卸载到云端。这种方法提高了流水线的可扩展性，确保测试之间的一致性，并简化了资源管理，使其成为现代容器化开发工作流的理想解决方案。

- 了解如何设置 GitHub Actions 工作流以自动化项目的构建和测试。
- 学习如何在 GitHub Actions 中配置 Testcontainers Cloud，将容器化测试卸载到云端，提高效率和资源管理。
- 探索 Testcontainers Cloud 如何与 GitHub 工作流集成，运行需要容器化服务（如数据库和消息代理）的集成测试。
