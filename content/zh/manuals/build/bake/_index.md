---
title: Bake
weight: 50
keywords: build, buildx, bake, buildkit, hcl, json, compose
aliases:
  - /build/customize/bake/
---

Bake 是 Docker Buildx 的一项功能，它允许您使用声明式文件定义构建配置，而不必在命令行中指定复杂的表达式。它还允许您通过单次调用并发运行多个构建任务。

Bake 文件可以采用 HCL、JSON 或 YAML 格式编写，其中 YAML 格式是 Docker Compose 文件的扩展。以下是一个 HCL 格式的 Bake 文件示例：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["frontend", "backend"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "frontend.Dockerfile"
  args = {
    NODE_VERSION = "22"
  }
  tags = ["myapp/frontend:latest"]
}

target "backend" {
  context = "./backend"
  dockerfile = "backend.Dockerfile"
  args = {
    GO_VERSION = "{{% param "example_go_version" %}}"
  }
  tags = ["myapp/backend:latest"]
}
```

`group` 块定义了一组可以并发构建的目标。每个 `target` 块定义了一个具有自身配置（如构建上下文、Dockerfile 和标签）的构建目标。

要使用上述 Bake 文件执行构建，您可以运行：

```console
$ docker buildx bake
```

这将执行 `default` 组，同时并发地构建 `frontend` 和 `backend` 目标。

## 入门指南

要了解如何开始使用 Bake，请前往 [Bake 简介](./introduction.md)。