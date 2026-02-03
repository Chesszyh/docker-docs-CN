---
title: 使用 GitHub Actions 在注册表间复制镜像
linkTitle: 在注册表间复制镜像
description: 使用 GitHub Actions 构建多平台镜像并在不同注册表之间进行复制
keywords: ci, github actions, gha, buildkit, buildx, registry, 复制镜像, 注册表
---

使用 Buildx 构建的 [多平台镜像](../../building/multi-platform.md) 可以使用 [`buildx imagetools create` 命令](/reference/cli/docker/buildx/imagetools/create.md) 从一个注册表复制到另一个注册表：

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
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            user/app:latest
            user/app:1.0.0

      - name: Push image to GHCR
        run: |
          docker buildx imagetools create \
            --tag ghcr.io/user/app:latest \
            --tag ghcr.io/user/app:1.0.0 \
            user/app:latest
```