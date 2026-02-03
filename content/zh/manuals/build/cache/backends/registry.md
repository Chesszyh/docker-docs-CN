---
title: 注册表缓存 (Registry cache)
description: 使用 OCI 注册表管理构建缓存
keywords: build, buildx, cache, backend, registry, 缓存, 后端, 注册表
aliases:
  - /build/building/cache/backends/registry/
---

`registry` 缓存存储后端可以被视为 `inline` 缓存的扩展。与内联缓存不同，注册表缓存与镜像完全分离，这使得使用更加灵活。基于注册表的缓存能完成内联缓存的所有功能，并且还有以下额外优势：

- 允许将缓存与生成的镜像产物分离，这样您就可以分发不含缓存内容的最终镜像。
- 它可以在 `max` 模式下高效地为多阶段构建提供缓存，而不仅仅针对最终阶段。
- 它可以与其他导出器配合使用，提供更大的灵活性，而不仅仅限于 `image` 导出器。

默认的 `docker` 驱动不支持此缓存存储后端。要使用此特性，请使用其他驱动创建一个新构建器。更多信息请参见 [构建驱动](/manuals/build/builders/drivers/_index.md)。

## 语法

与简单的内联缓存不同，注册表缓存支持多个配置参数：

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=registry,ref=<注册表>/<缓存镜像名>[,参数...] \
  --cache-from type=registry,ref=<注册表>/<缓存镜像名> .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称 | 选项 | 类型 | 默认值 | 说明 |
|---------------------|-------------------------|-------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| `ref`               | `cache-to`,`cache-from` | 字符串 | | 要导入的缓存镜像的全名。 |
| `mode`              | `cache-to`              | `min`,`max` | `min` | 要导出的缓存层，参见 [缓存模式][1]。 |
| `oci-mediatypes`    | `cache-to`              | `true`,`false` | `true` | 在导出的清单中使用 OCI 媒体类型，参见 [OCI 媒体类型][2]。 |
| `image-manifest`    | `cache-to`              | `true`,`false` | `true` | 使用 OCI 媒体类型时，为缓存镜像生成镜像清单而非镜像索引，参见 [OCI 媒体类型][2]。 |
| `compression`       | `cache-to`              | `gzip`,`estargz`,`zstd` | `gzip` | 压缩类型，参见 [缓存压缩][3]。 |
| `compression-level` | `cache-to`              | `0..22` | | 压缩级别，参见 [缓存压缩][3]。 |
| `force-compression` | `cache-to`              | `true`,`false` | `false` | 强制应用压缩，参见 [缓存压缩][3]。 |
| `ignore-error`      | `cache-to`              | 布尔值 | `false` | 忽略由于缓存导出失败而引起的错误。 |

[1]: _index.md#缓存模式
[2]: _index.md#oci-媒体类型
[3]: _index.md#缓存压缩

只要不与您推送镜像的目标位置相同，您可以为 `ref` 选择任何有效值。您可以选择不同的标签（例如 `foo/bar:latest` 和 `foo/bar:build-cache`）、独立于镜像的名称（例如 `foo/bar` 和 `foo/bar-cache`），甚至不同的存储库（例如 `docker.io/foo/bar` 和 `ghcr.io/foo/bar`）。您可以根据自己的需要来决定将镜像与缓存镜像分离的策略。

如果 `--cache-from` 目标不存在，则缓存导入步骤将失败，但构建会继续进行。

## 深入阅读

欲了解缓存简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `registry` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately)。