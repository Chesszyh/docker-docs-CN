---
title: Bake 中的变量 (Variables)
linkTitle: 变量 (Variables)
weight: 40
description: 了解如何在 Bake 文件中定义并使用变量
keywords: build, buildx, bake, buildkit, hcl, variables, 变量
---

您可以在 Bake 文件中定义并使用变量，以设置属性值、将其插值到其他值中，或者执行算术运算。变量可以定义默认值，并可以通过环境变量进行覆盖。

## 使用变量作为属性值

使用 `variable` 块来定义一个变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "docker.io/username/webapp:latest"
}
```

以下示例展示了如何在目标 (target) 中使用 `TAG` 变量。

```hcl {title=docker-bake.hcl}
target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [ TAG ]
}
```

## 将变量插值到数值中

Bake 支持将变量以字符串插值的形式嵌入到数值中。您可以使用 `${}` 语法将变量插值。以下示例定义了一个值为 `latest` 的 `TAG` 变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}
```

要将 `TAG` 变量插值到某个属性的值中，请使用 `${TAG}` 语法。

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

使用 `--print` 标志打印 Bake 文件可以查看解析后的构建配置中插值后的结果。

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

## 验证变量 (Validating variables)

要验证变量的值是否符合预期的类型、数值范围或其他条件，您可以使用 `validation` 块定义自定义验证规则。

在以下示例中，验证功能被用于强制执行变量值的数字约束；`PORT` 变量必须等于或大于 1024。

```hcl {title=docker-bake.hcl}
# 定义一个带有默认值和验证规则的变量 `PORT`
variable "PORT" {
  default = 3000  # 为 `PORT` 分配的默认值

  # 验证块，确保 `PORT` 是处于可接受范围内的有效数字
  validation {
    condition = PORT >= 1024  # 确保 `PORT` 至少为 1024
    error_message = "The variable 'PORT' must be 1024 or higher."  # 无效值时的错误消息
  }
}
```

如果 `condition` 表达式的评估结果为 `false`，则认为该变量值无效，构建调用将失败并发出 `error_message`。例如，如果设置 `PORT=443`，则条件评估为 `false`，并抛出错误。

在设置验证之前，数值会被强制转换为预期类型。这确保了通过环境变量设置的任何覆盖操作都能按预期工作。

### 验证多个条件

要评估多个条件，可以为变量定义多个 `validation` 块。所有条件必须同时为 `true`。

示例如下：

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
    # VAR 必须与正则表达式匹配结果完全一致：
    condition = VAR == regex("[a-zA-Z0-9]+", VAR)
    error_message = "The variable 'VAR' can only contain letters and numbers."
  }
}
```

此示例强制执行以下规则：

- 变量不得为空。
- 变量必须匹配特定的字符集。

对于无效输入（如 `VAR="hello@world"`），验证将失败。

### 验证变量间依赖关系

您可以在条件表达式中引用其他 Bake 变量，从而实现强制执行变量间依赖关系的验证。这可确保在继续操作前正确设置了依赖变量。

示例如下：

```hcl {title=docker-bake.hcl}
# 定义变量 `FOO`
variable "FOO" {}

# 定义变量 `BAR`，其验证规则引用了 `FOO`
variable "BAR" {
  # 验证块，确保在使用 `BAR` 时必须设置 `FOO`
  validation {
    condition = FOO != ""  # 检查 `FOO` 是否不是空字符串
    error_message = "The variable 'BAR' requires 'FOO' to be set."
  }
}
```

此配置确保只有在 `FOO` 被分配了非空值时才能使用 `BAR` 变量。如果尝试在未设置 `FOO` 的情况下进行构建，将触发验证错误。

## 对变量插值进行转义

如果您想在解析 Bake 定义时绕过变量插值，请使用双美元符号 (`$${VARIABLE}`)。

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

当指定了多个文件时，一个文件可以使用另一个文件中定义的变量。在以下示例中，`vars.hcl` 文件定义了一个 `BASE_IMAGE` 变量，其默认值为 `docker.io/library/alpine`。

```hcl {title=vars.hcl}
variable "BASE_IMAGE" {
  default = "docker.io/library/alpine"
}
```

以下 `docker-bake.hcl` 文件定义了一个 `BASE_LATEST` 变量，该变量引用了 `BASE_IMAGE` 变量。

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

当您使用 `-f` 标志同时指定 `vars.hcl` 和 `docker-bake.hcl` 并打印解析后的构建配置时，您会看到 `BASE_LATEST` 变量被解析为 `docker.io/library/alpine:latest`。

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

## 额外资源

以下是一些展示如何在 Bake 中使用变量的额外资源：

- 您可以使用环境变量覆盖 `variable` 的值。更多信息请参见 [覆盖配置](./overrides.md#环境变量)。
- 您可以在函数中引用并使用全局变量。参见 [HCL 函数](./funcs.md#函数中的变量)。
- 您可以在求值表达式时使用变量值。参见 [表达式求值](./expressions.md#带有变量的表达式)。