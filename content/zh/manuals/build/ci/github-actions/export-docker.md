---
title: 使用 GitHub Actions 导出至 Docker
linkTitle: 导出至 Docker
description: 使用 GitHub Actions 将构建结果加载到镜像库中
keywords: ci, github actions, gha, buildkit, buildx, docker, export, load, 导出, 加载
---

您可能希望构建结果能够通过 `docker images` 命令在 Docker 客户端中可见，以便在工作流的后续步骤中使用它：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build
        uses: docker/build-push-action@v6
        with:
          load: true
          tags: myimage:latest
      
      - name: Inspect
        run: |
          docker image inspect myimage:latest
```