---
description: 如何将 Docker Scout 与 GitHub Actions 集成
keywords: 供应链, 安全, ci, 持续集成, github actions
title: 将 Docker Scout 与 GitHub Actions 集成
linkTitle: GitHub Actions
---

以下示例展示了如何使用 GitHub Actions 设置 Docker Scout 工作流。该 Action 由拉取请求 (PR) 触发，构建镜像并使用 Docker Scout 将新版本与生产环境中运行的镜像版本进行比较。

此工作流使用 [docker/scout-action](https://github.com/docker/scout-action) GitHub Action 来运行 `docker scout compare` 命令，以可视化 PR 的镜像与您在生产环境中运行的镜像相比的情况。

## 前提条件

- 此示例假设您已有一个现有的镜像仓库 (在 Docker Hub 或其他注册表中)，且已启用 Docker Scout。
- 此示例利用了 [环境 (environments)](../environment/_index.md)，将 PR 中构建的镜像与名为 `production` 的环境中的同一镜像的不同版本进行比较。

## 步骤

首先，设置 GitHub Action 工作流来构建镜像。这部分不是 Docker Scout 特有的，但您需要构建一个镜像以便进行比较。

将以下内容添加到 GitHub Actions YAML 文件中：

```yaml
name: Docker

on:
  push:
    tags: ["*"]
    branches:
      - "main"
  pull_request:
    branches: ["**"]

env:
  # 注册表的主机名
  REGISTRY: docker.io
  # 镜像仓库，不带主机名和标签
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      # 对容器注册表进行身份验证
      - name: Authenticate to registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}
      
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      # 为 Docker 提取元数据 (标签、标签)
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          labels: |
            org.opencontainers.image.revision=${{ env.SHA }}
          tags: |
            type=edge,branch=$repo.default_branch
            type=semver,pattern=v{{version}}
            type=sha,prefix=,suffix=,format=short

      # 使用 Buildx 构建并推送 Docker 镜像
      # (在 PR 时不推送，而是加载)
      - name: Build and push Docker image
        id: build-and-push
        uses: docker/build-push-action@v6
        with:
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

这将创建工作流步骤以：

1. 设置 Docker buildx。
2. 对注册表进行身份验证。
3. 从 Git 引用和 GitHub 事件中提取元数据。
4. 构建 Docker 镜像并将其推送到注册表。

> [!NOTE]
>
> 此 CI 工作流运行对镜像的本地分析和评估。要在本地评估镜像，必须确保镜像已加载到运行器的本地镜像存储中。
>
> 如果您将镜像推送到注册表，或者构建了无法加载到运行器本地镜像存储的镜像，则此比较将无法工作。例如，多平台镜像或带有 SBOM 或来源证明的镜像无法加载到本地镜像存储。

完成这些设置后，您可以添加以下步骤来运行镜像比较：

```yaml
      # 如果 Docker Hub 是您的注册表且之前已通过身份验证，可以跳过此步骤
      - name: Authenticate to Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # 将 PR 中构建的镜像与生产环境中的镜像进行比较
      - name: Docker Scout
        id: docker-scout
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          ignore-unchanged: true
          only-severities: critical,high
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

`compare` 命令分析镜像并评估策略合规性，并将结果与 `production` 环境中的相应镜像进行交叉引用。此示例仅包含危急 (critical) 和高危 (high) 漏洞，并排除了两个镜像中都存在的漏洞，仅显示发生更改的内容。

默认情况下，GitHub Action 会在 PR 评论中输出比较结果。

![GitHub Action 中 Docker Scout 输出结果截图](../../images/gha-output.webp)

展开 **Policies** 部分以查看两个镜像之间策略合规性的差异。请注意，虽然本示例中的新镜像并未完全合规，但输出显示新镜像的情况较基准有所改善。

![GHA 策略评估输出](../../images/gha-policy-eval.webp)
