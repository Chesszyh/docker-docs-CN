---
title: 镜像与注册表导出器 (Image and registry exporters)
description: |
  镜像与注册表导出器用于创建一个可加载到本地镜像库或推送到注册表的镜像。
keywords: build, buildx, buildkit, exporter, image, registry, 导出器, 镜像, 注册表
alias:
  - /build/building/exporters/image-registry/
---

`image` 导出器将构建结果输出为容器镜像格式。`registry` 导出器与之完全相同，但它通过设置 `push=true` 自动执行推送操作。

## 语法

使用 `image` 和 `registry` 导出器构建容器镜像：

```console
$ docker buildx build --output type=image[,参数] .
$ docker buildx build --output type=registry[,参数] .
```

下表描述了可以传递给 `type=image` 的 `--output` 可用参数：

| 参数 | 类型 | 默认值 | 说明 |
| ---------------------- | -------------------------------------- | ------- | -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `name` | 字符串 | | 指定镜像名称（支持多个）。 |
| `push` | `true`,`false` | `false` | 创建镜像后进行推送。 |
| `push-by-digest` | `true`,`false` | `false` | 推送不带名称的镜像。 |
| `registry.insecure` | `true`,`false` | `false` | 允许推送到非安全注册表。 |
| `dangling-name-prefix` | `<值>` | | 以 `prefix@<摘要>` 命名镜像，用于匿名镜像。 |
| `name-canonical` | `true`,`false` | | 增加额外的规范化名称 `name@<摘要>`。 |
| `compression` | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip` | 压缩类型，参见 [压缩][1]。 |
| `compression-level` | `0..22` | | 压缩级别，参见 [压缩][1]。 |
| `force-compression` | `true`,`false` | `false` | 强制应用压缩，参见 [压缩][1]。 |
| `rewrite-timestamp` | `true`,`false` | `false` | 将文件时间戳重写为 `SOURCE_DATE_EPOCH` 的值。参见 [构建可重现性][4] 了解如何指定 `SOURCE_DATE_EPOCH` 值。 |
| `oci-mediatypes` | `true`,`false` | `false` | 在导出器清单中使用 OCI 媒体类型，参见 [OCI 媒体类型][2]。 |
| `oci-artifact` | `true`,`false` | `false` | 将证明格式化为 OCI 产物，参见 [OCI 媒体类型][2]。 |
| `unpack` | `true`,`false` | `false` | 创建后解压镜像（供 containerd 使用）。 |
| `store` | `true`,`false` | `true` | 将结果镜像存储到工作线程（如 containerd）的镜像库中，并确保镜像的所有 blob 都在内容存储库中。如果工作线程没有镜像库（例如使用 OCI 工作线程时），则忽略此项。 |
| `annotation.<键>` | 字符串 | | 为构建好的镜像附加带有相应 `键` 和 `值` 的注解，参见 [注解 (Annotations)][3]。 |

[1]: _index.md#压缩
[2]: _index.md#oci-媒体类型
[3]: #注解-annotations
[4]: https://github.com/moby/buildkit/blob/master/docs/build-repro.md
[5]: /manuals/build/metadata/attestations/_index.md#作为-oci-产物的证明

## 注解 (Annotations)

这些导出器支持使用 `annotation` 参数添加 OCI 注解，后跟使用点记法表示的注解名称。以下示例设置了 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<类型>,name=<注册表>/<镜像名>,annotation.org.opencontainers.image.title=<标题>" .
```

欲了解更多关于注解的信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 深入阅读

有关 `image` 或 `registry` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#imageregistry).