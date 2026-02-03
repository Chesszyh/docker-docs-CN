---
title: 使用 GitHub Actions 添加 SBOM 和来源证明
linkTitle: 证明 (Attestations)
description: 使用 GitHub Actions 为您的镜像添加 SBOM 和来源证明
keywords: ci, github actions, gha, buildkit, buildx, attestations, sbom, provenance, slsa, 证明, 来源
---

软件物料清单 (SBOM) 和来源 (provenance) [证明](../../metadata/attestations/_index.md) 增加了关于镜像内容以及镜像如何构建的元数据。

`docker/build-push-action` 的第 4 版及更高版本支持证明功能。

## 默认来源证明

`docker/build-push-action` GitHub Action 会在满足以下条件时自动为您的镜像添加来源证明：

- 如果 GitHub 仓库是公开的，则自动为镜像添加 `mode=max` 的来源证明。
- 如果 GitHub 仓库是私有的，则自动为镜像添加 `mode=min` 的来源证明。
- 如果您使用的是 [`docker` 导出器](../../exporters/oci-docker.md)，或者通过 `load: true` 将构建结果加载到运行器 (runner)，则不会向镜像添加任何证明。这些输出格式不支持证明。

> [!WARNING]
>
> 如果您使用 `docker/build-push-action` 为公开 GitHub 仓库中的代码构建镜像，默认附加到镜像的来源证明将包含构建参数 (build arguments) 的值。如果您错误地使用构建参数来传递机密信息（如用户凭据或身份验证令牌），这些机密将会暴露在来源证明中。请重构您的构建过程，改用 [机密挂载 (secret mounts)](/reference/cli/docker/buildx/build.md#secret) 来传递这些机密。同时记得更换任何可能已泄露的机密。

## 最高级别的来源证明 (Max-level provenance)

建议您在构建镜像时使用最高级别的来源证明。默认情况下，私有仓库仅添加最低级别 (min-level) 的来源，但您可以通过将 `docker/build-push-action` GitHub Action 的 `provenance` 输入设置为 `mode=max` 来手动覆盖来源级别。

请注意，向镜像添加证明意味着您必须直接将镜像推送到注册表，而不是加载到运行器的本地镜像库中。这是因为本地镜像库不支持加载带有证明的镜像。

```yaml
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

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          push: true
          provenance: mode=max
          tags: ${{ steps.meta.outputs.tags }}
```

## SBOM

SBOM 证明不会自动添加到镜像中。要添加 SBOM 证明，请将 `docker/build-push-action` 的 `sbom` 输入设置为 `true`。

请注意，向镜像添加证明意味着您必须直接将镜像推送到注册表，而不是加载到运行器的本地镜像库中。这是因为本地镜像库不支持加载带有证明的镜像。

```yaml
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

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          sbom: true
          push: true
          tags: ${{ steps.meta.outputs.tags }}
```