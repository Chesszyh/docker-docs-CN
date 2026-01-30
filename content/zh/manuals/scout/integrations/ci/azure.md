---
description: 如何将 Docker Scout 与 Microsoft Azure DevOps Pipelines 集成
keywords: 供应链, 安全, ci, 持续集成, azure, devops
title: 将 Docker Scout 与 Microsoft Azure DevOps Pipelines 集成
linkTitle: Azure DevOps Pipelines
---

以下示例在连接到 Azure DevOps 的仓库中运行，该仓库包含 Docker 镜像的定义和内容。管道由对 main 分支的提交触发，构建镜像并使用 Docker Scout 创建 CVE 报告。

首先，设置工作流的其余部分并设置所有管道步骤可用的变量。将以下内容添加到 _azure-pipelines.yml_ 文件中：

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "vonwig/nodejs-service"
```

这将工作流设置为应用程序使用特定的容器镜像，并使用构建 ID 为每个新镜像构建打标签。

将以下内容添加到 YAML 文件中：

```yaml
stages:
  - stage: Build
    displayName: Build image
    jobs:
      - job: Build
        displayName: Build
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
            displayName: Build an image
            inputs:
              command: build
              dockerfile: "$(Build.SourcesDirectory)/Dockerfile"
              repository: $(image)
              tags: |
                $(tag)
          - task: CmdLine@2
            displayName: Find CVEs on image
            inputs:
              script: |
                # 安装 Docker Scout CLI
                curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
                # 运行 Docker Scout CLI 需要登录 Docker Hub
                echo $(DOCKER_HUB_PAT) | docker login -u $(DOCKER_HUB_USER) --password-stdin
                # 获取已构建镜像的 CVE 报告，并在检测到危急 (critical) 或高危 (high) CVE 时使管道失败
                docker scout cves $(image):$(tag) --exit-code --only-severity critical,high
```

这将创建前面提到的流程。它使用检出的 Dockerfile 构建镜像并打标签，下载 Docker Scout CLI，然后针对新标签运行 `cves` 命令以生成 CVE 报告。它仅显示危急或高危漏洞。
