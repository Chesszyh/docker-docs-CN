---
title: 使用 GitHub Actions 的本地镜像库
linkTitle: 本地镜像库
description: 在 GitHub Actions 中创建并使用本地 OCI 镜像库
keywords: ci, github actions, gha, buildkit, buildx, 镜像库
---

出于测试目的，您可能需要创建一个 [本地镜像库](https://hub.docker.com/_/registry) 来推送镜像：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:2
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver-opts: network=host
      
      - name: Build and push to local registry
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: localhost:5000/name/app:latest
      
      - name: Inspect
        run: |
          docker buildx imagetools inspect localhost:5000/name/app:latest
```
