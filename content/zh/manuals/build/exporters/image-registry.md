---
title: Image 和 registry 导出器
description: |
  image 和 registry 导出器创建可以加载到本地镜像存储或推送到注册表的镜像
keywords: build, buildx, buildkit, exporter, image, registry
aliases:
  - /build/building/exporters/image-registry/
---

`image` 导出器将构建结果输出为容器镜像格式。`registry` 导出器是相同的，但它通过设置 `push=true` 自动推送结果。

## 概要

使用 `image` 和 `registry` 导出器构建容器镜像：

```console
$ docker buildx build --output type=image[,parameters] .
$ docker buildx build --output type=registry[,parameters] .
```

下表描述了可以传递给 `--output` 的 `type=image` 的可用参数：

| 参数              | 类型                                   | 默认值 | 描述                                                                                                                                                                                                                         |
| ---------------------- | -------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                 | String                                 |         | 指定镜像名称                                                                                                                                                                                                               |
| `push`                 | `true`,`false`                         | `false` | 创建镜像后推送。                                                                                                                                                                                                      |
| `push-by-digest`       | `true`,`false`                         | `false` | 推送镜像而不带名称。                                                                                                                                                                                                            |
| `registry.insecure`    | `true`,`false`                         | `false` | 允许推送到不安全的注册表。                                                                                                                                                                                                 |
| `dangling-name-prefix` | `<value>`                              |         | 使用 `prefix@<digest>` 命名镜像，用于匿名镜像                                                                                                                                        |
| `name-canonical`       | `true`,`false`                         |         | 添加额外的规范名称 `name@<digest>`                                                                                                                                                                                       |
| `compression`          | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，参见[压缩][1]                                                                                                                                                                                              |
| `compression-level`    | `0..22`                                |         | 压缩级别，参见[压缩][1]                                                                                                                                                                                             |
| `force-compression`    | `true`,`false`                         | `false` | 强制应用压缩，参见[压缩][1]                                                                                                                                                                  |
| `rewrite-timestamp`    | `true`,`false`                         | `false` | 将文件时间戳重写为 `SOURCE_DATE_EPOCH` 值。有关如何指定 `SOURCE_DATE_EPOCH` 值，请参阅[构建可重现性][4]。                                                                                      |
| `oci-mediatypes`       | `true`,`false`                         | `false` | 在导出器清单中使用 OCI 媒体类型，参见 [OCI 媒体类型][2]                                                                                                                                 |
| `oci-artifact`         | `true`,`false`                         | `false` | 证明格式化为 OCI 工件，参见 [OCI 媒体类型][2]                                                                                                                               |
| `unpack`               | `true`,`false`                         | `false` | 创建后解包镜像（用于 containerd）                                                                                                                                                                               |
| `store`                | `true`,`false`                         | `true`  | 将结果镜像存储到 worker（例如 containerd）的镜像存储，并确保镜像在内容存储中包含所有 blob。如果 worker 没有镜像存储（例如使用 OCI worker 时），则忽略。 |
| `annotation.<key>`     | String                                 |         | 将带有相应 `key` 和 `value` 的注解附加到构建的镜像，参见[注解][3]                                                                                  |

[1]: _index.md#compression
[2]: _index.md#oci-media-types
[3]: #annotations
[4]: https://github.com/moby/buildkit/blob/master/docs/build-repro.md
[5]: /manuals/build/metadata/attestations/_index.md#attestations-as-oci-artifacts

## 注解 {#annotations}

这些导出器支持使用 `annotation` 参数添加 OCI 注解，后跟使用点表示法的注解名称。以下示例设置 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

有关注解的更多信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 进一步阅读

有关 `image` 或 `registry` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#imageregistry)。
