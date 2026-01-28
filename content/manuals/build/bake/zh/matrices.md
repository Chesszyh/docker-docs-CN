---
title: 矩阵目标
weight: 70
description: 了解如何在 Bake 中定义和使用矩阵目标，将单个目标分叉为多个不同的变体
keywords: build, buildx, bake, buildkit, matrix, hcl, json
---

矩阵策略允许您根据指定的参数将单个目标分叉为多个不同的变体。这与 [GitHub Actions 的矩阵策略](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)的工作方式类似。您可以使用此功能来减少 Bake 定义中的重复。

matrix 属性是参数名称到值列表的映射。Bake 将每个可能的值组合构建为单独的目标。

每个生成的目标必须具有唯一的名称。要指定目标名称应如何解析，请使用 name 属性。

以下示例将 app 目标解析为 `app-foo` 和 `app-bar`。它还使用矩阵值来定义[目标构建阶段](/build/bake/reference/#targettarget)。

```hcl {title=docker-bake.hcl}
target "app" {
  name = "app-${tgt}"
  matrix = {
    tgt = ["foo", "bar"]
  }
  target = tgt
}
```

```console
$ docker buildx bake --print app
[+] Building 0.0s (0/0)
{
  "group": {
    "app": {
      "targets": [
        "app-foo",
        "app-bar"
      ]
    },
    "default": {
      "targets": [
        "app"
      ]
    }
  },
  "target": {
    "app-bar": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "bar"
    },
    "app-foo": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "foo"
    }
  }
}
```

## 多轴

您可以在矩阵中指定多个键来在多个轴上分叉目标。当使用多个矩阵键时，Bake 会构建每个可能的变体。

以下示例构建四个目标：

- `app-foo-1-0`
- `app-foo-2-0`
- `app-bar-1-0`
- `app-bar-2-0`

```hcl {title=docker-bake.hcl}
target "app" {
  name = "app-${tgt}-${replace(version, ".", "-")}"
  matrix = {
    tgt = ["foo", "bar"]
    version = ["1.0", "2.0"]
  }
  target = tgt
  args = {
    VERSION = version
  }
}
```

## 每个矩阵目标的多个值

如果您想在不只是单个值上区分矩阵，可以使用映射作为矩阵值。Bake 为每个映射创建一个目标，您可以使用点表示法访问嵌套值。

以下示例构建两个目标：

- `app-foo-1-0`
- `app-bar-2-0`

```hcl {title=docker-bake.hcl}
target "app" {
  name = "app-${item.tgt}-${replace(item.version, ".", "-")}"
  matrix = {
    item = [
      {
        tgt = "foo"
        version = "1.0"
      },
      {
        tgt = "bar"
        version = "2.0"
      }
    ]
  }
  target = item.tgt
  args = {
    VERSION = item.version
  }
}
```
