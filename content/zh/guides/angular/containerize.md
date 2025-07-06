---
title: 容器化 Angular 应用程序
linkTitle: 容器化
weight: 10
keywords: angular, node, image, initialize, build
description: 了解如何通过创建优化的、生产就绪的镜像，并遵循性能、安全性和可伸缩性的最佳实践，来使用 Docker 对 Angular 应用程序进行容器化。

---

## 先决条件

在开始之前，请确保你的系统上已安装并可用以下工具：

- 你已经安装了最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

> **Docker 新手？**  
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导你完成使用 Docker 对 Angular 应用程序进行容器化的完整过程。你将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提高性能、安全性、可伸缩性和部署效率。

在本指南结束时，你将能够：

- 使用 Docker 对 Angular 应用程序进行容器化。
- 创建并优化用于生产���建的 Dockerfile。
- 使用多阶段构建来最小化镜像大小。
- 使用自定义 NGINX 配置高效地提供应用程序。
- 通过遵循最佳实践来构建安全且可维护的 Docker 镜像。

---

## 获取示例应用程序

克隆示例应用程序以用于本指南。打开一个终端，导航到你想要工作的目录，然后运行以下命令来克隆 git 存储库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-angular-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助搭建容器化应用程序所需的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到你的项目根目录：

```console
$ cd docker-angular-sample
```

然后运行以下命令：

```console
$ docker init
```
你应该会看到类似以下的输出：

```text
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

CLI 将提示你有关应用程序设置的几个问题。
为保持一致性，请在出现提示时使用与以下示例中相同的响应：
| 问题                                                   | 答案          |
|------------------------------------------------------------|-----------------|
| 你的项目使用什么应用程序平台？           | Node            |
| 你想使用哪个版本的 Node？                   | 23.11.0-alpine  |
| 你想使用哪个包管理器？                  | npm             |
| 你想在启动服务器之前运行“npm run build”吗？ | yes             |
| 你的构建输出目录是什么？                    | dist            |
| 你想用什么命令来启动应用程序？          | npm run start   |
| 你的服务器在哪个端口上侦听？                      | 8080            |

完成后，你的项目目录将包含以下新文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 是通用 Node.js 应用程序的坚实起点。然而，Angular 是一个编译成静态资产的前端框架，因此我们需要调整 Dockerfile 以优化 Angular 应用程序在生产环境中的构建和提供方式。

### 第 1 步：改进生成的 Dockerfile 和配置

在此步骤中，你将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建来保持最终镜像的干净和小巧
- 使用 NGINX（一个快速安全的 Web 服务器）来提供应用程序
- 通过仅包含所需内容来提高性能和安全性

这些更新有助于确保你的应用程序易于部署、加载速度快且生产就绪。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，其中包含构建 Docker 镜像的逐步说明。它会自动打包你的应用程序及其依赖项和运行时环境。
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。


### 第 2 步：配置 Dockerfile

复制并替换现有 `Dockerfile` 的内容为以下配置：

```dockerfile
# =========================================
# 第 1 阶段：构建 Angular 应用程序
# =========================================
# =========================================
# 第 1 阶段：构建 Angular 应用程序
# =========================================
ARG NODE_VERSION=22.14.0-alpine
ARG NGINX_VERSION=alpine3.21

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 在容器内设置工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 使用 npm ci 安装项目依赖项（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 构建 Angular 应用程序
RUN npm run build 

# =========================================
# 第 2 阶段：准备 Nginx 以提供静态文件
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 使用内置的非 root 用户以遵循安全最佳实践
USER nginx

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态构建输出复制到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认的 NGINX 容器现在侦听端口 8080 而不是 80 
EXPOSE 8080

# 直接使用自定义配置启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]

```

> [!NOTE]
> 我们正在使用 nginx-unprivileged 而不是标准的 NGINX 镜像，以遵循安全最佳实践。
> 在最终镜像中以非 root 用户身份运行：
>- 减少攻击面
>- 符合 Docker 对容器强化的建议
>- 有助于遵守生产环境中更严格的安全策略

### 第 3 步：配置 .dockerignore 文件

`.dockerignore` 文件��诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
>这有助于：
>- 减小镜像大小
>- 加快构建过程
>- 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并替换现有 `.dockerignore` 的内容为以下配置：

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
# IDE 和特定于操作系统的文件
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
# 其他
# ================================
*.bak
*.old
*.tmp
```

### 第 4 步：创建 `nginx.conf` 文件

为了在容器内高效地提供你的 Angular 应用程序，你将使用自定义设置来配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩和对客户端路由的支持进行了优化。

在你的项目根目录中创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解有关配置 NGINX 的更多信息，请参阅 [官方 NGINX 文档](https://nginx.org/en/docs/)。


```nginx
worker_processes auto;

pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 日志记录
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

        # 静态资产缓存
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # 可选：显式资产路由
        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 第 5 步：构建 Angular 应用程序镜像

完成自定义配置后，你现在可以为你的 Angular 应用程序构建 Docker 镜像了。

更新后的设置包括：

- 更新后的设置包括一个干净的、生产就绪的 NGINX 配置，专门为 Angular 量身定制。
- 高效的多阶段 Docker 构建，确保最终镜像小巧安全。

完成前面的步骤后，你的项目目录现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在你的 Dockerfile 已配置好，你可以为你的 Angular 应用程序构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将你的应用程序打包成一个镜像。它包括当前目录（称为[构建上下文](/build/concepts/context/#what-is-a-build-context)）中的所有必要文件。

从你的项目根目录运行以下命令：

```console
$ docker build --tag docker-angular-sample .
```

此命令的作用：
- 使用当前目录 (.) 中的 Dockerfile
- 将应用程序及其依赖项打包成一个 Docker 镜像
- 将镜像标记为 docker-angular-sample，以便你以后可以引用它


#### 第 6 步：查看本地镜像

构建 Docker 镜像后，你可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地计算机上有哪些可用的镜像。由于你已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-angular-sample     latest            34e66bdb9d40   14 seconds ago   76.4MB
```

此输出提供了��关你的镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 有助于识别不同构建的版本标签（例如，latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时���戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，你应该会看到列出的 `docker-angular-sample` 镜像。

---

## 运行容器化的应用程序

在上一步中，你为你的 Angular 应用程序创建了一个 Dockerfile，并使用 docker build 命令构建了一个 Docker 镜像。现在是时候在容器中运行该镜像并验证你的应用程序是否按预期工作了。


在 `docker-angular-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看该应用程序。你应该会看到一个简单的 Angular Web 应用程序。

在终端中按 `ctrl+c` 以停止你的应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项来在与终端分离的情况下运行该应用程序。在 `docker-angular-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看该应用程序。你应该会在浏览器中看到你的 Angular 应用程序正在运行。


要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找一个暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
eb13026806d1   docker-angular-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-angular-sample-server-1
```


要停止该应用程序，请运行：

```console
$ docker compose down
```


> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，你学习了如何使用 Docker 对 Angular 应用程序进行容器化、构建和运行。通过遵循最佳实践，你创建了一个安全、优化且生产就绪的设置。

你完成的工作：
- 使用 `docker init` 初始化你的项目以搭建基本的 Docker 配置文件。
- 将默认的 `Dockerfile` 替换为多阶段构建，该构建编译 Angular 应用程序并使用 Nginx 提供静态文件。
- 替换默认的 `.dockerignore` 文件以排除不必要的文件，并保持镜像的干净和高效。
- 使用 `docker build` 构建你的 Docker 镜像。
- 使用 `docker compose up` 在前台和分离模式下运行容器。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证应用程序是否正在运行。
- 学习了如何使用 `docker compose down` 停止容器化的应用程序。

你现在拥有一个完全容器化的 Angular 应用程序，它在 Docker 容器中运行，并准备好在任何环境中充满信心和一致性地进行部署。

---

## 相关资源

探索官方参考和最佳实践以提高你的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 学习如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用程序。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止和移除容器、网络和卷。

---

## 下一步

你的 Angular 应用程序现在已容器化，你已准备好进入下一步。

在下一节中，你将学习如何使用 Docker 容器开发你的应用程序，从而在任何机器上实现一致、隔离且可重现的开发环境。
