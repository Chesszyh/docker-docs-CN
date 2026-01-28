---
title: 使用 Docker Hardened Image
linktitle: 使用镜像
description: 了解如何在 Dockerfile、CI 流水线和标准开发工作流中拉取、运行和引用 Docker Hardened Images。
keywords: use hardened image, docker pull secure image, non-root containers, multi-stage dockerfile, dev image variant
weight: 30
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

您可以像使用 Docker Hub 上的任何其他镜像一样使用 Docker Hardened Image（DHI）。DHI 遵循相同的熟悉使用模式。使用 `docker pull` 拉取它们，在 Dockerfile 中引用它们，并使用 `docker run` 运行容器。

关键区别在于 DHI 以安全为重点，有意保持最小化以减少攻击面。这意味着某些变体不包含 shell 或包管理器，并且可能默认以非 root 用户运行。

> [!NOTE]
>
> 您无需更改现有工作流。无论您是手动拉取镜像、在 Dockerfile 中引用它们，还是将它们集成到 CI 流水线中，DHI 的工作方式与您已经使用的镜像相同。

将 DHI [镜像](./mirror.md)到您组织的命名空间后，镜像即可使用。要找到您镜像的仓库，请前往 Hardened Images 目录中原始镜像的页面，然后选择 **View in repository** 以显示镜像仓库列表。

## 采用 DHI 时的注意事项

Docker Hardened Images 有意保持最小化以提高安全性。如果您正在更新现有的 Dockerfile 或框架以使用 DHI，请记住以下注意事项：

| 特性            | 详情                                                                                                                                                                                                                                               |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 无 shell 或包管理器 | 运行时镜像不包含 shell 或包管理器。在构建阶段使用 `-dev` 或 `-sdk` 变体运行 shell 命令或安装软件包，然后将制品复制到最小化的运行时镜像。                                         |
| 非 root 运行时    | 运行时 DHI 默认以非 root 用户运行。确保您的应用不需要特权访问，并且所有需要的文件对非 root 用户可读和可执行。                                                             |
| 端口               | 以非 root 用户运行的应用在旧版本的 Docker 或某些 Kubernetes 配置中无法绑定到低于 1024 的端口。为了兼容性，请使用高于 1024 的端口。                                             |
| 入口点         | DHI 可能不包含默认入口点，或者可能使用与您熟悉的原始镜像不同的入口点。检查镜像配置并相应地更新您的 `CMD` 或 `ENTRYPOINT` 指令。                                        |
| 多阶段构建  | 始终为框架使用多阶段构建：使用 `-dev` 镜像进行构建或安装依赖项，使用最小化的运行时镜像作为最终阶段。                                                                                                              |
| TLS 证书    | DHI 包含标准 TLS 证书。您无需手动安装 CA 证书。                                                                                                                                                               |

如果您正在迁移现有应用，请参阅[迁移现有应用以使用 Docker Hardened Images](./migrate.md)。

## 在 Dockerfile 中使用 DHI

要将 DHI 用作容器的基础镜像，请在 Dockerfile 的 `FROM` 指令中指定它：

```dockerfile
FROM <your-namespace>/dhi-<image>:<tag>
```

将镜像名称和标签替换为您要使用的变体。例如，如果您在构建阶段需要 shell 或包管理器，请使用 `-dev` 标签：

```dockerfile
FROM <your-namespace>/dhi-python:3.13-dev AS build
```

要了解如何探索可用变体，请参阅[探索镜像](./explore.md)。

> [!TIP]
>
> 使用多阶段 Dockerfile 分离构建和运行时阶段，在构建阶段使用 `-dev` 变体，在最终阶段使用最小化的运行时镜像。

## 从 Docker Hub 拉取 DHI

就像 Docker Hub 上的任何其他镜像一样，您可以使用 Docker CLI、Docker Hub Registry API 或在 CI 流水线中拉取 Docker Hardened Images（DHI）。

以下示例展示了如何使用 CLI 拉取 DHI：

```console
$ docker pull <your-namespace>/dhi-<image>:<tag>
```

您必须有权访问 Docker Hub 命名空间中的镜像。有关更多信息，请参阅[镜像 Docker Hardened Image](./mirror.md)。

## 运行 DHI

拉取镜像后，您可以使用 `docker run` 运行它。例如，假设仓库已镜像到您组织命名空间中的 `dhi-python`，启动一个容器并运行 Python 命令：

```console
$ docker run --rm <your-namespace>/dhi-python:3.13 python -c "print('Hello from DHI')"
```

## 在 CI/CD 流水线中使用 DHI

Docker Hardened Images 在您的 CI/CD 流水线中的工作方式与任何其他镜像相同。您可以在 Dockerfile 中引用它们，将它们作为流水线步骤的一部分拉取，或在构建和测试期间运行基于它们的容器。

与典型的容器镜像不同，DHI 还包含签名的[证明](../core-concepts/attestations.md)，如 SBOM 和来源元数据。如果您的工具支持，您可以将这些整合到流水线中以支持供应链安全、策略检查或审计要求。

为了加强您的软件供应链，请考虑在从 DHI 构建镜像时添加您自己的证明。这使您能够记录镜像的构建方式、验证其完整性，并使用 Docker Scout 等工具启用下游验证和[策略强制执行](./policies.md)。

要了解如何在构建过程中附加证明，请参阅 [Docker Build 证明](/manuals/build/metadata/attestations.md)。

## 为编译的可执行文件使用静态镜像

Docker Hardened Images 包含一个 `static` 镜像仓库，专门设计用于在极度最小化和安全的运行时中运行编译的可执行文件。

在较早的阶段使用 `-dev` 或其他构建器镜像编译您的二进制文件，然后将输出复制到 `static` 镜像中。

以下示例展示了一个多阶段 Dockerfile，用于构建 Go 应用并在最小化的静态镜像中运行它：

```dockerfile
#syntax=docker/dockerfile:1

FROM <your-namespace>/dhi-golang:1.22-dev AS build
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

FROM <your-namespace>/dhi-static:20230311
COPY --from=build /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

这种模式确保了一个没有不必要组件的加固运行时环境，将攻击面降到最低。

## 为基于框架的应用使用 dev 变体

如果您正在使用需要包管理器或构建工具的框架（如 Python、Node.js 或 Go）构建应用，请在开发或构建阶段使用 `-dev` 变体。这些变体包含必要的实用程序，如 shell、编译器和包管理器，以支持本地迭代和 CI 工作流。

在内部开发循环或隔离的 CI 阶段使用 `-dev` 镜像以最大化生产力。一旦您准备好为生产创建制品，请切换到较小的运行时变体以减少攻击面和镜像大小。

以下示例展示了如何使用 `-dev` 变体构建 Python 应用，并使用较小的运行时变体运行它：

```dockerfile
#syntax=docker/dockerfile:1

FROM <your-namespace>/dhi-python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM <your-namespace>/dhi-python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY image.py image.png ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/image.py" ]
```

这种模式将构建环境与运行时环境分离，有助于减小镜像大小并通过从最终镜像中移除不必要的工具来提高安全性。
