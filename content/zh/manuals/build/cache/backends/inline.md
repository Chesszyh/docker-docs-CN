---
title: 内联缓存 (Inline cache)
description: 将构建缓存嵌入到镜像中
keywords: build, buildx, cache, backend, inline, 缓存, 后端
aliases:
  - /build/building/cache/backends/inline/
---

`inline` 缓存存储后端是获取外部缓存的最简单方式，如果您已经在构建并推送镜像，那么它非常容易上手。

内联缓存的缺点是，在多阶段构建中的扩展性不如其他驱动程序好。它也无法在您的输出产物和缓存输出之间提供分离。这意味着如果您使用的是特别复杂的构建流程，或者不是直接将镜像导出到注册表，那么您可能需要考虑 [注册表 (registry)](./registry.md) 缓存。

## 语法

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=inline \
  --cache-from type=registry,ref=<注册表>/<镜像名> .
```

`inline` 缓存不支持任何额外参数。

要使用 `inline` 存储导出缓存，请向 `--cache-to` 选项传递 `type=inline`：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=inline .
```

或者，您也可以通过设置构建参数 `BUILDKIT_INLINE_CACHE=1` 来导出内联缓存，而不是使用 `--cache-to` 标志：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --build-arg BUILDKIT_INLINE_CACHE=1 .
```

要在未来的构建中导入生成的缓存，请向 `--cache-from` 传递 `type=registry`，这样您就可以从指定注册表中的 Docker 镜像内部提取缓存：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-from type=registry,ref=<注册表>/<镜像名> .
```

## 深入阅读

欲了解缓存简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `inline` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#inline-push-image-and-cache-together)。