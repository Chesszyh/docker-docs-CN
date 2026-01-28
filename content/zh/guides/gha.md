---
title: GitHub Actions 与 Docker 简介
linkTitle: GitHub Actions 与 Docker
summary: |
  学习如何使用 GitHub Actions 自动化镜像构建和推送。
params:
  tags: [devops]
  time: 10 minutes
---

本指南介绍如何使用 Docker 和 GitHub Actions 构建 CI 流水线。您将学习如何使用 Docker 官方 GitHub Actions 将应用程序构建为 Docker 镜像并推送到 Docker Hub。在指南结束时，您将拥有一个简单、功能完整的 Docker 构建 GitHub Actions 配置。您可以直接使用它，或根据需要进一步扩展。

## 前提条件

如果您想跟随本指南操作，请确保具备以下条件：

- Docker 账户。
- 熟悉 Dockerfile。

本指南假设您具备 Docker 概念的基础知识，但会提供在 GitHub Actions 工作流中使用 Docker 的说明。

## 获取示例应用

本指南与项目无关，假设您有一个带有 Dockerfile 的应用程序。

如果您需要一个示例项目来跟随操作，可以使用[这个示例应用程序](https://github.com/dvdksn/rpg-name-generator.git)，它包含一个用于构建应用程序容器化版本的 Dockerfile。或者，使用您自己的 GitHub 项目或从模板创建新仓库。

{{% dockerfile.inline %}}

{{ $data := resources.GetRemote "https://raw.githubusercontent.com/dvdksn/rpg-name-generator/refs/heads/main/Dockerfile" }}

```dockerfile {collapse=true}
{{ $data.Content }}
```

{{% /dockerfile.inline %}}

## 配置您的 GitHub 仓库

本指南中的工作流将您构建的镜像推送到 Docker Hub。为此，您必须在 GitHub Actions 工作流中使用 Docker 凭据（用户名和访问令牌）进行身份认证。

有关如何创建 Docker 访问令牌的说明，请参阅[创建和管理访问令牌](/manuals/security/for-developers/access-tokens.md)。

准备好 Docker 凭据后，将凭据添加到 GitHub 仓库，以便在 GitHub Actions 中使用：

1. 打开仓库的 **Settings**。
2. 在 **Security** 下，转到 **Secrets and variables > Actions**。
3. 在 **Secrets** 下，创建一个名为 `DOCKER_PASSWORD` 的新仓库密钥，包含您的 Docker 访问令牌。
4. 接下来，在 **Variables** 下，创建一个包含您 Docker Hub 用户名的 `DOCKER_USERNAME` 仓库变量。

## 设置 GitHub Actions 工作流

GitHub Actions 工作流定义了一系列自动化任务的步骤，例如响应提交或 pull request 等触发器来构建和推送 Docker 镜像。在本指南中，工作流专注于自动化 Docker 构建和测试，确保容器化应用程序在发布前正常工作。

在仓库的 `.github/workflows/` 目录中创建一个名为 `docker-ci.yml` 的文件。从基本工作流配置开始：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
```

此配置在推送到 main 分支和 pull request 时运行工作流。通过包含这两个触发器，您可以确保在合并之前镜像能够正确构建 pull request。

## 提取标签和注解的元数据

对于工作流的第一步，使用 `docker/metadata-action` 为镜像生成元数据。此 action 提取关于 Git 仓库的信息，例如分支名称和提交 SHA，并生成镜像元数据（如标签和注解）。

将以下 YAML 添加到工作流文件：

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image
```

这些步骤准备元数据以在构建和推送过程中标记和注解镜像。

- **Checkout** 步骤克隆 Git 仓库。
- **Extract Docker image metadata** 步骤提取 Git 元数据并为 Docker 构建生成镜像标签和注解。

## 向注册表进行身份认证

在构建镜像之前，向注册表进行身份认证以确保您可以将构建的镜像推送到注册表。

要向 Docker Hub 进行身份认证，请将以下步骤添加到工作流：

```yaml
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

此步骤使用[在仓库设置中配置](#配置您的-github-仓库)的 Docker 凭据。

## 构建并推送镜像

最后，构建最终生产镜像并将其推送到注册表。以下配置构建镜像并直接推送到注册表。

```yaml
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

在此配置中：

- `push: ${{ github.event_name != 'pull_request' }}` 确保仅在事件不是 pull request 时推送镜像。这样，工作流会为 pull request 构建和测试镜像，但仅为 main 分支的提交推送镜像。
- `tags` 和 `annotations` 使用 metadata action 的输出自动将一致的标签和[注解](/manuals/build/metadata/annotations.md)应用于镜像。

## 证明

SBOM（软件物料清单）和来源证明可提高安全性和可追溯性，确保您的镜像符合现代软件供应链要求。

通过少量额外配置，您可以配置 `docker/build-push-action` 在构建时为镜像生成软件物料清单（SBOM）和来源证明。

要生成此附加元数据，您需要对工作流进行两处更改：

- 在构建步骤之前，添加一个使用 `docker/setup-buildx-action` 的步骤。此 action 为 Docker 构建客户端配置默认客户端不支持的额外功能。
- 然后，更新 **Build and push Docker image** 步骤以同时启用 SBOM 和来源证明。

以下是更新后的代码片段：

```yaml
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

有关证明的更多详细信息，请参阅[文档](/manuals/build/metadata/attestations/_index.md)。

## 结论

根据前面部分概述的所有步骤，以下是完整的工作流配置：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

此工作流实现了使用 GitHub Actions 构建和推送 Docker 镜像的最佳实践。此配置可以直接使用，也可以根据项目需求扩展额外功能，例如[多平台](/manuals/build/building/multi-platform.md)。

### 进一步阅读

- 在 [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) 部分了解更多高级配置和示例。
- 对于更复杂的构建设置，您可能需要考虑 [Bake](/manuals/build/bake/_index.md)。（另请参阅[掌握 Buildx Bake 指南](/guides/bake/index.md)。）
- 了解 Docker 的托管构建服务，专为更快的多平台构建设计，请参阅 [Docker Build Cloud](/guides/docker-build-cloud/_index.md)。
