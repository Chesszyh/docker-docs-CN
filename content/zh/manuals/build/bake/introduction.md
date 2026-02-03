---
title: Bake 简介
linkTitle: 简介
weight: 10
description: 开始使用 Bake 来构建您的项目
keywords: bake, quickstart, build, project, introduction, getting started, 入门, 简介
---

Bake 是对 `docker build` 命令的一种抽象，它允许您更轻松地以一致的方式为您团队中的每个人管理构建配置（CLI 标志、环境变量等）。

Bake 是内置于 Buildx CLI 的一条命令，因此只要您安装了 Buildx，就可以通过 `docker buildx bake` 命令使用它。

## 使用 Bake 构建项目

以下是一个简单的 `docker build` 命令示例：

```console
$ docker build -f Dockerfile -t myapp:latest .
```

此命令构建当前目录下的 Dockerfile，并将生成的镜像打上 `myapp:latest` 标签。

要使用 Bake 表达相同的构建配置：

```hcl {title=docker-bake.hcl}
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
}
```

Bake 提供了一种结构化的方式来管理您的构建配置，它使您不必每次都记住 `docker build` 的所有 CLI 标志。有了这个文件，构建镜像只需简单地运行：

```console
$ docker buildx bake myapp
```

对于简单的构建，`docker build` 和 `docker buildx bake` 之间的区别微乎其微。然而，随着构建配置变得越来越复杂，Bake 提供了一种更有序的方式来管理这种复杂性，而这通过 `docker build` 的 CLI 标志是很难实现的。它还提供了一种在团队中分享构建配置的方式，确保每个人都使用相同的配置，以一致的方式构建镜像。

## Bake 文件格式

您可以用 HCL、YAML (Docker Compose 文件) 或 JSON 编写 Bake 文件。通常，HCL 是最具表现力和灵活性的格式，这就是为什么在本教程以及使用 Bake 的项目中，您会看到大多数示例都使用 HCL。

可以为目标 (target) 设置的属性与 `docker build` 的 CLI 标志非常相似。例如，考虑以下 `docker build` 命令：

```console
$ docker build \
  -f Dockerfile \
  -t myapp:latest \
  --build-arg foo=bar \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  .
```

对应的 Bake 配置为：

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
> 请查看 [Docker VS Code 扩展 (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它支持 linting、代码导航和漏洞扫描。

## 下一步

要了解更多关于使用 Bake 的信息，请参阅以下主题：

- 了解如何在 Bake 中定义并使用 [目标 (targets)](./targets.md)
- 要查看可为目标设置的所有属性，请参阅 [Bake 文件参考](/build/bake/reference/)