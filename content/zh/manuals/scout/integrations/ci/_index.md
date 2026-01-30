---
description: 如何在持续集成管道中设置 Docker Scout
keywords: 扫描, 漏洞, Hub, 供应链, 安全, ci, 持续集成, github actions, gitlab
title: 在持续集成中使用 Docker Scout
linkTitle: 持续集成
aliases:
- /scout/ci/
---

您可以在构建 Docker 镜像时，通过使用 GitHub action 或 Docker Scout CLI 插件在持续集成管道中对其进行分析。

提供的集成：

- [GitHub Actions](gha.md)
- [GitLab](gitlab.md)
- [Microsoft Azure DevOps Pipelines](azure.md)
- [Circle CI](circle-ci.md)
- [Jenkins](jenkins.md)

您还可以在 CI/CD 管道中添加运行时集成，这允许您在部署镜像时将其分配给环境 (如 `production` 或 `staging`)。有关更多信息，请参阅 [环境监控](../environment/_index.md)。
