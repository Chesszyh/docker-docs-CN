---
title: 注解 (Annotations)
description: 注解指定关于 OCI 镜像的额外元数据
keywords: build, buildkit, 注解, 元数据
---

注解（Annotations）为镜像提供描述性元数据。使用注解来记录任意信息并将其附加到镜像上，这有助于使用者和工具了解镜像的来源、内容以及如何使用。

注解与 [标签 (labels)] 类似，在某种意义上甚至有所重合。两者服务于同一目的：为资源附加元数据。作为一般原则，您可以将注解和标签的区别理解如下：

- 注解描述 OCI 镜像组件，例如 [清单 (manifests)]、[索引 (indexes)] 和 [描述符 (descriptors)]。
- 标签描述 Docker 资源，例如镜像、容器、网络和卷。

OCI 镜像 [规范 (specification)] 定义了注解的格式，以及一组预定义的注解键。遵循指定的标准可确保 Docker Scout 等工具能够自动且一致地呈现镜像的元数据。

注解不应与 [证明 (attestations)] 混淆：

- 证明包含了关于镜像如何构建以及包含什么内容的信息。证明作为镜像索引上的独立清单附加。证明尚未被开放容器计划 (OCI) 标准化。
- 注解包含关于镜像的任意元数据。注解可以作为标签附加到镜像 [配置 (config)] 上，或者作为属性附加到镜像索引或清单上。

## 添加注解

您可以在构建时，或者在创建镜像清单或索引时为镜像添加注解。

> [!NOTE]
> 
> Docker Engine 镜像库不支持加载带有注解的镜像。要构建带有注解的镜像，请务必使用 `--push` CLI 标志或 [registry 导出器](/manuals/build/exporters/image-registry.md) 将镜像直接推送到镜像库。

要在命令行上指定注解，请在 `docker build` 命令中使用 `--annotation` 标志：

```console
$ docker build --push --annotation "foo=bar" .
```

如果您使用的是 [Bake](/manuals/build/bake/_index.md)，可以使用 `annotations` 属性为指定目标指定注解：

```hcl
target "default" {
  output = ["type=registry"]
  annotations = ["foo=bar"]
}
```

有关如何为使用 GitHub Actions 构建的镜像添加注解的示例，请参阅 [使用 GitHub Actions 添加镜像注解](/manuals/build/ci/github-actions/annotations.md)。

您还可以为使用 `docker buildx imagetools create` 创建的镜像添加注解。此命令仅支持向索引或清单描述符添加注解，请参阅 [CLI 参考](/reference/cli/docker/buildx/imagetools/create.md#annotation)。

## 检查注解

要查看 **镜像索引** 上的注解，请使用 `docker buildx imagetools inspect` 命令。这将显示索引的任何注解以及索引包含的描述符（对清单的引用）。以下示例展示了描述符上的 `org.opencontainers.image.documentation` 注解，以及索引上的 `org.opencontainers.image.authors` 注解。

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

## 指定注解层级

默认情况下，注解会被添加到镜像清单中。您可以通过在注解字符串前加上特殊类型声明来指定将其附加到哪个层级（OCI 镜像组件）：

```console
$ docker build --annotation "<TYPE>:<KEY>=<VALUE>" .
```

支持以下类型：

- `manifest`：为清单添加注解。
- `index`：为根索引添加注解。
- `manifest-descriptor`：为索引中的清单描述符添加注解。
- `index-descriptor`：为镜像布局中的索引描述符添加注解。

例如，构建一个将 `foo=bar` 注解附加到镜像索引的镜像：

```console
$ docker build --tag <IMAGE> --push --annotation "index:foo=bar" .
```

请注意，构建必须生成您指定的组件，否则构建将失败。例如，以下操作无效，因为 `docker` 导出器不生成索引：

```console
$ docker build --output type=docker --annotation "index:foo=bar" .
```

同样，以下示例也不起作用，因为 buildx 在某些情况下（例如显式禁用来源证明时）默认创建 `docker` 输出：

```console
$ docker build --provenance=false --annotation "index:foo=bar" .
```

可以通过逗号分隔来指定多个类型，从而将注解添加到多个层级。以下示例创建了一个在镜像索引和镜像清单上都有 `foo=bar` 注解的镜像：

```console
$ docker build --tag <IMAGE> --push --annotation "index,manifest:foo=bar" .
```

您还可以在类型前缀的方括号内指定平台限定符，以便仅为匹配特定操作系统和架构的组件添加注解。以下示例仅为 `linux/amd64` 清单添加 `foo=bar` 注解：

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
[标签 (labels)]: /manuals/engine/manage-resources/labels.md
[证明 (attestations)]: /manuals/build/metadata/attestations/_index.md
[清单 (manifests)]: https://github.com/opencontainers/image-spec/blob/main/manifest.md
[索引 (indexes)]: https://github.com/opencontainers/image-spec/blob/main/image-index.md
[描述符 (descriptors)]: https://github.com/opencontainers/image-spec/blob/main/descriptor.md
[配置 (config)]: https://github.com/opencontainers/image-spec/blob/main/config.md
