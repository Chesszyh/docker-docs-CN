---
title: 使用 GitHub Actions 在不同任务间共享已构建的镜像
linkTitle: 在不同任务间共享镜像
description: 在不推送到注册表的情况下，在不同运行器之间共享镜像
keywords: ci, github actions, gha, buildkit, buildx, 共享镜像
---

由于每个任务都在其独立的运行器中隔离运行，您无法在不同任务之间直接使用已构建的镜像，除非您使用的是 [自托管运行器 (self-hosted runners)](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) 或 [Docker Build Cloud](/build-cloud)。但是，您可以使用 [actions/upload-artifact](https://github.com/actions/upload-artifact) 和 [actions/download-artifact](https://github.com/actions/download-artifact) Actions 在工作流的 [任务间传递数据](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow)：

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and export
        uses: docker/build-push-action@v6
        with:
          tags: myimage:latest
          outputs: type=docker,dest=${{ runner.temp }}/myimage.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}/myimage.tar

  use:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}

      - name: Load image
        run: |
          docker load --input ${{ runner.temp }}/myimage.tar
          docker image ls -a
```