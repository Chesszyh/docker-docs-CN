---
title: 使用 GitHub Actions 添加 SBOM 和来源证明
linkTitle: 证明 (Attestations)
description: 使用 GitHub Actions 为镜像添加 SBOM 和来源证明
keywords: ci, github actions, gha, buildkit, buildx, 证明, sbom, 来源, slsa
---

软件物料清单 (SBOM) 和来源 (provenance) [证明](../../metadata/attestations/_index.md) 增加了关于镜像内容及其构建方式的元数据。

`docker/build-push-action` 的第 4 版及更高版本支持证明功能。

## 默认来源证明

`docker/build-push-action` GitHub Action 会在满足以下条件时自动为您的镜像添加来源证明：

- 如果 GitHub 仓库是公开的，则会自动向镜像添加 `mode=max` 的来源证明。
- 如果 GitHub 仓库是私有的，则会自动向镜像添加 `mode=min` 的来源证明。
- 如果您正在使用 [`docker` 导出器](../../exporters/oci-docker.md)，或者使用 `load: true` 将构建结果加载到 runner 中，则不会向镜像添加任何证明。这些输出格式不支持证明。

> [!WARNING]
>
> 如果您正在使用 `docker/build-push-action` 为公开 GitHub 仓库中的代码构建镜像，默认附加到镜像的来源证明将包含构建参数的值。如果您滥用构建参数向构建传递密钥（如用户凭据或身份验证令牌），这些密钥将暴露在来源证明中。请重构您的构建，改用 [密钥挂载](/reference/cli/docker/buildx/build.md#secret) 来传递这些密钥。同时请记得更换任何可能已泄露的密钥。

## 最高级别的来源证明

建议您在构建镜像时使用最高级别 (`max-level`) 的来源证明。默认情况下，私有仓库仅添加最低级别 (`min-level`) 的来源证明，但您可以通过将 `docker/build-push-action` GitHub Action 的 `provenance` 输入设置为 `mode=max` 来手动覆盖来源级别。

请注意，为镜像添加证明意味着您必须直接将镜像推送到镜像库，而不能将其加载到 runner 的本地镜像库中。这是因为本地镜像库不支持加载带有证明的镜像。

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

请注意，为镜像添加证明意味着您必须直接将镜像推送到镜像库，而不能将其加载到 runner 的本地镜像库中。这是因为本地镜像库不支持加载带有证明的镜像。

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
