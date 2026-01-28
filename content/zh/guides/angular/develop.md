---
title: 使用容器进行 Angular 开发
linkTitle: 开发您的应用
weight: 30
keywords: angular, development, node
description: 了解如何使用容器在本地开发 Angular 应用程序。

---

## 前提条件

完成[容器化 Angular 应用程序](containerize.md)。

---

## 概述

在本节中，您将学习如何使用 Docker Compose 为容器化的 Angular 应用程序设置生产和开发环境。此设置允许您通过 Nginx 提供静态生产构建服务，并使用 Compose Watch 的实时重载开发服务器在容器内高效开发。

您将学习如何：
- 为生产和开发配置单独的容器
- 在开发中使用 Compose Watch 启用自动文件同步
- 实时调试和预览更改，无需手动重建

---

## 自动更新服务（开发模式）

使用 Compose Watch 自动将源文件更改同步到容器化的开发环境中。这提供了无缝、高效的开发体验，无需手动重启或重建容器。

## 步骤 1：创建开发 Dockerfile

在项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# 阶段 1：开发 - Angular 应用程序
# =========================================

# 定义要使用的 Node.js 版本（使用 Alpine 以减小体积）
ARG NODE_VERSION=22.14.0-alpine

# 设置开发的基础镜像
FROM node:${NODE_VERSION} AS dev

# 设置环境变量以指示开发模式
ENV NODE_ENV=development

# 设置容器内的工作目录
WORKDIR /app

# 首先只复制依赖文件以优化 Docker 缓存
COPY package.json package-lock.json ./

# 使用 npm 安装依赖，并使用缓存加速后续构建
RUN --mount=type=cache,target=/root/.npm npm ci

# 将所有应用程序源文件复制到容器中
COPY . .

# 暴露 Angular 开发服务器使用的端口（默认为 4200）
EXPOSE 4200

# 启动 Angular 开发服务器并绑定到所有网络接口
CMD ["npm", "start", "--", "--host=0.0.0.0"]

```

此文件使用开发服务器为 Angular 应用程序设置轻量级开发环境。


### 步骤 2：更新您的 `compose.yaml` 文件

打开 `compose.yaml` 文件并定义两个服务：一个用于生产（`angular-prod`），一个用于开发（`angular-dev`）。

以下是 Angular 应用程序的示例配置：

```yaml
services:
  angular-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-angular-sample
    ports:
      - "8080:8080"

  angular-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "4200:4200"
    develop:
      watch:
        - action: sync
          path: .
          target: /app
```
- `angular-prod` 服务使用 Nginx 构建并提供静态生产应用程序服务。
- `angular-dev` 服务运行 Angular 开发服务器，支持实时重载和热模块替换。
- `watch` 使用 Compose Watch 触发文件同步。

> [!NOTE]
> 有关更多详细信息，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 4：启动 Compose Watch

从项目根目录运行以下命令以在 watch 模式下启动容器

```console
$ docker compose watch angular-dev
```

### 步骤 5：使用 Angular 测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在文本编辑器中打开 `src/app/app.component.html` 文件。

2. 找到以下行：

    ```html
    <h1>Docker Angular Sample Application</h1>
    ```

3. 将其更改为：

    ```html
    <h1>Hello from Docker Compose Watch</h1>
    ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:4200](http://localhost:4200)。

您应该立即看到更新的文本出现，无需手动重建容器。这确认文件监视和自动同步按预期工作。

---

## 总结

在本节中，您使用 Docker 和 Docker Compose 为 Angular 应用程序设置了完整的开发和生产工作流程。

以下是您完成的内容：
- 创建了 `Dockerfile.dev` 以简化具有热重载功能的本地开发
- 在 `compose.yaml` 文件中定义了单独的 `angular-dev` 和 `angular-prod` 服务
- 使用 Compose Watch 启用实时文件同步，获得更流畅的开发体验
- 通过修改和预览组件验证了实时更新无缝工作

通过此设置，您现在可以完全在容器内构建、运行和迭代 Angular 应用程序 — 跨环境高效且一致。

---

## 相关资源

通过以下指南加深知识并改进容器化开发工作流程：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发期间自动同步源代码更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效、生产就绪的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写干净、安全且优化的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解在 `compose.yaml` 中配置服务的完整语法和选项。
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久化和管理数据

## 下一步

在下一节中，您将学习如何在 Docker 容器内运行 Angular 应用程序的单元测试。这确保了跨所有环境的一致测试，并消除了对本地机器设置的依赖。
