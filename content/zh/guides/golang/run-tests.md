---
title: 使用 Go test 运行你的测试
linkTitle: 运行测试
weight: 30
keywords: build, go, golang, test
description: 如何在容器中构建和运行你的 Go 测试
aliases:
  - /get-started/golang/run-tests/
  - /language/golang/run-tests/
  - /guides/language/golang/run-tests/
---

## 先决条件

完成本指南的 [构建 Go 镜像](build-images.md) 部分。

## 概览

测试是现代软件开发的重要组成部分。测试对不同的开发团队来说可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，你将了解在构建时在 Docker 中运行单元测试。

在本节中，使用你在 [构建 Go 镜像](build-images.md) 中克隆的 `docker-gs-ping` 项目。

## 在构建时运行测试

要在构建时运行测试，你需要向 `Dockerfile.multistage` 添加一个测试阶段。示例应用程序存储库中的 `Dockerfile.multistage` 已经包含以下内容：

```dockerfile {hl_lines="15-17"}
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

运行以下命令以使用 `run-test-stage` 阶段作为目标构建镜像并查看测试结果。包括 `--progress plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，以及 `--target run-test-stage` 以针对测试阶段。

```console
$ docker build -f Dockerfile.multistage -t docker-gs-ping-test --progress plain --no-cache --target run-test-stage .
```

你应该看到包含以下内容的输出。

```text
#13 [run-test-stage 1/1] RUN go test -v ./...
#13 4.915 === RUN   TestIntMinBasic
#13 4.915 --- PASS: TestIntMinBasic (0.00s)
#13 4.915 === RUN   TestIntMinTableDriven
#13 4.915 === RUN   TestIntMinTableDriven/0,1
#13 4.915 === RUN   TestIntMinTableDriven/1,0
#13 4.915 === RUN   TestIntMinTableDriven/2,-2
#13 4.915 === RUN   TestIntMinTableDriven/0,-1
#13 4.915 === RUN   TestIntMinTableDriven/-1,0
#13 4.915 --- PASS: TestIntMinTableDriven (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/1,0 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/2,-2 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,-1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/-1,0 (0.00s)
#13 4.915 PASS
```

## 后续步骤

在本节中，你学习了如何在构建镜像时运行测试。接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 管道。
