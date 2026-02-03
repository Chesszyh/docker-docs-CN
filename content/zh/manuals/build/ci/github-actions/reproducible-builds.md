---
title: 在 GitHub Actions 中实现可重现构建
linkTitle: 可重现构建
description: 如何使用 SOURCE_EPOCH 环境变量在 GitHub Actions 中创建可重现的构建
keywords: build, buildx, github actions, ci, gha, reproducible builds, SOURCE_DATE_EPOCH, 可重现构建
---

`SOURCE_DATE_EPOCH` 是一个 [标准化环境变量][source_date_epoch]，用于指示构建工具生成可重现（reproducible）的输出。在构建时设置该环境变量，会使镜像索引、镜像配置以及文件元数据中的时间戳反映指定的 Unix 时间。

[source_date_epoch]: https://reproducible-builds.org/docs/source-date-epoch/

要在 GitHub Actions 中设置该环境变量，请在构建步骤中使用内置的 `env` 属性。

## Unix Epoch 时间戳

以下示例将 `SOURCE_DATE_EPOCH` 变量设置为 0（即 Unix Epoch）。

{{< tabs group="action" >}}
{{< tab name="`docker/build-push-action`" >}}

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
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: 0
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

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
        uses: docker/bake-action@v6
        env:
          SOURCE_DATE_EPOCH: 0
```

{{< /tab >}}
{{< /tabs >}}

## Git 提交时间戳

以下示例将 `SOURCE_DATE_EPOCH` 设置为 Git 提交时间戳。

{{< tabs group="action" >}}
{{< tab name="`docker/build-push-action`" >}}

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

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/build-push-action@v6
        with:
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

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

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/bake-action@v6
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

{{< /tab >}}
{{< /tabs >}}

## 额外信息

欲了解更多关于 BuildKit 中对 `SOURCE_DATE_EPOCH` 的支持，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch)。