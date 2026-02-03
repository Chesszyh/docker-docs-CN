---
title: 注解 (Annotations)
description: 注解指定了关于 OCI 镜像的额外元数据
keywords: build, buildkit, annotations, metadata, 注解, 元数据
aliases:
- /build/building/annotations/
---

注解 (Annotations) 为镜像提供描述性元数据。使用注解来记录任意信息并将其附加到镜像上，这有助于使用者和工具理解镜像的来源、内容及使用方法。

注解与 [标签 (labels)] 类似，并在某种程度上有所重叠。两者都服务于同一个目的：为资源附加元数据。作为一个通用原则，您可以按如下方式理解注解与标签的区别：

- **注解** 描述 OCI 镜像组件，例如 [清单 (manifests)]、[索引 (indexes)] 和 [描述符 (descriptors)]。
- **标签** 描述 Docker 资源，例如镜像、容器、网络和卷。

OCI 镜像 [规范 (specification)] 定义了注解的格式，以及一组预定义的注解键。遵循指定的标准可以确保有关镜像的元数据能被 Docker Scout 等工具自动且一致地呈现。

注解不应与 [证明 (attestations)] 混淆：

- **证明** 包含关于镜像如何构建以及包含哪些内容的信息。证明作为镜像索引上的一个独立清单附加。证明并未由 Open Container Initiative (OCI) 进行标准化。
- **注解** 包含关于镜像的任意元数据。注解作为标签附加在镜像 [配置 (config)] 中，或者作为属性附加在镜像索引或清单上。

## 添加注解

您可以在构建镜像时，或者在创建镜像清单或索引时添加注解。

> [!NOTE]
> 
> Docker Engine 镜像库不支持加载带有注解的镜像。要使用注解进行构建，请确保直接将镜像推送到注册表，可以使用 `--push` CLI 标志或 [注册表导出器](/manuals/build/exporters/image-registry.md)。

要在命令行指定注解，请为 `docker build` 命令使用 `--annotation` 标志：

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

有关如何向通过 GitHub Actions 构建的镜像添加注解的示例，请参阅 [使用 GitHub Actions 添加镜像注解](/manuals/build/ci/github-actions/annotations.md)。

您还可以向使用 `docker buildx imagetools create` 创建的镜像添加注解。此命令仅支持向索引或清单描述符添加注解，请参阅 [CLI 参考](/reference/cli/docker/buildx/imagetools/create.md#annotation)。

## 检查注解 (Inspect)

要查看 **镜像索引 (image index)** 上的注解，请使用 `docker buildx imagetools inspect` 命令。这将显示索引及其包含的描述符（对清单的引用）的所有注解。以下示例显示了描述符上的 `org.opencontainers.image.documentation` 注解，以及索引上的 `org.opencontainers.image.authors` 注解。

```console {hl_lines=["10-12","19-21"]}
$ docker buildx imagetools inspect <镜像名> --raw
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

要检查清单上的注解，请使用 `docker buildx imagetools inspect` 命令并指定 `<镜像名>@<摘要>`，其中 `<摘要>` 是清单的 digest：

```console {hl_lines="22-25"}
$ docker buildx imagetools inspect <镜像名>@sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb --raw
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

默认情况下，注解被添加到镜像清单中。您可以通过在注解字符串前加上特殊的类型声明，来指定要将注解附加到哪个级别（OCI 镜像组件）：

```console
$ docker build --annotation "<类型>:<键>=<值>" .
```

支持以下类型：

- `manifest`：为清单添加注解。
- `index`：为根索引添加注解。
- `manifest-descriptor`：为索引中的清单描述符添加注解。
- `index-descriptor`：为镜像布局中的索引描述符添加注解。

例如，要构建一个在镜像索引上附带注解 `foo=bar` 的镜像：

```console
$ docker build --tag <镜像名> --push --annotation "index:foo=bar" .
```

请注意，构建任务必须生成您指定的组件，否则构建将失败。例如，以下操作无效，因为 `docker` 导出器不会生成索引：

```console
$ docker build --output type=docker --annotation "index:foo=bar" .
```

同样，以下示例也不起作用，因为在某些情况下（如显式禁用来源证明时），Buildx 默认会创建一个 `docker` 输出：

```console
$ docker build --provenance=false --annotation "index:foo=bar" .
```

可以使用逗号分隔指定多个类型，以便在多个级别添加注解。以下示例创建了一个在镜像索引和镜像清单上都带有 `foo=bar` 注解的镜像：

```console
$ docker build --tag <镜像名> --push --annotation "index,manifest:foo=bar" .
```

您还可以在类型前缀的方括号内指定平台限定符，以便仅为匹配特定操作系统和架构的组件添加注解。以下示例仅为 `linux/amd64` 清单添加 `foo=bar` 注解：

```console
$ docker build --tag <镜像名> --push --annotation "manifest[linux/amd64]:foo=bar" .
```

## 相关信息

相关文章：

- [使用 GitHub Actions 添加镜像注解](/manuals/build/ci/github-actions/annotations.md)
- [注解 OCI 规范][specification]

参考信息：

- [`docker buildx build --annotation`](/reference/cli/docker/buildx/build.md#annotation)
- [Bake 文件参考：`annotations`](/manuals/build/bake/reference.md#targetannotations)
- [`docker buildx imagetools create --annotation`](/reference/cli/docker/buildx/imagetools/create.md#annotation)

<!-- 链接 -->

[specification]: https://github.com/opencontainers/image-spec/blob/main/annotations.md
[attestations]: /manuals/build/metadata/attestations/_index.md
[config]: https://github.com/opencontainers/image-spec/blob/main/config.md
[descriptors]: https://github.com/opencontainers/image-spec/blob/main/descriptor.md
[indexes]: https://github.com/opencontainers/image-spec/blob/main/image-index.md
[labels]: /manuals/engine/manage-resources/labels.md
[manifests]: https://github.com/opencontainers/image-spec/blob/main/manifest.md