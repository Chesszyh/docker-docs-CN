---
title: 在 GitHub Actions 中使用本地注册表
linkTitle: 本地注册表
description: 在 GitHub Actions 中创建并使用本地 OCI 注册表
keywords: ci, github actions, gha, buildkit, buildx, registry, 本地注册表
---

出于测试目的，您可能需要创建一个 [本地注册表](https://hub.docker.com/_/registry) 并向其中推送镜像：

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