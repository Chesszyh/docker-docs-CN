---
title: 使用 GitHub Actions 导出到 Docker
linkTitle: Export to Docker
description: 使用 GitHub Actions 将构建结果加载到镜像存储
keywords: ci, github actions, gha, buildkit, buildx, docker, export, load
---

您可能希望通过 `docker images` 在 Docker 客户端中使用您的构建结果，以便在工作流的其他步骤中使用它：

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
