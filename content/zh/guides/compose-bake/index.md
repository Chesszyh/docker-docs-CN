---
title: 使用 Bake 构建 Compose 项目
description: 学习如何使用 Docker Buildx Bake 构建 Docker Compose 项目
summary: |
  本指南演示如何使用 Bake 为 Docker Compose 项目构建生产级镜像。
languages: []
tags: [devops]
params:
  time: 20 分钟
---

本指南探讨如何使用 Bake 为包含多个服务的 Docker Compose 项目构建镜像。

[Docker Buildx Bake](/manuals/build/bake/_index.md) 是一个构建编排工具，支持为构建进行声明式配置，就像 Docker Compose 为定义运行时堆栈所做的那样。对于使用 Docker Compose 启动本地开发服务的项目，Bake 提供了一种无缝扩展项目的方式，实现生产就绪的构建配置。

## 前置条件

本指南假设您熟悉以下内容：

- Docker Compose
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 概述

本指南将使用 [dvdksn/example-voting-app](https://github.com/dvdksn/example-voting-app) 仓库作为使用 Docker Compose 的 monorepo（单体仓库）示例，该仓库可以使用 Bake 进行扩展。

```console
$ git clone https://github.com/dvdksn/example-voting-app.git
$ cd example-voting-app
```

此仓库使用 Docker Compose 在 `compose.yaml` 文件中定义运行应用程序的运行时配置。该应用由以下服务组成：

| 服务     | 描述                                                            |
| -------- | --------------------------------------------------------------- |
| `vote`   | 一个 Python 前端 Web 应用，允许您在两个选项之间投票。            |
| `result` | 一个 Node.js Web 应用，实时显示投票结果。                        |
| `worker` | 一个 .NET 工作进程，消费投票并将其存储到数据库中。               |
| `db`     | 一个由 Docker 卷支持的 Postgres 数据库。                         |
| `redis`  | 一个收集新投票的 Redis 实例。                                    |
| `seed`   | 一个用模拟数据填充数据库的实用工具容器。                         |

`vote`、`result` 和 `worker` 服务从此仓库的代码构建，而 `db` 和 `redis` 使用 Docker Hub 上预先存在的 Postgres 和 Redis 镜像。`seed` 服务是一个实用工具，针对前端服务发起请求以填充数据库，用于测试目的。

## 使用 Compose 构建

当您启动 Docker Compose 项目时，任何定义了 `build` 属性的服务都会在服务启动前自动构建。以下是示例仓库中 `vote` 服务的构建配置：

```yaml {title="compose.yaml"}
services:
  vote:
    build:
      context: ./vote # 构建上下文
      target: dev # Dockerfile 阶段
```

`vote`、`result` 和 `worker` 服务都指定了构建配置。运行 `docker compose up` 将触发这些服务的构建。

您知道也可以仅使用 Compose 来构建服务镜像吗？`docker compose build` 命令允许您使用 Compose 文件中指定的构建配置调用构建。例如，要使用此配置构建 `vote` 服务，运行：

```console
$ docker compose build vote
```

省略服务名称可一次构建所有服务：

```console
$ docker compose build
```

当您只需要构建镜像而不运行服务时，`docker compose build` 命令非常有用。

Compose 文件格式支持许多用于定义构建配置的属性。例如，要指定镜像的标签名称，请在服务上设置 `image` 属性。

```yaml
services:
  vote:
    image: username/vote
    build:
      context: ./vote
      target: dev
    #...

  result:
    image: username/result
    build:
      context: ./result
    #...

  worker:
    image: username/worker
    build:
      context: ./worker
    #...
```

运行 `docker compose build` 会创建三个具有完全限定镜像名称的服务镜像，您可以将其推送到 Docker Hub。

`build` 属性支持[广泛的](/reference/compose-file/build.md)构建配置选项。然而，构建生产级镜像通常与本地开发中使用的镜像不同。为避免在 Compose 文件中添加可能不适合本地构建的构建配置，可以考虑使用 Bake 来构建发布镜像，从而将生产构建与本地构建分离。这种方法分离关注点：使用 Compose 进行本地开发，使用 Bake 进行生产就绪构建，同时仍然重用服务定义和基本构建配置。

## 使用 Bake 构建

与 Compose 一样，Bake 从配置文件解析项目的构建定义。Bake 支持 HashiCorp 配置语言（HCL）、JSON 和 Docker Compose YAML 格式。当您将 Bake 与多个文件一起使用时，它会找到并合并所有适用的配置文件为一个统一的构建配置。Compose 文件中定义的构建选项会被 Bake 文件中指定的选项扩展或在某些情况下覆盖。

以下部分探讨如何使用 Bake 扩展 Compose 文件中定义的生产构建选项。

### 查看构建配置

Bake 会自动从服务的 `build` 属性创建构建配置。使用 Bake 的 `--print` 标志查看给定 Compose 文件的构建配置。此标志评估构建配置并以 JSON 格式输出构建定义。

```console
$ docker buildx bake --print
```

JSON 格式的输出显示将要执行的组以及该组的所有目标。组是构建的集合，目标代表单个构建。

```json
{
  "group": {
    "default": {
      "targets": [
        "vote",
        "result",
        "worker",
        "seed"
      ]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
    },
    "seed": {
      "context": "seed-data",
      "dockerfile": "Dockerfile",
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "target": "dev",
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
    }
  }
}
```

如您所见，Bake 创建了一个包含四个目标的 `default` 组：

- `seed`
- `vote`
- `result`
- `worker`

此组从您的 Compose 文件自动创建；它包含所有包含构建配置的服务。要使用 Bake 构建这组服务，运行：

```console
$ docker buildx bake
```

### 自定义构建组

首先重新定义 Bake 执行的默认构建组。当前默认组包含 `seed` 目标——一个仅用于用模拟数据填充数据库的 Compose 服务。由于此目标不生成生产镜像，因此不需要包含在构建组中。

要自定义 Bake 使用的构建配置，在仓库根目录与 `compose.yaml` 文件并列创建一个名为 `docker-bake.hcl` 的新文件。

```console
$ touch docker-bake.hcl
```

打开 Bake 文件并添加以下配置：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["vote", "result", "worker"]
}
```

保存文件并再次打印您的 Bake 定义。

```console
$ docker buildx bake --print
```

JSON 输出显示 `default` 组只包含您关心的目标。

```json
{
  "group": {
    "default": {
      "targets": ["vote", "result", "worker"]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
      "tags": ["username/result"]
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "dev"
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
      "tags": ["username/worker"]
    }
  }
}
```

这里，每个目标的构建配置（context、tags 等）从 `compose.yaml` 文件获取。组由 `docker-bake.hcl` 文件定义。

### 自定义目标

Compose 文件当前将 `dev` 阶段定义为 `vote` 服务的构建目标。这对于在本地开发中运行的镜像是合适的，因为 `dev` 阶段包含额外的开发依赖项和配置。然而，对于生产镜像，您需要改为目标 `final` 镜像。

要修改 `vote` 服务使用的目标阶段，在 Bake 文件中添加以下配置：

```hcl
target "vote" {
  target = "final"
}
```

这会在使用 Bake 运行构建时用不同的值覆盖 Compose 文件中指定的 `target` 属性。Compose 文件中的其他构建选项（tag、context）保持不变。您可以通过使用 `docker buildx bake --print vote` 检查 `vote` 目标的构建配置来验证：

```json
{
  "group": {
    "default": {
      "targets": ["vote"]
    }
  },
  "target": {
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "final"
    }
  }
}
```

### 附加构建功能

生产级构建通常具有与开发构建不同的特性。以下是您可能想要为生产镜像添加的一些示例。

多平台
: 对于本地开发，您只需要为本地平台构建镜像，因为这些镜像只会在您的机器上运行。但对于推送到注册表的镜像，通常最好为多个平台构建，特别是 arm64 和 amd64。

证明
: [证明](/manuals/build/metadata/attestations/_index.md)是附加到镜像的清单，描述镜像是如何创建的以及它包含哪些组件。将证明附加到镜像有助于确保镜像遵循软件供应链最佳实践。

注解
: [注解](/manuals/build/metadata/annotations.md)为镜像提供描述性元数据。使用注解记录任意信息并将其附加到镜像，这有助于消费者和工具了解镜像的来源、内容以及如何使用。

> [!TIP]
> 为什么不直接在 Compose 文件中定义这些附加构建选项？
>
> Compose 文件格式中的 `build` 属性不支持所有构建功能。此外，某些功能（如多平台构建）可能会大幅增加构建服务所需的时间。对于本地开发，最好保持构建步骤简单快速，将额外功能留给发布构建。

要将这些属性添加到使用 Bake 构建的镜像，请按如下方式更新 Bake 文件：

```hcl
group "default" {
  targets = ["vote", "result", "worker"]
}

target "_common" {
  annotations = ["org.opencontainers.image.authors=username"]
  platforms = ["linux/amd64", "linux/arm64"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
}

target "vote" {
  inherits = ["_common"]
  target = "final"
}

target "result" {
  inherits = ["_common"]
}

target "worker" {
  inherits = ["_common"]
}
```

这定义了一个新的 `_common` 目标，它定义了可重用的构建配置，用于向镜像添加多平台支持、注解和证明。此可重用目标由构建目标继承。

通过这些更改，使用 Bake 构建项目会为 `linux/amd64` 和 `linux/arm64` 架构生成三组多平台镜像。每个镜像都附有作者注解，以及 SBOM 和来源证明记录。

## 结论

本指南中演示的模式为使用 Docker Compose 的项目管理生产就绪 Docker 镜像提供了一种有用的方法。使用 Bake 可以让您访问 Buildx 和 BuildKit 的所有强大功能，并且还有助于以合理的方式分离开发和构建配置。

### 延伸阅读

有关如何使用 Bake 的更多信息，请查看以下资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [从 Compose 文件使用 Bake 构建](/manuals/build/bake/compose-file.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [精通 Docker Buildx Bake：多平台构建、测试及更多](/guides/bake/index.md)
- [Bake GitHub Action](https://github.com/docker/bake-action)
