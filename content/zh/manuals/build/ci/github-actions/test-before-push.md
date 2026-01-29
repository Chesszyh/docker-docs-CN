---
title: 使用 GitHub Actions 在推送前测试
linkTitle: 在推送前测试
description: 了解如何在将镜像推送到镜像库之前对其进行验证
keywords: ci, github actions, gha, buildkit, buildx, 测试
---

在某些情况下，您可能希望在推送镜像之前验证其是否按预期工作。以下工作流通过几个步骤来实现这一目标：

1. 构建镜像并导出到 Docker
2. 测试您的镜像
3. 多平台构建并推送镜像

```yaml
name: ci

on:
  push:

env:
  TEST_TAG: user/app:test
  LATEST_TAG: user/app:latest

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

      - name: Build and export to Docker
        uses: docker/build-push-action@v6
        with:
          load: true
          tags: ${{ env.TEST_TAG }}

      - name: Test
        run: |
          docker run --rm ${{ env.TEST_TAG }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ env.LATEST_TAG }}
```

> [!NOTE]
>
> 在此工作流中，`linux/amd64` 镜像仅被构建一次。该镜像在第一次构建，随后的步骤会使用第一个“构建并推送”步骤中的内部缓存。第二个“构建并推送”步骤仅构建 `linux/arm64`。
