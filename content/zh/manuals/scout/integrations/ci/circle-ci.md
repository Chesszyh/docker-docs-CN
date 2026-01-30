---
description: 如何将 Docker Scout 与 Circle CI 集成
keywords: 供应链, 安全, ci, 持续集成, circle ci
title: 将 Docker Scout 与 Circle CI 集成
linkTitle: Circle CI
---

以下示例在 CircleCI 中被触发时运行。触发后，它会检出 "docker/scout-demo-service:latest" 镜像和标签，然后使用 Docker Scout 创建 CVE 报告。

将以下内容添加到 _.circleci/config.yml_ 文件中。

首先，设置工作流的其余部分。将以下内容添加到 YAML 文件中：

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/base:stable
    environment:
      IMAGE_TAG: docker/scout-demo-service:latest
```

这定义了工作流使用的容器镜像以及该镜像的环境变量。

将以下内容添加到 YAML 文件中，以定义工作流的步骤：

```yaml
steps:
  # 检出仓库文件
  - checkout
  
  # 设置一个独立的 Docker 环境来运行 `docker` 命令
  - setup_remote_docker:
      version: 20.10.24

  # 安装 Docker Scout 并登录 Docker Hub
  - run:
      name: Install Docker Scout
      command: |
        env
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /home/circleci/bin
        echo $DOCKER_HUB_PAT | docker login -u $DOCKER_HUB_USER --password-stdin

  # 构建 Docker 镜像
  - run:
      name: Build Docker image
      command: docker build -t $IMAGE_TAG .
  
  # 运行 Docker Scout          
  - run:
      name: Scan image for CVEs
      command: |
        docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high
```

这会检出仓库文件，然后设置一个独立的 Docker 环境来运行命令。

它安装 Docker Scout，登录 Docker Hub，构建 Docker 镜像，然后运行 Docker Scout 以生成 CVE 报告。它仅显示危急 (critical) 或高危 (high) 漏洞。

最后，为工作流和工作流的任务添加名称：

```yaml
workflows:
  build-docker-image:
    jobs:
      - build
```
