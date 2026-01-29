---
title: Bake 目标
linkTitle: 目标 (Targets)
weight: 20
description: 了解如何在 Bake 中定义和使用目标
keywords: bake, 目标, targets, buildx, docker, buildkit, 默认
---

Bake 文件中的目标代表一次构建调用。它保存了您通常使用标志传递给 `docker build` 命令的所有信息。

```hcl {title=docker-bake.hcl}
target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要使用 Bake 构建一个目标，请将该目标的名称传递给 `bake` 命令。

```console
$ docker buildx bake webapp
```

您可以通过向 `bake` 命令传递多个目标名称来一次构建多个目标。

```console
$ docker buildx bake webapp api tests
```

## 默认目标

如果您在运行 `docker buildx bake` 时没有指定目标，Bake 将构建名为 `default` 的目标。

```hcl {title=docker-bake.hcl}
target "default" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要构建此目标，请运行不带任何参数的 `docker buildx bake`：

```console
$ docker buildx bake
```

## 目标属性

您可以为目标设置的属性与 `docker build` 的 CLI 标志非常相似，并增加了一些 Bake 特有的额外属性。

有关可以为目标设置的所有属性，请参阅 [Bake 参考](/build/bake/reference#target)。

## 对目标进行分组

您可以使用 `group` 块将多个目标组合在一起。当您想要一次构建多个目标时，这非常有用。

```hcl {title=docker-bake.hcl}
group "all" {
  targets = ["webapp", "api", "tests"]
}

target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}

target "api" {
  dockerfile = "api.Dockerfile"
  tags = ["docker.io/username/api:latest"]
  context = "https://github.com/username/api"
}

target "tests" {
  dockerfile = "tests.Dockerfile"
  contexts = {
    webapp = "target:webapp"
    api = "target:api"
  }
  output = ["type=local,dest=build/tests"]
  context = "."
}
```

要构建一个组中的所有目标，请将该组的名称传递给 `bake` 命令。

```console
$ docker buildx bake all
```

## 其他资源

请参阅以下页面以了解更多关于 Bake 功能的信息：

- 了解如何在 Bake 中使用 [变量](./variables.md) 使您的构建配置更加灵活。
- 在 [矩阵](./matrices.md) 中了解如何使用矩阵构建具有不同配置的多个镜像。
- 前往 [Bake 文件参考](/build/bake/reference/) 了解可以在 Bake 文件中设置的所有属性及其语法。
