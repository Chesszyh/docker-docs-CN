---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 60
keywords: CI/CD, GitHub( Actions), Angular
description: 了解如何为您的 Angular 应用程序使用 GitHub Actions 配置 CI/CD。

---

## 前提条件

完成本指南的所有前面章节，从[容器化 Angular 应用程序](containerize.md)开始。

您还必须拥有：
- 一个 [GitHub](https://github.com/signup) 账户。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账户。

---

## 概述

在本节中，您将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置 CI/CD 流水线，以自动完成以下操作：

- 在 Docker 容器内构建您的 Angular 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将您的 GitHub 仓库连接到 Docker Hub

要使 GitHub Actions 能够构建和推送 Docker 镜像，您需要在新的 GitHub 仓库中安全地存储您的 Docker Hub 凭据。

### 步骤 1：生成 Docker Hub 凭据并设置 GitHub Secrets

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌（PAT）
   1. 前往您的 **Docker Hub 账户 → 账户设置 → 安全**。
   2. 生成一个具有**读/写**权限的新访问令牌。
   3. 为其命名，例如 `docker-angular-sample`。
   4. 复制并保存令牌 — 您将在步骤 4 中需要它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 创建仓库
   1. 前往您的 **Docker Hub 账户 → 创建仓库**。
   2. 对于仓库名称，使用描述性名称 — 例如：`angular-sample`。
   3. 创建后，复制并保存仓库名称 — 您将在步骤 4 中需要它。

3. 为您的 Angular 项目创建一个新的 [GitHub 仓库](https://github.com/new)

4. 将 Docker Hub 凭据添加为 GitHub 仓库密钥

   在您新创建的 GitHub 仓库中：

   1. 导航至：
   **Settings → Secrets and variables → Actions → New repository secret**。

   2. 添加以下密钥：

   | 名称              | 值                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 您的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 您的 Docker Hub 访问令牌（在步骤 1 中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 您的 Docker 项目名称（在步骤 2 中创建）   |

   这些密钥允许 GitHub Actions 在自动化工作流程中安全地与 Docker Hub 进行身份验证。

5. 将您的本地项目连接到 GitHub

   通过在项目根目录运行以下命令，将您的本地项目 `docker-angular-sample` 链接到您刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为您的实际 GitHub 用户名和仓库名称。

   要确认您的本地项目已正确连接到远程 GitHub 仓库，请运行：

   ```console
   $ git remote -v
   ```

   您应该看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认您的本地仓库已正确链接并准备好将源代码推送到 GitHub。

6. 将源代码推送到 GitHub

   按照以下步骤将您的本地项目提交并推送到 GitHub 仓库：

   1. 暂存所有文件以进行提交。

      ```console
      $ git add -A
      ```
      此命令暂存所有更改 — 包括新建、修改和删除的文件 — 准备提交。


   2. 使用描述性消息提交暂存的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，用描述性消息快照暂存的更改。

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将您的本地提交推送到远程 GitHub 仓库的 `main` 分支并设置上游分支。

完成后，您的代码将在 GitHub 上可用，您配置的任何 GitHub Actions 工作流程将自动运行。

> [!NOTE]
> 了解更多关于此步骤中使用的 Git 命令：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新建、修改、删除）以进行提交
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到 GitHub 仓库
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：设置工作流程

现在您将创建一个 GitHub Actions 工作流程，用于构建 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 在 GitHub 上转到您的仓库，并在顶部菜单中选择 **Actions** 选项卡。

2. 在提示时选择 **Set up a workflow yourself**。

    这将打开一个内联编辑器，用于在您的仓库中创建新的工作流程文件。默认情况下，它将保存到：
   `.github/workflows/main.yml`


3. 将以下工作流程配置添加到新文件：

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
      # 1. 检出源代码
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. 设置 Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. 缓存 Docker 层
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. 缓存 npm 依赖
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. 提取元数据
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. 构建开发 Docker 镜像
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. 使用 Jasmine 运行 Angular 测试
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

      # 8. 登录 Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. 构建并推送生产镜像
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

此工作流程为您的 Angular 应用程序执行以下任务：
- 在每次针对 `main` 分支的 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建开发 Docker 镜像，针对测试进行优化。
- 在干净的容器化环境中使用 Vitest 执行单元测试，以确保一致性。
- 如果任何测试失败，立即停止工作流程 — 强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖以加快 CI 运行速度。
- 使用 GitHub 仓库密钥安全地与 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建生产就绪镜像。
- 使用 `latest` 和短 SHA 标签标记并推送最终镜像到 Docker Hub 以实现可追溯性。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行工作流程

添加工作流程文件后，是时候触发并观察 CI/CD 流程的运行了。

1. 提交并推送您的工作流程文件

   - 在 GitHub 编辑器中选择"Commit changes…"。

   - 此推送将自动触发 GitHub Actions 流水线。

2. 监控工作流程执行

   - 转到 GitHub 仓库中的 Actions 选项卡。
   - 点击进入工作流程运行以跟踪每个步骤：**build**、**test** 和（如果成功）**push**。

3. 在 Docker Hub 上验证 Docker 镜像

   - 工作流程成功运行后，访问您的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 您应该在仓库下看到一个新镜像，其中包含：
      - 仓库名称：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最近成功的构建；非常适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，用于版本跟踪、回滚和可追溯性。

> [!TIP] 保护您的 main 分支
> 为了维护代码质量并防止意外的直接推送，请启用分支保护规则：
>  - 导航到您的 **GitHub 仓库 → Settings → Branches**。
>  - 在 Branch protection rules 下，点击 **Add rule**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *Require a pull request before merging*。
>     - *Require status checks to pass before merging*。
>
>  这确保只有经过测试和审核的代码才能合并到 `main` 分支。
---

## 总结

在本节中，您使用 GitHub Actions 为容器化的 Angular 应用程序设置了完整的 CI/CD 流水线。

以下是您完成的内容：

- 为您的项目创建了一个新的 GitHub 仓库。
- 生成了安全的 Docker Hub 访问令牌，并将其作为密钥添加到 GitHub。
- 定义了一个 GitHub Actions 工作流程，该工作流程：
   - 在 Docker 容器内构建您的应用程序。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，将生产就绪镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流程执行。
- 确认您的镜像已成功发布到 Docker Hub。

通过此设置，您的 Angular 应用程序现在已准备好跨环境进行自动化测试和部署 — 提高了信心、一致性和团队生产力。

---

## 相关资源

深入了解容器化应用程序的自动化和最佳实践：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化您的工作流程
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建
- [GitHub Actions 工作流程语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流程的完整参考
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化您的镜像以提高性能和安全性

---

## 下一步

接下来，了解如何在部署前在 Kubernetes 上本地测试和调试 Angular 工作负载。这有助于确保您的应用程序在类生产环境中按预期运行，减少部署时的意外情况。
