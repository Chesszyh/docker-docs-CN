---
description: 如何将 Docker Scout 与 Circle CI 集成
keywords: supply chain, security, ci, continuous integration, circle ci
title: 将 Docker Scout 与 Circle CI 集成
linkTitle: Circle CI
---

以下示例在 CircleCI 中触发时运行。触发时，它会签出 "docker/scout-demo-service:latest" 镜像和标签，然后使用 Docker Scout 创建 CVE 报告。

将以下内容添加到 _.circleci/config.yml_ 文件。

首先，设置工作流的其余部分。将以下内容添加到 YAML 文件：

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/base:stable
    environment:
      IMAGE_TAG: docker/scout-demo-service:latest
```

这定义了工作流使用的容器镜像和镜像的环境变量。

将以下内容添加到 YAML 文件以定义工作流的步骤：

```yaml
steps:
  # Checkout the repository files
  - checkout

  # Set up a separate Docker environment to run `docker` commands in
  - setup_remote_docker:
      version: 20.10.24

  # Install Docker Scout and login to Docker Hub
  - run:
      name: Install Docker Scout
      command: |
        env
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /home/circleci/bin
        echo $DOCKER_HUB_PAT | docker login -u $DOCKER_HUB_USER --password-stdin

  # Build the Docker image
  - run:
      name: Build Docker image
      command: docker build -t $IMAGE_TAG .

  # Run Docker Scout
  - run:
      name: Scan image for CVEs
      command: |
        docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high
```

这会签出仓库文件，然后设置一个单独的 Docker 环境来运行命令。

它安装 Docker Scout，登录到 Docker Hub，构建 Docker 镜像，然后运行 Docker Scout 生成 CVE 报告。它仅显示严重或高危漏洞。

最后，添加工作流的名称和工作流的作业：

```yaml
workflows:
  build-docker-image:
    jobs:
      - build
```
