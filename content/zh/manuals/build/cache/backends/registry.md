---
title: Registry 缓存
description: 使用 OCI 镜像库管理构建缓存
keywords: build, buildx, cache, backend, registry
---

`registry` 缓存存储可以被视为 `inline` 缓存的扩展。与 `inline` 缓存不同，`registry` 缓存完全独立于镜像，这允许更灵活的使用方式——基于 `registry` 的缓存可以完成 `inline` 缓存的所有功能，甚至更多：

- 允许将缓存和生成的镜像构件分离，以便您分发的最终镜像内部不包含缓存。
- 它可以在 `max` 模式下高效地缓存多阶段构建，而不仅仅是最后阶段。
- 它可以与其他导出器配合使用以获得更多灵活性，而不仅仅是 `image` 导出器。

默认的 `docker` 驱动程序不支持此缓存存储后端。要使用此功能，请使用不同的驱动程序创建一个新构建器。有关更多信息，请参阅 [构建驱动程序](/manuals/build/builders/drivers/_index.md)。

## 概要

与较简单的 `inline` 缓存不同，`registry` 缓存支持多个配置参数：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

下表描述了您可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称 | 选项 | 类型 | 默认值 | 描述 |
|:--------------------|:-------------------------|:-------------------------|:---------|:---------------------------------------------------------------------------------------------------------------------------------|
| `ref`               | `cache-to`,`cache-from` | 字符串                  |         | 要导入的缓存镜像的全名。                                                                                         |
| `mode`              | `cache-to`              | `min`,`max`             | `min`   | 要导出的缓存层，请参阅 [缓存模式][1]。                                                                                    |
| `oci-mediatypes`    | `cache-to`              | `true`,`false`          | `true`  | 在导出的清单中使用 OCI 媒体类型，请参阅 [OCI 媒体类型][2]。                                                            |
| `image-manifest`    | `cache-to`              | `true`,`false`          | `true`  | 使用 OCI 媒体类型时，为缓存镜像生成单个镜像清单而不是镜像索引，请参阅 [OCI 媒体类型][2]。 |
| `compression`       | `cache-to`              | `gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，请参阅 [缓存压缩][3]。                                                                                   |
| `compression-level` | `cache-to`              | `0..22`                 |         | 压缩级别，请参阅 [缓存压缩][3]。                                                                                  |
| `force-compression` | `cache-to`              | `true`,`false`          | `false` | 强制应用压缩，请参阅 [缓存压缩][3]。                                                                         |
| `ignore-error`      | `cache-to`              | 布尔值                 | `false` | 忽略由于缓存导出失败引起的错误。                                                                                   |

[1]: _index.md#缓存模式
[2]: _index.md#OCI-媒体类型
[3]: _index.md#缓存压缩

您可以为 `ref` 选择任何有效值，只要它与您推送镜像的目标位置不同即可。您可以选择不同的标签（例如 `foo/bar:latest` 和 `foo/bar:build-cache`）、独立的镜像名称（例如 `foo/bar` 和 `foo/bar-cache`），甚至是不同的仓库（例如 `docker.io/foo/bar` 和 `ghcr.io/foo/bar`）。将镜像与缓存镜像分离的策略由您决定。

如果 `--cache-from` 目标不存在，则缓存导入步骤将失败，但构建会继续。

## 延伸阅读

有关缓存的简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `registry` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately)。
