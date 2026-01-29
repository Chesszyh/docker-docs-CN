---
title: 构建变量
linkTitle: 变量 (Variables)
weight: 20
description: 使用构建参数和环境变量配置构建
keywords: build, 构建参数, 变量, 参数, env, 环境变量, 配置
aliases:
- /build/buildkit/color-output-controls/
- /build/building/env-vars/
- /build/guide/build-args/
---

在 Docker 构建中，构建参数 (`ARG`) 和环境变量 (`ENV`) 都是向构建过程传递信息的手段。您可以使用它们来参数化构建，从而实现更灵活且可配置的构建。

> [!WARNING]
>
> 构建参数和环境变量不适合用于向构建传递密钥，因为它们会暴露在最终镜像中。相反，请使用密钥挂载（secret mounts）或 SSH 挂载（SSH mounts），它们能安全地将密钥暴露给构建。
>
> 有关更多信息，请参阅 [构建密钥](./secrets.md)。

## 相同点与不同点

构建参数和环境变量有相似之处。它们都在 Dockerfile 中声明，并且都可以通过 `docker build` 命令的标志进行设置。两者都可用于参数化构建。但它们各自服务的目的不同。

### 构建参数 (Build arguments)

构建参数是 Dockerfile 自身的变量。使用它们可以参数化 Dockerfile 指令的值。例如，您可以使用构建参数指定要安装的依赖项版本。

构建参数除非在指令中使用，否则对构建没有影响。它们在从镜像实例化的容器中是不可访问或不存在的，除非显式地从 Dockerfile 传递到镜像文件系统或配置中。它们可能会持久化在镜像元数据（如来源证明）和镜像历史中，这就是为什么它们不适合保存密钥。

它们使 Dockerfile 更灵活，且更易于维护。

有关如何使用构建参数的示例，请参阅 [`ARG` 使用示例](#arg-使用示例)。

### 环境变量 (Environment variables)

环境变量会被传递到构建执行环境，并持久化在从镜像实例化的容器中。

环境变量主要用于：

- 配置构建的执行环境
- 设置容器的默认环境变量

环境变量如果被设置，可以直接影响构建的执行以及应用程序的行为或配置。

您不能在构建时覆盖或设置环境变量。环境变量的值必须在 Dockerfile 中声明。您可以结合使用环境变量和构建参数，从而允许在构建时配置环境变量。

有关如何使用环境变量配置构建的示例，请参阅 [`ENV` 使用示例](#env-使用示例)。

## `ARG` 使用示例

构建参数通常用于指定构建中使用的组件版本，例如镜像变体或软件包版本。

将版本指定为构建参数可以让您在不手动更新 Dockerfile 的情况下使用不同版本进行构建。这也使得 Dockerfile 的维护更加容易，因为它允许您在文件顶部声明版本。

构建参数也可以是多处复用值的一种方式。例如，如果您在构建中使用了多种风味的 `alpine` ，可以确保在所有地方使用相同的 `alpine` 版本：

- `golang:1.22-alpine${ALPINE_VERSION}`
- `python:3.12-alpine${ALPINE_VERSION}`
- `nginx:1-alpine${ALPINE_VERSION}`

以下示例使用构建参数定义了 `node` 和 `alpine` 的版本。

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION="{{% param example_node_version %}}"
ARG ALPINE_VERSION="{{% param example_alpine_version %}}"

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS base
WORKDIR /src

FROM base AS build
COPY package*.json ./
RUN npm ci
RUN npm run build

FROM base AS production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /src/dist/ .
CMD ["node", "app.js"]
```

在这种情况下，构建参数具有默认值。在调用构建时指定它们的值是可选多。要覆盖默认值，您可以使用 `--build-arg` CLI 标志：

```console
$ docker build --build-arg NODE_VERSION=current .
```

有关如何使用构建参数的更多信息，请参阅：

- [`ARG` Dockerfile 参考](/reference/dockerfile.md#arg)
- [`docker build --build-arg` 参考](/reference/cli/docker/buildx/build.md#build-arg)

## `ENV` 使用示例

使用 `ENV` 声明环境变量会使该变量对构建阶段的所有后续指令可用。以下示例显示了在通过 `npm` 安装 JavaScript 依赖项之前将 `NODE_ENV` 设置为 `production`。设置此变量后，`npm` 会忽略仅供本地开发使用的软件包。

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
WORKDIR /app
COPY package*.json ./
ENV NODE_ENV=production
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

默认情况下，环境变量在构建时不可配置。如果您想在构建时更改 `ENV` 的值，可以结合使用环境变量和构建参数：

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
WORKDIR /app
COPY package*.json ./
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

使用此 Dockerfile，您可以使用 `--build-arg` 覆盖 `NODE_ENV` 的默认值：

```console
$ docker build --build-arg NODE_ENV=development .
```

请注意，由于您设置的环境变量会持久化在容器中，使用它们可能会对应用程序的运行时产生意外的副作用。

有关如何在构建中使用环境变量的更多信息，请参阅：

- [`ENV` Dockerfile 参考](/reference/dockerfile.md#env)

## 作用域 (Scoping)

在 Dockerfile 全局作用域中声明的构建参数不会自动继承到构建阶段中。它们仅在全局作用域内可访问。

```dockerfile
# syntax=docker/dockerfile:1

# 以下构建参数在全局作用域内声明：
ARG NAME="joe"

FROM alpine
# 以下指令无法访问 $NAME 构建参数，
# 因为该参数是在全局作用域定义的，而不是针对此阶段定义的。
RUN echo "hello ${NAME}!"
```

此示例中的 `echo` 命令评估结果为 `hello !` ，因为 `NAME` 构建参数的值不在作用域内。要将全局构建参数继承到某个阶段，您必须显式声明（消耗）它们：

```dockerfile
# syntax=docker/dockerfile:1

# 在全局作用域内声明构建参数
ARG NAME="joe"

FROM alpine
# 在构建阶段中声明使用该构建参数
ARG NAME
RUN echo $NAME
```

一旦在某个阶段声明或声明使用了某个构建参数，它就会被子阶段自动继承。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# 在构建阶段中声明构建参数
ARG NAME="joe"

# 基于 "base" 创建一个新阶段
FROM base AS build
# NAME 构建参数在此处可用，因为它是在父阶段声明的
RUN echo "hello $NAME!"
```

下图进一步展示了构建参数和环境变量的继承在多阶段构建中是如何工作的。

{{< figure src="../../images/build-variables.svg" class="invertible" >}}

## 预定义构建参数

本节介绍默认对所有构建可用的预定义构建参数。

### 多平台构建参数

多平台构建参数描述了构建的构建平台和目标平台。

构建平台（Build platform）是指运行构建器（BuildKit 守护进程）的宿主系统的操作系统、架构和平台变体。

- `BUILDPLATFORM`
- `BUILDOS`
- `BUILDARCH`
- `BUILDVARIANT`

目标平台（Target platform）参数保存了构建的目标平台的值，这些值通过 `docker build` 命令的 `--platform` 标志指定。

- `TARGETPLATFORM`
- `TARGETOS`
- `TARGETARCH`
- `TARGETVARIANT`

这些参数对于在多平台构建中进行交叉编译非常有用。它们在 Dockerfile 的全局作用域内可用，但不会被构建阶段自动继承。要在阶段内使用它们，您必须声明它们：

```dockerfile
# syntax=docker/dockerfile:1

# 预定义构建参数在全局作用域内可用
FROM --platform=$BUILDPLATFORM golang
# 要将它们继承到某个阶段，请使用 ARG 声明它们
ARG TARGETOS
RUN GOOS=$TARGETOS go build -o ./exe .
```

有关多平台构建参数的更多信息，请参阅 [多平台参数](/reference/dockerfile.md#全局作用域中的自动平台参数)。

### 代理参数

代理构建参数允许您指定构建时使用的代理。您不需要在 Dockerfile 中声明或引用这些参数。通过 `--build-arg` 指定代理就足以让您的构建使用该代理。

默认情况下，代理参数会自动从构建缓存和 `docker history` 的输出中排除。如果您确实在 Dockerfile 中引用了这些参数，则代理配置会进入构建缓存。

构建器遵循以下代理构建参数。这些变量不区分大小写。

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `FTP_PROXY`
- `NO_PROXY`
- `ALL_PROXY`

为您的构建配置代理：

```console
$ docker build --build-arg HTTP_PROXY=https://my-proxy.example.com .
```

有关代理构建参数的更多信息，请参阅 [代理参数](/reference/dockerfile.md#predefined-args)。

## 构建工具配置变量

以下环境变量用于启用、禁用或更改 Buildx 和 BuildKit 的行为。请注意，这些变量并不用于配置构建容器；它们在构建内部不可用，且与 `ENV` 指令无关。它们被用于配置 Buildx 客户端或 BuildKit 守护进程。

| 变量 | 类型 | 说明 |
|-----------------------------------------------------------------------------|-------------------|------------------------------------------------------------------|
| [BUILDKIT_COLORS](#buildkit_colors)                                         | 字符串 | 配置终端输出的文本颜色。 |
| [BUILDKIT_HOST](#buildkit_host)                                             | 字符串 | 指定用于远程构建器的主机。 |
| [BUILDKIT_PROGRESS](#buildkit_progress)                                     | 字符串 | 配置进度输出的类型。 |
| [BUILDKIT_TTY_LOG_LINES](#buildkit_tty_log_lines)                           | 字符串 | 日志行数（适用于 TTY 模式下的活动步骤）。 |
| [BUILDX_BAKE_GIT_AUTH_HEADER](#buildx_bake_git_auth_header)                 | 字符串 | 远程 Bake 文件的 HTTP 身份验证方案。 |
| [BUILDX_BAKE_GIT_AUTH_TOKEN](#buildx_bake_git_auth_token)                   | 字符串 | 远程 Bake 文件的 HTTP 身份验证令牌。 |
| [BUILDX_BAKE_GIT_SSH](#buildx_bake_git_ssh)                                 | 字符串 | 远程 Bake 文件的 SSH 身份验证。 |
| [BUILDX_BUILDER](#buildx_builder)                                           | 字符串 | 指定要使用的构建器实例。 |
| [BUILDX_CONFIG](#buildx_config)                                             | 字符串 | 指定配置、状态和日志的位置。 |
| [BUILDX_CPU_PROFILE](#buildx_cpu_profile)                                   | 字符串 | 在指定位置生成 `pprof` CPU 分析文件。 |
| [BUILDX_EXPERIMENTAL](#buildx_experimental)                                 | 布尔值 | 开启实验性功能。 |
| [BUILDX_GIT_CHECK_DIRTY](#buildx_git_check_dirty)                           | 布尔值 | 启用对脏（dirty）Git 检出的检测。 |
| [BUILDX_GIT_INFO](#buildx_git_info)                                         | 布尔值 | 移除来源证明中的 Git 信息。 |
| [BUILDX_GIT_LABELS](#buildx_git_labels)                                     | 字符串 \| 布尔值 | 向镜像添加 Git 来源标签。 |
| [BUILDX_MEM_PROFILE](#buildx_mem_profile)                                   | 字符串 | 在指定位置生成 `pprof` 内存分析文件。 |
| [BUILDX_METADATA_PROVENANCE](#buildx_metadata_provenance)                   | 字符串 \| 布尔值 | 自定义包含在元数据文件中的来源信息。 |
| [BUILDX_METADATA_WARNINGS](#buildx_metadata_warnings)                       | 字符串 | 在元数据文件中包含构建警告。 |
| [BUILDX_NO_DEFAULT_ATTESTATIONS](#buildx_no_default_attestations)           | 布尔值 | 关闭默认的来源证明。 |
| [BUILDX_NO_DEFAULT_LOAD](#buildx_no_default_load)                           | 布尔值 | 默认情况下关闭将镜像加载到镜像库的操作。 |
| [EXPERIMENTAL_BUILDKIT_SOURCE_POLICY](#experimental_buildkit_source_policy) | 字符串 | 指定 BuildKit 源策略文件。 |

BuildKit 还支持一些额外的配置参数。请参阅 [BuildKit 内置构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)。

您可以用不同的方式表示环境变量的布尔值。例如，`true`、`1` 和 `T` 都会被评估为 true。评估是通过 Go 标准库中的 `strconv.ParseBool` 函数完成的。详情请参阅 [参考文档](https://pkg.go.dev/strconv#ParseBool)。

### BUILDKIT_COLORS

更改终端输出的颜色。将 `BUILDKIT_COLORS` 设置为以下格式的 CSV 字符串：

```console
$ export BUILDKIT_COLORS="run=123,20,245:error=yellow:cancel=blue:warning=white"
```

颜色值可以是任何有效的 RGB 十六进制代码，或者是 [BuildKit 预定义颜色](https://github.com/moby/buildkit/blob/master/util/progress/progressui/colors.go) 之一。

根据 [no-color.org](https://no-color.org/) 的建议，将 `NO_COLOR` 设置为任何值都会关闭彩色输出。

### BUILDKIT_HOST

{{< summary-bar feature_name="Buildkit host" >}}

您使用 `BUILDKIT_HOST` 指定用作远程构建器的 BuildKit 守护进程的地址。这与将地址作为 `docker buildx create` 的位置参数指定是一样的。

用法：

```console
$ export BUILDKIT_HOST=tcp://localhost:1234
$ docker buildx create --name=remote --driver=remote
```

如果您同时指定了 `BUILDKIT_HOST` 环境变量和位置参数，则位置参数优先。

### BUILDKIT_PROGRESS

设置 BuildKit 进度输出的类型。有效值为：

- `auto`（默认）
- `plain`
- `tty`
- `quiet`
- `rawjson`

用法：

```console
$ export BUILDKIT_PROGRESS=plain
```

### BUILDKIT_TTY_LOG_LINES

您可以通过将 `BUILDKIT_TTY_LOG_LINES` 设置为一个数字（默认为 `6`）来更改 TTY 模式下活动步骤可见的日志行数。

```console
$ export BUILDKIT_TTY_LOG_LINES=8
```

### EXPERIMENTAL_BUILDKIT_SOURCE_POLICY

允许您指定一个 [BuildKit 源策略 (Source policy)](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#reproducing-the-pinned-dependencies) 文件，用于创建带有固定依赖项的可复现构建。

```console
$ export EXPERIMENTAL_BUILDKIT_SOURCE_POLICY=./policy.json
```

示例：

```json
{
  "rules": [
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "docker-image://docker.io/library/alpine:latest"
      },
      "updates": {
        "identifier": "docker-image://docker.io/library/alpine:latest@sha256:4edbd2beb5f78b1014028f4fbb99f3237d9561100b6881aabbf5acce2c4f9454"
      }
    },
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "https://raw.githubusercontent.com/moby/buildkit/v0.10.1/README.md"
      },
      "updates": {
        "attrs": {"http.checksum": "sha256:6e4b94fc270e708e1068be28bd3551dc6917a4fc5a61293d51bb36e6b75c4b53"}
      }
    },
    {
      "action": "DENY",
      "selector": {
        "identifier": "docker-image://docker.io/library/golang*"
      }
    }
  ]
}
```

### BUILDX_BAKE_GIT_AUTH_HEADER

{{< summary-bar feature_name="Buildx bake Git auth token" >}}

设置在私有 Git 仓库中使用远程 Bake 定义时的 HTTP 身份验证方案。这等同于 [`GIT_AUTH_HEADER` 密钥](./secrets#http-身份验证方案)，但方便了 Bake 在加载远程 Bake 文件时进行预检身份验证。支持的值有 `bearer`（默认）和 `basic`。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_HEADER=basic
```

### BUILDX_BAKE_GIT_AUTH_TOKEN

{{< summary-bar feature_name="Buildx bake Git auth token" >}}

设置在私有 Git 仓库中使用远程 Bake 定义时的 HTTP 身份验证令牌。这等同于 [`GIT_AUTH_TOKEN` 密钥](./secrets#远程上下文的-git-身份验证)，但方便了 Bake 在加载远程 Bake 文件时进行预检身份验证。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_TOKEN=$(cat git-token.txt)
```

### BUILDX_BAKE_GIT_SSH

{{< summary-bar feature_name="Buildx bake Git SSH" >}}

允许您指定一个 SSH 代理套接字（agent socket）文件路径列表，在私有仓库中使用远程 Bake 定义时，将其转发给 Bake 以向 Git 服务器进行身份验证。这类似于构建的 SSH 挂载，但方便了 Bake 在解析构建定义时进行预检身份验证。

通常不需要设置此环境，因为 Bake 默认会使用 `SSH_AUTH_SOCK` 代理套接字。只有当您想使用具有不同文件路径的套接字时，才需要指定此变量。此变量可以通过以逗号分隔的字符串接受多个路径。

用法：

```console
$ export BUILDX_BAKE_GIT_SSH=/run/foo/listener.sock,~/.creds/ssh.sock
```

### BUILDX_BUILDER

覆盖配置的构建器实例。与 `docker buildx --builder` CLI 标志相同。

用法：

```console
$ export BUILDX_BUILDER=my-builder
```

### BUILDX_CONFIG

您可以使用 `BUILDX_CONFIG` 指定用于构建配置、状态和日志的目录。此目录的查找顺序如下：

- `$BUILDX_CONFIG`
- `$DOCKER_CONFIG/buildx`
- `~/.docker/buildx`（默认）

用法：

```console
$ export BUILDX_CONFIG=/usr/local/etc
```

### BUILDX_CPU_PROFILE

{{< summary-bar feature_name="Buildx CPU profile" >}}

如果指定，Buildx 将在指定位置生成 `pprof` CPU 分析文件。

> [!NOTE]
> 此属性仅在开发 Buildx 时有用。分析数据与分析构建性能无关。

用法：

```console
$ export BUILDX_CPU_PROFILE=buildx_cpu.prof
```

### BUILDX_EXPERIMENTAL

启用实验性构建功能。

用法：

```console
$ export BUILDX_EXPERIMENTAL=1
```

### BUILDX_GIT_CHECK_DIRTY

{{< summary-bar feature_name="Buildx Git check dirty" >}}

当设置为 true 时，会检查 [来源证明 (provenance attestations)](/manuals/build/metadata/attestations/slsa-provenance.md) 的源码控制信息中是否存在脏状态。

用法：

```console
$ export BUILDX_GIT_CHECK_DIRTY=1
```

### BUILDX_GIT_INFO

{{< summary-bar feature_name="Buildx Git info" >}}

当设置为 false 时，从 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 中移除源码控制信息。

用法：

```console
$ export BUILDX_GIT_INFO=0
```

### BUILDX_GIT_LABELS

{{< summary-bar feature_name="Buildx Git labels" >}}

根据 Git 信息，为您构建的镜像添加来源标签。这些标签是：

- `com.docker.image.source.entrypoint`：Dockerfile 相对于项目根目录的位置
- `org.opencontainers.image.revision`：Git commit 修订版本
- `org.opencontainers.image.source`：仓库的 SSH 或 HTTPS 地址

示例：

```json
  "Labels": {
    "com.docker.image.source.entrypoint": "Dockerfile",
    "org.opencontainers.image.revision": "5734329c6af43c2ae295010778cd308866b95d9b",
    "org.opencontainers.image.source": "git@github.com:foo/bar.git"
  }
```

用法：

- 设置 `BUILDX_GIT_LABELS=1` 以包含 `entrypoint` 和 `revision` 标签。
- 设置 `BUILDX_GIT_LABELS=full` 以包含所有标签。

如果仓库处于脏状态， `revision` 会加上 `-dirty` 后缀。

### BUILDX_MEM_PROFILE

{{< summary-bar feature_name="Buildx mem profile" >}}

如果指定，Buildx 将在指定位置生成 `pprof` 内存分析文件。

> [!NOTE]
> 此属性仅在开发 Buildx 时有用。分析数据与分析构建性能无关。

用法：

```console
$ export BUILDX_MEM_PROFILE=buildx_mem.prof
```

### BUILDX_METADATA_PROVENANCE

{{< summary-bar feature_name="Buildx metadata provenance" >}}

默认情况下，Buildx 通过 [`--metadata-file` 标志](/reference/cli/docker/buildx/build/#metadata-file) 在元数据文件中包含最少的来源信息。此环境变量允许您自定义元数据文件中包含的来源信息：
* `min` 设置最小来源（默认）。
* `max` 设置完整来源。
* `disabled`、`false` 或 `0` 不设置任何来源。

### BUILDX_METADATA_WARNINGS

{{< summary-bar feature_name="Buildx metadata warnings" >}}

默认情况下，Buildx 不会通过 [`--metadata-file` 标志](/reference/cli/docker/buildx/build/#metadata-file) 在元数据文件中包含构建警告。您可以将此环境变量设置为 `1` 或 `true` 以包含它们。

### BUILDX_NO_DEFAULT_ATTESTATIONS

{{< summary-bar feature_name="Buildx no default" >}}

默认情况下，BuildKit v0.11 及更高版本会为您构建的镜像添加 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。将 `BUILDX_NO_DEFAULT_ATTESTATIONS=1` 设置为禁用默认来源证明。

用法：

```console
$ export BUILDX_NO_DEFAULT_ATTESTATIONS=1
```

### BUILDX_NO_DEFAULT_LOAD

当您使用 `docker` 驱动程序构建镜像时，构建完成后镜像会自动加载到镜像库。将 `BUILDX_NO_DEFAULT_LOAD` 设置为禁用镜像自动加载到本地容器库的操作。

用法：

```console
$ export BUILDX_NO_DEFAULT_LOAD=1
```
