---
description: 如何在持续集成流水线中设置 Docker Scout
keywords: scanning, vulnerabilities, Hub, supply chain, security, ci, continuous integration,
  github actions, gitlab
title: 在持续集成中使用 Docker Scout
linkTitle: 持续集成
aliases:
- /scout/ci/
---

您可以在构建 Docker 镜像时，使用 GitHub Action 或 Docker Scout CLI 插件在持续集成流水线中分析它们。

可用的集成：

- [GitHub Actions](gha.md)
- [GitLab](gitlab.md)
- [Microsoft Azure DevOps Pipelines](azure.md)
- [Circle CI](circle-ci.md)
- [Jenkins](jenkins.md)

您还可以在 CI/CD 流水线中添加运行时集成，这样可以在部署镜像时将其分配到环境，例如 `production` 或 `staging`。有关更多信息，请参阅[环境监控](../environment/_index.md)。
