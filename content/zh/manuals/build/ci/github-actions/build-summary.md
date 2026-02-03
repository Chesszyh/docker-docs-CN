---
title: GitHub Actions 构建摘要
linkTitle: 构建摘要
description: 使用 GitHub Actions 获取 Docker 构建概览
keywords: github actions, gha, build, summary, annotation, 构建摘要, 摘要, 注解
---

用于构建和推送镜像的 Docker GitHub Actions 会为您的构建生成一份任务摘要，概述执行情况及所使用的物料：

- 一份展示所使用的 Dockerfile、构建时长及缓存利用率的摘要
- 构建的输入项，如构建参数 (build arguments)、标签 (tags/labels) 和构建上下文
- 对于使用 [Bake](../../bake/_index.md) 的构建，还会显示完整的 Bake 定义

![GitHub Actions 构建摘要](../images/gha_build_summary.png)

如果您使用以下版本的 [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images) 或 [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake) GitHub Actions，构建任务摘要将自动出现：

- `docker/build-push-action@v6`
- `docker/bake-action@v6`

要查看任务摘要，请在任务完成后打开 GitHub 中的任务详情页面。摘要对失败和成功的构建均可用。对于失败的构建，摘要还会显示导致构建失败的错误消息：

![构建摘要错误消息](../images/build_summary_error.png)

## 将构建记录导入 Docker Desktop

{{< summary-bar feature_name="导入构建" >}}

任务摘要包含一个下载该运行任务的构建记录存档链接。该构建记录存档是一个 ZIP 文件，包含了关于单次或多次构建（如果您使用 `docker/bake-action` 构建多个目标）的详情。您可以将此存档导入 Docker Desktop，通过 [Docker Desktop **Builds** 视图](/manuals/desktop/use-desktop/builds.md) 提供的强大图形界面进一步分析构建性能。

要将构建记录存档导入 Docker Desktop：

1. 下载并安装 [Docker Desktop](/get-started/get-docker.md)。

2. 从 GitHub Actions 任务摘要中下载构建记录存档。

3. 打开 Docker Desktop 中的 **Builds** 视图。

4. 点击 **Import build** 按钮，然后选择您下载的 `.zip` 格式任务摘要。或者，在打开导入构建对话框后，直接将 ZIP 文件拖放到 Docker Desktop 窗口中。

5. 选择 **Import** 添加构建记录。

几秒钟后，来自 GitHub Actions 运行任务的构建记录将出现在 Builds 视图的 **Completed builds** 选项卡下。选择列表中的条目，即可查看所有输入项、结果、构建步骤以及缓存利用率的详细视图。

## 禁用任务摘要

要禁用任务摘要，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_SUMMARY` 环境变量：

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

要禁用向 GitHub 上传构建记录存档，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_RECORD_UPLOAD` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

通过此配置，构建摘要仍会生成，但其中不会包含下载构建记录存档的链接。

## 限制

构建摘要目前不支持以下场景：

- 使用 [Docker Build Cloud](/manuals/build-cloud/_index.md) 的构建。对 Docker Build Cloud 的支持计划在未来的版本中推出。
- 托管在 GitHub Enterprise Server 上的存储库。目前仅支持托管在 GitHub.com 上的存储库查看摘要。