---
title: Registry 缓存
description: 使用 OCI 注册表管理构建缓存
keywords: build, buildx, cache, backend, registry
aliases:
  - /build/building/cache/backends/registry/
---

`registry` 缓存存储可以被视为 `inline` 缓存的扩展。与 `inline` 缓存不同，`registry` 缓存与镜像完全分离，这允许更灵活的使用——`registry` 支持的缓存可以做 inline 缓存能做的所有事情，甚至更多：

- 允许分离缓存和生成的镜像产物，这样你可以分发最终镜像而无需在其中包含缓存。
- 它可以在 `max` 模式下高效地缓存多阶段构建，而不仅仅是最终阶段。
- 它可以与其他导出器一起工作以获得更多灵活性，而不仅仅是 `image` 导出器。

此缓存存储后端不支持默认的 `docker` 驱动程序。要使用此功能，请使用不同的驱动程序创建一个新的构建器。有关更多信息，请参阅[构建驱动程序](/manuals/build/builders/drivers/_index.md)。

## 概要

与更简单的 `inline` 缓存不同，`registry` 缓存支持多个配置参数：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称                | 选项                    | 类型                    | 默认值  | 描述                                                                                                             |
|---------------------|-------------------------|-------------------------|---------|------------------------------------------------------------------------------------------------------------------|
| `ref`               | `cache-to`,`cache-from` | String                  |         | 要导入的缓存镜像的完整名称。                                                                                      |
| `mode`              | `cache-to`              | `min`,`max`             | `min`   | 要导出的缓存层，参见[缓存模式][1]。                                                                               |
| `oci-mediatypes`    | `cache-to`              | `true`,`false`          | `true`  | 在导出的清单中使用 OCI 媒体类型，参见 [OCI 媒体类型][2]。                                                          |
| `image-manifest`    | `cache-to`              | `true`,`false`          | `true`  | 使用 OCI 媒体类型时，为缓存镜像生成镜像清单而不是镜像索引，参见 [OCI 媒体类型][2]。                                 |
| `compression`       | `cache-to`              | `gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，参见[缓存压缩][3]。                                                                                     |
| `compression-level` | `cache-to`              | `0..22`                 |         | 压缩级别，参见[缓存压缩][3]。                                                                                     |
| `force-compression` | `cache-to`              | `true`,`false`          | `false` | 强制应用压缩，参见[缓存压缩][3]。                                                                                 |
| `ignore-error`      | `cache-to`              | Boolean                 | `false` | 忽略由缓存导出失败引起的错误。                                                                                    |

[1]: _index.md#cache-mode
[2]: _index.md#oci-media-types
[3]: _index.md#cache-compression

你可以为 `ref` 选择任何有效的值，只要它与你推送镜像的目标位置不同即可。你可以选择不同的标签（例如，`foo/bar:latest` 和 `foo/bar:build-cache`）、不同的镜像名称（例如，`foo/bar` 和 `foo/bar-cache`），甚至不同的仓库（例如，`docker.io/foo/bar` 和 `ghcr.io/foo/bar`）。由你决定使用哪种策略来分离镜像和缓存镜像。

如果 `--cache-from` 目标不存在，则缓存导入步骤将失败，但构建会继续。

## 延伸阅读

有关缓存的介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `registry` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately)。
