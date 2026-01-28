---
title: Bake 中的变量
linkTitle: 变量
weight: 40
description:
keywords: build, buildx, bake, buildkit, hcl, variables
---

您可以在 Bake 文件中定义和使用变量来设置属性值、将它们插入到其他值中以及执行算术运算。变量可以用默认值定义，并可以用环境变量覆盖。

## 将变量用作属性值

使用 `variable` 块定义变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "docker.io/username/webapp:latest"
}
```

以下示例展示了如何在目标中使用 `TAG` 变量。

```hcl {title=docker-bake.hcl}
target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [ TAG ]
}
```

## 将变量插入到值中

Bake 支持将变量字符串插值到值中。您可以使用 `${}` 语法将变量插入到值中。以下示例定义了一个值为 `latest` 的 `TAG` 变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}
```

要将 `TAG` 变量插入到属性值中，请使用 `${TAG}` 语法。

```hcl {title=docker-bake.hcl}
group "default" {
  targets = [ "webapp" ]
}

variable "TAG" {
  default = "latest"
}

target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

使用 `--print` 标志打印 Bake 文件会在解析的构建配置中显示插值后的值。

```console
$ docker buildx bake --print
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
      "tags": ["docker.io/username/webapp:latest"]
    }
  }
}
```

## 验证变量

要验证变量的值是否符合预期的类型、值范围或其他条件，您可以使用 `validation` 块定义自定义验证规则。

在以下示例中，验证用于对变量值强制执行数字约束；`PORT` 变量必须是 1024 或更高。

```hcl {title=docker-bake.hcl}
# 定义一个带有默认值和验证规则的变量 `PORT`
variable "PORT" {
  default = 3000  # 分配给 `PORT` 的默认值

  # 验证块，确保 `PORT` 是可接受范围内的有效数字
  validation {
    condition = PORT >= 1024  # 确保 `PORT` 至少为 1024
    error_message = "The variable 'PORT' must be 1024 or higher."  # 无效值的错误消息
  }
}
```

如果 `condition` 表达式求值为 `false`，则变量值被认为无效，构建调用将失败并发出 `error_message`。例如，如果 `PORT=443`，条件求值为 `false`，并引发错误。

在设置验证之前，值会被强制转换为预期类型。这确保使用环境变量设置的任何覆盖都能按预期工作。

### 验证多个条件

要评估多个条件，请为变量定义多个 `validation` 块。所有条件必须为 `true`。

以下是一个示例：

```hcl {title=docker-bake.hcl}
# 定义一个带有多个验证规则的变量 `VAR`
variable "VAR" {
  # 第一个验证块：确保变量不为空
  validation {
    condition = VAR != ""
    error_message = "The variable 'VAR' must not be empty."
  }

  # 第二个验证块：确保值仅包含字母数字字符
  validation {
    # VAR 和正则表达式匹配结果必须相同：
    condition = VAR == regex("[a-zA-Z0-9]+", VAR)
    error_message = "The variable 'VAR' can only contain letters and numbers."
  }
}
```

此示例强制执行：

- 变量不能为空。
- 变量必须匹配特定的字符集。

对于像 `VAR="hello@world"` 这样的无效输入，验证将失败。

### 验证变量依赖关系

您可以在条件表达式中引用其他 Bake 变量，从而实现强制变量之间依赖关系的验证。这确保在继续之前正确设置了依赖变量。

以下是一个示例：

```hcl {title=docker-bake.hcl}
# 定义一个变量 `FOO`
variable "FOO" {}

# 定义一个带有引用 `FOO` 的验证规则的变量 `BAR`
variable "BAR" {
  # 验证块，确保如果使用 `BAR`，则 `FOO` 必须已设置
  validation {
    condition = FOO != ""  # 检查 `FOO` 不是空字符串
    error_message = "The variable 'BAR' requires 'FOO' to be set."
  }
}
```

此配置确保只有在 `FOO` 被赋予非空值时才能使用 `BAR` 变量。尝试在不设置 `FOO` 的情况下构建将触发验证错误。

## 转义变量插值

如果您想在解析 Bake 定义时绕过变量插值，请使用双美元符号（`$${VARIABLE}`）。

```hcl {title=docker-bake.hcl}
target "webapp" {
  dockerfile-inline = <<EOF
  FROM alpine
  ARG TARGETARCH
  RUN echo "Building for $${TARGETARCH/amd64/x64}"
  EOF
  platforms = ["linux/amd64", "linux/arm64"]
}
```

```console
$ docker buildx bake --progress=plain
...
#8 [linux/arm64 2/2] RUN echo "Building for arm64"
#8 0.036 Building for arm64
#8 DONE 0.0s

#9 [linux/amd64 2/2] RUN echo "Building for x64"
#9 0.046 Building for x64
#9 DONE 0.1s
...
```

## 跨文件在变量中使用变量

当指定多个文件时，一个文件可以使用另一个文件中定义的变量。在以下示例中，`vars.hcl` 文件定义了一个默认值为 `docker.io/library/alpine` 的 `BASE_IMAGE` 变量。

```hcl {title=vars.hcl}
variable "BASE_IMAGE" {
  default = "docker.io/library/alpine"
}
```

以下 `docker-bake.hcl` 文件定义了一个引用 `BASE_IMAGE` 变量的 `BASE_LATEST` 变量。

```hcl {title=docker-bake.hcl}
variable "BASE_LATEST" {
  default = "${BASE_IMAGE}:latest"
}

target "webapp" {
  contexts = {
    base = BASE_LATEST
  }
}
```

当您使用 `-f` 标志指定 `vars.hcl` 和 `docker-bake.hcl` 文件打印解析的构建配置时，您会看到 `BASE_LATEST` 变量被解析为 `docker.io/library/alpine:latest`。

```console
$ docker buildx bake -f vars.hcl -f docker-bake.hcl --print app
```

```json
{
  "target": {
    "webapp": {
      "context": ".",
      "contexts": {
        "base": "docker.io/library/alpine:latest"
      },
      "dockerfile": "Dockerfile"
    }
  }
}
```

## 附加资源

以下是一些展示如何在 Bake 中使用变量的附加资源：

- 您可以使用环境变量覆盖 `variable` 值。有关更多信息，请参阅[覆盖配置](./overrides.md#environment-variables)。
- 您可以在函数中引用和使用全局变量。请参阅 [HCL 函数](./funcs.md#variables-in-functions)
- 您可以在计算表达式时使用变量值。请参阅[表达式求值](./expressions.md#expressions-with-variables)
