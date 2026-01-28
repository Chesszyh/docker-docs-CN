---
title: Bake 中的表达式求值
linkTitle: 表达式
weight: 50
description: 了解 Bake 的高级功能，如用户定义函数
keywords: build, buildx, bake, buildkit, hcl, expressions, evaluation, math, arithmetic, conditionals
aliases:
  - /build/bake/advanced/
---

HCL 格式的 Bake 文件支持表达式求值，这允许您执行算术运算、有条件地设置值等。

## 算术运算

您可以在表达式中执行算术运算。以下示例展示了如何将两个数字相乘。

```hcl {title=docker-bake.hcl}
sum = 7*6

target "default" {
  args = {
    answer = sum
  }
}
```

使用 `--print` 标志打印 Bake 文件会显示 `answer` 构建参数的计算值。

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "answer": "42"
      }
    }
  }
}
```

## 三元运算符

您可以使用三元运算符有条件地注册一个值。

以下示例仅在变量不为空时添加标签，使用内置的 `notequal` [函数](./funcs.md)。

```hcl {title=docker-bake.hcl}
variable "TAG" {}

target "default" {
  context="."
  dockerfile="Dockerfile"
  tags = [
    "my-image:latest",
    notequal("",TAG) ? "my-image:${TAG}": ""
  ]
}
```

在这种情况下，`TAG` 是一个空字符串，因此生成的构建配置仅包含硬编码的 `my-image:latest` 标签。

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["my-image:latest"]
    }
  }
}
```

## 带变量的表达式

您可以将表达式与[变量](./variables.md)结合使用来有条件地设置值，或执行算术运算。

以下示例使用表达式根据变量的值来设置值。如果变量 `FOO` 大于 5，则 `v1` 构建参数设置为 "higher"，否则设置为 "lower"。如果 `IS_FOO` 变量为 true，则 `v2` 构建参数设置为 "yes"，否则设置为 "no"。

```hcl {title=docker-bake.hcl}
variable "FOO" {
  default = 3
}

variable "IS_FOO" {
  default = true
}

target "app" {
  args = {
    v1 = FOO > 5 ? "higher" : "lower"
    v2 = IS_FOO ? "yes" : "no"
  }
}
```

使用 `--print` 标志打印 Bake 文件会显示 `v1` 和 `v2` 构建参数的计算值。

```console
$ docker buildx bake --print app
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "v1": "lower",
        "v2": "yes"
      }
    }
  }
}
```
