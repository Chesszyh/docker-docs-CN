---
title: 在 CI 中评估策略合规性
description: |
  配置您的持续集成管道，在镜像的策略评估结果较基准变差时使其失败
keywords: scout, 供应链, 策略, ci
---

在持续集成 (CI) 管道中添加策略评估可帮助您检测并防止代码更改导致策略合规性相对于基准变差的情况。

CI 环境中推荐的策略评估方案包括评估本地镜像并将其结果与基准进行比较。如果本地镜像的策略合规性比指定的基准差，则 CI 运行将失败并报错。如果策略合规性有所改善或保持不变，则 CI 运行成功。

这种比较是相对的，这意味着它只关心您的 CI 镜像是否比基准更好或更差。它不是对通过或失败所有策略的绝对检查。通过相对于您定义的基准进行测量，您可以快速了解某项更改对策略合规性是产生积极影响还是消极影响。

## 工作原理

在 CI 中进行策略评估时，您会对在 CI 管道中构建的镜像运行本地策略评估。要运行本地评估，您评估的镜像必须存在于运行 CI 工作流的镜像存储中。首先构建或拉取镜像，然后运行评估。

要运行策略评估并在本地镜像合规性差于比较基准时触发失败，您需要指定作为基准的镜像版本。您可以硬编码一个特定的镜像引用，但更好的解决方案是使用 [环境 (environments)](../integrations/environment/_index.md) 从环境中自动推断镜像版本。以下示例使用环境将 CI 镜像与 `production` 环境中的镜像进行比较。

## 示例

以下关于如何在 CI 中运行策略评估的示例使用了 [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout) 来对 CI 中构建的镜像执行 `compare` 命令。`compare` 命令有一个 `to-env` 输入，它将针对名为 `production` 的环境运行比较。`exit-on` 输入设置为 `policy`，这意味着仅当策略合规性恶化时，比较才会失败。

此示例不假设您使用 Docker Hub 作为容器注册表。因此，此工作流使用了两次 `docker/login-action`：

- 一次用于对您的容器注册表进行身份验证。
- 另一次用于对 Docker 进行身份验证，以便拉取 `production` 镜像的分析结果。

如果您使用 Docker Hub 作为容器注册表，则只需身份验证一次。

> [!NOTE]
>
> 由于 Docker Engine 的限制，目前不支持将多平台镜像或带有证明的镜像加载到镜像存储中。
>
> 为了使策略评估工作，必须将镜像加载到运行器的本地镜像存储中。请确保您构建的是不带证明的单平台镜像，并加载构建结果。否则，策略评估将失败。

另请注意任务的 `pull-requests: write` 权限。Docker Scout GitHub Action 默认会添加一条包含评估结果的拉取请求 (PR) 评论，这需要该权限。有关详情，请参阅 [拉取请求评论](https://github.com/docker/scout-action#pull-request-comments)。

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

以下屏幕截图显示了当 PR 镜像的策略评估结果较基准变差导致检查失败时，GitHub PR 评论的样子。

![GitHub PR 中的策略评估评论](../images/scout-policy-eval-ci.webp)

此示例演示了如何使用 GitHub Actions 在 CI 中运行策略评估。Docker Scout 还支持其他 CI 平台。有关更多信息，请参阅 [Docker Scout CI 集成](../integrations/_index.md#continuous-integration)。
