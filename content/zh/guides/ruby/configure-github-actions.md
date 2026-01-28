---
title: 使用 GitHub Actions 自动化你的构建
linkTitle: 使用 GitHub Actions 自动化你的构建
weight: 20
keywords: ci/cd, github actions, ruby, flask
description: 了解如何为你的 Ruby on Rails 应用程序配置使用 GitHub Actions 的 CI/CD。
aliases:
  - /language/ruby/configure-ci-cd/
  - /guides/language/ruby/configure-ci-cd/
  - /guides/ruby/configure-ci-cd/
---

## 先决条件

完成本指南的所有前几节，从 [容器化 Ruby on Rails 应用程序](containerize.md) 开始。你必须拥有 [GitHub](https://github.com/signup) 帐户和 [Docker](https://hub.docker.com/signup) 帐户才能完成本节。

如果你还没有为你的项目创建 [GitHub 存储库](https://github.com/new)，现在是时候创建了。创建存储库后，不要忘记 [添加远程](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) 并确保你可以提交并 [推送你的代码](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) 到 GitHub。

1. 在你的项目 GitHub 存储库中，打开 **Settings**（设置），然后转到 **Secrets and variables**（密钥和变量） > **Actions**。

2. 在 **Variables**（变量）选项卡下，创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**（存储库变量），并将你的 Docker ID 作为值。

3. 为 Docker Hub 创建一个新的 [个人访问令牌 (PAT)](/manuals/security/for-developers/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保存储权限包括读取和写入。

4. 将 PAT 作为 **Repository secret**（存储库密钥）添加到你的 GitHub 存储库中，名称为 `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是内置于 GitHub 中的 CI/CD（持续集成和持续部署）自动化工具。它允许你定义自定义工作流，以便在发生特定事件（例如，推送代码、创建拉取请求等）时构建、测试和部署你的代码。工作流是一个基于 YAML 的自动化脚本，它定义了触发时要执行的一系列步骤。工作流存储在存储库的 `.github/workflows/` 目录下。

在本节中，你将学习如何设置和使用 GitHub Actions 来构建你的 Docker 镜像并将其推送到 Docker Hub。你将完成以下步骤：

1. 定义 GitHub Actions 工作流。
2. 运行工作流。

## 1. 定义 GitHub Actions 工作流

你可以通过在存储库的 `.github/workflows/` 目录中创建一个 YAML 文件来创建 GitHub Actions 工作流。为此，请使用你喜欢的文本编辑器或 GitHub Web 界面。以下步骤展示了如何使用 GitHub Web 界面创建工作流文件。

如果你更喜欢使用 GitHub Web 界面，请按照以下步骤操作：

1. 转到 GitHub 上的存储库，然后选择 **Actions** 选项卡。

2. 选择 **set up a workflow yourself**（自己设置工作流）。

   这将带你到一个页面，用于在你的存储库中创建一个新的 GitHub Actions 工作流文件。默认情况下，该文件是在 `.github/workflows/main.yml` 下创建的，我们将名称更改为 `build.yml`。

如果你更喜欢使用文本编辑器，请在存储库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

将以下内容添加到文件中：

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
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

每个 GitHub Actions 工作流都包含一个或多个作业。每个作业由步骤组成。每个步骤可以运行一组命令或使用已经 [存在的操作](https://github.com/marketplace?type=actions)。上面的操作有三个步骤：

1. [**Login to Docker Hub**](https://github.com/docker/login-action)：此操作使用你之前创建的 Docker ID 和个人访问令牌 (PAT) 登录到 Docker Hub。

2. [**Set up Docker Buildx**](https://github.com/docker/setup-buildx-action)：此操作设置 Docker [Buildx](https://github.com/docker/buildx)，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**Build and push**](https://github.com/docker/build-push-action)：此操作构建 Docker 镜像并将其推送到 Docker Hub。`tags` 参数指定镜像名称和标签。本例中使用 `latest` 标签。

## 2. 运行工作流

让我们提交更改，并将它们推送到 `main` 分支。在上面的工作流中，触发器设置为 `main` 分支上的 `push` 事件。这意味着每次你向 `main` 分支推送更改时，工作流都会运行。你可以 [在此处](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) 找到有关工作流触发器的更多信息。

转到 GitHub 存储库的 **Actions** 选项卡。它显示工作流。选择工作流会显示所有步骤的细分。

工作流完成后，转到你的 [Docker Hub 上的存储库](https://hub.docker.com/repositories)。如果你在该列表中看到新的存储库，则意味着 GitHub Actions 工作流已成功将镜像推送到 Docker Hub。

## 总结

在本节中，你了解了如何为你的 Ruby on Rails 应用程序设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

在下一节中，你将了解如何使用容器开发你的应用程序。
