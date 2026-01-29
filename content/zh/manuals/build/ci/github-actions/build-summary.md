---
title: GitHub Actions 构建摘要
linkTitle: 构建摘要 (Build summary)
description: 了解 GitHub Actions 中 Docker 构建的概览
keywords: github actions, gha, build, summary, annotation
---

Docker 的用于构建和推送镜像的 GitHub Actions 会为您的构建生成作业摘要，概述执行情况和使用的材料：

- 显示所使用的 Dockerfile、构建时长和缓存利用率的摘要
- 构建的输入，例如构建参数、标签（tags）、标签（labels）和构建上下文
- 对于使用 [Bake](../../bake/_index.md) 的构建，显示该构建的完整 bake 定义

![GitHub Actions 构建摘要](../images/gha_build_summary.png)

如果您使用以下版本的 [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images) 或 [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake) GitHub Actions，Docker 构建的作业摘要将自动出现：

- `docker/build-push-action@v6`
- `docker/bake-action@v6`

要查看作业摘要，请在作业完成后打开 GitHub 中的作业详情页面。该摘要对失败和成功的构建均可用。如果构建失败，摘要还会显示导致构建失败的错误消息：

![构建摘要错误消息](../images/build_summary_error.png)

## 将构建记录导入 Docker Desktop

{{< summary-bar feature_name="导入构建" >}}

作业摘要包含一个下载该运行的构建记录归档文件的链接。构建记录归档文件是一个 ZIP 文件，包含关于一次构建（如果使用 `docker/bake-action` 构建多个目标，则包含多次构建）的详细信息。您可以将此构建记录归档文件导入 Docker Desktop，它提供了一个强大的图形界面，通过 [Docker Desktop **Builds**（构建）视图](/manuals/desktop/use-desktop/builds.md) 进一步分析构建性能。

将构建记录归档文件导入 Docker Desktop 的步骤：

1. 下载并安装 [Docker Desktop](/get-started/get-docker.md)。

2. 从 GitHub Actions 的作业摘要中下载构建记录归档文件。

3. 打开 Docker Desktop 中的 **Builds** 视图。

4. 选择 **Import build**（导入构建）按钮，然后浏览您下载的 `.zip` 归档作业摘要。或者，在打开导入构建对话框后，将构建记录归档 ZIP 文件拖放到 Docker Desktop 窗口中。

5. 选择 **Import**（导入）以添加构建记录。

几秒钟后，来自 GitHub Actions 运行的构建将出现在 Builds 视图的 **Completed builds**（已完成的构建）选项卡下。要检查构建并查看所有输入、结果、构建步骤和缓存利用率的详细视图，请选择列表中的项目。

## 禁用作业摘要

要禁用作业摘要，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_SUMMARY` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_SUMMARY: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## 禁用构建记录上传

要禁用将构建记录归档文件上传到 GitHub，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_RECORD_UPLOAD` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

在此配置下，仍会生成构建摘要，但不包含下载构建记录归档文件的链接。

## 局限性

目前不支持以下情况的构建摘要：

- 使用 [Docker Build Cloud](/manuals/build-cloud/_index.md) 的构建。对 Docker Build Cloud 的支持计划在未来版本中推出。
- 托管在 GitHub Enterprise 服务器上的仓库。摘要仅能用于托管在 GitHub.com 上的仓库。
