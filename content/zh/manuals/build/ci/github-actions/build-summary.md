---
title: GitHub Actions 构建摘要
linkTitle: Build summary
description: 通过 GitHub Actions 获取 Docker 构建的概览
keywords: github actions, gha, build, summary, annotation
---

Docker 用于构建和推送镜像的 GitHub Actions 会为您的构建生成作业摘要，概述执行过程和使用的材料：

- 显示使用的 Dockerfile、构建持续时间和缓存利用率的摘要
- 构建的输入，如构建参数、标签、标注和构建上下文
- 对于使用 [Bake](../../bake/_index.md) 的构建，会显示完整的 bake 定义

![GitHub Actions 构建摘要](../images/gha_build_summary.png)

如果您使用以下版本的 [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images) 或 [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake) GitHub Actions，Docker 构建的作业摘要会自动出现：

- `docker/build-push-action@v6`
- `docker/bake-action@v6`

要查看作业摘要，请在作业完成后在 GitHub 中打开作业的详情页面。摘要对于失败和成功的构建都可用。对于失败的构建，摘要还会显示导致构建失败的错误消息：

![构建摘要错误消息](../images/build_summary_error.png)

## 将构建记录导入 Docker Desktop

{{< summary-bar feature_name="Import builds" >}}

作业摘要包含一个用于下载该运行的构建记录存档的链接。构建记录存档是一个 ZIP 文件，包含关于构建（如果使用 `docker/bake-action` 构建多个目标，则包含多个构建）的详细信息。您可以将此构建记录存档导入 Docker Desktop，这为您提供了一个强大的图形界面，可通过 [Docker Desktop **Builds** 视图](/manuals/desktop/use-desktop/builds.md)进一步分析构建的性能。

要将构建记录存档导入 Docker Desktop：

1. 下载并安装 [Docker Desktop](/get-started/get-docker.md)。

2. 从 GitHub Actions 中的作业摘要下载构建记录存档。

3. 在 Docker Desktop 中打开 **Builds** 视图。

4. 选择 **Import build** 按钮，然后浏览您下载的 `.zip` 存档作业摘要。或者，您可以在打开导入构建对话框后将构建记录存档 ZIP 文件拖放到 Docker Desktop 窗口中。

5. 选择 **Import** 来添加构建记录。

几秒钟后，GitHub Actions 运行中的构建将出现在 Builds 视图的 **Completed builds** 选项卡下。要检查构建并查看所有输入、结果、构建步骤和缓存利用率的详细视图，请选择列表中的项目。

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

要禁用将构建记录存档上传到 GitHub，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_RECORD_UPLOAD` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

使用此配置，构建摘要仍会生成，但不包含下载构建记录存档的链接。

## 限制

以下情况目前不支持构建摘要：

- 使用 [Docker Build Cloud](/manuals/build-cloud/_index.md) 的构建。计划在未来版本中支持 Docker Build Cloud。
- 托管在 GitHub Enterprise Servers 上的仓库。摘要只能在托管于 GitHub.com 上的仓库中查看。
