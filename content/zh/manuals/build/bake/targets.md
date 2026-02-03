---
title: Bake 目标 (Targets)
linkTitle: 目标 (Targets)
weight: 20
description: 了解如何在 Bake 中定义并使用目标
keywords: bake, target, targets, buildx, docker, buildkit, default, 目标
---

Bake 文件中的一个目标 (target) 代表一次构建调用。它保存了您通常在 `docker build` 命令中使用标志传递的所有信息。

```hcl {title=docker-bake.hcl}
target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要使用 Bake 构建某个目标，请将该目标的名称传递给 `bake` 命令。

```console
$ docker buildx bake webapp
```

您可以通过向 `bake` 命令传递多个目标名称来一次性构建多个目标。

```console
$ docker buildx bake webapp api tests
```

## 默认目标 (Default target)

如果您在运行 `docker buildx bake` 时未指定目标，Bake 将构建名为 `default` 的目标。

```hcl {title=docker-bake.hcl}
target "default" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要构建此目标，只需运行不带任何参数的 `docker buildx bake`：

```console
$ docker buildx bake
```

## 目标属性

您可以为目标设置的属性与 `docker build` 的 CLI 标志非常相似，并增加了一些特定于 Bake 的额外属性。

欲了解可为目标设置的所有属性，请参阅 [Bake 参考](/build/bake/reference#target)。

## 对目标进行分组

您可以使用 `group` 块将多个目标组合在一起。当您想一次性构建多个目标时，这非常有用。

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

要构建组中的所有目标，请将该组的名称传递给 `bake` 命令。

```console
$ docker buildx bake all
```

## 额外资源

参考以下页面了解更多关于 Bake 功能的信息：

- 了解如何使用 Bake 中的 [变量 (variables)](./variables.md) 使您的构建配置更加灵活。
- 了解如何使用 [矩阵 (matrices)](./matrices.md) 以不同的配置构建多个镜像。
- 前往 [Bake 文件参考](/build/bake/reference/) 了解您可以配置的所有属性及其语法。