---
title: Azure Pipelines 与 Docker 简介
linkTitle: Azure Pipelines 与 Docker
summary: |
  学习如何使用 Azure Pipelines 自动化 Docker 镜像的构建和推送。
params:
  tags: [devops]
  time: 10 minutes
---

> 本指南为社区贡献内容。Docker 在此感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 的宝贵贡献。

## 前提条件

开始之前，请确保满足以下要求：

- 拥有一个 [Docker Hub 账户](https://hub.docker.com) 并生成访问令牌。
- 拥有一个活跃的 [Azure DevOps 项目](https://dev.azure.com/)，并连接了 [Git 仓库](https://learn.microsoft.com/en-us/azure/devops/repos/git/?view=azure-devops)。
- 项目根目录或适当的构建上下文中包含有效的 [`Dockerfile`](https://docs.docker.com/engine/reference/builder/)。

## 概述

本指南将引导您使用 [Azure Pipelines](https://azure.microsoft.com/en-us/products/devops/pipelines) 构建和推送 Docker 镜像，为容器化应用程序实现精简且安全的 CI 工作流程。您将学习如何：

- 安全配置 Docker 身份认证。
- 设置自动化流水线以构建和推送镜像。

## 配置 Azure DevOps 与 Docker Hub 协同工作

### 步骤 1：配置 Docker Hub 服务连接

要使用 Azure Pipelines 安全地与 Docker Hub 进行身份认证：

1. 在 Azure DevOps 项目中，导航至 **Project Settings > Service Connections**。
2. 选择 **New service connection > Docker Registry**。
3. 选择 **Docker Hub** 并提供您的 Docker Hub 凭据或访问令牌。
4. 为服务连接指定一个易于识别的名称，例如 `my-docker-registry`。
5. 仅向需要访问的特定流水线授予权限，以提高安全性并遵循最小权限原则。

> [!IMPORTANT]
>
> 除非绝对必要，否则请避免选择向所有流水线授予访问权限的选项。始终应用最小权限原则。

### 步骤 2：创建流水线

将以下 `azure-pipelines.yml` 文件添加到仓库的根目录：

```yaml
# 在提交到 main 分支时触发流水线
trigger:
  - main

# 在针对 main 分支的 pull request 时触发流水线
pr:
  - main

# 定义在整个流水线中复用的变量
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'

stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
    jobs:
      - job: DockerJob
        displayName: Build and Push
        pool:
          vmImage: ubuntu-latest
          demands:
            - docker
        steps:
          - checkout: self
            displayName: Checkout Code

          - task: Docker@2
            displayName: Docker Login
            inputs:
              command: login
              containerRegistry: 'my-docker-registry'  # 服务连接名称

          - task: Docker@2
            displayName: Build Docker Image
            inputs:
              command: build
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)
              dockerfile: './Dockerfile'
              arguments: |
                --sbom=true
                --attest type=provenance
                --cache-from $(imageName):latest
            env:
              DOCKER_BUILDKIT: 1

          - task: Docker@2
            displayName: Push Docker Image
            condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
            inputs:
              command: push
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)

          # 可选：为自托管代理注销
          - script: docker logout
            displayName: Docker Logout (Self-hosted only)
            condition: ne(variables['Agent.OS'], 'Windows_NT')
```

## 此流水线的功能

此流水线自动化了 main 分支的 Docker 镜像构建和部署过程。它通过缓存、标记和条件清理等最佳实践确保安全高效的工作流程。具体功能如下：

- 在针对 `main` 分支的提交和 pull request 时触发。
- 使用 Azure DevOps 服务连接安全地与 Docker Hub 进行身份认证。
- 使用 Docker BuildKit 构建和标记 Docker 镜像以利用缓存。
- 将 buildId 和 latest 标签同时推送到 Docker Hub。
- 如果在自托管的 Linux 代理上运行，则退出 Docker 登录。


## 流水线工作原理

### 步骤 1：定义流水线触发器

```yaml
trigger:
  - main

pr:
  - main
```

此流水线在以下情况下自动触发：
- 推送到 `main` 分支的提交
- 针对 `main` 分支的 pull request

> [!TIP]
> 了解更多：[在 Azure Pipelines 中定义流水线触发器](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops)

### 步骤 2：定义通用变量

```yaml
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'
```

这些变量确保在整个流水线步骤中保持一致的命名、版本控制和复用：

- `imageName`：Docker Hub 上的镜像路径
- `buildTag`：每次流水线运行的唯一标签
- `latestTag`：指向最新镜像的稳定别名

> [!IMPORTANT]
>
> 变量 `dockerUsername` 不会自动设置。
> 请在 Azure DevOps 流水线变量中安全地设置它：
>   1. 前往 **Pipelines > Edit > Variables**
>   2. 添加 `dockerUsername` 并填入您的 Docker Hub 用户名
>
> 了解更多：[在 Azure Pipelines 中定义和使用变量](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch)

### 步骤 3：定义流水线阶段和作业

```yaml
stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
```

此阶段仅在源分支为 `main` 时执行。

> [!TIP]
>
> 了解更多：[Azure Pipelines 中的阶段条件](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/stages?view=azure-devops&tabs=yaml)


### 步骤 4：作业配置

```yaml
jobs:
  - job: DockerJob
  displayName: Build and Push
  pool:
    vmImage: ubuntu-latest
    demands:
      - docker
```

此作业使用 Microsoft 托管代理提供的具有 Docker 支持的最新 Ubuntu 虚拟机镜像。如有必要，可以将其替换为自托管代理的自定义池。

> [!TIP]
>
> 了解更多：[在流水线中指定池](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/pools-queues?view=azure-devops&tabs=yaml%2Cbrowser)

#### 步骤 4.1：检出代码

```yaml
steps:
  - checkout: self
    displayName: Checkout Code
```

此步骤将仓库代码拉取到构建代理中，以便流水线可以访问 Dockerfile 和应用程序文件。

> [!TIP]
>
> 了解更多：[checkout 步骤文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/steps-checkout?view=azure-pipelines)

#### 步骤 4.2：向 Docker Hub 进行身份认证

```yaml
- task: Docker@2
  displayName: Docker Login
  inputs:
    command: login
    containerRegistry: 'my-docker-registry'  # 替换为您的服务连接名称
```

使用预配置的 Azure DevOps Docker 注册表服务连接进行安全身份认证，而不直接暴露凭据。

> [!TIP]
>
> 了解更多：[为 Docker Hub 使用服务连接](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops#docker-hub-or-others)

#### 步骤 4.3：构建 Docker 镜像

```yaml
 - task: Docker@2
    displayName: Build Docker Image
    inputs:
      command: build
      repository: $(imageName)
      tags: |
          $(buildTag)
          $(latestTag)
      dockerfile: './Dockerfile'
      arguments: |
          --sbom=true
          --attest type=provenance
          --cache-from $(imageName):latest
    env:
      DOCKER_BUILDKIT: 1
```

此命令构建镜像时包含：

- 两个标签：一个使用唯一的 Build ID，另一个为 latest
- 启用 Docker BuildKit 以加快构建速度和高效的层缓存
- 从最近推送的 latest 镜像拉取缓存
- 软件物料清单（SBOM）以实现供应链透明度
- 来源证明以验证镜像的构建方式和位置

> [!TIP]
>
> 了解更多：
> - [Azure Pipelines 的 Docker 任务](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2?view=azure-pipelines&tabs=yaml)
> - [Docker SBOM 证明](/manuals/build/metadata/attestations/slsa-provenance.md)

#### 步骤 4.4：推送 Docker 镜像

```yaml
- task: Docker@2
  displayName: Push Docker Image
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  inputs:
      command: push
      repository: $(imageName)
      tags: |
        $(buildTag)
        $(latestTag)
```

通过应用此条件，流水线在每次运行时都会构建 Docker 镜像以确保及早发现问题，但仅在更改合并到 main 分支时才将镜像推送到注册表——保持 Docker Hub 的整洁和专注

此步骤将两个标签上传到 Docker Hub：
- `$(buildTag)` 确保每次运行的可追溯性。
- `latest` 用于引用最新镜像。

#### 步骤 4.5  退出 Docker 登录（自托管代理）

```yaml
- script: docker logout
  displayName: Docker Logout (Self-hosted only)
  condition: ne(variables['Agent.OS'], 'Windows_NT')
```

在基于 Linux 的自托管代理上，在流水线结束时执行 docker logout，以主动清理凭据并增强安全态势。

## 总结

通过此 Azure Pipelines CI 设置，您可以获得：

- 使用内置服务连接进行安全的 Docker 身份认证。
- 由代码更改触发的自动化镜像构建和标记。
- 利用 Docker BuildKit 缓存实现高效构建。
- 在持久代理上通过注销进行安全清理。
- 使用 SBOM 和证明构建符合现代软件供应链要求的镜像

## 了解更多

- [Azure Pipelines 文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops)：配置和管理 Azure DevOps 中 CI/CD 流水线的综合指南。
- [Azure Pipelines 的 Docker 任务](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/build/docker)：在 Azure Pipelines 中使用 Docker 任务构建和推送镜像的详细参考。
- [Docker Buildx Bake](/manuals/build/bake/_index.md)：探索 Docker 用于复杂、多阶段和多平台构建设置的高级构建工具。另请参阅 [掌握 Buildx Bake 指南](/guides/bake/index.md) 获取实用示例和最佳实践。
- [Docker Build Cloud](/guides/docker-build-cloud/_index.md)：了解 Docker 的托管构建服务，用于在云中进行更快、可扩展的多平台镜像构建。
