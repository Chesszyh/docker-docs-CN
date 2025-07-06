---
title: 使用 GitHub Actions 自动化你的构建
linkTitle: 使用 GitHub Actions 自动化你的构建
weight: 60
keywords: CI/CD, GitHub( Actions), Angular
description: 了解如何使用 GitHub Actions 为你的 Angular 应用程序配置 CI/CD。

---

## 先决条件

完成本指南的所有先前部分，从[容器化 Angular 应用程序](containerize.md)开始。

你还必须拥有：
- 一个 [GitHub](https://github.com/signup) 帐户。
- 一个 [Docker Hub](https://hub.docker.com/signup) 帐户。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 CI/CD 管道，以自动执行以下操作：

- 在 Docker 容器内构建你的 Angular 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将你的 GitHub 存储库连接到 Docker Hub

要使 GitHub Actions 能够构建和推送 Docker 镜像，你需要将你的 Docker Hub 凭据安全地存储在你的新 GitHub 存储库中。

### 第 1 步：生成 Docker Hub 凭据���设置 GitHub 机密

1. 从 [Docker Hub](https://hub.docker.com) 创建一个个人访问令牌 (PAT)
   1. 转到你的 **Docker Hub 帐户 → 帐户设置 → 安全**。
   2. 生成一个具有**读/写**权限的新访问令牌。
   3. 将其命名为类似 `docker-angular-sample` 的名称。
   4. 复制并保存该令牌——你将在第 4 步中需要它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 中创建一个存储库
   1. 转到你的 **Docker Hub 帐户 → 创建一个存储库**。
   2. 对于存储库名称，使用一个描述性的名称——例如：`angular-sample`。
   3. 创建后，复制并保存存储库名称——你将在第 4 步中需要它。

3. 为你的 Angular 项目创建一个新的 [GitHub 存储库](https://github.com/new)

4. 将 Docker Hub 凭据添加为 GitHub 存储库机密

   在你新创建的 GitHub 存储库中：
   
   1. 导航到：
   **设置 → 机密和变量 → 操作 → 新建存储库机密**。

   2. 添加以下机密：

   | 名称              | 值                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 你的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 你的 Docker Hub 访问令牌（在第 1 步中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 你的 Docker 项目���称（在第 2 步中创建）   |

   这些机密允许 GitHub Actions 在自动化工作流程期间安全地向 Docker Hub 进行身份验证。

5. 将你的本地项目连接到 GitHub

   通过从你的项目根目录运行以下命令，将你的本地项目 `docker-angular-sample` 链接到你刚刚创建的 GitHub 存储库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为你的实际 GitHub 用户名和存储库名称。

   要确认你的本地项目已正确连接到远程 GitHub 存储库，请运行：

   ```console
   $ git remote -v
   ```

   你应该会看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了你的本地存储库已正确链接并准备好将你的源代码推送到 GitHub。

6. 将你的源代码推送到 GitHub

   按照以下步骤提交并将你的本地项目推送到你的 GitHub 存储库：

   1. 将所有文件暂存以进行提交。

      ```console
      $ git add -A
      ```
      此命令将所有更改（包括新文件、修改��的文件和已删除的文件）暂存，为提交做准备。


   2. 使用描述性消息提交暂存的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，该提交使用描述性消息快照暂存的更改。

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将你的本地提交推送到远程 GitHub 存储库的 `main` 分支，并设置上游分支。

一旦完成，你的代码将在 GitHub 上可用，并且你配置的任何 GitHub Actions 工作流程都将自动运行。

> [!NOTE]  
> 了解有关此步骤中使用的 Git 命令的更多信息：
> - [Git add](https://git-scm.com/docs/git-add) – 将更改（新的、修改的、删除的）暂存以进行提交
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到你的 GitHub 存储库
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程存储库 URL

---

### 第 2 步：设置工作流程

现在，你将创建一个 GitHub Actions 工作流程，该工作流程将构建你的 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 转到你在 GitHub 上的存储库，然后在顶部菜单中选择 **Actions** 选项卡。

2. 出现提示时，选择 **Set up a workflow yourself**。

    这将打开一个内联编辑器以创建新的工作流程文件。默认情况下，它将保存到：
   `.github/workflows/main.yml`

   
3. 将以下工作流程配置添加到新文件中：

```yaml
name: CI/CD – Angular Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test, and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. Extract metadata
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build dev Docker image
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Angular tests with Jasmine
      - name: Run Angular Jasmine tests inside container
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npm run test -- --ci --runInBand"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Log in to Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image
      - name: Build and push production image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
```

此工作流程为你的 Angular 应用程序执行以下任务：
- 在每次针对 `main` 分支的 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建一个开发 Docker 镜像，该镜像针对测试进行了优化。
- 在一个干净的、容器化的环境中使用 Vitest 执行单元测试，以确保一致性。
- 如果任何测试失败，则立即停止工作流程——强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖项，以加快 CI 运行速度。
- 使用 GitHub 存储库机密安全地向 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建一个生产就绪的镜像。
- 使用 `latest` 和短 SHA 标签标记并推送到 Docker Hub，以实现可追溯性。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 第 3 步：运行工作流程

添加工作流程文件后，是时候触发并观察 CI/CD 过程的实际运行了。

1. 提交并推送你的工作流程文件

   - 在 GitHub 编辑器中选择“Commit changes…”。

   - 此推送将自动触发 GitHub Actions 管道。

2. 监控工作流程执行

   - 转到 GitHub 存储库中的 Actions 选项卡。
   - 单击工作流程运行以跟踪每个步骤：**构建**、**测试**和（如果成功）**推送**。

3. 在 Docker Hub 上验证 Docker 镜像

   - 成功运行工作流程后，访问你的 [Docker Hub 存储库](https://hub.docker.com/repositories)。
   - 你应该会在你的存储库下看到一个新镜像，其中包含：
      - 存储库名称：`${your-repository-name}`
      - 标签包括：
         - `latest` – 表示最近一次成功的构建；非常适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，可用于版本跟踪、回滚和可追溯性。

> [!TIP] 保护你的主分支
> 为了保持代码质量并防止意外的直接推送，请启用分支保护规则：
>  - 导航到你的 **GitHub 存储库 → 设置 → 分支**。
>  - 在分支保护规则下，单击 **添加规则**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *合并前需要拉取请求*。
>     - *合并前需要状态检查通过*。
>
>  这可确保只有经过测试和审查的代码才能合并到 `main` 分支中。
---

## 总结

在本节中，你使用 GitHub Actions 为你的容器化 Angular 应用程序设置了一个完整的 CI/CD 管道。

以下是你完成的工作：

- 为你的项目创建了一个新的 GitHub 存储库。
- 生成了一个安全的 Docker Hub 访问令牌，并将其作为机密添加到 GitHub。
- 定义了一个 GitHub Actions 工作流程，该工作流程：
   - 在 Docker 容器内构建你的应用程序。
   - 在一致的、容器化的环境中运行测试。
   - 如果测试通过，则将生产就绪的镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流程的执行。
- 确认你的镜像已成功发布到 Docker Hub。

通过此设置，你的 Angular 应用程序现在已准备好在各种环境中进行自动化测试和部署——从而提高了信心、一致性和团队生产力。

---

## 相关资源

加深你对自动化和容器化应用程序最佳实践的理解：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化你的工作流程
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建
- [GitHub Actions 的工作流程语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流程的完整参考
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化你的镜像以提高性能和安全性

---

## 下一步

接下来，学习如何在部署前在 Kubernetes 上本地测试和调试你的 Angular 工作负载。这有助于你确保你的应用程序在类似生产的环境中按预期运行，从而减少部署期间的意外情况。
