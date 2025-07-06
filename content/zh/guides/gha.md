---
title: Docker 与 GitHub Actions 简介
linkTitle: GitHub Actions 和 Docker
summary: |
  了解如何使用 GitHub Actions 自动构建和推送镜像。
params:
  tags: [devops]
  time: 10 分钟
---

本指南介绍了如何使用 Docker 和
GitHub Actions 构建 CI 管道。您将学习如何使用 Docker 的官方 GitHub Actions
将您的应用程序构建为 Docker 镜像并将其推送到 Docker Hub。在本
指南结束时，您将拥有一个用于
Docker 构建的简单、实用的 GitHub Actions 配置。您可以按原样使用它，也可以根据您的需要进一步扩展它
。

## 先决条件

如果您想学习本指南，请确保您具备以下条件：

- 一个 Docker 帐户。
- 熟悉 Dockerfile。

本指南假定您对 Docker 概念有基本的了解，但提供了
在 GitHub Actions 工作流中使用 Docker 的说明。

## 获取示例应用程序

本指南与项目无关，并假定您有一个带有
Dockerfile 的应用程序。

如果您需要一个示例项目来学习，您可以使用[此示例
应用程序](https://github.com/dvdksn/rpg-name-generator.git)，其中包含
一个用于构建应用程序容器化版本的 Dockerfile。或者，
使用您自己的 GitHub 项目或从模板创建一个新存储库。

{{% dockerfile.inline %}}

{{ $data := resources.GetRemote "https://raw.githubusercontent.com/dvdksn/rpg-name-generator/refs/heads/main/Dockerfile" }}

```dockerfile {collapse=true}
{{ $data.Content }}
```

{{% /dockerfile.inline %}}

## 配置您的 GitHub 存储库

本指南中的工作流会将您构建的镜像推送到 Docker Hub。为此，
您必须在 GitHub Actions 工作流中
使用您的 Docker 凭据（用户名和访问令牌）进行身份验证。

有关如何创建 Docker 访问令牌的说明，请参阅
[创建和管理访问令牌](/manuals/security/for-developers/access-tokens.md)。

准备好 Docker 凭据后，将凭据添加到您的 GitHub
存储库，以便您可以在 GitHub Actions 中使用它们：

1. 打开您的存储库的 **设置**。
2. 在 **安全** 下，转到 **机密和变量 > 操作**。
3. 在 **机密** 下，创建一个名为 `DOCKER_PASSWORD` 的新存储库机密，
   其中包含您的 Docker 访问令牌。
4. 接下来，在 **变量** 下，创建一个 `DOCKER_USERNAME` 存储库变量，
   其中包含您的 Docker Hub 用户名。

## 设置您的 GitHub Actions 工作流

GitHub Actions 工作流定义了一系列步骤来自动化任务，例如
构建和推送 Docker 镜像，以响应诸如提交或
拉取请求之类的触发器。在本指南中，工作流侧重于自动化 Docker 构建
和测试，确保您的容器化应用程序在
发布之前正常工作。

在您的存储库的 `.github/workflows/` 目录中创建一个名为 `docker-ci.yml` 的文件
。从基本工作流配置开始：

```yaml
name: 构建和推送 Docker 镜像

on:
  push:
    branches:
      - main
  pull_request:
```

此配置在推送到主分支和
拉取请求时运行工作流。通过包含这两个触发器，您可以确保在
合并拉取请求之前，镜像可以正确构建。

## 提取标签和注释的元数据

对于工作流的第一步，使用 `docker/metadata-action` 为
您的镜像生成元数据。此操作会提取有关您的
Git 存储库的信息，例如分支名称和提交 SHA，并生成
镜像元数据，例如标签和注释。

将以下 YAML 添加到您的工作流文件中：

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 签出
        uses: actions/checkout@v4
      - name: 提取 Docker 镜像元数据
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image
```

这些步骤准备元数据以在构建
和推送过程中标记和注释您的镜像。

- **签出** 步骤克隆 Git 存储库。
- **提取 Docker 镜像元数据** 步骤提取 Git 元数据并
  为 Docker 构建生成镜像标签和注释。

## 向您的注册表进行身份验证

在构建镜像之前，请向您的注册表进行身份验证，以确保您
可以将构建的镜像推送到注册表。

要使用 Docker Hub 进行身份验证，请将以下步骤添加到您的工作流中：

```yaml
      - name: 登录到 Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

此步骤使用[在存储库设置中配置的 Docker 凭据](#configure-your-github-repository)。

## 构建和推送镜像

最后，构建最终的生产镜像并将其推送到您的注册表。以下
配置构建镜像并将其直接推送到注册表。

```yaml
      - name: 构建和推送 Docker 镜像
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

在此配置中：

- `push: ${{ github.event_name != 'pull_request' }}` 确保仅在
  事件不是拉取请求时才推送镜像。这样，工作流
  会为拉取请求构建和测试镜像，但仅为提交到
  ���分支的镜像推送镜像。
- `tags` 和 `annotations` 使用元数据操作的输出来自动
  将一致的标签和[注释](/manuals/build/metadata/annotations.md)应用于
  镜像。

## 证明

SBOM（软件物料清单）和出处证明可提高安全性和
可追溯性，确保您的镜像满足现代软件供应链
要求。

通过少量额外的配置，您可以配置
`docker/build-push-action` 以在构建时为镜像生成软件物料清单 (SBOM) 和
出处证明。

要生成此附加元数据，您需要对您的
工作流进行两项更改：

- 在构建步骤之前，添加一个使用 `docker/setup-buildx-action` 的步骤。
  此操作会使用默认客户端不支持的附加功能
  配置您的 Docker 构建客户端。
- 然后，更新 **构建和推送 Docker 镜像** 步骤以同时启用 SBOM 和
  出处证明。

这是更新后的代码段：

```yaml
      - name: 设置 Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: 构建和推送 Docker 镜像
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

有关证明的更多详细��息，请参阅
[文档](/manuals/build/metadata/attestations/_index.md)。

## 结论

通过上一节中概述的所有步骤，以下是完整的工作流
配置：

```yaml
name: 构建和推送 Docker 镜像

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 签出
        uses: actions/checkout@v4

      - name: 提取 Docker 镜像元数据
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image

      - name: 登录到 Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: 设置 Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: 构建和推送 Docker 镜像
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

此工作流实现了使用
GitHub Actions 构建和推送 Docker 镜像的最佳实践。此配置可以按原样使用，也可以根据您的项目需求
使用其他功能进行扩展，例如
[多平台](/manuals/build/building/multi-platform.md)。

### 延伸阅读

- 在 [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) 部分了解有关高级配置和示例的更多信息。
- 对于更复杂的构建设置，您可能需要考虑 [Bake](/manuals/build/bake/_index.md)。（另请参阅 [Mastering Buildx Bake 指南](/guides/bake/index.md)。）
- 了解 Docker 的托管构建服务，该服务专为更快、多平台的构建而设计，请参阅 [Docker Build Cloud](/guides/docker-build-cloud/_index.md)。
