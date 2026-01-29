---
title: 覆盖配置
description: 了解如何覆盖 Bake 文件中的配置，以使用不同的属性进行构建。
keywords: build, buildx, bake, buildkit, hcl, json, 覆盖, 配置
aliases:
  - /build/bake/configuring-build/
---

Bake 支持从文件中加载构建定义，但有时您需要更大的灵活性来配置这些定义。例如，您可能希望在特定环境中构建或针对特定目标构建时覆盖某个属性。

以下属性可以被覆盖：

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

要覆盖这些属性，您可以使用以下方法：

- [文件覆盖](#文件覆盖)
- [命令行覆盖](#命令行)
- [环境变量覆盖](#环境变量)

## 文件覆盖

您可以加载多个定义了目标构建配置的 Bake 文件。当您想要将配置分离到不同的文件中以便更好地组织，或者根据加载了哪些文件来有条件地覆盖配置时，这非常有用。

### 默认文件查找

您可以使用 `--file` 或 `-f` 标志来指定要加载的文件。如果您没有指定任何文件，Bake 将按照以下顺序进行查找：

1. `compose.yaml`
2. `compose.yml`
3. `docker-compose.yml`
4. `docker-compose.yaml`
5. `docker-bake.json`
6. `docker-bake.hcl`
7. `docker-bake.override.json`
8. `docker-bake.override.hcl`

如果找到了多个 Bake 文件，所有文件都将被加载并合并为一个定义。文件将按照查找顺序进行合并。

```console
$ docker buildx bake --print
[+] Building 0.0s (1/1) FINISHED                                                                                                                                                                                            
 => [internal] load local bake definitions                                                                                                                                                                             0.0s
 => => reading compose.yaml 45B / 45B                                                                                                                                                                                  0.0s
 => => reading docker-bake.hcl 113B / 113B                                                                                                                                                                             0.0s
 => => reading docker-bake.override.hcl 65B / 65B
```

如果合并的文件包含重复的属性定义，根据属性的不同，这些定义要么被合并，要么被最后一次出现的内容覆盖。

Bake 将尝试按照发现顺序加载所有文件。如果多个文件定义了同一个目标，属性要么被合并，要么被覆盖。在覆盖的情况下，最后加载的内容优先。

例如，给定以下文件：

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

```hcl {title=docker-bake.override.hcl}
variable "TAG" {
  default = "bar"
}
```

由于在默认查找顺序中 `docker-bake.override.hcl` 是最后加载的，因此 `TAG` 变量被覆盖为 `bar`。

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["username/my-app:bar"]
    }
  }
}
```

### 手动文件覆盖

您可以使用 `--file` 标志显式指定要加载的文件，并以此作为有条件地应用覆盖文件的一种方式。

例如，您可以创建一个文件，为特定环境定义一组配置，并且仅在为该环境构建时加载它。以下示例显示了如何加载一个将 `TAG` 变量设置为 `bar` 的 `override.hcl` 文件。随后，该 `TAG` 变量在 `default` 目标中使用。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

```hcl {title=overrides.hcl}
variable "TAG" {
  default = "bar"
}
```

在不带 `--file` 标志的情况下打印构建配置显示 `TAG` 变量被设置为默认值 `foo`。

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:foo"
      ]
    }
  }
}
```

使用 `--file` 标志加载 `overrides.hcl` 文件将 `TAG` 变量覆盖为值 `bar`。

```console
$ docker buildx bake -f docker-bake.hcl -f overrides.hcl --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:bar"
      ]
    }
  }
}
```

## 命令行

您还可以通过命令行的 [`--set` 标志](/reference/cli/docker/buildx/bake.md#set) 来覆盖目标配置：

```hcl
# docker-bake.hcl
target "app" {
  args = {
    mybuildarg = "foo"
  }
}
```

```console
$ docker buildx bake --set app.args.mybuildarg=bar --set app.platform=linux/arm64 app --print
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
        "mybuildarg": "bar"
      },
      "platforms": ["linux/arm64"]
    }
  }
}
```

还支持 [https://golang.org/pkg/path/#Match](https://golang.org/pkg/path/#Match) 中定义的模式匹配语法：

```console
$ docker buildx bake --set foo*.args.mybuildarg=value  # 为所有以 "foo" 开头的目标覆盖构建参数
$ docker buildx bake --set *.platform=linux/arm64      # 为所有目标覆盖平台
$ docker buildx bake --set foo*.no-cache               # 仅对以 "foo" 开头的目标绕过缓存
```

可以通过 `--set` 覆盖的完整属性列表如下：

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

## 环境变量

您还可以使用环境变量来覆盖配置。

Bake 允许您使用环境变量来覆盖 `variable` 块的值。只有 `variable` 块可以通过环境变量覆盖。这意味着您需要在 Bake 文件中定义这些变量，然后设置同名的环境变量来覆盖它。

以下示例显示了如何在 Bake 文件中定义一个带有默认值的 `TAG` 变量，并使用环境变量覆盖它。

```hcl
variable "TAG" {
  default = "latest"
}

target "default" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

```console
$ export TAG=$(git rev-parse --short HEAD)
$ docker buildx bake --print webapp
```

`TAG` 变量被覆盖为环境变量的值，即由 `git rev-parse --short HEAD` 生成的短 commit 哈希。

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
      "tags": ["docker.io/username/webapp:985e9e9"]
    }
  }
}
```

### 类型强制转换

支持使用环境变量覆盖非字符串变量。作为环境变量传递的值会首先被强制转换为合适的类型。

以下示例定义了一个 `PORT` 变量。`backend` 目标原样使用 `PORT` 变量，而 `frontend` 目标使用 `PORT` 的值加 1。

```hcl
variable "PORT" {
  default = 3000
}

group "default" {
  targets = ["backend", "frontend"]
}

target "backend" {
  args = {
    PORT = PORT
  }
}

target "frontend" {
  args = {
    PORT = add(PORT, 1)
  }
}
```

使用环境变量覆盖 `PORT` 时，会先将该值强制转换为预期的类型（整数），然后再运行 `frontend` 目标中的表达式。

```console
$ PORT=7070 docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": [
        "backend",
        "frontend"
      ]
    }
  },
  "target": {
    "backend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7070"
      }
    },
    "frontend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7071"
      }
    }
  }
}
```
