---
title: 精通 Docker Buildx Bake：多平台构建、测试及更多
linkTitle: 精通 Docker Buildx Bake
description: >
  学习如何使用 Buildx Bake 管理简单和复杂的构建配置。
summary: >
  学习使用 Buildx Bake 通过声明式配置自动化 Docker 构建和测试。
tags: [devops]
languages: [go]
params:
  time: 30 分钟
  featured: true
  image: /images/guides/bake.webp
---

本指南演示如何使用 Docker Buildx Bake 简化和自动化构建镜像、测试和生成构建产物的过程。通过在声明式的 `docker-bake.hcl` 文件中定义构建配置，您可以消除手动脚本，并为复杂构建、测试和产物生成启用高效的工作流。

## 前提假设

本指南假设您熟悉以下内容：

- Docker
- [Buildx](/manuals/build/concepts/overview.md#buildx)
- [BuildKit](/manuals/build/concepts/overview.md#buildkit)
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 前置条件

- 您的机器上安装了最新版本的 Docker。
- 安装了 Git 以克隆仓库。
- 您正在使用 [containerd](/manuals/desktop/features/containerd.md) 镜像存储。

## 简介

本指南使用一个示例项目来演示 Docker Buildx Bake 如何简化您的构建和测试工作流。该仓库包含 Dockerfile 和 `docker-bake.hcl` 文件，为您提供一个可立即使用的设置来尝试 Bake 命令。

首先克隆示例仓库：

```bash
git clone https://github.com/dvdksn/bakeme.git
cd bakeme
```

Bake 文件 `docker-bake.hcl` 使用声明式语法定义构建目标，使用 target 和 group，让您能够高效管理复杂构建。

以下是 Bake 文件的原始内容：

```hcl
target "default" {
  target = "image"
  tags = [
    "bakeme:latest",
  ]
  attest = [
    "type=provenance,mode=max",
    "type=sbom",
  ]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

`target` 关键字为 Bake 定义构建目标。`default` 目标定义了在命令行上未指定特定目标时要构建的目标。以下是 `default` 目标选项的快速摘要：

- `target`：Dockerfile 中的目标构建阶段。
- `tags`：分配给镜像的标签。
- `attest`：附加到镜像的[证明](/manuals/build/metadata/attestations/_index.md)。

  > [!TIP]
  > 证明提供元数据，如构建来源（跟踪镜像构建的来源）和 SBOM（软件物料清单），对安全审计和合规性非常有用。

- `platforms`：要构建的平台变体。

要执行此构建，只需在仓库根目录运行以下命令：

```console
$ docker buildx bake
```

使用 Bake，您可以避免冗长、难以记忆的命令行咒语，通过用结构化配置文件替换手动、容易出错的脚本来简化构建配置管理。

作为对比，以下是不使用 Bake 时此构建命令的样子：

```console
$ docker buildx build \
  --target=image \
  --tag=bakeme:latest \
  --provenance=true \
  --sbom=true \
  --platform=linux/amd64,linux/arm64,linux/riscv64 \
  .
```

## 测试和代码检查

Bake 不仅用于定义构建配置和运行构建。您还可以使用 Bake 运行测试，有效地将 BuildKit 用作任务运行器。在容器中运行测试非常适合确保可重复的结果。本节展示如何添加两种类型的测试：

- 使用 `go test` 进行单元测试。
- 使用 `golangci-lint` 进行代码风格检查。

按照测试驱动开发（TDD）的方式，首先在 Bake 文件中添加一个新的 `test` 目标：

```hcl
target "test" {
  target = "test"
  output = ["type=cacheonly"]
}
```

> [!TIP]
> 使用 `type=cacheonly` 确保构建输出被有效丢弃；层会保存到 BuildKit 的缓存中，但 Buildx 不会尝试将结果加载到 Docker Engine 的镜像存储中。
>
> 对于测试运行，您不需要导出构建输出——只有测试执行才重要。

要执行此 Bake 目标，运行 `docker buildx bake test`。此时，您将收到一个错误，指示 Dockerfile 中不存在 `test` 阶段。

```console
$ docker buildx bake test
[+] Building 1.2s (6/6) FINISHED
 => [internal] load local bake definitions
...
ERROR: failed to solve: target stage "test" could not be found
```

要满足此目标，请添加相应的 Dockerfile 目标。这里的 `test` 阶段基于与构建阶段相同的基础阶段。

```dockerfile
FROM base AS test
RUN --mount=target=. \
    --mount=type=cache,target=/go/pkg/mod \
    go test .
```

> [!TIP]
> [`--mount=type=cache` 指令](/manuals/build/cache/optimize.md#use-cache-mounts)在构建之间缓存 Go 模块，通过避免重新下载依赖项来提高构建性能。此共享缓存确保在构建、测试和其他阶段都可使用相同的依赖集。

现在，使用 Bake 运行 `test` 目标将评估此项目的单元测试。如果您想验证它是否有效，可以对 `main_test.go` 进行任意更改以使测试失败。

接下来，要启用代码检查，在 Bake 文件中添加另一个名为 `lint` 的目标：

```hcl
target "lint" {
  target = "lint"
  output = ["type=cacheonly"]
}
```

并在 Dockerfile 中添加构建阶段。此阶段将使用 Docker Hub 上的官方 `golangci-lint` 镜像。

> [!TIP]
> 由于此阶段依赖于执行外部依赖项，通常最好将要使用的版本定义为构建参数。这使您能够通过将依赖版本集中到 Dockerfile 开头来更轻松地管理未来的版本升级。

```dockerfile {hl_lines=[2,"6-8"]}
ARG GO_VERSION="1.23"
ARG GOLANGCI_LINT_VERSION="1.61"

#...

FROM golangci/golangci-lint:v${GOLANGCI_LINT_VERSION}-alpine AS lint
RUN --mount=target=.,rw \
    golangci-lint run
```

最后，要同时运行两个测试，您可以在 Bake 文件中使用 `groups` 结构。一个组可以指定多个目标，通过单次调用运行。

```hcl
group "validate" {
  targets = ["test", "lint"]
}
```

现在，运行两个测试就像这样简单：

```console
$ docker buildx bake validate
```

## 构建变体

有时您需要构建程序的多个版本。以下示例使用 Bake 通过[矩阵](/manuals/build/bake/matrices.md)构建程序的独立"release"和"debug"变体。使用矩阵可让您运行具有不同配置的并行构建，节省时间并确保一致性。

矩阵将单个构建扩展为多个构建，每个代表矩阵参数的唯一组合。这意味着您可以编排 Bake 并行构建程序的生产版本和开发版本，只需最少的配置更改。

本指南的示例项目设置为使用构建时选项来有条件地启用调试日志和跟踪功能。

- 如果您使用 `go build -tags="debug"` 编译程序，将启用额外的日志和跟踪功能（开发模式）。
- 如果您不使用 `debug` 标签构建，程序将使用默认日志记录器编译（生产模式）。

通过添加定义要构建的变量组合的 matrix 属性来更新 Bake 文件：

```diff {title="docker-bake.hcl"}
 target "default" {
+  matrix = {
+    mode = ["release", "debug"]
+  }
+  name = "image-${mode}"
   target = "image"
```

`matrix` 属性定义要构建的变体（"release"和"debug"）。`name` 属性定义矩阵如何扩展为多个不同的构建目标。在这种情况下，matrix 属性将构建扩展为两个工作流：`image-release` 和 `image-debug`，每个使用不同的配置参数。

接下来，定义一个名为 `BUILD_TAGS` 的构建参数，它接受矩阵变量的值。

```diff {title="docker-bake.hcl"}
   target = "image"
+  args = {
+    BUILD_TAGS = mode
+  }
   tags = [
```

您还需要更改这些构建的镜像标签分配方式。目前，两个矩阵路径都会生成相同的镜像标签名称，并相互覆盖。更新 `tags` 属性，使用条件运算符根据矩阵变量值设置标签。

```diff {title="docker-bake.hcl"}
   tags = [
-    "bakeme:latest",
+    mode == "release" ? "bakeme:latest" : "bakeme:dev"
   ]
```

- 如果 `mode` 是 `release`，标签名为 `bakeme:latest`
- 如果 `mode` 是 `debug`，标签名为 `bakeme:dev`

最后，更新 Dockerfile 以在编译阶段使用 `BUILD_TAGS` 参数。当 `-tags="${BUILD_TAGS}"` 选项计算为 `-tags="debug"` 时，编译器使用 [`debug.go`](https://github.com/dvdksn/bakeme/blob/75c8a41e613829293c4bd3fc3b4f0c573f458f42/debug.go#L1) 文件中的 `configureLogging` 函数。

```diff {title=Dockerfile}
 # build compiles the program
 FROM base AS build
-ARG TARGETOS TARGETARCH
+ARG TARGETOS TARGETARCH BUILD_TAGS
 ENV GOOS=$TARGETOS
 ENV GOARCH=$TARGETARCH
 RUN --mount=target=. \
        --mount=type=cache,target=/go/pkg/mod \
-       go build -o "/usr/bin/bakeme" .
+       go build -tags="${BUILD_TAGS}" -o "/usr/bin/bakeme" .
```

完成。通过这些更改，您的 `docker buildx bake` 命令现在可以构建两个多平台镜像变体。您可以使用 `docker buildx bake --print` 命令检查 Bake 生成的规范构建配置。运行此命令显示 Bake 将运行一个包含两个具有不同构建参数和镜像标签的目标的 `default` 组。

```json {collapse=true}
{
  "group": {
    "default": {
      "targets": ["image-release", "image-debug"]
    }
  },
  "target": {
    "image-debug": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "debug"
      },
      "tags": ["bakeme:dev"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    },
    "image-release": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "release"
      },
      "tags": ["bakeme:latest"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    }
  }
}
```

算上所有平台变体，这意味着构建配置生成 6 个不同的镜像。

```console
$ docker buildx bake
$ docker image ls --tree

IMAGE                   ID             DISK USAGE   CONTENT SIZE   USED
bakeme:dev              f7cb5c08beac       49.3MB         28.9MB
├─ linux/riscv64        0eae8ba0367a       9.18MB         9.18MB
├─ linux/arm64          56561051c49a         30MB         9.89MB
└─ linux/amd64          e8ca65079c1f        9.8MB          9.8MB

bakeme:latest           20065d2c4d22       44.4MB         25.9MB
├─ linux/riscv64        7cc82872695f       8.21MB         8.21MB
├─ linux/arm64          e42220c2b7a3       27.1MB         8.93MB
└─ linux/amd64          af5b2dd64fde       8.78MB         8.78MB
```

## 导出构建产物

导出二进制文件等构建产物对于部署到没有 Docker 或 Kubernetes 的环境非常有用。例如，如果您的程序需要在用户的本地机器上运行。

> [!TIP]
> 本节讨论的技术不仅适用于二进制文件等构建输出，还适用于任何类型的产物，如测试报告。

对于 Go 和 Rust 等编译后二进制文件通常可移植的编程语言，创建仅导出二进制文件的替代构建目标很简单。您只需要在 Dockerfile 中添加一个空阶段，其中只包含要导出的二进制文件。

首先，让我们添加一种快速方法来为本地平台构建二进制文件并将其导出到本地文件系统的 `./build/local`。

在 `docker-bake.hcl` 文件中，创建一个新的 `bin` 目标。在此阶段，将 `output` 属性设置为本地文件系统路径。Buildx 会自动检测到输出看起来像文件路径，并使用[本地导出器](/manuals/build/exporters/local-tar.md)将结果导出到指定路径。

```hcl
target "bin" {
  target = "bin"
  output = ["build/bin"]
  platforms = ["local"]
}
```

请注意，此阶段指定了 `local` 平台。默认情况下，如果未指定 `platforms`，构建目标为 BuildKit 主机的操作系统和架构。如果您使用 Docker Desktop，这通常意味着构建目标为 `linux/amd64` 或 `linux/arm64`，即使您的本地机器是 macOS 或 Windows，因为 Docker 运行在 Linux 虚拟机中。使用 `local` 平台强制目标平台匹配您的本地环境。

接下来，在 Dockerfile 中添加 `bin` 阶段，从构建阶段复制编译的二进制文件。

```dockerfile
FROM scratch AS bin
COPY --from=build "/usr/bin/bakeme" /
```

现在您可以使用 `docker buildx bake bin` 导出本地平台版本的二进制文件。例如，在 macOS 上，此构建目标生成 [Mach-O 格式](https://en.wikipedia.org/wiki/Mach-O)的可执行文件——macOS 的标准可执行格式。

```console
$ docker buildx bake bin
$ file ./build/bin/bakeme
./build/bin/bakeme: Mach-O 64-bit executable arm64
```

接下来，让我们添加一个目标来构建程序的所有平台变体。为此，您可以[继承](/manuals/build/bake/inheritance.md)刚刚创建的 `bin` 目标，并通过添加所需的平台来扩展它。

```hcl
target "bin-cross" {
  inherits = ["bin"]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

现在，构建 `bin-cross` 目标会为所有平台创建二进制文件。子目录会自动为每个变体创建。

```console
$ docker buildx bake bin-cross
$ tree build/
build/
└── bin
    ├── bakeme
    ├── linux_amd64
    │   └── bakeme
    ├── linux_arm64
    │   └── bakeme
    └── linux_riscv64
        └── bakeme

5 directories, 4 files
```

要同时生成"release"和"debug"变体，您可以像使用默认目标那样使用矩阵。使用矩阵时，您还需要根据矩阵值区分输出目录，否则二进制文件会在每次矩阵运行时写入相同位置。

```hcl
target "bin-all" {
  inherits = ["bin-cross"]
  matrix = {
    mode = ["release", "debug"]
  }
  name = "bin-${mode}"
  args = {
    BUILD_TAGS = mode
  }
  output = ["build/bin/${mode}"]
}
```

```console
$ rm -r ./build/
$ docker buildx bake bin-all
$ tree build/
build/
└── bin
    ├── debug
    │   ├── linux_amd64
    │   │   └── bakeme
    │   ├── linux_arm64
    │   │   └── bakeme
    │   └── linux_riscv64
    │       └── bakeme
    └── release
        ├── linux_amd64
        │   └── bakeme
        ├── linux_arm64
        │   └── bakeme
        └── linux_riscv64
            └── bakeme

10 directories, 6 files
```

## 结论

Docker Buildx Bake 简化了复杂的构建工作流，实现高效的多平台构建、测试和产物导出。通过将 Buildx Bake 集成到您的项目中，您可以简化 Docker 构建，使构建配置可移植，并更轻松地处理复杂配置。

尝试不同的配置并扩展您的 Bake 文件以满足项目需求。您可以考虑将 Bake 集成到 CI/CD 流水线中，以自动化构建、测试和产物部署。Buildx Bake 的灵活性和强大功能可以显著改善您的开发和部署流程。

### 延伸阅读

有关如何使用 Bake 的更多信息，请查看以下资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [矩阵目标](/manuals/build/bake/matrices.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [Bake GitHub Action](https://github.com/docker/bake-action)
