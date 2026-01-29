---
title: 本地缓存
description: 使用本地文件系统目录管理构建缓存
keywords: build, buildx, cache, backend, local
alias:
  - /build/building/cache/backends/local/
---

`local` 缓存存储是一个简单的缓存选项，它将您的缓存作为文件存储在文件系统的目录中，底层目录结构使用 [OCI 镜像布局 (OCI image layout)](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)。如果您只是进行测试，或者想要灵活地自行管理共享存储解决方案，本地缓存是一个不错的选择。

## 概要

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir[,parameters...] \
  --cache-from type=local,src=path/to/local/dir .
```

下表描述了您可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称 | 选项 | 类型 | 默认值 | 描述 |
|:--------------------|:--------------|:-------------------------|:---------|:---------------------------------------------------------------------------------------------------------------------------------|
| `src`               | `cache-from` | 字符串                  |         | 导入缓存的本地目录路径。                                                                     |
| `digest`            | `cache-from` | 字符串                  |         | 要导入的清单摘要（digest），请参阅 [缓存版本控制][4]。                                                                        |
| `dest`              | `cache-to`   | 字符串                  |         | 导出缓存的本地目录路径。                                                                       |
| `mode`              | `cache-to`   | `min`,`max`             | `min`   | 要导出的缓存层，请参阅 [缓存模式][1]。                                                                                    |
| `oci-mediatypes`    | `cache-to`   | `true`,`false`          | `true`  | 在导出的清单中使用 OCI 媒体类型，请参阅 [OCI 媒体类型][2]。                                                            |
| `image-manifest`    | `cache-to`   | `true`,`false`          | `true`  | 使用 OCI 媒体类型时，为缓存镜像生成单个镜像清单而不是镜像索引，请参阅 [OCI 媒体类型][2]。 |
| `compression`       | `cache-to`   | `gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，请参阅 [缓存压缩][3]。                                                                                   |
| `compression-level` | `cache-to`   | `0..22`                 |         | 压缩级别，请参阅 [缓存压缩][3]。                                                                                  |
| `force-compression` | `cache-to`   | `true`,`false`          | `false` | 强制应用压缩，请参阅 [缓存压缩][3]。                                                                         |
| `ignore-error`      | `cache-to`   | 布尔值                 | `false` | 忽略由于缓存导出失败引起的错误。                                                                                   |

[1]: _index.md#缓存模式
[2]: _index.md#OCI-媒体类型
[3]: _index.md#缓存压缩
[4]: #缓存版本控制

如果 `src` 缓存不存在，则缓存导入步骤将失败，但构建会继续。

## 缓存版本控制

<!-- FIXME: update once https://github.com/moby/buildkit/pull/3111 is released -->

本节介绍本地文件系统上缓存的版本控制工作原理，以及如何使用 `digest` 参数使用旧版本的缓存。

如果您手动检查缓存目录，可以看到生成的 OCI 镜像布局：

```console
$ ls cache
blobs  index.json  ingest
$ cat cache/index.json | jq
{
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.index.v1+json",
      "digest": "sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707",
      "size": 1560,
      "annotations": {
        "org.opencontainers.image.ref.name": "latest"
      }
    }
  ]
}
```

与其他缓存类型一样，本地缓存在导出时会通过替换 `index.json` 文件的内容而被替换。然而，先前的缓存仍可在 `blobs` 目录中找到。这些旧缓存可以通过摘要进行寻址，并无限期保留。因此，本地缓存的大小将持续增长（有关更多信息，请参阅 [`moby/buildkit#1896`](https://github.com/moby/buildkit/issues/1896)）。

在使用 `--cache-from` 导入缓存时，您可以指定 `digest` 参数来强制加载较旧版本的缓存，例如：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir \
  --cache-from type=local,ref=path/to/local/dir,digest=sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707 .
```

## 延伸阅读

有关缓存的简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `local` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#local-directory-1)。
