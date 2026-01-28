---
title: 使用 GitHub Actions 构建多平台镜像
linkTitle: Multi-platform image
description: 使用 GitHub Actions 通过 QEMU 模拟或多个原生构建器为多种架构构建
keywords: ci, github actions, gha, buildkit, buildx, multi-platform
---

您可以使用 `platforms` 选项构建[多平台镜像](../../building/multi-platform.md)，如以下示例所示：

> [!NOTE]
>
> - 有关可用平台的列表，请参阅 [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action。
> - 如果您需要支持更多平台，可以使用 [Docker Setup QEMU](https://github.com/docker/setup-qemu-action) action 配合 QEMU。

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
          platforms: linux/amd64,linux/arm64
          push: true
          tags: user/app:latest
```

## 构建和加载多平台镜像

GitHub Actions 运行器的默认 Docker 设置不支持在构建后将多平台镜像加载到运行器的本地镜像存储中。要加载多平台镜像，您需要为 Docker Engine 启用 containerd 镜像存储选项。

无法直接配置 GitHub Actions 运行器中的默认 Docker 设置，但您可以使用 `docker/setup-docker-action` 来自定义作业的 Docker Engine 和 CLI 设置。

以下示例工作流启用 containerd 镜像存储，构建多平台镜像，并将结果加载到 GitHub 运行器的本地镜像存储中。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker
        uses: docker/setup-docker-action@v4
        with:
          daemon-config: |
            {
              "debug": true,
              "features": {
                "containerd-snapshotter": true
              }
            }

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          load: true
          tags: user/app:latest
```

## 在多个运行器之间分发构建

在前面的示例中，每个平台都在同一个运行器上构建，这可能需要很长时间，具体取决于平台数量和您的 Dockerfile。

要解决这个问题，您可以使用矩阵策略将每个平台的构建分发到多个运行器，并使用 [`buildx imagetools create` 命令](/reference/cli/docker/buildx/imagetools/create.md)创建清单列表。

以下工作流将使用矩阵策略在专用运行器上为每个平台构建镜像，并按摘要推送。然后，`merge` 作业将创建清单列表并推送到 Docker Hub。[`metadata` action](https://github.com/docker/metadata-action) 用于设置标签和标注。

```yaml
name: ci

on:
  push:

env:
  REGISTRY_IMAGE: user/app

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        platform:
          - linux/amd64
          - linux/arm64
    steps:
      - name: Prepare
        run: |
          platform=${{ matrix.platform }}
          echo "PLATFORM_PAIR=${platform//\//-}" >> $GITHUB_ENV

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push by digest
        id: build
        uses: docker/build-push-action@v6
        with:
          platforms: ${{ matrix.platform }}
          labels: ${{ steps.meta.outputs.labels }}
          tags: ${{ env.REGISTRY_IMAGE }}
          outputs: type=image,push-by-digest=true,name-canonical=true,push=true

      - name: Export digest
        run: |
          mkdir -p ${{ runner.temp }}/digests
          digest="${{ steps.build.outputs.digest }}"
          touch "${{ runner.temp }}/digests/${digest#sha256:}"

      - name: Upload digest
        uses: actions/upload-artifact@v4
        with:
          name: digests-${{ env.PLATFORM_PAIR }}
          path: ${{ runner.temp }}/digests/*
          if-no-files-found: error
          retention-days: 1

  merge:
    runs-on: ubuntu-latest
    needs:
      - build
    steps:
      - name: Download digests
        uses: actions/download-artifact@v4
        with:
          path: ${{ runner.temp }}/digests
          pattern: digests-*
          merge-multiple: true

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Create manifest list and push
        working-directory: ${{ runner.temp }}/digests
        run: |
          docker buildx imagetools create $(jq -cr '.tags | map("-t " + .) | join(" ")' <<< "$DOCKER_METADATA_OUTPUT_JSON") \
            $(printf '${{ env.REGISTRY_IMAGE }}@sha256:%s ' *)

      - name: Inspect image
        run: |
          docker buildx imagetools inspect ${{ env.REGISTRY_IMAGE }}:${{ steps.meta.outputs.version }}
```

### 使用 Bake

也可以使用 Bake 和 [bake action](https://github.com/docker/bake-action) 在多个运行器上构建。

您可以在[这个 GitHub 仓库](https://github.com/crazy-max/docker-linguist)中找到一个实际示例。

以下示例实现了与[上一节](#distribute-build-across-multiple-runners)中描述的相同结果。

```hcl
variable "DEFAULT_TAG" {
  default = "app:local"
}

// Special target: https://github.com/docker/metadata-action#bake-definition
target "docker-metadata-action" {
  tags = ["${DEFAULT_TAG}"]
}

// Default target if none specified
group "default" {
  targets = ["image-local"]
}

target "image" {
  inherits = ["docker-metadata-action"]
}

target "image-local" {
  inherits = ["image"]
  output = ["type=docker"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm/v6",
    "linux/arm/v7",
    "linux/arm64"
  ]
}
```

```yaml
name: ci

on:
  push:

env:
  REGISTRY_IMAGE: user/app

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.platforms.outputs.matrix }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Create matrix
        id: platforms
        run: |
          echo "matrix=$(docker buildx bake image-all --print | jq -cr '.target."image-all".platforms')" >>${GITHUB_OUTPUT}

      - name: Show matrix
        run: |
          echo ${{ steps.platforms.outputs.matrix }}

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}

      - name: Rename meta bake definition file
        run: |
          mv "${{ steps.meta.outputs.bake-file }}" "${{ runner.temp }}/bake-meta.json"

      - name: Upload meta bake definition
        uses: actions/upload-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}/bake-meta.json
          if-no-files-found: error
          retention-days: 1

  build:
    runs-on: ubuntu-latest
    needs:
      - prepare
    strategy:
      fail-fast: false
      matrix:
        platform: ${{ fromJson(needs.prepare.outputs.matrix) }}
    steps:
      - name: Prepare
        run: |
          platform=${{ matrix.platform }}
          echo "PLATFORM_PAIR=${platform//\//-}" >> $GITHUB_ENV

      - name: Download meta bake definition
        uses: actions/download-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        id: bake
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ runner.temp }}/bake-meta.json
          targets: image
          set: |
            *.tags=${{ env.REGISTRY_IMAGE }}
            *.platform=${{ matrix.platform }}
            *.output=type=image,push-by-digest=true,name-canonical=true,push=true

      - name: Export digest
        run: |
          mkdir -p ${{ runner.temp }}/digests
          digest="${{ fromJSON(steps.bake.outputs.metadata).image['containerimage.digest'] }}"
          touch "${{ runner.temp }}/digests/${digest#sha256:}"

      - name: Upload digest
        uses: actions/upload-artifact@v4
        with:
          name: digests-${{ env.PLATFORM_PAIR }}
          path: ${{ runner.temp }}/digests/*
          if-no-files-found: error
          retention-days: 1

  merge:
    runs-on: ubuntu-latest
    needs:
      - build
    steps:
      - name: Download meta bake definition
        uses: actions/download-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}

      - name: Download digests
        uses: actions/download-artifact@v4
        with:
          path: ${{ runner.temp }}/digests
          pattern: digests-*
          merge-multiple: true

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Create manifest list and push
        working-directory: ${{ runner.temp }}/digests
        run: |
          docker buildx imagetools create $(jq -cr '.target."docker-metadata-action".tags | map(select(startswith("${{ env.REGISTRY_IMAGE }}")) | "-t " + .) | join(" ")' ${{ runner.temp }}/bake-meta.json) \
            $(printf '${{ env.REGISTRY_IMAGE }}@sha256:%s ' *)

      - name: Inspect image
        run: |
          docker buildx imagetools inspect ${{ env.REGISTRY_IMAGE }}:$(jq -r '.target."docker-metadata-action".args.DOCKER_META_VERSION' ${{ runner.temp }}/bake-meta.json)
```
