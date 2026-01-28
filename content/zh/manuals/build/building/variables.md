---
title: 构建变量
linkTitle: 变量
weight: 20
description: 使用构建参数和环境变量配置构建
keywords: build, args, variables, parameters, env, environment variables, config
aliases:
- /build/buildkit/color-output-controls/
- /build/building/env-vars/
- /build/guide/build-args/
---

在 Docker Build 中，构建参数（`ARG`）和环境变量（`ENV`）都可以作为向构建过程传递信息的方式。你可以使用它们来参数化构建，实现更灵活和可配置的构建。

> [!WARNING]
>
> 构建参数和环境变量不适合用于向构建传递密钥，因为它们会暴露在最终镜像中。相反，使用密钥挂载或 SSH 挂载，它们可以安全地向构建公开密钥。
>
> 有关更多信息，请参阅[构建密钥](./secrets.md)。

## 相似性和差异性

构建参数和环境变量是相似的。它们都在 Dockerfile 中声明，并且可以使用 `docker build` 命令的标志设置。两者都可以用于参数化构建。但它们各自有不同的用途。

### 构建参数

构建参数是 Dockerfile 本身的变量。使用它们来参数化 Dockerfile 指令的值。例如，你可以使用构建参数指定要安装的依赖项的版本。

除非在指令中使用，构建参数对构建没有影响。除非明确地从 Dockerfile 传递到镜像文件系统或配置中，否则它们不会在从镜像实例化的容器中可访问或存在。它们可能会保留在镜像元数据中，作为出处证明和镜像历史记录，这就是为什么它们不适合保存密钥。

它们使 Dockerfile 更灵活，更易于维护。

有关如何使用构建参数的示例，请参阅 [`ARG` 使用示例](#arg-使用示例)。

### 环境变量

环境变量会传递到构建执行环境，并保留在从镜像实例化的容器中。

环境变量主要用于：

- 配置构建的执行环境
- 为容器设置默认环境变量

如果设置了环境变量，它们可以直接影响构建的执行，以及应用程序的行为或配置。

你无法在构建时覆盖或设置环境变量。环境变量的值必须在 Dockerfile 中声明。你可以将环境变量和构建参数结合使用，以允许在构建时配置环境变量。

有关如何使用环境变量配置构建的示例，请参阅 [`ENV` 使用示例](#env-使用示例)。

## `ARG` 使用示例

构建参数通常用于指定组件的版本，例如构建中使用的镜像变体或包版本。

将版本指定为构建参数可以让你在不必手动更新 Dockerfile 的情况下使用不同的版本进行构建。这也使 Dockerfile 更易于维护，因为它允许你在文件顶部声明版本。

构建参数也可以是在多个地方重用值的一种方式。例如，如果你在构建中使用多种 `alpine` 变体，你可以确保在所有地方使用相同版本的 `alpine`：

- `golang:1.22-alpine${ALPINE_VERSION}`
- `python:3.12-alpine${ALPINE_VERSION}`
- `nginx:1-alpine${ALPINE_VERSION}`

以下示例使用构建参数定义 `node` 和 `alpine` 的版本。

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

在这种情况下，构建参数有默认值。在调用构建时指定它们的值是可选的。要覆盖默认值，你可以使用 `--build-arg` CLI 标志：

```console
$ docker build --build-arg NODE_VERSION=current .
```

有关如何使用构建参数的更多信息，请参考：

- [`ARG` Dockerfile 参考](/reference/dockerfile.md#arg)
- [`docker build --build-arg` 参考](/reference/cli/docker/buildx/build.md#build-arg)

## `ENV` 使用示例

使用 `ENV` 声明环境变量使该变量对构建阶段中的所有后续指令可用。以下示例展示了在使用 `npm` 安装 JavaScript 依赖项之前将 `NODE_ENV` 设置为 `production` 的示例。设置该变量使 `npm` 省略仅用于本地开发所需的包。

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

默认情况下，环境变量在构建时不可配置。如果你想在构建时更改 `ENV` 的值，你可以将环境变量和构建参数结合使用：

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

使用这个 Dockerfile，你可以使用 `--build-arg` 覆盖 `NODE_ENV` 的默认值：

```console
$ docker build --build-arg NODE_ENV=development .
```

请注意，因为你设置的环境变量会保留在容器中，使用它们可能会导致应用程序运行时的意外副作用。

有关如何在构建中使用环境变量的更多信息，请参考：

- [`ENV` Dockerfile 参考](/reference/dockerfile.md#env)

## 作用域

在 Dockerfile 全局作用域中声明的构建参数不会自动继承到构建阶段中。它们只能在全局作用域中访问。

```dockerfile
# syntax=docker/dockerfile:1

# The following build argument is declared in the global scope:
ARG NAME="joe"

FROM alpine
# The following instruction doesn't have access to the $NAME build argument
# because the argument was defined in the global scope, not for this stage.
RUN echo "hello ${NAME}!"
```

此示例中的 `echo` 命令评估为 `hello !`，因为 `NAME` 构建参数的值超出了作用域。要将全局构建参数继承到阶段中，你必须使用它们：

```dockerfile
# syntax=docker/dockerfile:1

# Declare the build argument in the global scope
ARG NAME="joe"

FROM alpine
# Consume the build argument in the build stage
ARG NAME
RUN echo $NAME
```

一旦在阶段中声明或使用了构建参数，它会自动被子阶段继承。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# Declare the build argument in the build stage
ARG NAME="joe"

# Create a new stage based on "base"
FROM base AS build
# The NAME build argument is available here
# since it's declared in a parent stage
RUN echo "hello $NAME!"
```

以下图表进一步说明了构建参数和环境变量继承在多阶段构建中的工作方式。

{{< figure src="../../images/build-variables.svg" class="invertible" >}}

## 预定义构建参数

本节描述默认情况下所有构建可用的预定义构建参数。

### 多平台构建参数

多平台构建参数描述构建的构建平台和目标平台。

构建平台是运行构建器（BuildKit 守护程序）的主机系统的操作系统、架构和平台变体。

- `BUILDPLATFORM`
- `BUILDOS`
- `BUILDARCH`
- `BUILDVARIANT`

目标平台参数保存构建目标平台的相同值，使用 `docker build` 命令的 `--platform` 标志指定。

- `TARGETPLATFORM`
- `TARGETOS`
- `TARGETARCH`
- `TARGETVARIANT`

这些参数对于在多平台构建中进行交叉编译很有用。它们在 Dockerfile 的全局作用域中可用，但它们不会自动被构建阶段继承。要在阶段内使用它们，你必须声明它们：

```dockerfile
# syntax=docker/dockerfile:1

# Pre-defined build arguments are available in the global scope
FROM --platform=$BUILDPLATFORM golang
# To inherit them to a stage, declare them with ARG
ARG TARGETOS
RUN GOOS=$TARGETOS go build -o ./exe .
```

有关多平台构建参数的更多信息，请参阅[多平台参数](/reference/dockerfile.md#automatic-platform-args-in-the-global-scope)

### 代理参数

代理构建参数让你可以为构建指定要使用的代理。你不需要在 Dockerfile 中声明或引用这些参数。使用 `--build-arg` 指定代理就足以让你的构建使用代理。

代理参数默认自动从构建缓存和 `docker history` 的输出中排除。如果你在 Dockerfile 中引用这些参数，代理配置最终会进入构建缓存。

构建器遵循以下代理构建参数。变量不区分大小写。

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `FTP_PROXY`
- `NO_PROXY`
- `ALL_PROXY`

要为你的构建配置代理：

```console
$ docker build --build-arg HTTP_PROXY=https://my-proxy.example.com .
```

有关代理构建参数的更多信息，请参阅[代理参数](/reference/dockerfile.md#predefined-args)。

## 构建工具配置变量

以下环境变量启用、禁用或更改 Buildx 和 BuildKit 的行为。请注意，这些变量不用于配置构建容器；它们在构建内不可用，与 `ENV` 指令无关。它们用于配置 Buildx 客户端或 BuildKit 守护程序。

| 变量                                                                        | 类型              | 描述                                                             |
|-----------------------------------------------------------------------------|-------------------|------------------------------------------------------------------|
| [BUILDKIT_COLORS](#buildkit_colors)                                         | String            | 配置终端输出的文本颜色。                                         |
| [BUILDKIT_HOST](#buildkit_host)                                             | String            | 指定用于远程构建器的主机。                                       |
| [BUILDKIT_PROGRESS](#buildkit_progress)                                     | String            | 配置进度输出的类型。                                             |
| [BUILDKIT_TTY_LOG_LINES](#buildkit_tty_log_lines)                           | String            | 日志行数（TTY 模式下活动步骤的）。                               |
| [BUILDX_BAKE_GIT_AUTH_HEADER](#buildx_bake_git_auth_header)                 | String            | 远程 Bake 文件的 HTTP 认证方案。                                 |
| [BUILDX_BAKE_GIT_AUTH_TOKEN](#buildx_bake_git_auth_token)                   | String            | 远程 Bake 文件的 HTTP 认证令牌。                                 |
| [BUILDX_BAKE_GIT_SSH](#buildx_bake_git_ssh)                                 | String            | 远程 Bake 文件的 SSH 认证。                                      |
| [BUILDX_BUILDER](#buildx_builder)                                           | String            | 指定要使用的构建器实例。                                         |
| [BUILDX_CONFIG](#buildx_config)                                             | String            | 指定配置、状态和日志的位置。                                     |
| [BUILDX_CPU_PROFILE](#buildx_cpu_profile)                                   | String            | 在指定位置生成 `pprof` CPU 配置文件。                            |
| [BUILDX_EXPERIMENTAL](#buildx_experimental)                                 | Boolean           | 开启实验性功能。                                                 |
| [BUILDX_GIT_CHECK_DIRTY](#buildx_git_check_dirty)                           | Boolean           | 启用脏 Git 检出检测。                                            |
| [BUILDX_GIT_INFO](#buildx_git_info)                                         | Boolean           | 在出处证明中移除 Git 信息。                                      |
| [BUILDX_GIT_LABELS](#buildx_git_labels)                                     | String \| Boolean | 向镜像添加 Git 出处标签。                                        |
| [BUILDX_MEM_PROFILE](#buildx_mem_profile)                                   | String            | 在指定位置生成 `pprof` 内存配置文件。                            |
| [BUILDX_METADATA_PROVENANCE](#buildx_metadata_provenance)                   | String \| Boolean | 自定义元数据文件中包含的出处信息。                               |
| [BUILDX_METADATA_WARNINGS](#buildx_metadata_warnings)                       | String            | 在元数据文件中包含构建警告。                                     |
| [BUILDX_NO_DEFAULT_ATTESTATIONS](#buildx_no_default_attestations)           | Boolean           | 关闭默认的出处证明。                                             |
| [BUILDX_NO_DEFAULT_LOAD](#buildx_no_default_load)                           | Boolean           | 默认关闭加载镜像到镜像存储。                                     |
| [EXPERIMENTAL_BUILDKIT_SOURCE_POLICY](#experimental_buildkit_source_policy) | String            | 指定 BuildKit 源策略文件。                                       |

BuildKit 还支持一些额外的配置参数。请参阅 [BuildKit 内置构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)。

你可以用不同的方式表达环境变量的布尔值。例如，`true`、`1` 和 `T` 都评估为 true。评估使用 Go 标准库中的 `strconv.ParseBool` 函数完成。有关详细信息，请参阅[参考文档](https://pkg.go.dev/strconv#ParseBool)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### BUILDKIT_COLORS

更改终端输出的颜色。将 `BUILDKIT_COLORS` 设置为以下格式的 CSV 字符串：

```console
$ export BUILDKIT_COLORS="run=123,20,245:error=yellow:cancel=blue:warning=white"
```

颜色值可以是任何有效的 RGB 十六进制代码，或 [BuildKit 预定义颜色](https://github.com/moby/buildkit/blob/master/util/progress/progressui/colors.go)之一。

将 `NO_COLOR` 设置为任何值都会关闭彩色输出，如 [no-color.org](https://no-color.org/) 所建议的。

### BUILDKIT_HOST

{{< summary-bar feature_name="Buildkit host" >}}

你使用 `BUILDKIT_HOST` 指定用作远程构建器的 BuildKit 守护程序的地址。这与将地址指定为 `docker buildx create` 的位置参数相同。

用法：

```console
$ export BUILDKIT_HOST=tcp://localhost:1234
$ docker buildx create --name=remote --driver=remote
```

如果你同时指定了 `BUILDKIT_HOST` 环境变量和位置参数，则参数优先。

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

你可以通过将 `BUILDKIT_TTY_LOG_LINES` 设置为数字（默认为 `6`）来更改 TTY 模式下活动步骤可见的日志行数。

```console
$ export BUILDKIT_TTY_LOG_LINES=8
```

### EXPERIMENTAL_BUILDKIT_SOURCE_POLICY

让你指定一个 [BuildKit 源策略](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#reproducing-the-pinned-dependencies)文件，用于创建具有固定依赖项的可重现构建。

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

在私有 Git 仓库中使用远程 Bake 定义时设置 HTTP 认证方案。这相当于 [`GIT_AUTH_HEADER` 密钥](./secrets#http-authentication-scheme)，但便于在 Bake 加载远程 Bake 文件时进行预检认证。支持的值为 `bearer`（默认）和 `basic`。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_HEADER=basic
```

### BUILDX_BAKE_GIT_AUTH_TOKEN

{{< summary-bar feature_name="Buildx bake Git auth token" >}}

在私有 Git 仓库中使用远程 Bake 定义时设置 HTTP 认证令牌。这相当于 [`GIT_AUTH_TOKEN` 密钥](./secrets#git-authentication-for-remote-contexts)，但便于在 Bake 加载远程 Bake 文件时进行预检认证。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_TOKEN=$(cat git-token.txt)
```

### BUILDX_BAKE_GIT_SSH

{{< summary-bar feature_name="Buildx bake Git SSH" >}}

让你指定要转发给 Bake 的 SSH 代理套接字文件路径列表，用于在私有仓库中使用远程 Bake 定义时向 Git 服务器进行认证。这类似于构建的 SSH 挂载，但便于在 Bake 解析构建定义时进行预检认证。

通常不需要设置此环境变量，因为 Bake 默认会使用 `SSH_AUTH_SOCK` 代理套接字。你只需要在想使用不同文件路径的套接字时指定此变量。此变量可以使用逗号分隔的字符串接受多个路径。

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

你可以使用 `BUILDX_CONFIG` 指定用于构建配置、状态和日志的目录。此目录的查找顺序如下：

- `$BUILDX_CONFIG`
- `$DOCKER_CONFIG/buildx`
- `~/.docker/buildx`（默认）

用法：

```console
$ export BUILDX_CONFIG=/usr/local/etc
```

### BUILDX_CPU_PROFILE

{{< summary-bar feature_name="Buildx CPU profile" >}}

如果指定，Buildx 会在指定位置生成 `pprof` CPU 配置文件。

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

设置为 true 时，检查[出处证明](/manuals/build/metadata/attestations/slsa-provenance.md)中源代码控制信息的脏状态。

用法：

```console
$ export BUILDX_GIT_CHECK_DIRTY=1
```

### BUILDX_GIT_INFO

{{< summary-bar feature_name="Buildx Git info" >}}

设置为 false 时，从[出处证明](/manuals/build/metadata/attestations/slsa-provenance.md)中移除源代码控制信息。

用法：

```console
$ export BUILDX_GIT_INFO=0
```

### BUILDX_GIT_LABELS

{{< summary-bar feature_name="Buildx Git labels" >}}

根据 Git 信息向你构建的镜像添加出处标签。标签为：

- `com.docker.image.source.entrypoint`：Dockerfile 相对于项目根目录的位置
- `org.opencontainers.image.revision`：Git 提交修订版本
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

- 设置 `BUILDX_GIT_LABELS=1` 包含 `entrypoint` 和 `revision` 标签。
- 设置 `BUILDX_GIT_LABELS=full` 包含所有标签。

如果仓库处于脏状态，`revision` 会获得 `-dirty` 后缀。

### BUILDX_MEM_PROFILE

{{< summary-bar feature_name="Buildx mem profile" >}}

如果指定，Buildx 会在指定位置生成 `pprof` 内存配置文件。

> [!NOTE]
> 此属性仅在开发 Buildx 时有用。分析数据与分析构建性能无关。

用法：

```console
$ export BUILDX_MEM_PROFILE=buildx_mem.prof
```

### BUILDX_METADATA_PROVENANCE

{{< summary-bar feature_name="Buildx metadata provenance" >}}

默认情况下，Buildx 通过 [`--metadata-file` 标志](/reference/cli/docker/buildx/build/#metadata-file)在元数据文件中包含最小的出处信息。此环境变量允许你自定义元数据文件中包含的出处信息：
* `min` 设置最小出处（默认）。
* `max` 设置完整出处。
* `disabled`、`false` 或 `0` 不设置任何出处。

### BUILDX_METADATA_WARNINGS

{{< summary-bar feature_name="Buildx metadata warnings" >}}

默认情况下，Buildx 不通过 [`--metadata-file` 标志](/reference/cli/docker/buildx/build/#metadata-file)在元数据文件中包含构建警告。你可以将此环境变量设置为 `1` 或 `true` 来包含它们。

### BUILDX_NO_DEFAULT_ATTESTATIONS

{{< summary-bar feature_name="Buildx no default" >}}

默认情况下，BuildKit v0.11 及更高版本会向你构建的镜像添加[出处证明](/manuals/build/metadata/attestations/slsa-provenance.md)。设置 `BUILDX_NO_DEFAULT_ATTESTATIONS=1` 以禁用默认的出处证明。

用法：

```console
$ export BUILDX_NO_DEFAULT_ATTESTATIONS=1
```

### BUILDX_NO_DEFAULT_LOAD

当你使用 `docker` 驱动程序构建镜像时，镜像会在构建完成时自动加载到镜像存储中。设置 `BUILDX_NO_DEFAULT_LOAD` 以禁用自动将镜像加载到本地容器存储。

用法：

```console
$ export BUILDX_NO_DEFAULT_LOAD=1
```

<!-- vale Docker.HeadingSentenceCase = YES -->
