---
title: 使用 GitHub Actions 自动化你的构建
linkTitle: 使用 GitHub Actions 自动化你的构建
weight: 60
keywords: CI/CD, GitHub( Actions), React.js, Next.js
description: 了解如何为你的 React.js 应用程序配置使用 GitHub Actions 的 CI/CD.

---

## 先决条件

完成本指南的所有前几节，从 [容器化 React.js 应用程序](containerize.md) 开始。

你还必须拥有：
- 一个 [GitHub](https://github.com/signup) 帐户。
- 一个 [Docker Hub](https://hub.docker.com/signup) 帐户。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 **CI/CD 管道**，以自动执行：

- 在 Docker 容器内构建你的 React.js 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将你的 GitHub 存储库连接到 Docker Hub

为了使 GitHub Actions 能够构建和推送 Docker 镜像，你将在新的 GitHub 存储库中安全地存储你的 Docker Hub 凭据。

### 第一步：将你的 GitHub 存储库连接到 Docker Hub

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌 (PAT)
   1. 转到你的 **Docker Hub 帐户 → Account Settings（帐户设置） → Security（安全）**。
   2. 生成一个新的具有 **Read/Write（读/写）** 权限的访问令牌。
   3. 将其命名为类似 `docker-reactjs-sample` 的名称。
   4. 复制并保存令牌 —— 你将在第四步中需要它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 中创建一个存储库
   1. 转到你的 **Docker Hub 帐户 → Create a repository（创建存储库）**。
   2. 对于存储库名称，使用描述性名称 —— 例如：`reactjs-sample`。
   3. 创建后，复制并保存存储库名称 —— 你将在第四步中需要它。

3. 为你的 React.js 项目创建一个新的 [GitHub 存储库](https://github.com/new)

4. 将 Docker Hub 凭据添加为 GitHub 存储库密钥

   在你新创建的 GitHub 存储库中：
   
   1. 导航到：
   **Settings（设置） → Secrets and variables（密钥和变量） → Actions → New repository secret（新存储库密钥）**。

   2. 添加以下密钥：

   | 名称              | 值                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 你的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 你的 Docker Hub 访问令牌（在步骤 1 中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 你的 Docker 项目名称（在步骤 2 中创建）   |

   这些密钥允许 GitHub Actions 在自动化工作流程期间安全地通过 Docker Hub 进行身份验证。

5. 将你的本地项目连接到 GitHub

   通过从项目根目录运行以下命令，将你的本地项目 `docker-reactjs-sample` 链接到你刚刚创建的 GitHub 存储库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为你实际的 GitHub 用户名和存储库名称。

   要确认你的本地项目是否正确连接到远程 GitHub 存储库，请运行：

   ```console
   $ git remote -v
   ```

   你应该看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了你的本地存储库已正确链接，并准备好将你的源代码推送到 GitHub。

6. 将你的源代码推送到 GitHub

   按照以下步骤提交并将本地项目推送到你的 GitHub 存储库：

   1. 暂存所有文件以进行提交。

      ```console
      $ git add -A
      ```
      此命令暂存所有更改 —— 包括新文件、修改的文件和删除的文件 —— 准备提交。


   2. 提交你的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，用描述性消息快照暂存的更改。

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将你的本地提交推送到远程 GitHub 存储库的 `main` 分支，并设置上游分支。

完成后，你的代码将在 GitHub 上可用，并且你配置的任何 GitHub Actions 工作流都将自动运行。

> [!NOTE]  
> 了解此步骤中使用的 Git 命令的更多信息：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新增、修改、删除）以进行提交
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到你的 GitHub 存储库
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程存储库 URL

---

### 第二步：设置工作流

现在你将创建一个 GitHub Actions 工作流，该工作流构建你的 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 转到 GitHub 上的存储库，然后在顶部菜单中选择 **Actions** 选项卡。

2. 出现提示时选择 **Set up a workflow yourself（自己设置工作流）**。

    这将打开一个内联编辑器来创建一个新的工作流文件。默认情况下，它将保存到：
   `.github/workflows/main.yml`

   
3. 将以下工作流配置添加到新文件：

```yaml
name: CI/CD – React.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Fetches full history for better caching/context

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

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
          load: true # Load to local Docker daemon for testing
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Vitest tests
      - name: Run Vitest tests and generate report
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npx vitest run --reporter=verbose"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Login to Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push prod image
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

此工作流为你的 React.js 应用程序执行以下任务：
- 在针对 `main` 分支的每次 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建开发 Docker 镜像，针对测试进行了优化。
- 在干净的容器化环境中使用 Vitest 执行单元测试，以确保一致性。
- 如果任何测试失败，立即停止工作流 —— 强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖项，以加快 CI 运行速度。
- 使用 GitHub 存储库密钥安全地通过 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建生产就绪的镜像。
- 标记并将最终镜像推送到 Docker Hub，包含 `latest` 和短 SHA 标签以便于追溯。

> [!NOTE]
> 有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 第三步：运行工作流

添加工作流文件后，是时候触发并观察 CI/CD 过程的运行了。

1. 提交并推送你的工作流文件

   在 GitHub 编辑器中选择 "Commit changes…"（提交更改...）。

   - 此推送将自动触发 GitHub Actions 管道。

2. 监控工作流执行

   1. 转到 GitHub 存储库中的 Actions 选项卡。
   2. 点击工作流运行以跟踪每个步骤：**build**、**test** 和（如果成功）**push**。

3. 在 Docker Hub 上验证 Docker 镜像

   - 工作流成功运行后，访问你的 [Docker Hub 存储库](https://hub.docker.com/repositories)。
   - 你应该在你的存储库下看到一个新镜像，具有：
      - 存储库名称：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最近成功的构建；非常适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，对于版本跟踪、回滚和追溯非常有用。

> [!TIP] 保护你的 main 分支
> 为了保持代码质量并防止意外直接推送，请启用分支保护规则：
>  - 导航到你的 **GitHub repo（存储库） → Settings（设置） → Branches（分支）**。
>  - 在 Branch protection rules（分支保护规则）下，点击 **Add rule（添加规则）**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *Require a pull request before merging（合并前需要拉取请求）*。
>     - *Require status checks to pass before merging（合并前需要通过状态检查）*。
>
>  这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，你使用 GitHub Actions 为容器化的 React.js 应用程序设置了完整的 CI/CD 管道。

你完成了以下工作：

- 为你的项目创建了一个新的 GitHub 存储库。
- 生成了一个安全的 Docker Hub 访问令牌并将其作为密钥添加到 GitHub。
- 定义了一个 GitHub Actions 工作流以：
   - 在 Docker 容器内构建你的应用程序。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，将生产就绪的镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流执行。
- 确认你的镜像已成功发布到 Docker Hub。

通过此设置，你的 React.js 应用程序现在可以进行自动化测试和跨环境部署 —— 提高了信心、一致性和团队生产力。

---

## 相关资源

加深你对自动化和容器化应用程序最佳实践的理解：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化你的工作流程
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化你的镜像以获得性能和安全性

---

## 下一步

接下来，了解如何在部署之前在 Kubernetes 上本地测试和调试你的 React.js 工作负载。这有助于确保你的应用程序在类似生产的环境中按预期运行，从而减少部署期间的意外情况。
