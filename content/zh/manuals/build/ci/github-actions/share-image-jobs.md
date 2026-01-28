---
title: 使用 GitHub Actions 在作业之间共享构建的镜像
linkTitle: Share image between jobs
description: 在不推送到镜像仓库的情况下在运行器之间共享镜像
keywords: ci, github actions, gha, buildkit, buildx
---

由于每个作业在其自己的运行器中隔离运行，除非您使用[自托管运行器](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)或 [Docker Build Cloud](/build-cloud)，否则无法在作业之间使用构建的镜像。但是，您可以使用 [actions/upload-artifact](https://github.com/actions/upload-artifact) 和 [actions/download-artifact](https://github.com/actions/download-artifact) actions 在工作流中[在作业之间传递数据](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow)：

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
