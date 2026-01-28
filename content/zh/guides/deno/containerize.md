---
title: 容器化 Deno 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: deno, containerize, initialize
description: 学习如何容器化 Deno 应用程序。
aliases:
  - /language/deno/containerize/
---

## 前提条件

* 您需要有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

长期以来，Node.js 一直是服务器端 JavaScript 应用程序的首选运行时。然而，近年来出现了新的替代运行时，包括 [Deno](https://deno.land/)。与 Node.js 一样，Deno 是 JavaScript 和 TypeScript 运行时，但它采用了全新的方法，具有现代安全特性、内置标准库和原生 TypeScript 支持。

为什么要使用 Docker 开发 Deno 应用程序？拥有多种运行时选择是令人兴奋的，但在不同环境中一致地管理多个运行时及其依赖项可能很棘手。这正是 Docker 大显身手的地方。使用容器按需创建和销毁环境简化了运行时管理并确保了一致性。此外，随着 Deno 的持续发展，Docker 有助于建立可靠且可重现的开发环境，最大限度地减少设置挑战并简化工作流程。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

现在您的 `deno-docker` 目录中应该有以下内容。

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

## 理解示例应用程序

示例应用程序是一个简单的 Deno 应用程序，它使用 Oak 框架创建一个简单的 API，返回 JSON 响应。应用程序监听 8000 端口，当您在浏览器中访问应用程序时返回消息 `{"Status" : "OK"}`。

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// Define a route that returns JSON
router.get("/", (context) => {
  context.response.body = { Status: "OK" };
  context.response.type = "application/json";
});

app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
```

## 创建 Dockerfile

在 Dockerfile 中，您会注意到 `FROM` 指令使用 `denoland/deno:latest`
作为基础镜像。这是 Deno 的官方镜像。该镜像[可在 Docker Hub 上获取](https://hub.docker.com/r/denoland/deno)。

```dockerfile
# Use the official Deno image
FROM denoland/deno:latest

# Set the working directory
WORKDIR /app

# Copy server code into the container
COPY server.ts .

# Set permissions (optional but recommended for security)
USER deno

# Expose port 8000
EXPOSE 8000

# Run the Deno server
CMD ["run", "--allow-net", "server.ts"]
```

除了指定 `denoland/deno:latest` 作为基础镜像外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将 `server.ts` 复制到容器中。
- 将用户设置为 `deno`，以非 root 用户身份运行应用程序。
- 暴露 8000 端口以允许流量到达应用程序。
- 使用 `CMD` 指令运行 Deno 服务器。
- 使用 `--allow-net` 标志允许应用程序进行网络访问。`server.ts` 文件使用 Oak 框架创建一个监听 8000 端口的简单 API。

## 运行应用程序

确保您在 `deno-docker` 目录中。在终端中运行以下命令来构建和运行应用程序。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。您将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序在后台运行，与终端分离。在 `deno-docker` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。


在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行 Deno 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)

## 下一步

在下一节中，您将学习如何使用容器开发应用程序。
