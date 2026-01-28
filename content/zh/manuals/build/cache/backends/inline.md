---
title: 内联缓存
description: 将构建缓存嵌入到镜像中
keywords: build, buildx, cache, backend, inline
aliases:
  - /build/building/cache/backends/inline/
---

`inline` 缓存存储后端是获取外部缓存的最简单方式，如果你已经在构建和推送镜像，它很容易上手使用。

内联缓存的缺点是它在多阶段构建中的扩展性不如其他驱动程序。它也不提供输出产物和缓存输出之间的分离。这意味着如果你使用特别复杂的构建流程，或者不直接将镜像导出到注册表，那么你可能需要考虑使用 [registry](./registry.md) 缓存。

## 概要

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline \
  --cache-from type=registry,ref=<registry>/<image> .
```

`inline` 缓存不支持额外的参数。

要使用 `inline` 存储导出缓存，请将 `type=inline` 传递给 `--cache-to` 选项：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline .
```

或者，你也可以通过设置构建参数 `BUILDKIT_INLINE_CACHE=1` 来导出内联缓存，而不是使用 `--cache-to` 标志：

```console
$ docker buildx build --push -t <registry>/<image> \
  --build-arg BUILDKIT_INLINE_CACHE=1 .
```

要在未来的构建中导入生成的缓存，请将 `type=registry` 传递给 `--cache-from`，这允许你从指定注册表中的 Docker 镜像内部提取缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-from type=registry,ref=<registry>/<image> .
```

## 延伸阅读

有关缓存的介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `inline` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#inline-push-image-and-cache-together)。
