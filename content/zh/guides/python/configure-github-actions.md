---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 40
keywords: ci/cd, github actions, python, flask
description: 学习如何使用 GitHub Actions 为您的 Python 应用程序配置 CI/CD。
aliases:
  - /language/python/configure-ci-cd/
  - /guides/language/python/configure-ci-cd/
  - /guides/python/configure-ci-cd/
---

## 前提条件

完成本指南之前的所有章节，从[容器化 Python 应用程序](containerize.md)开始。您必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户才能完成本节内容。

如果您还没有为项目创建 [GitHub 仓库](https://github.com/new)，现在是时候创建了。创建仓库后，别忘了[添加远程仓库](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)，并确保可以将代码[推送到 GitHub](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push)。

1. 在项目的 GitHub 仓库中，打开 **Settings**，进入 **Secrets and variables** > **Actions**。

2. 在 **Variables** 标签页下，创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**，值为您的 Docker ID。

3. 为 Docker Hub 创建一个新的[个人访问令牌 (PAT)](/manuals/security/for-developers/access-tokens.md#create-an-access-token)。您可以将此令牌命名为 `docker-tutorial`。确保访问权限包含读取和写入权限。

4. 在您的 GitHub 仓库中添加 PAT 作为 **Repository secret**，命名为
   `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是内置于 GitHub 的 CI/CD（持续集成和持续部署）自动化工具。它允许您定义自定义工作流程，在特定事件发生时（例如推送代码、创建拉取请求等）自动构建、测试和部署代码。工作流程是基于 YAML 的自动化脚本，定义了触发时要执行的一系列步骤。工作流程存储在仓库的 `.github/workflows/` 目录中。

在本节中，您将学习如何设置和使用 GitHub Actions 来构建 Docker 镜像并将其推送到 Docker Hub。您将完成以下步骤：

1. 定义 GitHub Actions 工作流程。
2. 运行工作流程。

## 1. 定义 GitHub Actions 工作流程

您可以通过在仓库的 `.github/workflows/` 目录中创建 YAML 文件来创建 GitHub Actions 工作流程。您可以使用您喜欢的文本编辑器或 GitHub 网页界面来完成此操作。以下步骤展示如何使用 GitHub 网页界面创建工作流程文件。

如果您偏好使用 GitHub 网页界面，请按照以下步骤操作：

1. 在 GitHub 上进入您的仓库，然后选择 **Actions** 标签页。

2. 选择 **set up a workflow yourself**。

   这将带您进入一个页面，用于在仓库中创建新的 GitHub Actions 工作流程文件。默认情况下，文件创建在 `.github/workflows/main.yml`，让我们将其重命名为 `build.yml`。

如果您偏好使用文本编辑器，请在仓库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

将以下内容添加到文件中：

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run pyright
        run: pyright

  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

每个 GitHub Actions 工作流程包含一个或多个作业（job）。每个作业由多个步骤组成。每个步骤可以运行一组命令或使用已有的 [actions](https://github.com/marketplace?type=actions)。上述 action 包含三个步骤：

1. [**Login to Docker Hub**](https://github.com/docker/login-action)：此 action 使用您之前创建的 Docker ID 和个人访问令牌 (PAT) 登录 Docker Hub。

2. [**Set up Docker Buildx**](https://github.com/docker/setup-buildx-action)：此 action 设置 Docker [Buildx](https://github.com/docker/buildx)，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**Build and push**](https://github.com/docker/build-push-action)：此 action 构建 Docker 镜像并将其推送到 Docker Hub。`tags` 参数指定镜像名称和标签。本示例中使用 `latest` 标签。

## 2. 运行工作流程

让我们提交更改并推送到 `main` 分支。在上述工作流程中，触发器设置为 `main` 分支上的 `push` 事件。这意味着每次您将更改推送到 `main` 分支时，工作流程都会运行。您可以在[这里](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)找到更多关于工作流程触发器的信息。

进入 GitHub 仓库的 **Actions** 标签页。它会显示工作流程。选择工作流程可以查看所有步骤的详细分解。

当工作流程完成后，进入您在 [Docker Hub 上的仓库](https://hub.docker.com/repositories)。如果您在列表中看到新的仓库，说明 GitHub Actions 工作流程已成功将镜像推送到 Docker Hub。

## 总结

在本节中，您学习了如何为 Python 应用程序设置 GitHub Actions 工作流程，包括：

- 运行 pre-commit hooks 进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 构建并推送 Docker 镜像

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流程语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

在下一节中，您将学习如何使用 Kubernetes 进行本地开发。
