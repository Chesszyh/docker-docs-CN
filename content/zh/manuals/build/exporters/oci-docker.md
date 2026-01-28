---
title: OCI 和 Docker 导出器
keywords: build, buildx, buildkit, exporter, oci, docker
description: >
  OCI 和 Docker 导出器在本地文件系统上创建镜像布局 tarball
aliases:
  - /build/building/exporters/oci-docker/
---

`oci` 导出器将构建结果输出为 [OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/main/image-layout.md) tarball。`docker` 导出器的行为相同，但它导出的是 Docker 镜像布局。

[`docker` 驱动程序](/manuals/build/builders/drivers/docker.md)不支持这些导出器。如果您想生成这些输出，必须使用 `docker-container` 或其他驱动程序。

## 概要

使用 `oci` 和 `docker` 导出器构建容器镜像：

```console
$ docker buildx build --output type=oci[,parameters] .
```

```console
$ docker buildx build --output type=docker[,parameters] .
```

下表描述了可用的参数：

| 参数           | 类型                                   | 默认值 | 描述                                                                                                                           |
| ------------------- | -------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | String                                 |         | 指定镜像名称                                                                                                                 |
| `dest`              | String                                 |         | 路径                                                                                                                  |
| `tar`               | `true`,`false`                         | `true`  | 将输出打包为 tarball 布局                                                                                               |
| `compression`       | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，参见[压缩][1]                                                                                                |
| `compression-level` | `0..22`                                |         | 压缩级别，参见[压缩][1]                                                                                               |
| `force-compression` | `true`,`false`                         | `false` | 强制应用压缩，参见[压缩][1]                                                                                    |
| `oci-mediatypes`    | `true`,`false`                         |         | 在导出器清单中使用 OCI 媒体类型。`type=oci` 默认为 `true`，`type=docker` 默认为 `false`。参见 [OCI 媒体类型][2] |
| `annotation.<key>`  | String                                 |         | 将带有相应 `key` 和 `value` 的注解附加到构建的镜像，参见[注解][3]                                    |

[1]: _index.md#compression
[2]: _index.md#oci-media-types
[3]: #annotations

## 注解 {#annotations}

这些导出器支持使用 `annotation` 参数添加 OCI 注解，后跟使用点表示法的注解名称。以下示例设置 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

有关注解的更多信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 进一步阅读

有关 `oci` 或 `docker` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#docker-tarball)。
