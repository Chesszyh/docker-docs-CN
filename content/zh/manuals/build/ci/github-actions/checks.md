---
title: 通过 GitHub Actions 验证构建配置
linkTitle: 构建检查 (Build checks)
description: 了解如何使用 GitHub Actions 中的构建检查功能来验证构建配置并识别违反最佳实践的情况。
keywords: github actions, gha, build, checks, 构建检查, 验证
---

[构建检查 (Build checks)](/manuals/build/checks.md) 允许您在不实际运行构建的情况下验证 `docker build` 配置。

## 使用 `docker/build-push-action` 运行检查

要在 GitHub Actions 工作流中使用 `build-push-action` 运行构建检查，请将 `call` 输入参数设置为 `check`。设置此参数后，如果构建配置检测到任何检查警告，工作流将失败。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Validate build configuration
        uses: docker/build-push-action@v6
        with:
          call: check

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
```

## 使用 `docker/bake-action` 运行检查

如果您使用 Bake 和 `docker/bake-action` 运行构建，则无需在 GitHub Actions 工作流配置中指定任何特殊输入。相反，请定义一个调用 `check` 方法的 Bake 目标，并在 CI 中调用该目标。

```hcl
target "build" {
  dockerfile = "Dockerfile"
  args = {
    FOO = "bar"
  }
}
target "validate-build" {
  inherits = ["build"]
  call = "check"
}
```

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Validate build configuration
        uses: docker/bake-action@v6
        with:
          targets: validate-build

      - name: Build
        uses: docker/bake-action@v6
        with:
          targets: build
          push: true
```