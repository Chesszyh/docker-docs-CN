---
title: 在 CI 中评估策略合规性
description: |
  配置您的持续集成流水线，当镜像的策略评估相对于基线变差时失败
keywords: scout, supply chain, policy, ci
---

将策略评估添加到您的持续集成流水线中，可帮助您检测和防止代码更改导致策略合规性相对于基线变差的情况。

在 CI 环境中进行策略评估的推荐策略是评估本地镜像并将结果与基线进行比较。如果本地镜像的策略合规性比指定的基线差，CI 运行将以错误失败。如果策略合规性更好或保持不变，CI 运行将成功。

这种比较是相对的，意味着它只关注您的 CI 镜像相对于基线是更好还是更差。这不是通过或失败所有策略的绝对检查。通过相对于您定义的基线进行测量，您可以快速看到更改对策略合规性的影响是正面还是负面。

## 工作原理

当您在 CI 中进行策略评估时，您在 CI 流水线中构建的镜像上运行本地策略评估。要运行本地评估，您评估的镜像必须存在于运行 CI 工作流的镜像存储中。构建或拉取镜像，然后运行评估。

要运行策略评估并在本地镜像的合规性比比较基线差时触发失败，您需要指定要用作基线的镜像版本。您可以硬编码特定的镜像引用，但更好的解决方案是使用[环境](../integrations/environment/_index.md)从环境中自动推断镜像版本。以下示例使用环境将 CI 镜像与 `production` 环境中的镜像进行比较。

## 示例

以下关于如何在 CI 中运行策略评估的示例使用 [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout) 对在 CI 中构建的镜像执行 `compare` 命令。compare 命令有一个 `to-env` 输入，它将针对名为 `production` 的环境运行比较。`exit-on` 输入设置为 `policy`，意味着只有在策略合规性恶化时比较才会失败。

此示例不假设您使用 Docker Hub 作为容器镜像仓库。因此，此工作流使用 `docker/login-action` 两次：

- 一次用于向您的容器镜像仓库进行身份验证。
- 再一次用于向 Docker 进行身份验证以拉取您 `production` 镜像的分析结果。

如果您使用 Docker Hub 作为容器镜像仓库，您只需要进行一次身份验证。

> [!NOTE]
>
> 由于 Docker Engine 的限制，不支持将多平台镜像或带有证明的镜像加载到镜像存储中。
>
> 要使策略评估正常工作，您必须将镜像加载到运行器的本地镜像存储中。确保您正在构建没有证明的单平台镜像，并且正在加载构建结果。否则，策略评估将失败。

还要注意作业的 `pull-requests: write` 权限。Docker Scout GitHub Action 默认会添加带有评估结果的拉取请求评论，这需要此权限。有关详细信息，请参阅 [Pull Request Comments](https://github.com/docker/scout-action#pull-request-comments)。

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
  REGISTRY: docker.io
  IMAGE_NAME: <IMAGE_NAME>
  DOCKER_ORG: <ORG>

jobs:
  build:
    permissions:
      pull-requests: write

    runs-on: ubuntu-latest
    steps:
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build image
        id: build-and-push
        uses: docker/build-push-action@v4
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}

      - name: Authenticate with Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Compare
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          platform: "linux/amd64"
          ignore-unchanged: true
          only-severities: critical,high
          organization: ${{ env.DOCKER_ORG }}
          exit-on: policy
```

以下截图展示了当策略评估检查失败时 GitHub PR 评论的样子，因为 PR 镜像的策略相对于基线变差了。

![GitHub PR 中的策略评估评论](../images/scout-policy-eval-ci.webp)

此示例演示了如何使用 GitHub Actions 在 CI 中运行策略评估。Docker Scout 还支持其他 CI 平台。有关更多信息，请参阅 [Docker Scout CI 集成](../integrations/_index.md#continuous-integration)。
