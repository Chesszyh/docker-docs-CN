---
description: 自动构建的工作原理
keywords: docker hub, automated builds
title: 自动构建
weight: 90
aliases:
- /docker-hub/builds/how-builds-work/
---

{{< summary-bar feature_name="Automated builds" >}}

Docker Hub 可以从外部仓库的源代码自动构建镜像，并自动将构建的镜像推送到您的 Docker 仓库。

![自动构建仪表板](images/index-dashboard.png)

当您设置自动构建（automated builds，也称为 autobuilds）时，您需要创建一个分支和标签列表，指定要构建为 Docker 镜像的内容。当您向源代码分支（例如 GitHub 中的分支）推送代码时，如果该分支对应列表中的某个镜像标签，推送操作会使用 webhook 触发新的构建，从而生成一个 Docker 镜像。构建完成的镜像随后会被推送到 Docker Hub。

> [!NOTE]
>
> 您仍然可以使用 `docker push` 将预构建的镜像推送到已配置自动构建的仓库。

如果您配置了自动测试，这些测试会在构建之后、推送到镜像仓库之前运行。您可以使用这些测试来创建持续集成工作流，使测试失败的构建不会将构建的镜像推送到仓库。自动测试本身不会将镜像推送到镜像仓库。[了解自动镜像测试](automated-testing.md)。

根据您的[订阅计划](https://www.docker.com/pricing)，您可能获得并发构建功能，这意味着可以同时运行 `N` 个自动构建。`N` 的值根据您的订阅计划配置。一旦有 `N+1` 个构建正在运行，任何额外的构建都会进入队列，稍后执行。

队列中待处理构建的最大数量为 30 个，Docker Hub 会丢弃超出的请求。Pro 订阅的并发构建数量为 5 个，Team 和 Business 订阅的并发构建数量为 15 个。
自动构建可以处理最大 10 GB 的镜像。
