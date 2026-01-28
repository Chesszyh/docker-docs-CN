---
title: 容器化 Angular 应用程序
linkTitle: 容器化
weight: 10
keywords: angular, node, image, initialize, build
description: 了解如何使用 Docker 容器化 Angular 应用程序，通过遵循性能、安全性和可扩展性的最佳实践来创建优化的、生产就绪的镜像。

---

## 前提条件

在开始之前，请确保以下工具已安装并在您的系统上可用：

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **Docker 新手？**
> 从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 Angular 应用程序的完整流程。您将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提高性能、安全性、可扩展性和部署效率。

在本指南结束时，您将能够：

- 使用 Docker 容器化 Angular 应用程序。
- 创建并优化用于生产构建的 Dockerfile。
- 使用多阶段构建最小化镜像大小。
- 使用自定义 NGINX 配置高效地提供应用程序服务。
- 遵循最佳实践构建安全且可维护的 Docker 镜像。

---

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，导航到您想要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-angular-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，帮助搭建容器化应用程序所需的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到项目目录的根目录：

```console
$ cd docker-angular-sample
```

然后运行以下命令：

```console
$ docker init
```
您将看到类似以下的输出：

```text
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

CLI 将提示您回答一些关于应用程序设置的问题。
为了保持一致性，请在提示时使用下面示例中显示的相同答案：
| 问题                                                   | 答案          |
|------------------------------------------------------------|-----------------|
| What application platform does your project use?           | Node            |
| What version of Node do you want to use?                   | 23.11.0-alpine  |
| Which package manager do you want to use?                  | npm             |
| Do you want to run "npm run build" before starting server? | yes             |
| What directory is your build output to?                    | dist            |
| What command do you want to use to start the app?          | npm run start   |
| What port does your server listen on?                      | 8080            |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 是通用 Node.js 应用程序的良好起点。然而，Angular 是一个前端框架，会编译成静态资源，因此我们需要调整 Dockerfile 以优化 Angular 应用程序在生产环境中的构建和服务方式。

### 步骤 1：改进生成的 Dockerfile 和配置

在此步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建保持最终镜像整洁且小巧
- 使用 NGINX（一个快速且安全的 Web 服务器）提供应用程序服务
- 通过仅包含所需内容来提高性能和安全性

这些更新有助于确保您的应用程序易于部署、加载快速且生产就绪。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的逐步说明。它自动化了将应用程序及其依赖项和运行时环境打包在一起的过程。
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。


### 步骤 2：配置 Dockerfile

复制以下配置并替换现有 `Dockerfile` 的内容：

```dockerfile
# =========================================
# 阶段 1：构建 Angular 应用程序
# =========================================
# =========================================
# 阶段 1：构建 Angular 应用程序
# =========================================
ARG NODE_VERSION=22.14.0-alpine
ARG NGINX_VERSION=alpine3.21

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制包相关文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 使用 npm ci 安装项目依赖（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将其余应用程序源代码复制到容器中
COPY . .

# 构建 Angular 应用程序
RUN npm run build

# =========================================
# 阶段 2：准备 Nginx 提供静态文件服务
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 使用内置的非 root 用户以遵循安全最佳实践
USER nginx

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态构建输出复制到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 NGINX 容器现在监听端口 8080 而不是 80
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]

```

> [!NOTE]
> 我们使用 nginx-unprivileged 而不是标准 NGINX 镜像以遵循安全最佳实践。
> 在最终镜像中以非 root 用户运行：
>- 减少攻击面
>- 符合 Docker 对容器加固的建议
>- 有助于遵守生产环境中更严格的安全策略

### 步骤 3：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
>这有助于：
>- 减小镜像大小
>- 加快构建过程
>- 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制以下配置并替换现有 `.dockerignore` 的内容：

```dockerignore
# ================================
# Node 和构建输出
# ================================
node_modules
dist
out-tsc
.angular
.cache
.tmp

# ================================
# 测试和覆盖率
# ================================
coverage
jest
cypress
cypress/screenshots
cypress/videos
reports
playwright-report
.vite
.vitepress

# ================================
# 环境和日志文件
# ================================
*.env*
!*.env.production
*.log
*.tsbuildinfo

# ================================
# IDE 和操作系统特定文件
# ================================
.vscode
.idea
.DS_Store
Thumbs.db
*.swp

# ================================
# 版本控制和 CI 文件
# ================================
.git
.gitignore

# ================================
# Docker 和本地编排
# ================================
Dockerfile
Dockerfile.*
.dockerignore
docker-compose.yml
docker-compose*.yml

# ================================
# 杂项
# ================================
*.bak
*.old
*.tmp
```

### 步骤 4：创建 `nginx.conf` 文件

为了在容器内高效地提供 Angular 应用程序服务，您需要使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩和客户端路由支持进行了优化。

在项目目录的根目录创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解更多关于配置 NGINX 的信息，请参阅 [NGINX 官方文档](https://nginx.org/en/docs/)。


```nginx
worker_processes auto;

pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 日志
    access_log off;
    error_log  /dev/stderr warn;

    # 性能
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/x-javascript
        application/json
        application/xml
        application/xml+rss
        font/ttf
        font/otf
        image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root /usr/share/nginx/html;
        index index.html;

        # Angular 路由
        location / {
            try_files $uri $uri/ /index.html;
        }

        # 静态资源缓存
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # 可选：显式资源路由
        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 步骤 5：构建 Angular 应用程序镜像

配置好自定义设置后，您现在可以为 Angular 应用程序构建 Docker 镜像了。

更新后的设置包括：

- 更新后的设置包括专门为 Angular 定制的干净、生产就绪的 NGINX 配置。
- 高效的多阶段 Docker 构建，确保最终镜像小巧且安全。

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在您的 Dockerfile 已配置好，您可以为 Angular 应用程序构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将您的应用程序打包成镜像。它包含当前目录（称为[构建上下文](/build/concepts/context/#what-is-a-build-context)）中的所有必要文件。

从项目根目录运行以下命令：

```console
$ docker build --tag docker-angular-sample .
```

此命令的作用：
- 使用当前目录（.）中的 Dockerfile
- 将应用程序及其依赖项打包到 Docker 镜像中
- 将镜像标记为 docker-angular-sample，以便稍后引用


#### 步骤 6：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上有哪些可用镜像。由于您已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-angular-sample     latest            34e66bdb9d40   14 seconds ago   76.4MB
```

此输出提供有关镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 帮助识别不同构建的版本标签（例如 latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该看到列出的 `docker-angular-sample` 镜像。

---

## 运行容器化应用程序

在上一步中，您为 Angular 应用程序创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证应用程序是否按预期工作。


在 `docker-angular-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该看到一个简单的 Angular Web 应用程序。

在终端中按 `ctrl+c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序在后台运行，与终端分离。在 `docker-angular-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该看到 Angular 应用程序在浏览器中运行。


要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
eb13026806d1   docker-angular-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-angular-sample-server-1
```


要停止应用程序，请运行：

```console
$ docker compose down
```


> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Angular 应用程序。通过遵循最佳实践，您创建了安全、优化且生产就绪的设置。

您完成的内容：
- 使用 `docker init` 初始化项目以搭建基本的 Docker 配置文件。
- 将默认 `Dockerfile` 替换为多阶段构建，用于编译 Angular 应用程序并使用 Nginx 提供静态文件服务。
- 替换默认 `.dockerignore` 文件以排除不必要的文件，保持镜像整洁高效。
- 使用 `docker build` 构建 Docker 镜像。
- 使用 `docker compose up` 运行容器，包括前台模式和分离模式。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证应用程序正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用程序。

您现在拥有一个完全容器化的 Angular 应用程序，运行在 Docker 容器中，可以自信且一致地部署到任何环境。

---

## 相关资源

探索官方参考和最佳实践以优化您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 学习如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资源。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用程序。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并删除容器、网络和卷。

---

## 下一步

您的 Angular 应用程序现已容器化，您可以继续进行下一步了。

在下一节中，您将学习如何使用 Docker 容器开发应用程序，实现跨任何机器的一致、隔离和可重现的开发环境。
