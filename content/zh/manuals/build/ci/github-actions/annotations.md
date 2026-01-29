---
title: 使用 GitHub Actions 添加镜像注解
linkTitle: 注解 (Annotations)
description: 使用 GitHub Actions 为镜像组件添加 OCI 注解
keywords: ci, github actions, gha, buildkit, buildx, 注解, oci
---

注解（Annotations）允许您为 OCI 镜像组件（如清单、索引和描述符）指定任意元数据。

要在通过 GitHub Actions 构建镜像时添加注解，请使用 [metadata-action] 自动创建符合 OCI 标准的注解。metadata action 会创建一个 `annotations` 输出，您可以同时在 [build-push-action] 和 [bake-action] 中引用它。

[metadata-action]: https://github.com/docker/metadata-action#overwrite-labels-and-annotations
[build-push-action]: https://github.com/docker/build-push-action/
[bake-action]: https://github.com/docker/bake-action/

{{< tabs >}}
{{< tab name="build-push-action" >}}

```yaml {hl_lines=32}
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

{{< /tab >}}
{{< tab name="bake-action" >}}

```yaml {hl_lines=37}
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file-tags }}
            cwd://${{ steps.meta.outputs.bake-file-annotations }}
          push: true
```

{{< /tab >}}
{{< /tabs >}}

## 配置注解层级

默认情况下，注解放置在镜像清单（manifests）上。要配置 [注解层级](../../metadata/annotations.md#指定注解层级)，请在 `metadata-action` 步骤中将 `DOCKER_METADATA_ANNOTATIONS_LEVELS` 环境变量设置为包含所有要添加注解层级的逗号分隔列表。例如，将 `DOCKER_METADATA_ANNOTATIONS_LEVELS` 设置为 `index` 会导致注解出现在镜像索引（image index）上，而不是清单上。

以下示例同时在镜像索引和清单上创建注解。

```yaml {hl_lines=28}
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
        env:
          DOCKER_METADATA_ANNOTATIONS_LEVELS: manifest,index

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

> [!NOTE]
>
> 构建必须生成您想要添加注解的组件。例如，要为镜像索引添加注解，构建必须生成一个索引。如果构建仅生成清单，而您指定了 `index` 或 `index-descriptor`，则构建会失败。
