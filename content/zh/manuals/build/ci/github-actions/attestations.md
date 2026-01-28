---
title: 使用 GitHub Actions 添加 SBOM 和来源证明
linkTitle: Attestations
description: 使用 GitHub Actions 为您的镜像添加 SBOM 和来源证明
keywords: ci, github actions, gha, buildkit, buildx, attestations, sbom, provenance, slsa
---

软件物料清单（Software Bill of Material，SBOM）和来源（provenance）[证明](../../metadata/attestations/_index.md)会添加关于镜像内容及其构建方式的元数据。

`docker/build-push-action` 版本 4 及更高版本支持证明功能。

## 默认来源证明

`docker/build-push-action` GitHub Action 会自动为您的镜像添加来源证明，条件如下：

- 如果 GitHub 仓库是公开的，会自动添加 `mode=max` 的来源证明到镜像中。
- 如果 GitHub 仓库是私有的，会自动添加 `mode=min` 的来源证明到镜像中。
- 如果您使用的是 [`docker` 导出器](../../exporters/oci-docker.md)，或者使用 `load: true` 将构建结果加载到运行器，则不会向镜像添加证明。这些输出格式不支持证明。

> [!WARNING]
>
> 如果您使用 `docker/build-push-action` 为公开 GitHub 仓库中的代码构建镜像，默认附加到镜像的来源证明会包含构建参数的值。如果您误用构建参数来传递密钥给构建，例如用户凭据或认证令牌，这些密钥会在来源证明中暴露。请重构您的构建，改用 [secret mounts](/reference/cli/docker/buildx/build.md#secret) 来传递这些密钥。同时请记得轮换任何可能已暴露的密钥。

## 最大级别来源证明

建议您使用最大级别（max-level）的来源证明来构建镜像。私有仓库默认只添加最小级别（min-level）的来源证明，但您可以通过在 `docker/build-push-action` GitHub Action 上将 `provenance` 输入设置为 `mode=max` 来手动覆盖来源级别。

请注意，向镜像添加证明意味着您必须直接将镜像推送到镜像仓库，而不是将镜像加载到运行器的本地镜像存储中。这是因为本地镜像存储不支持加载带有证明的镜像。

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

SBOM 证明不会自动添加到镜像中。要添加 SBOM 证明，请将 `docker/build-push-action` 的 `sbom` 输入设置为 true。

请注意，向镜像添加证明意味着您必须直接将镜像推送到镜像仓库，而不是将镜像加载到运行器的本地镜像存储中。这是因为本地镜像存储不支持加载带有证明的镜像。

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
