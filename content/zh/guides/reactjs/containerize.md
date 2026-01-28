---
title: 容器化 React.js 应用程序
linkTitle: 容器化
weight: 10
keywords: react.js, node, image, initialize, build
description: 了解如何使用 Docker 容器化 React.js 应用程序，通过使用性能、安全性和可扩展性的最佳实践创建优化的、生产就绪的镜像。

---

## 先决条件

在开始之前，确保你的系统上安装并可用以下工具：

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

> **Docker 新手？**
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将带你完成使用 Docker 容器化 React.js 应用程序的完整过程。你将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提高性能、安全性、可扩展性和部署效率。

在本指南结束时，你将：

- 使用 Docker 容器化 React.js 应用程序。
- 创建并优化用于生产构建的 Dockerfile。
- 使用多阶段构建来最小化镜像大小。
- 使用自定义 NGINX 配置高效地服务应用程序。
- 遵循构建安全且可维护的 Docker 镜像的最佳实践。

---

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录切换到你想工作的目录，然后运行以下命令来克隆 git 存储库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-reactjs-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可以帮助为你的应用程序搭建必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到你的项目目录的根目录：

```console
$ cd docker-reactjs-sample
```

然后运行以下命令：

```console
$ docker init
```
你会看到类似以下的输出：

```text
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

CLI 会提示你回答几个关于你的应用程序设置的问题。
为了保持一致性，请在提示时使用下面示例中显示的相同回答：
| 问题 | 回答 |
|------------------------------------------------------------|-----------------|
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 22.14.0-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run dev |
| What port does your server listen on? | 8080 |

完成后，你的项目目录将包含以下新文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

由 `docker init` 生成的默认 Dockerfile 是通用 Node.js 应用程序的一个很好的起点。然而，React.js 是一个前端库，它编译成静态资产，因此我们需要定制 Dockerfile 以针对 React 应用程序在生产环境中的构建和服务方式进行优化。

### 第一步：审查生成的文件

在这一步中，你将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建来保持最终镜像的清洁和较小体积
- 使用 NGINX（一个快速且安全的 Web 服务器）来服务应用程序
- 通过仅包含所需内容来提高性能和安全性

这些更新有助于确保你的应用程序易于部署、加载快速且已准备好投入生产。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，其中包含构建 Docker 镜像的分步说明。它自动打包你的应用程序及其依赖项和运行时环境。
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。


### 第二步：配置 Dockerfile 文件

复制并用以下配置替换现有的 `Dockerfile` 内容：

```dockerfile
# =========================================
# Stage 1: Build the React.js Application
# =========================================
ARG NODE_VERSION=22.14.0-alpine
ARG NGINX_VERSION=alpine3.21

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the React.js application (outputs to /app/dist)
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Use a built-in non-root user for security best practices
USER nginx

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx  --from=builder /app/dist /usr/share/nginx/html

# Expose port 8080 to allow HTTP traffic
# Note: The default NGINX container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

### 第三步：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时排除哪些文件和文件夹。


> [!NOTE]
> 这有助于：
> - 减小镜像大小
> - 加快构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并用以下配置替换现有的 `.dockerignore` 内容：

```dockerignore
# Ignore dependencies and build output
node_modules/
dist/
out/
.tmp/
.cache/

# Ignore Vite, Webpack, and React-specific build artifacts
.vite/
.vitepress/
.eslintcache
.npm/
coverage/
jest/
cypress/
cypress/screenshots/
cypress/videos/
reports/

# Ignore environment and config files (sensitive data)
*.env*
*.log

# Ignore TypeScript build artifacts (if using TypeScript)
*.tsbuildinfo

# Ignore lockfiles (optional if using Docker for package installation)
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Ignore local development files
.git/
.gitignore
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db

# Ignore Docker-related files (to avoid copying unnecessary configs)
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml

# Ignore build-specific cache files
*.lock

```

### 第四步：创建 `nginx.conf` 文件

为了在容器内高效地服务你的 React.js 应用程序，你将使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩以及客户端路由支持进行了优化。

在项目目录的根目录中创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解有关配置 NGINX 的更多信息，请参阅 [NGINX 官方文档](https://nginx.org/en/docs/)。


```nginx
worker_processes auto;

# Store PID in /tmp (always writable)
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Disable logging to avoid permission issues
    access_log off;
    error_log  /dev/stderr warn;

    # Optimize static file serving
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # Gzip compression for optimized delivery
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    gzip_vary on;

    server {
        listen       8080;
        server_name  localhost;

        # Root directory where React.js build files are placed
        root /usr/share/nginx/html;
        index index.html;

        # Serve React.js static files with proper caching
        location / {
            try_files $uri /index.html;
        }

        # Serve static assets with long cache expiration
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # Handle React.js client-side routing
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 第五步：构建 React.js 应用程序镜像

有了自定义配置，你现在就可以为你的 React.js 应用程序构建 Docker 镜像了。

更新后的设置包括：

- 优化的浏览器缓存和 gzip 压缩
- 安全的非 root 日志记录，以避免权限问题
- 通过将不匹配的路由重定向到 `index.html` 来支持 React 客户端路由

完成前面的步骤后，你的项目目录现在应该包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在 Dockerfile 已配置完毕，你可以为 React.js 应用程序构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将你的应用程序打包成一个镜像。它包括来自当前目录的所有必要文件（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）。

从项目根目录运行以下命令：

```console
$ docker build --tag docker-reactjs-sample .
```

该命令的作用：
- 使用当前目录 (.) 中的 Dockerfile
- 将应用程序及其依赖项打包成一个 Docker 镜像
- 将镜像标记为 docker-reactjs-sample，以便稍后引用


#### 第六步：查看本地镜像

构建 Docker 镜像后，你可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上有哪些可用镜像。由于你已经在终端中工作，我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-reactjs-sample     latest            f39b47a97156   14 seconds ago   75.8MB
```

此输出提供了有关镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 一个版本标签，有助于识别不同的构建（例如，latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，你应该会看到列出的 `docker-reactjs-sample` 镜像。

---

## 运行容器化应用程序

在上一步中，你为 React.js 应用程序创建了一个 Dockerfile，并使用 docker build 命令构建了一个 Docker 镜像。现在是时候在容器中运行该镜像并验证你的应用程序是否按预期工作了。


在 `docker-reactjs-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该会看到一个简单的 React.js Web 应用程序。

在终端中按 `ctrl+c` 停止你的应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序与终端分离运行。在 `docker-reactjs-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该会看到一个简单的 Web 应用程序预览。


要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动的容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
88bced6ade95   docker-reactjs-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-reactjs-sample-server-1
```


要停止应用程序，请运行：

```console
$ docker compose down
```


> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，你学习了如何使用 Docker 容器化、构建和运行 React.js 应用程序。通过遵循最佳实践，你创建了一个安全、优化且生产就绪的设置。

你完成了以下工作：
- 使用 `docker init` 初始化你的项目，以搭建基本的 Docker 配置文件。
- 将默认的 `Dockerfile` 替换为多阶段构建，该构建编译 React.js 应用程序并使用 Nginx 服务静态文件。
- 替换了默认的 `.dockerignore` 文件以排除不必要的文件，并保持镜像清洁高效。
- 使用 `docker build` 构建了你的 Docker 镜像。
- 使用 `docker compose up` 运行容器，包括前台和分离模式。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证了应用程序正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用程序。

你现在拥有了一个完全容器化的 React.js 应用程序，在 Docker 容器中运行，并准备好充满信心地一致地部署到任何环境。

---

## 相关资源

探索官方参考资料和最佳实践，以磨练你的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动并运行多容器应用程序。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 下一步

随着 React.js 应用程序现在已容器化，你已准备好进入下一步。

在下一节中，你将学习如何使用 Docker 容器开发你的应用程序，从而在任何机器上实现一致、隔离且可重现的开发环境。
