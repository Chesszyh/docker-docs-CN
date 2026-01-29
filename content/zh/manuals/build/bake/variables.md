---
title: Bake 中的变量
linkTitle: 变量 (Variables)
weight: 40
description: 
keywords: build, buildx, bake, buildkit, hcl, 变量
---

您可以在 Bake 文件中定义和使用变量来设置属性值、将其插值到其他值中以及执行算术运算。变量可以定义默认值，并且可以通过环境变量进行覆盖。

## 使用变量作为属性值

使用 `variable` 块来定义变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "docker.io/username/webapp:latest"
}
```

以下示例显示了如何在目标中使用 `TAG` 变量。

```hcl {title=docker-bake.hcl}
target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [ TAG ]
}
```

## 将变量插值到值中

Bake 支持将变量通过字符串插值到值中。您可以使用 `${}` 语法将变量插值到值中。以下示例定义了一个值为 `latest` 的 `TAG` 变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}
```

要将 `TAG` 变量插值到属性的值中，请使用 `${TAG}` 语法。

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

使用 `--print` 标志打印 Bake 文件显示了已解析的构建配置中的插值。

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

要验证变量的值是否符合预期类型、值范围或其他条件，可以使用 `validation` 块定义自定义验证规则。

在以下示例中，验证用于对变量值强制执行数值约束；`PORT` 变量必须大于或等于 1024。

```hcl {title=docker-bake.hcl}
# 定义一个带有默认值和验证规则的变量 `PORT`
variable "PORT" {
  default = 3000  # 分配给 `PORT` 的默认值

  # 验证块，确保 `PORT` 是在可接受范围内的有效数字
  validation {
    condition = PORT >= 1024  # 确保 `PORT` 至少为 1024
    error_message = "变量 'PORT' 必须大于或等于 1024。"  # 无效值时的错误消息
  }
}
```

如果 `condition` 表达式的评估结果为 `false`，则该变量值被视为无效，从而导致构建调用失败并发出 `error_message`。例如，如果 `PORT=443`，则条件评估为 `false`，并触发错误。

在设置验证之前，值会被强制转换为预期的类型。这确保了使用环境变量设置的任何覆盖都能按预期工作。

### 验证多个条件

要评估多个条件，请为变量定义多个 `validation` 块。所有条件必须均为 `true`。

示例如下：

```hcl {title=docker-bake.hcl}
# 定义一个带有多个验证规则的变量 `VAR`
variable "VAR" {
  # 第一个验证块：确保变量不能为空
  validation {
    condition = VAR != ""
    error_message = "变量 'VAR' 不能为空。"
  }

  # 第二个验证块：确保值仅包含字母数字字符
  validation {
    # VAR 必须与正则表达式匹配结果完全一致：
    condition = VAR == regex("[a-zA-Z0-9]+", VAR)
    error_message = "变量 'VAR' 只能包含字母和数字。"
  }
}
```

此示例强制执行：

- 变量不能为空。
- 变量必须匹配特定的字符集。

对于像 `VAR="hello@world"` 这样的无效输入，验证将失败。

### 验证变量依赖关系

您可以在条件表达式中引用其他 Bake 变量，从而实现强制变量间依赖关系的验证。这可确保在继续操作之前正确设置了相关的依赖变量。

示例如下：

```hcl {title=docker-bake.hcl}
# 定义变量 `FOO`
variable "FOO" {}

# 定义带有引用 `FOO` 的验证规则的变量 `BAR`
variable "BAR" {
  # 验证块，确保在使用 `BAR` 时已设置 `FOO`
  validation {
    condition = FOO != ""  # 检查 `FOO` 是否不是空字符串
    error_message = "变量 'BAR' 要求必须设置 'FOO'。"
  }
}
```

此配置确保仅在 `FOO` 已分配非空值时才能使用 `BAR` 变量。尝试在未设置 `FOO` 的情况下进行构建将触发验证错误。

## 转义变量插值

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

## 跨文件使用变量中的变量

当指定了多个文件时，一个文件可以使用在另一个文件中定义的变量。在以下示例中，`vars.hcl` 文件定义了一个默认值为 `docker.io/library/alpine` 的 `BASE_IMAGE` 变量。

```hcl {title=vars.hcl}
variable "BASE_IMAGE" {
  default = "docker.io/library/alpine"
}
```

以下 `docker-bake.hcl` 文件定义了一个引用了 `BASE_IMAGE` 变量的 `BASE_LATEST` 变量。

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

当您使用 `-f` 标志指定 `vars.hcl` 和 `docker-bake.hcl` 文件来打印已解析的构建配置时，您会看到 `BASE_LATEST` 变量被解析为 `docker.io/library/alpine:latest`。

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

## 其他资源

以下是一些展示如何在 Bake 中使用变量的其他资源：

- 您可以使用环境变量覆盖 `variable` 的值。有关更多信息，请参阅 [覆盖配置](./overrides.md#环境变量)。
- 您可以在函数中引用并使用全局变量。请参阅 [HCL 函数](./funcs.md#函数中的变量)。
- 您可以在评估表达式时使用变量值。请参阅 [表达式评估](./expressions.md#带有变量的表达式)。
