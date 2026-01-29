---
title: 使用 GitHub Actions 管理标签和标签 (Tags and Labels)
linkTitle: 标签 (Tags and labels)
description: 使用 GitHub Actions 自动为镜像分配标签
keywords: ci, github actions, gha, buildkit, buildx, tags, labels
---

如果您想要“自动”管理标签（tags）并使标签（labels）符合 [OCI 镜像格式规范](https://github.com/opencontainers/image-spec/blob/master/annotations.md)，可以在专用的设置步骤中完成。以下工作流将使用 [Docker Metadata Action](https://github.com/docker/metadata-action)，根据 GitHub Actions 事件和 Git 元数据来处理标签：

```yaml
name: ci

on:
  schedule:
    - cron: "0 10 * * *"
  push:
    branches:
      - "**"
    tags:
      - "v*.*.*"
  pull_request:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          # 用于标签基准名称的 Docker 镜像列表
          images: |
            name/app
            ghcr.io/username/app
          # 根据以下事件/属性生成 Docker 标签
          tags: |
            type=schedule
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - name: Login to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GHCR
        if: github.event_name != 'pull_request'
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
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```
