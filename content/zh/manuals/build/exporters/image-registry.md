---
title: 镜像和镜像库导出器
description: 镜像和镜像库导出器创建可加载到本地镜像库或推送到镜像库的镜像
keywords: build, buildx, buildkit, 导出器, 镜像, 镜像库
alias:
  - /build/building/exporters/image-registry/
---

`image` 导出器将构建结果以容器镜像格式输出。`registry` 导出器与之相同，但它通过设置 `push=true` 自动推送结果。

## 概要

使用 `image` 和 `registry` 导出器构建容器镜像：

```console
$ docker buildx build --output type=image[,parameters] .
$ docker buildx build --output type=registry[,parameters] .
```

下表描述了您可以传递给 `type=image` 的 `--output` 的可用参数：

| 参数 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `name`                 | 字符串                                 |         | 指定镜像名称                                                                                                                                                                                                               |
| `push`                 | `true`,`false`                         | `false` | 创建镜像后推送。                                                                                                                                                                                                      |
| `push-by-digest`       | `true`,`false`                         | `false` | 推送不带名称的镜像。                                                                                                                                                                                                            |
| `registry.insecure`    | `true`,`false`                         | `false` | 允许推送到不安全的镜像库。                                                                                                                                                                                                 |
| `dangling-name-prefix` | `<值>`                              |         | 使用 `prefix@<摘要>` 命名镜像，用于匿名镜像                                                                                                                                                                        |
| `name-canonical`       | `true`,`false`                         |         | 添加额外的规范名称 `name@<摘要>`                                                                                                                                                                                       |
| `compression`          | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，请参阅 [压缩][1]                                                                                                                                                                                              |
| `compression-level`    | `0..22`                                |         | 压缩级别，请参阅 [压缩][1]                                                                                                                                                                                             |
| `force-compression`    | `true`,`false`                         | `false` | 强制应用压缩，请参阅 [压缩][1]                                                                                                                                                                                  |
| `rewrite-timestamp`    | `true`,`false`                         | `false` | 将文件时间戳重写为 `SOURCE_DATE_EPOCH` 值。有关如何指定 `SOURCE_DATE_EPOCH` 值，请参阅 [构建可复现性][4]。                                                                                      |
| `oci-mediatypes`       | `true`,`false`                         | `false` | 在导出清单中使用 OCI 媒体类型，请参阅 [OCI 媒体类型][2]                                                                                                                                                                 |
| `oci-artifact`         | `true`,`false`                         | `false` | 证明格式化为 OCI 构件，请参阅 [OCI 媒体类型][2]                                                                                                                                                               |
| `unpack`               | `true`,`false`                         | `false` | 创建后解压镜像（用于 containerd）                                                                                                                                                                               |
| `store`                | `true`,`false`                         | `true`  | 将结果镜像存储到 worker（例如 containerd）的镜像库中，并确保镜像在内容存储中具有所有 blob。如果 worker 没有镜像库（例如使用 OCI worker 时），则忽略此项。 | 
| `annotation.<key>`     | 字符串                                 |         | 将带有相应 `key` 和 `value` 的注解附加到构建的镜像上，请参阅 [注解][3]                                                                                                                                  |

[1]: _index.md#压缩
[2]: _index.md#OCI-媒体类型
[3]: #注解
[4]: https://github.com/moby/buildkit/blob/master/docs/build-repro.md
[5]: /manuals/build/metadata/attestations/_index.md#将证明作为-OCI-构件

## 注解

这些导出器支持使用 `annotation` 参数添加 OCI 注解，后接使用点号表示法的注解名称。以下示例设置了 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

有关注解的更多信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 延伸阅读

有关 `image` 或 `registry` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#imageregistry)。
