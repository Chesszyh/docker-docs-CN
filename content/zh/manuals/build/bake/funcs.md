---
title: 函数 (Functions)
weight: 60
description: 了解如何在 Bake 中使用内置和用户自定义的 HCL 函数
keywords: build, buildx, bake, buildkit, hcl, functions, user-defined, built-in, custom, gocty, 函数
---

当您需要以比简单的字符串拼接或插值更复杂的方式处理构建配置中的数值时，HCL 函数非常有用。

## 标准库

Bake 内置支持 [`go-cty` 标准库函数](https://github.com/zclconf/go-cty/tree/main/cty/function/stdlib)。以下示例展示了 `add` 函数的用法。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${add(123, 1)}"
  }
}
```

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## 用户自定义函数

如果内置的标准库函数无法满足您的需求，您可以创建 [用户自定义函数](https://github.com/hashicorp/hcl/tree/main/ext/userfunc) 来实现您想要的功能。

以下示例定义了一个 `increment` 函数。

```hcl {title=docker-bake.hcl}
function "increment" {
  params = [number]
  result = number + 1
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${increment(123)}"
  }
}
```

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## 函数中的变量

您可以在函数内部引用 [变量](./variables) 和标准库函数。

您不能在函数中引用其他用户自定义函数。

以下示例在自定义函数中使用了一个全局变量 (`REPO`)。

```hcl {title=docker-bake.hcl}
# docker-bake.hcl
variable "REPO" {
  default = "user/repo"
}

function "tag" {
  params = [tag]
  result = ["${REPO}:${tag}"]
}

target "webapp" {
  tags = tag("v1")
}
```

使用 `--print` 标志打印 Bake 文件显示，`tag` 函数使用了 `REPO` 的值来设置标签的前缀。

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["user/repo:v1"]
    }
  }
}
```