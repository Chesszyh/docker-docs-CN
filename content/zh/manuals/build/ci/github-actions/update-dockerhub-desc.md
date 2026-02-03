---
title: 使用 GitHub Actions 更新 Docker Hub 描述
linkTitle: 更新 Docker Hub 描述
description: 了解如何使用 GitHub Actions 更新 Docker Hub 存储库的 README 描述
keywords: ci, github actions, gha, buildkit, buildx, docker hub, 存储库描述
---

您可以使用名为 [Docker Hub Description](https://github.com/peter-evans/dockerhub-description) 的第三方 Action 来更新 Docker Hub 存储库的描述：

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

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest

      - name: Update repo description
        uses: peter-evans/dockerhub-description@e98e4d1628a5f3be2be7c231e50981aee98723ae # v4.0.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          repository: user/app
```