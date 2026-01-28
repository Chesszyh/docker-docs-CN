---
title: 迁移现有应用以使用 Docker Hardened Images
linktitle: 迁移应用
description: 按照分步指南更新您的 Dockerfile，采用 Docker Hardened Images 实现安全、最小化和生产就绪的构建。
weight: 50
keywords: migrate dockerfile, hardened base image, multi-stage build, non-root containers, secure container build
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

本指南帮助您将现有的 Dockerfile 迁移到使用 Docker Hardened Images（DHI）。DHI 是最小化且以安全为重点的，这可能需要对您的基础镜像、构建过程和运行时配置进行调整。

本指南侧重于迁移框架镜像，例如用于使用 Go、Python 或 Node.js 等语言从源代码构建应用的镜像。如果您正在迁移应用镜像，如数据库、代理或其他预构建服务，许多相同的原则仍然适用。

## 迁移注意事项

DHI 省略了常见工具，如 shell 和包管理器，以减少攻击面。它们还默认以非 root 用户运行。因此，迁移到 DHI 通常需要对您的 Dockerfile 进行以下更改：


| 项目               | 迁移说明                                                                                                                                                                                                                                                                                                                 |
|:-------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 基础镜像         | 将 Dockerfile 中的基础镜像替换为 Docker Hardened Image。                                                                                                                                                                                                      |
| 包管理 | 用于运行时的镜像不包含包管理器。仅在带有 `dev` 标签的镜像中使用包管理器。利用多阶段构建，将必要的制品从构建阶段复制到运行时阶段。                                                                                                                                                                        |
| 非 root 用户      | 默认情况下，用于运行时的镜像以 nonroot 用户运行。确保必要的文件和目录对 nonroot 用户可访问。                                                                                                                                              |
| 多阶段构建  | 在构建阶段使用带有 `dev` 或 `sdk` 标签的镜像，在运行时使用非 dev 镜像。                                                                                                                                                                                     |
| TLS 证书   | DHI 默认包含标准 TLS 证书。无需安装 TLS 证书。                                                                                                                                                                               |
| 端口              | 用于运行时的 DHI 默认以 nonroot 用户运行。因此，在 Kubernetes 中或在 20.10 之前版本的 Docker Engine 中运行时，这些镜像中的应用无法绑定到特权端口（低于 1024）。为避免问题，请将应用配置为在容器内监听 1025 或更高的端口。 |
| 入口点        | DHI 可能具有与 Docker Official Images 等镜像不同的入口点。检查 DHI 的入口点并根据需要更新您的 Dockerfile。                                                                                                                                        |
| 无 shell           | 用于运行时的 DHI 不包含 shell。在构建阶段使用 dev 镜像运行 shell 命令，然后将制品复制到运行时阶段。                                                                                                                                            |

有关更多详情和故障排除提示，请参阅[故障排除](/manuals/dhi/troubleshoot.md)。

## 迁移现有应用

以下步骤概述了迁移过程。

### 步骤 1：更新 Dockerfile 中的基础镜像

将应用 Dockerfile 中的基础镜像更新为加固镜像。这通常是标记为 `dev` 或 `sdk` 的镜像，因为它具有安装软件包和依赖项所需的工具。

以下来自 Dockerfile 的示例 diff 片段显示了旧基础镜像被新的加固镜像替换。

```diff
- ## Original base image
- FROM golang:1.22

+ ## Updated to use hardened base image
+ FROM <your-namespace>/dhi-golang:1.22-dev
```

### 步骤 2：更新 Dockerfile 中的运行时镜像

为确保您的最终镜像尽可能最小化，您应该使用[多阶段构建](/manuals/build/building/multi-stage.md)。Dockerfile 中的所有阶段都应使用加固镜像。虽然中间阶段通常使用标记为 `dev` 或 `sdk` 的镜像，但最终的运行时阶段应使用运行时镜像。

利用构建阶段编译您的应用，并将生成的制品复制到最终的运行时阶段。这确保了您的最终镜像是最小化且安全的。

请参阅[示例 Dockerfile 迁移](#示例-dockerfile-迁移)部分，了解如何更新您的 Dockerfile 的示例。

## 示例 Dockerfile 迁移

以下迁移示例展示了迁移前和迁移后的 Dockerfile。

### Go 示例

{{< tabs >}}
{{< tab name="Before" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM golang:latest

WORKDIR /app
ADD . ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< tab name="After" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Compile Go application ===
FROM <your-namespace>/dhi-golang:1-alpine3.21-dev AS builder

WORKDIR /app
ADD . ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

# === Final stage: Create minimal runtime image ===
FROM <your-namespace>/dhi-golang:1-alpine3.21

WORKDIR /app
COPY --from=builder /app/main  /app/main

ENTRYPOINT ["/app/main"]
```
{{< /tab >}}
{{< /tabs >}}

### Node.js 示例

{{< tabs >}}
{{< tab name="Before" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM node:latest
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY image.jpg ./image.jpg
COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< tab name="After" >}}

```dockerfile
#syntax=docker/dockerfile:1

#=== Build stage: Install dependencies and build application ===#
FROM <your-namespace>/dhi-node:23-alpine3.21-dev AS builder
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY image.jpg ./image.jpg
COPY . .

#=== Final stage: Create minimal runtime image ===#
FROM <your-namespace>/dhi-node:23-alpine3.21
ENV PATH=/app/node_modules/.bin:$PATH

COPY --from=builder --chown=node:node /usr/src/app /app

WORKDIR /app

CMD ["index.js"]
```
{{< /tab >}}
{{< /tabs >}}

### Python 示例

{{< tabs >}}
{{< tab name="Before" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM python:latest AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY image.py image.png ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/image.py" ]
```

{{< /tab >}}
{{< tab name="After" >}}

```dockerfile
#syntax=docker/dockerfile:1

#=== Build stage: Install dependencies and create virtual environment ===#
FROM <your-namespace>/dhi-python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#=== Final stage: Create minimal runtime image ===#
FROM <your-namespace>/dhi-python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY image.py image.png ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/image.py" ]
```

{{< /tab >}}
{{< /tabs >}}
