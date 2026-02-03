---
title: OCI 与 Docker 导出器 (OCI and Docker exporters)
keywords: build, buildx, buildkit, exporter, oci, docker, 导出器
description: >
  OCI 与 Docker 导出器用于在本地文件系统上创建一个镜像布局的 tar 包
alias:
  - /build/building/exporters/oci-docker/
---

`oci` 导出器将构建结果输出为一个 [OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/main/image-layout.md) 的 tar 包。`docker` 导出器的行为类似，不同之处在于它导出的是 Docker 镜像布局。

[`docker` 驱动](/manuals/build/builders/drivers/docker.md) 不支持这些导出器。如果您想要生成此类输出，必须使用 `docker-container` 或其他驱动程序。

## 语法

使用 `oci` 和 `docker` 导出器构建容器镜像：

```console
$ docker buildx build --output type=oci[,参数] .
```

```console
$ docker buildx build --output type=docker[,参数] .
```

下表描述了可用参数：

| 参数 | 类型 | 默认值 | 说明 |
| :------------------- | :-------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `name` | 字符串 | | 指定镜像名称（支持多个）。 |
| `dest` | 字符串 | | 目标路径。 |
| `tar` | `true`,`false` | `true` | 将输出打包为 tar 布局格式。 |
| `compression` | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip` | 压缩类型，参见 [压缩][1]。 |
| `compression-level` | `0..22` | | 压缩级别，参见 [压缩][1]。 |
| `force-compression` | `true`,`false` | `false` | 强制应用压缩，参见 [压缩][1]。 |
| `oci-mediatypes` | `true`,`false` | | 在导出器清单中使用 OCI 媒体类型。对于 `type=oci` 默认为 `true`，对于 `type=docker` 默认为 `false`。参见 [OCI 媒体类型][2]。 |
| `annotation.<键>` | 字符串 | | 为构建好的镜像附加带有相应 `键` 和 `值` 的注解，参见 [注解 (Annotations)][3]。 |

[1]: _index.md#压缩
[2]: _index.md#oci-媒体类型
[3]: #注解-annotations

## 注解 (Annotations)

这些导出器支持使用 `annotation` 参数添加 OCI 注解，后跟使用点记法表示的注解名称。以下示例设置了 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<类型>,name=<注册表>/<镜像名>,annotation.org.opencontainers.image.title=<标题>" .
```

欲了解更多关于注解的信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 深入阅读

有关 `oci` 或 `docker` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#docker-tarball)。