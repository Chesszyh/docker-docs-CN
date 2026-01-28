---
description: 了解如何优化和管理您的 Docker Hub 使用量。
keywords: Docker Hub, limit, usage
title: 优化 Docker Hub 使用量的最佳实践
linkTitle: 优化使用量
weight: 40
---

使用以下步骤帮助优化和管理个人和组织的 Docker Hub 使用量：

1. [查看您的 Docker Hub 使用量](https://hub.docker.com/usage)。

2. 使用 Docker Hub 使用数据来识别哪些账户消耗最多数据，确定峰值使用时间，并识别哪些镜像与最多数据使用量相关。此外，寻找使用趋势，例如以下内容：

   - 低效的拉取行为：识别频繁访问的仓库，以评估您是否可以优化缓存实践或整合使用量以减少拉取。
   - 低效的自动化系统：检查哪些自动化工具（如 CI/CD 管道）可能导致较高的拉取率，并配置它们以避免不必要的镜像拉取。

3. 通过以下方式优化镜像拉取：

   - 使用缓存：通过[镜像](/docker-hub/mirror/)或在您的 CI/CD 管道中实施本地镜像缓存以减少冗余拉取。
   - 自动化手动工作流程：通过配置自动化系统仅在镜像有新版本可用时才拉取，避免不必要的拉取。

4. 通过以下方式优化您的存储：

    - 定期审计并[删除整个仓库](../repos/delete.md)中未标记、未使用或过时的镜像。
    - 使用[镜像管理](../repos/manage/hub-images/manage.md)删除仓库中陈旧和过时的镜像。

5. 对于组织，通过执行以下操作来监控和执行组织策略：

   - 定期[查看 Docker Hub 使用量](https://hub.docker.com/usage)以监控使用情况。
   - [强制登录](/security/for-admins/enforce-sign-in/)以确保您可以监控用户的使用量，并且用户可以获得更高的使用限制。
   - 在 Docker 中查找重复的用户账户，并根据需要从组织中删除账户。
