---
description: 如何将 Docker Scout 与 GitLab CI 集成
keywords: 供应链, 安全, ci, 持续集成, gitlab
title: 将 Docker Scout 与 GitLab CI/CD 集成
linkTitle: GitLab CI/CD
---

以下示例在包含 Docker 镜像定义和内容的仓库中的 GitLab CI 中运行。管道由提交触发，构建镜像。如果提交是对默认分支的，它会使用 Docker Scout 获取 CVE 报告。如果提交是对不同分支的，它会使用 Docker Scout 将新版本与当前发布的版本进行比较。

## 步骤

首先，设置工作流的其余部分。有很多内容不是针对 Docker Scout 的，但却是创建待比较镜像所必需的。

将以下内容添加到仓库根目录下的 `.gitlab-ci.yml` 文件中。

```yaml
docker-build:
  image: docker:latest
  stage: build
  services:
    - docker:dind
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

    # 安装 curl 和 Docker Scout CLI
    - |
      apk add --update curl
      curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- 
      apk del curl 
      rm -rf /var/cache/apk/*
    # 运行 Docker Scout CLI 需要登录 Docker Hub
    - echo "$DOCKER_HUB_PAT" | docker login -u "$DOCKER_HUB_USER" --password-stdin
```

这将工作流设置为使用 Docker-in-Docker 模式构建 Docker 镜像，即在容器内运行 Docker。

然后，它会下载 `curl` 和 Docker Scout CLI 插件，并使用仓库设置中定义的环境变量登录 Docker 注册表。

将以下内容添加到 YAML 文件中：

```yaml
script:
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      tag=""
      echo "Running on default branch '$CI_DEFAULT_BRANCH': tag = 'latest'"
    else
      tag=":$CI_COMMIT_REF_SLUG"
      echo "Running on branch '$CI_COMMIT_BRANCH': tag = $tag"
    fi
  - docker build --pull -t "$CI_REGISTRY_IMAGE${tag}" .
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      # 获取已构建镜像的 CVE 报告，并在检测到危急 (critical) 或高危 (high) CVE 时使管道失败
      docker scout cves "$CI_REGISTRY_IMAGE${tag}" --exit-code --only-severity critical,high    
    else
      # 将分支中的镜像与默认分支中的最新镜像进行比较，如果检测到新的危急或高危 CVE，则使管道失败
      docker scout compare "$CI_REGISTRY_IMAGE${tag}" --to "$CI_REGISTRY_IMAGE:latest" --exit-code --only-severity critical,high --ignore-unchanged
    fi

  - docker push "$CI_REGISTRY_IMAGE${tag}"
```

这将创建前面提到的流程。如果提交是对默认分支的，Docker Scout 会生成 CVE 报告。如果提交是对不同分支的，Docker Scout 会将新版本与当前发布的版本进行比较。它仅显示危急或高危漏洞，并忽略自上次分析以来未发生变化的漏洞。

将以下内容添加到 YAML 文件中：

```yaml
rules:
  - if: $CI_COMMIT_BRANCH
    exists:
      - Dockerfile
```

这些最后几行确保仅在提交包含 Dockerfile 且提交是对 CI 分支的情况下运行管道。

## 视频演示

以下是使用 GitLab 设置工作流过程的视频演示。

<iframe class="border-0 w-full aspect-video mb-8" allow="fullscreen" src="https://www.loom.com/embed/451336c4508c42189532108fc37b2560?sid=f912524b-276d-417d-b44a-c2d39719aa1a"></iframe>
