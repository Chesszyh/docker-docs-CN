---
title: 使用 GitHub Actions 进行可复现构建
linkTitle: 可复现构建 (Reproducible builds)
description: 如何在 GitHub Actions 中使用 SOURCE_EPOCH 环境变量创建可复现构建
keywords: build, buildx, github actions, ci, gha, 可复现构建, SOURCE_DATE_EPOCH
---

`SOURCE_DATE_EPOCH` 是一个 [标准化的环境变量][source_date_epoch]，用于指示构建工具产生可复现的输出。为构建设置该环境变量，会使镜像索引、配置和文件元数据中的时间戳反映指定的 Unix 时间。

[source_date_epoch]: https://reproducible-builds.org/docs/source-date-epoch/

要在 GitHub Actions 中设置此环境变量，请在构建步骤中使用内置的 `env` 属性。

## Unix 纪元时间戳

以下示例将 `SOURCE_DATE_EPOCH` 变量设置为 0，即 Unix 纪元（Unix epoch）。

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

## Git commit 时间戳

以下示例将 `SOURCE_DATE_EPOCH` 设置为 Git commit 的时间戳。

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

## 其他信息

有关 BuildKit 中 `SOURCE_DATE_EPOCH` 支持的更多信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch)。
