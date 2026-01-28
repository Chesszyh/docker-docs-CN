---
title: 容器化 Golang 应用
linkTitle: 容器化你的应用
weight: 20
keywords: go, golang, containerize, initialize
description: 了詹如何容器化 Golang 应用。
---

容器化有助于你将应用及其依赖部件包袋到一个称为容器的单一包中。此包可以在任何平台上运行，而无需担心环境问题。在本节中，你将学习如何使用 Docker 容器化 Golang 应用。

要容器化 Golang 应用，首先需要创建一个 Dockerfile。Dockerfile 包含在容器中构建和运行应用的指令。此外，在创建 Dockerfile 时，你可以遵循不同的最佳实践集来优化镜像大小并使其更安全。

## 创建 Dockerfile

在 Golang 应用的根目录中创建一个名为 `Dockerfile` 的新文件。Dockerfile 包含在容器中构建和运行应用的指令。

以下是 Golang 应用的 Dockerfile。你也可以在 `go-prometheus-monitoring` 目录中找到此文件。

```dockerfile
# Use the official Golang image as the base
FROM golang:1.24-alpine AS builder

# Set environment variables
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Set working directory inside the container
WORKDIR /build

# Copy go.mod and go.sum files for dependency installation
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the entire application source
COPY . .

# Build the Go binary
RUN go build -o /app .

# Final lightweight stage
FROM alpine:3.21 AS final

# Copy the compiled binary from the builder stage
COPY --from=builder /app /bin/app

# Expose the application's port
EXPOSE 8000

# Run the application
CMD ["bin/app"]
```

## 了詹来看 Dockerfile

Dockerfile 包含两个阶段：

1. **构建阶段**：此阶段使用官方 Golang 镗像作为基础，并设置必要的环境变量。它还设置容器内的工作目录，复制用于依赖安装的 `go.mod` 和 `go.sum` 文件，下载依赖，复制所有应用源代码，并构建 Go 二进制文件。

    你使用 `golang:1.24-alpine` 镗像作为构建阶段的基础镗像。`CGO_ENABLED=0` 环境变量禁用 CGO，这对于构建静态二进制文件很有用。你还将 `GOOS` 和 `GOARCH` 环境变量分别设置为 `linux` 和 `amd64`，以便为 Linux 平台构建二进制文件。

2. **最终阶段**：此阶段使用官方 Alpine 镗像作为基础，并从构建阶段复制编译好的二进制文件。它还公开应用的端口并运行应用。

    你使用 `alpine:3.21` 镗像作为最终阶段的基础镗像。你将编译好的二进制文件从构建阶段复制到最终镗像中。你使用 `EXPOSE` 指令公开应用的端口，并使用 `CMD` 指令运行应用。

    除了多阶段构建之外，Dockerfile 还遵循了最佳实践，如使用官方镗像、设置工作目录以及只将必要文件复制到最终镗像。你可以通过其他最佳实践进一步优化 Dockerfile。

## 构建 Docker 镗像并运行应用

有了 Dockerfile 后，你就可以构建 Docker 镗像称用容器中运行应用。

要构建 Docker 镗像，请在终端的环境中运行以下命令：

```console
$ docker build -t go-api:latest .
```

构建镗像后，你可以使用以下命令在容器中运行应用：

```console
$ docker run -p 8000:8000 go-api:latest
```

应用将在容器内开始运行，你可以通过 `http://localhost:8000` 访问它。你也可以使用 `docker ps` 命令查查正在运行的容器。

```console
$ docker ps
```

## 总结

在本节中，你学习了如何使用 Dockerfile 容器化 Golang 应用。你创建了一个多阶段 Dockerfile 以在容器中构建和运行应用。你还了解了关于优化 Docker 镗像大小并使其更安全的最佳实践。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)

## 下一步骤

在下一节中，你将学习如何使用 Docker Compose 连接并同时运行多个服务，以便使用 Prometheus 和 Grafana 监控 Golang 应用。
