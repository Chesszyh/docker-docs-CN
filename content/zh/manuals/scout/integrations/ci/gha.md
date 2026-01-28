---
description: 如何将 Docker Scout 与 GitHub Actions 集成
keywords: supply chain, security, ci, continuous integration, github actions
title: 将 Docker Scout 与 GitHub Actions 集成
linkTitle: GitHub Actions
---

以下示例展示了如何使用 GitHub Actions 设置 Docker Scout 工作流。当拉取请求触发时，该 Action 会构建镜像并使用 Docker Scout 将新版本与在生产环境中运行的镜像版本进行比较。

此工作流使用 [docker/scout-action](https://github.com/docker/scout-action) GitHub Action 来运行 `docker scout compare` 命令，以可视化拉取请求的镜像与您在生产环境中运行的镜像之间的差异。

## 前提条件

- 此示例假设您有一个现有的镜像仓库（在 Docker Hub 或其他镜像仓库中），并且已启用 Docker Scout。
- 此示例使用[环境](../environment/_index.md)，将拉取请求中构建的镜像与名为 `production` 的环境中相同镜像的不同版本进行比较。

## 步骤

首先，设置 GitHub Action 工作流来构建镜像。这里没有特定于 Docker Scout 的内容，但您需要构建一个镜像才能进行比较。

将以下内容添加到 GitHub Actions YAML 文件：

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
  # Hostname of your registry
  REGISTRY: docker.io
  # Image repository, without hostname and tag
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      # Authenticate to the container registry
      - name: Authenticate to registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      # Extract metadata (tags, labels) for Docker
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

      # Build and push Docker image with Buildx
      # (don't push on PR, load instead)
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

这创建了以下工作流步骤：

1. 设置 Docker buildx。
2. 向镜像仓库进行身份验证。
3. 从 Git 引用和 GitHub 事件中提取元数据。
4. 构建 Docker 镜像并将其推送到镜像仓库。

> [!NOTE]
>
> 此 CI 工作流对您的镜像运行本地分析和评估。要在本地评估镜像，您必须确保镜像已加载到运行器的本地镜像存储中。
>
> 如果您将镜像推送到镜像仓库，或者构建的镜像无法加载到运行器的本地镜像存储，此比较将不起作用。例如，多平台镜像或带有 SBOM 或来源证明的镜像无法加载到本地镜像存储。

完成此设置后，您可以添加以下步骤来运行镜像比较：

```yaml
      # You can skip this step if Docker Hub is your registry
      # and you already authenticated before
      - name: Authenticate to Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # Compare the image built in the pull request with the one in production
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

compare 命令分析镜像并评估策略合规性，并将结果与 `production` 环境中相应镜像进行交叉引用。此示例仅包含严重和高危漏洞，并排除两个镜像中都存在的漏洞，仅显示已更改的内容。

GitHub Action 默认将比较结果输出到拉取请求评论中。

![在 GitHub Action 中显示 Docker Scout 输出结果的截图](../../images/gha-output.webp)

展开 **Policies** 部分可查看两个镜像之间策略合规性的差异。请注意，虽然此示例中的新镜像尚未完全合规，但输出显示与基准相比，新镜像的情况有所改善。

![GHA 策略评估输出](../../images/gha-policy-eval.webp)
