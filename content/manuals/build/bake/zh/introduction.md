---
title: Bake 简介
linkTitle: 简介
weight: 10
description: 开始使用 Bake 来构建您的项目
keywords: bake, quickstart, build, project, introduction, getting started
---

Bake 是 `docker build` 命令的抽象，它让您可以更轻松地以一致的方式管理构建配置（CLI 标志、环境变量等），供团队中的每个人使用。

Bake 是内置于 Buildx CLI 中的命令，因此只要您安装了 Buildx，您就可以通过 `docker buildx bake` 命令访问 bake。

## 使用 Bake 构建项目

以下是一个简单的 `docker build` 命令示例：

```console
$ docker build -f Dockerfile -t myapp:latest .
```

此命令构建当前目录中的 Dockerfile 并将生成的镜像标记为 `myapp:latest`。

要使用 Bake 表达相同的构建配置：

```hcl {title=docker-bake.hcl}
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
}
```

Bake 提供了一种结构化的方式来管理您的构建配置，它使您不必每次都记住 `docker build` 的所有 CLI 标志。有了这个文件，构建镜像就像运行以下命令一样简单：

```console
$ docker buildx bake myapp
```

对于简单的构建，`docker build` 和 `docker buildx bake` 之间的差异很小。然而，随着您的构建配置变得越来越复杂，Bake 提供了一种更结构化的方式来管理这种复杂性，而使用 `docker build` 的 CLI 标志来管理会很困难。它还提供了一种在团队中共享构建配置的方式，这样每个人都以一致的方式使用相同的配置来构建镜像。

## Bake 文件格式

您可以使用 HCL、YAML（Docker Compose 文件）或 JSON 格式编写 Bake 文件。一般来说，HCL 是最具表达力和灵活性的格式，这就是为什么您会在本文档的大多数示例以及使用 Bake 的项目中看到它被使用。

可以为目标设置的属性与 `docker build` 的 CLI 标志非常相似。例如，考虑以下 `docker build` 命令：

```console
$ docker build \
  -f Dockerfile \
  -t myapp:latest \
  --build-arg foo=bar \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  .
```

Bake 等价物为：

```hcl {title=docker-bake.hcl}
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  args = {
    foo = "bar"
  }
  no-cache = true
  platforms = ["linux/amd64", "linux/arm64"]
}
```

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Bake 文件编辑体验？
> 请查看 [Docker VS Code 扩展（Beta 版）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它提供 lint、代码导航和漏洞扫描功能。

## 后续步骤

要了解有关使用 Bake 的更多信息，请参阅以下主题：

- 了解如何在 Bake 中定义和使用[目标](./targets.md)
- 要查看可以为目标设置的所有属性，请参阅 [Bake 文件参考](/build/bake/reference/)。
