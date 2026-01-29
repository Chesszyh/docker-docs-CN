---
title: 使用 GitHub Actions 导出到 Docker
linkTitle: 导出到 Docker
description: 使用 GitHub Actions 将构建结果加载到镜像库
keywords: ci, github actions, gha, buildkit, buildx, docker, 导出, load
---

您可能希望通过 `docker images` 让 Docker 客户端可以使用您的构建结果，以便在工作流的另一个步骤中使用它：

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
