---
description: 使用 CLI 客户端将您的运行时环境与 Docker Scout 集成
keywords: docker scout, integration, image analysis, runtime, workloads, cli, environments
title: 使用 CLI 进行通用环境集成
linkTitle: 通用（CLI）
---

{{% include "scout-early-access.md" %}}

您可以通过在 CI 工作流中运行 Docker Scout CLI 客户端来创建通用环境集成。CLI 客户端以二进制文件形式在 GitHub 上提供，也以容器镜像形式在 Docker Hub 上提供。使用客户端调用 `docker scout environment` 命令将镜像分配到环境。

有关如何使用 `docker scout environment` 命令的更多信息，请参阅 [CLI 参考](/reference/cli/docker/scout/environment.md)。

## 示例

在开始之前，请在您的 CI 系统中设置以下环境变量：

- `DOCKER_SCOUT_HUB_USER`：您的 Docker Hub 用户名
- `DOCKER_SCOUT_HUB_PASSWORD`：您的 Docker Hub 个人访问令牌

确保这些变量对您的项目可访问。

{{< tabs >}}
{{< tab name="Circle CI" >}}

```yaml
version: 2.1

jobs:
  record_environment:
    machine:
      image: ubuntu-2204:current
    image: namespace/repo
    steps:
      - run: |
          if [[ -z "$CIRCLE_TAG" ]]; then
            tag="$CIRCLE_TAG"
            echo "Running tag '$CIRCLE_TAG'"
          else
            tag="$CIRCLE_BRANCH"
            echo "Running on branch '$CI_COMMIT_BRANCH'"
          fi
          echo "tag = $tag"
      - run: docker run -it \
          -e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \
          -e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \
          docker/scout-cli:1.0.2 environment \
          --org "<MY_DOCKER_ORG>" \
          "<ENVIRONMENT>" ${image}:${tag}
```

{{< /tab >}}
{{< tab name="GitLab" >}}

以下示例使用 [Docker executor](https://docs.gitlab.com/runner/executors/docker.html)。

```yaml
variables:
  image: namespace/repo

record_environment:
  image: docker/scout-cli:1.0.2
  script:
    - |
      if [[ -z "$CI_COMMIT_TAG" ]]; then
        tag="latest"
        echo "Running tag '$CI_COMMIT_TAG'"
      else
        tag="$CI_COMMIT_REF_SLUG"
        echo "Running on branch '$CI_COMMIT_BRANCH'"
      fi
      echo "tag = $tag"
    - environment --org <MY_DOCKER_ORG> "PRODUCTION" ${image}:${tag}
```

{{< /tab >}}
{{< tab name="Azure DevOps" >}}

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "namespace/repo"

stages:
  - stage: Docker Scout
    displayName: Docker Scout environment integration
    jobs:
      - job: Record
        displayName: Record environment
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
          - script: docker run -it \
              -e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \
              -e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \
              docker/scout-cli:1.0.2 environment \
              --org "<MY_DOCKER_ORG>" \
              "<ENVIRONMENT>" $(image):$(tag)
```

{{< /tab >}}
{{< tab name="Jenkins" >}}

```groovy
stage('Analyze image') {
    steps {
        // Install Docker Scout
        sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

        // Log into Docker Hub
        sh 'echo $DOCKER_SCOUT_HUB_PASSWORD | docker login -u $DOCKER_SCOUT_HUB_USER --password-stdin'

        // Analyze and fail on critical or high vulnerabilities
        sh 'docker-scout environment --org "<MY_DOCKER_ORG>" "<ENVIRONMENT>" $IMAGE_TAG
    }
}
```

{{< /tab >}}
{{< /tabs >}}
