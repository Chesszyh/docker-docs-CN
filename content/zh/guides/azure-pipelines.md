---
title: Docker 与 Azure Pipelines 简介
linkTitle: Azure Pipelines 和 Docker
summary: |
  了解如何使用 Azure Pipelines 自动构建和推送 Docker 镜像。
params:
  tags: [devops]
  time: 10 分钟
---

> 本指南由社区贡献。Docker 感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 的宝贵贡献。

## 先决条件

在开始之前，请确保您满足以下要求：

- 一个带有生成访问令牌的 [Docker Hub 帐户](https://hub.docker.com)。
- 一个带有连接的 [Git 存储库](https://learn.microsoft.com/en-us/azure/devops/repos/git/?view=azure-devops) 的活动 [Azure DevOps 项目](https://dev.azure.com/)。
- 一个在其根目录或适当的构建上下文中包含有效 [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) 的项目。

## 概述

本指南将引导您使用 [Azure Pipelines](https://azure.microsoft.com/en-us/products/devops/pipelines) 构建和推送 Docker 镜像，从而为容器化应用程序启用简化的安全 CI 工作流。您将学习如何：

- 安全地配置 Docker 身份验证。
- 设置���动化管道以构建和推送镜像。

## 设置 Azure DevOps 以使用 Docker Hub

### 步骤 1：配置 Docker Hub 服务连接

要使用 Azure Pipelines 安全地向 Docker Hub 进行身份验证：

1. 在您的 Azure DevOps 项目中，导航到 **项目设置 > 服务连接**。
2. 选择 **新建服务连接 > Docker 注册表**。
3. 选择 **Docker Hub** 并提供您的 Docker Hub 凭据或访问令牌。
4. 为服务连接指定一个可识别的名称，例如 `my-docker-registry`。
5. 仅向需要它的特定管道授予访问权限，以提高安全性和最低权限。

> [!IMPORTANT]
>
> 除非绝对必要，否则不要选择授予所有管道访问权限的选项。始终应用最低权限原则。

### 步骤 2：创建您的管道

将以下 `azure-pipelines.yml` 文件添加到您的存储库的根目录：

```yaml
# 在提交到主分支时触发管道
trigger:
  - main

# 在针对主分支的拉取请求上触发管道
pr:
  - main

# 定义变量以在整个管道中重用
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'

stages:
  - stage: BuildAndPush
    displayName: 构建和推送 Docker 镜像
    jobs:
      - job: DockerJob
        displayName: 构建和推送
        pool:
          vmImage: ubuntu-latest
          demands:
            - docker
        steps:
          - checkout: self
            displayName: 签出代码

          - task: Docker@2
            displayName: Docker 登录
            inputs:
              command: login
              containerRegistry: 'my-docker-registry'  # 服务连接名称

          - task: Docker@2
            displayName: 构建 Docker 镜像
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
            displayName: 推送 Docker 镜像
            condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
            inputs:
              command: push
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)

          # 可选：为自托管代理注销
          - script: docker logout
            displayName: Docker 注销（仅限自托管）
            condition: ne(variables['Agent.OS'], 'Windows_NT')
```

## 此管道的作用

此管道可自动执行主分支的 Docker 镜像构建和部署过程。它通过缓存、标记和条件清理等最佳实践确保了安全高效的工作流。它的作用如下：

- 在提交和针对 `main` 分支的拉取请求上触发。
- 使用 Azure DevOps 服务连接安全地向 Docker Hub 进行身份验证。
- 使用 Docker BuildKit 构建和标记 Docker 镜像以进行缓存。
- 将 buildId 和 latest 标签都推送到 Docker Hub。
- 如果在自托管的 Linux 代理上运行，则从 Docker 注销。


## 管道如何工作

### 步骤 1：定义管道触发器

```yaml
trigger:
  - main

pr:
  - main
```

此管道在以下情况下自动触发：
- 推送到 `main` 分支的提交
- 针对 `main` 主分支的拉取请求

> [!TIP]
> 了解更多：[在 Azure Pipelines 中定义管道触发器](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops)

### 步骤 2：定义通用变量

```yaml
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'
```

这些变量可确保在整个管道步骤中保持一致的命名、版本控制和重用：

- `imageName`：您在 Docker Hub 上的镜像路径
- `buildTag`：每个管道运行的唯一标记
- `latestTag`：您最新镜像的稳定别名

> [!IMPORTANT]
>
> 变量 `dockerUsername` 不会自动设置。
> 在您的 Azure DevOps 管道变量中安全地设置它：
>   1. 转到 **管道 > 编辑 > 变量**
>   2. 添加 `dockerUsername` 并使用您的 Docker Hub 用户名
>
> 了解更多：[在 Azure Pipelines 中定义和使用变量](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch)
 
### 步骤 3：定义管道阶段和作业

```yaml
stages:
  - stage: BuildAndPush
    displayName: 构建和推送 Docker 镜像
```

此阶段仅在源分支为 `main` 时执行。

> [!TIP]
>
> 了解更多：[Azure Pipelines 中的阶段条件](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/stages?view=azure-devops&tabs=yaml)


### 步骤 4：作业配置

```yaml
jobs:
  - job: DockerJob
  displayName: 构建和推送
  pool:
    vmImage: ubuntu-latest
    demands:
      - docker
```

此作业利用 Microsoft 托管代理提供的具有 Docker 支持的最新 Ubuntu VM 镜像。如有必要，可以将其替换为自托管代理的自定义池。

> [!TIP]
>
> 了解更多：[在您的管道中指定池](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/pools-queues?view=azure-devops&tabs=yaml%2Cbrowser)

#### 步骤 4.1：签出代码

```yaml
steps:
  - checkout: self
    displayName: 签出代码
```

此步骤将您的存储库代码拉入构建代理，以便管道可以访问 Dockerfile 和应用程序文件。

> [!TIP]
>
> 了解更多：[checkout 步骤文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/steps-checkout?view=azure-pipelines)

#### 步骤 4.2：向 Docker Hub 进行身份验证

```yaml
- task: Docker@2
  displayName: Docker 登录
  inputs:
    command: login
    containerRegistry: 'my-docker-registry'  # 替换为您的服务连接名称
```

使用预配置的 Azure DevOps Docker 注册表服务连接进行安全身份验证，而无需直接公开凭据。

> [!TIP]
>
> 了解更多：[使用服务连接到 Docker Hub](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops#docker-hub-or-others)

#### 步骤 4.3：构建 Docker 镜像

```yaml
 - task: Docker@2
    displayName: 构建 Docker 镜像
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

这将使用以下内容构建镜像：

- 两个标签：一个带有唯一的构建 ID，一个作为最新标签
- 启用 Docker BuildKit 以加快构建速度并有效利用层缓存
- 从最近推送的最新镜像中拉取缓存
- 软件物料清单 (SBOM) 以实现供应链透明度
- 出处证明以验证镜像的构建方式和位置

> [!TIP]
>
> 了解更多：
> - [适用于 Azure Pipelines 的 Docker 任务](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2?view=azure-pipelines&tabs=yaml)
> - [Docker SBOM 证明](/manuals/build/metadata/attestations/slsa-provenance.md)

#### 步骤 4.4：推送 Docker 镜像

```yaml
- task: Docker@2
  displayName: 推送 Docker 镜像
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  inputs:
      command: push
      repository: $(imageName)
      tags: |
        $(buildTag)
        $(latestTag)
```

通过应用此条件，管道会在每次运行时构建 Docker 镜像以确保及早发现问题，但仅在将更改合并到主分支时才将镜像推送到注册表——保持您的 Docker Hub 清洁和专注

这将两个标签都上传到 Docker Hub：
- `$(buildTag)` 确保每次运行的可追溯性。
- `latest` 用于最新的镜像引用。

#### 步骤 4.5  从 Docker 注销（自托管代理）

```yaml
- script: docker logout
  displayName: Docker 注销（仅限自托管）
  condition: ne(variables['Agent.OS'], 'Windows_NT')
```

在基于 Linux 的自托管代理上，在管道结束时执行 docker logout，以主动清理凭据并增强安全状况。

## 总结

通过此 Azure Pipelines CI 设置，您可以获得：

- 使用内置服务连接进行安全的 Docker 身份验证。
- 由代码更改触发的自动化镜像构建和标记。
- 利用 Docker BuildKit 缓存进行高效构建。
- 在持久代理上通过注销进行安全清理。
- 构建符合现代软件供应链要求的镜像，并带有 SBOM 和证明

## 了解更多

- [Azure Pipelines 文档](https://learn.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops)：配置和管理 Azure DevOps 中 CI/CD 管道的综合指南。
- [适用于 Azure Pipelines 的 Docker 任务](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/build/docker)：在 Azure Pipelines 中使用 Docker 任务构建和推送镜像的详细参考。
- [Docker Buildx Bake](/manuals/build/bake/_index.md)：探索 Docker 的高级构建工具，用于复杂、多阶段和多平台的构建设置。另请参阅 [Mastering Buildx Bake Guide](/guides/bake/index.md) 以���取实际示例和最佳实践。
- [Docker Build Cloud](/guides/docker-build-cloud/_index.md)：了解 Docker 的托管构建服务，可在云中实现更快、可扩展和多平台的镜像构建。
