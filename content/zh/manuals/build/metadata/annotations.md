---
title: 注解
description: 注解指定有关 OCI 镜像的附加元数据
keywords: build, buildkit, annotations, metadata
aliases:
- /build/building/annotations/
---

注解（Annotation）为镜像提供描述性元数据。使用注解记录任意信息并将其附加到您的镜像，这有助于消费者和工具了解镜像的来源、内容以及如何使用。

注解与[标签（Label）][labels]类似，在某种意义上有所重叠。两者都服务于相同的目的：将元数据附加到资源。作为一般原则，您可以将注解和标签之间的区别理解如下：

- 注解描述 OCI 镜像组件，例如[清单（Manifest）][manifests]、[索引（Index）][indexes]和[描述符（Descriptor）][descriptors]。
- 标签描述 Docker 资源，例如镜像、容器、网络和卷。

OCI 镜像[规范][specification]定义了注解的格式，以及一组预定义的注解键。遵守指定的标准可确保有关镜像的元数据能够被 Docker Scout 等工具自动且一致地呈现。

注解不应与[证明（Attestation）][attestations]混淆：

- 证明包含有关镜像如何构建以及包含什么内容的信息。证明作为单独的清单附加到镜像索引上。证明未由 Open Container Initiative 标准化。
- 注解包含有关镜像的任意元数据。注解作为标签附加到镜像[配置（Config）][config]，或作为属性附加到镜像索引或清单。

## 添加注解

您可以在构建时或创建镜像清单或索引时向镜像添加注解。

> [!NOTE]
>
> Docker Engine 镜像存储不支持加载带有注解的镜像。要使用注解进行构建，请确保使用 `--push` CLI 标志或 [registry 导出器](/manuals/build/exporters/image-registry.md) 直接将镜像推送到注册表。

要在命令行上指定注解，请使用 `docker build` 命令的 `--annotation` 标志：

```console
$ docker build --push --annotation "foo=bar" .
```

如果您使用 [Bake](/manuals/build/bake/_index.md)，可以使用 `annotations` 属性为给定目标指定注解：

```hcl
target "default" {
  output = ["type=registry"]
  annotations = ["foo=bar"]
}
```

有关如何使用 GitHub Actions 向镜像添加注解的示例，请参阅[使用 GitHub Actions 添加镜像注解](/manuals/build/ci/github-actions/annotations.md)

您还可以使用 `docker buildx imagetools create` 向创建的镜像添加注解。此命令仅支持向索引或清单描述符添加注解，请参阅 [CLI 参考](/reference/cli/docker/buildx/imagetools/create.md#annotation)。

## 检查注解

要查看**镜像索引**上的注解，请使用 `docker buildx imagetools inspect` 命令。这会显示索引和索引包含的描述符（对清单的引用）的任何注解。以下示例显示了描述符上的 `org.opencontainers.image.documentation` 注解和索引上的 `org.opencontainers.image.authors` 注解。

```console {hl_lines=["10-12","19-21"]}
$ docker buildx imagetools inspect <IMAGE> --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb",
      "size": 911,
      "annotations": {
        "org.opencontainers.image.documentation": "https://foo.example/docs",
      },
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
  ],
  "annotations": {
    "org.opencontainers.image.authors": "dvdksn"
  }
}
```

要检查清单上的注解，请使用 `docker buildx imagetools inspect` 命令并指定 `<IMAGE>@<DIGEST>`，其中 `<DIGEST>` 是清单的摘要：

```console {hl_lines="22-25"}
$ docker buildx imagetools inspect <IMAGE>@sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:4368b6959a78b412efa083c5506c4887e251f1484ccc9f0af5c406d8f76ece1d",
    "size": 850
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:2c03dbb20264f09924f9eab176da44e5421e74a78b09531d3c63448a7baa7c59",
      "size": 3333033
    },
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:4923ad480d60a548e9b334ca492fa547a3ce8879676685b6718b085de5aaf142",
      "size": 61887305
    }
  ],
  "annotations": {
    "index,manifest:org.opencontainers.image.vendor": "foocorp",
    "org.opencontainers.image.source": "https://git.example/foo.git",
  }
}
```

## 指定注解级别

默认情况下，注解会添加到镜像清单。您可以通过在注解字符串前添加特殊类型声明来指定要将注解附加到哪个级别（OCI 镜像组件）：

```console
$ docker build --annotation "<TYPE>:<KEY>=<VALUE>" .
```

支持以下类型：

- `manifest`：注解清单。
- `index`：注解根索引。
- `manifest-descriptor`：注解索引中的清单描述符。
- `index-descriptor`：注解镜像布局中的索引描述符。

例如，构建一个将注解 `foo=bar` 附加到镜像索引的镜像：

```console
$ docker build --tag <IMAGE> --push --annotation "index:foo=bar" .
```

请注意，构建必须生成您指定的组件，否则构建将失败。例如，以下命令不起作用，因为 `docker` 导出器不生成索引：

```console
$ docker build --output type=docker --annotation "index:foo=bar" .
```

同样，以下示例也不起作用，因为在某些情况下（例如当显式禁用 provenance 证明时），buildx 默认创建 `docker` 输出：

```console
$ docker build --provenance=false --annotation "index:foo=bar" .
```

可以指定用逗号分隔的类型，将注解添加到多个级别。以下示例创建一个在镜像索引和镜像清单上都有 `foo=bar` 注解的镜像：

```console
$ docker build --tag <IMAGE> --push --annotation "index,manifest:foo=bar" .
```

您还可以在类型前缀中使用方括号指定平台限定符，仅注解匹配特定操作系统和架构的组件。以下示例仅将 `foo=bar` 注解添加到 `linux/amd64` 清单：

```console
$ docker build --tag <IMAGE> --push --annotation "manifest[linux/amd64]:foo=bar" .
```

## 相关信息

相关文章：

- [使用 GitHub Actions 添加镜像注解](/manuals/build/ci/github-actions/annotations.md)
- [注解 OCI 规范][specification]

参考信息：

- [`docker buildx build --annotation`](/reference/cli/docker/buildx/build.md#annotation)
- [Bake 文件参考：`annotations`](/manuals/build/bake/reference.md#targetannotations)
- [`docker buildx imagetools create --annotation`](/reference/cli/docker/buildx/imagetools/create.md#annotation)

<!-- links -->

[specification]: https://github.com/opencontainers/image-spec/blob/main/annotations.md
[attestations]: /manuals/build/metadata/attestations/_index.md
[config]: https://github.com/opencontainers/image-spec/blob/main/config.md
[descriptors]: https://github.com/opencontainers/image-spec/blob/main/descriptor.md
[indexes]: https://github.com/opencontainers/image-spec/blob/main/image-index.md
[labels]: /manuals/engine/manage-resources/labels.md
[manifests]: https://github.com/opencontainers/image-spec/blob/main/manifest.md
