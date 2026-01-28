---
title: 为你的 Go 应用程序配置 CI/CD
linkTitle: 配置 CI/CD
weight: 40
keywords: go, CI/CD, local, development
description: 了解如何为你的 Go 应用程序配置 CI/CD
aliases:
  - /language/golang/configure-ci-cd/
  - /guides/language/golang/configure-ci-cd/
---

## 先决条件

完成本指南的前面部分，从 [构建 Go 镜像](build-images.md) 开始。你必须拥有 [GitHub](https://github.com/signup) 帐户和 [Docker](https://hub.docker.com/signup) 帐户才能完成本节。

## 概览

在本节中，你将学习如何设置和使用 GitHub Actions 来构建和推送你的 Docker 镜像到 Docker Hub。你将完成以下步骤：

1. 在 GitHub 上创建一个新的存储库。
2. 定义 GitHub Actions 工作流程。
3. 运行工作流程。

## 第一步：创建存储库

创建 GitHub 存储库，配置 Docker Hub 凭据，并推送你的源代码。

1. 在 GitHub 上 [创建一个新存储库](https://github.com/new)。

2. 打开存储库 **Settings**（设置），然后转到 **Secrets and variables**（机密和变量） > **Actions**。

3. 创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**（存储库变量），并将你的 Docker ID 作为值。

4. 为 Docker Hub 创建一个新的 [个人访问令牌 (PAT)](/manuals/security/for-developers/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包括 Read（读取）和 Write（写入）。

5. 将 PAT 添加为 GitHub 存储库中的 **Repository secret**（存储库机密），名称为 `DOCKERHUB_TOKEN`。

6. 在机器上的本地存储库中，运行以下命令将 origin 更改为你刚刚创建的存储库。确保将 `your-username` 更改为你的 GitHub 用户名，将 `your-repository` 更改为你创建的存储库的名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 运行以下命令以暂存、提交并将你的本地存储库推送到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my commit"
   $ git push -u origin main
   ```

## 第二步：设置工作流程

设置 GitHub Actions 工作流程以构建、测试镜像并将其推送到 Docker Hub。

1. 转到 GitHub 上的存储库，然后选择 **Actions** 选项卡。

2. 选择 **set up a workflow yourself**（自行设置工作流程）。

   这会将你带到一个页面，用于在你的存储库中创建新的 GitHub actions 工作流程文件，默认位于 `.github/workflows/main.yml` 下。

3. 在编辑器窗口中，复制并粘贴以下 YAML 配置并提交更改。

   ```yaml
   name: ci

   on:
     push:
       branches:
         - main

   jobs:
     build:
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
             platforms: linux/amd64,linux/arm64
             push: true
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

   有关 `docker/build-push-action` 的 YAML 语法的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 第三步：运行工作流程

保存工作流程文件并运行作业。

1. 选择 **Commit changes...**（提交更改...）并将更改推送到 `main` 分支。

   推送提交后，工作流程会自动启动。

2. 转到 **Actions** 选项卡。它显示工作流程。

   选择工作流程会显示所有步骤的细分。

3. 工作流程完成后，转到你的 [Docker Hub 上的存储库](https://hub.docker.com/repositories)。

   如果你在该列表中看到新存储库，则表示 GitHub Actions 已成功将镜像推送到 Docker Hub。

## 总结

在本节中，你学习了如何为你的应用程序设置 GitHub Actions 工作流程。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流程语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 后续步骤

接下来，了解如何在部署之前在 Kubernetes 上本地测试和调试你的工作负载。
