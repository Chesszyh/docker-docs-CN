---
title: 构建证明
keywords: build, attestations, sbom, provenance, metadata
description: |
  介绍 Docker Build 的 SBOM 和 provenance 证明，它们是什么以及为什么存在
aliases:
  - /build/attestations/
---

{{< youtube-embed qOzcycbTs4o >}}

构建证明（Attestation）描述镜像是如何构建的，以及它包含什么内容。证明由 BuildKit 在构建时创建，并作为元数据附加到最终镜像。

证明的目的是使检查镜像并了解其来源、创建者及创建方式以及包含内容成为可能。这使您能够就镜像如何影响应用程序的供应链安全做出明智的决策。它还支持使用策略引擎根据您定义的策略规则验证镜像。

有两种类型的构建证明可用：

- 软件物料清单（SBOM，Software Bill of Materials）：镜像包含的软件工件列表，或用于构建镜像的软件工件列表。
- Provenance（来源证明）：镜像是如何构建的。

## 证明的目的

开源和第三方软件包的使用比以往任何时候都更加普遍。开发人员共享和重用代码是因为它有助于提高生产力，使团队能够更快地创建更好的产品。

导入和使用未经审查的外部创建的代码会带来严重的安全风险。即使您确实审查了所使用的软件，新的零日漏洞也会频繁被发现，这需要开发团队采取行动进行修复。

构建证明使查看镜像的内容及其来源变得更加容易。使用证明来分析和决定是否使用某个镜像，或查看您已经使用的镜像是否暴露于漏洞。

## 创建证明

当您使用 `docker buildx build` 构建镜像时，可以使用 `--provenance` 和 `--sbom` 选项向生成的镜像添加证明记录。您可以选择添加 SBOM 或 provenance 证明类型之一，或两者都添加。

```console
$ docker buildx build --sbom=true --provenance=true .
```

> [!NOTE]
>
> 默认镜像存储不支持证明。如果您使用默认镜像存储并使用默认的 `docker` 驱动程序构建镜像，或使用带有 `--load` 标志的其他驱动程序，证明将会丢失。
>
> 要确保证明被保留，您可以：
>
> - 使用带有 `--push` 标志的 `docker-container` 驱动程序直接将镜像推送到注册表。
> - 启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)。

> [!NOTE]
>
> Provenance 证明默认启用，使用 `mode=min` 选项。您可以使用 `--provenance=false` 标志或设置 [`BUILDX_NO_DEFAULT_ATTESTATIONS`](/manuals/build/building/variables.md#buildx_no_default_attestations) 环境变量来禁用 provenance 证明。
>
> 使用 `--provenance=true` 标志会默认附加 `mode=min` 的 provenance 证明。有关更多详细信息，请参阅 [Provenance 证明](./slsa-provenance.md)。

BuildKit 在构建镜像时生成证明。证明记录以 in-toto JSON 格式包装，并作为清单附加到最终镜像的镜像索引中。

## 存储

BuildKit 以 [in-toto 格式](https://github.com/in-toto/attestation)生成证明，该格式由 Linux 基金会支持的 [in-toto 框架](https://in-toto.io/)定义。

证明作为清单附加到镜像索引中。证明的数据记录存储为 JSON blob。

由于证明作为清单附加到镜像，这意味着您可以检查注册表中任何镜像的证明，而无需拉取整个镜像。

所有 BuildKit 导出器都支持证明。`local` 和 `tar` 无法将证明保存到镜像清单，因为它输出的是文件目录或 tarball，而不是镜像。相反，这些导出器将证明写入导出根目录中的一个或多个 JSON 文件。

## 示例

以下示例显示了 SBOM 证明的截断 in-toto JSON 表示。

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "pkg:docker/<registry>/<image>@<tag/digest>?platform=<platform>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
      "created": "2022-12-15T11:47:54.546747383Z",
      "creators": ["Organization: Anchore, Inc", "Tool: syft-v0.60.3"],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core-da0f600b-7f0a-4de0-8432-f83703e6bc4f",
    "name": "/run/src/core",
    // list of files that the image contains, e.g.:
    "files": [
      {
        "SPDXID": "SPDXRef-1ac501c94e2f9f81",
        "comment": "layerID: sha256:9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e",
        "fileName": "/bin/busybox",
        "licenseConcluded": "NOASSERTION"
      }
    ],
    // list of packages that were identified for this image:
    "packages": [
      {
        "name": "busybox",
        "originator": "Person: Sören Tempel <soeren+alpine@soeren-tempel.net>",
        "sourceInfo": "acquired package info from APK DB: lib/apk/db/installed",
        "versionInfo": "1.35.0-r17",
        "SPDXID": "SPDXRef-980737451f148c56",
        "description": "Size optimized toolbox of many common UNIX utilities",
        "downloadLocation": "https://busybox.net/",
        "licenseConcluded": "GPL-2.0-only",
        "licenseDeclared": "GPL-2.0-only"
        // ...
      }
    ],
    // files-packages relationship
    "relationships": [
      {
        "relatedSpdxElement": "SPDXRef-1ac501c94e2f9f81",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-980737451f148c56"
      },
      ...
    ],
    "spdxVersion": "SPDX-2.2"
  }
}
```

要深入了解证明存储方式的细节，请参阅[镜像证明存储（BuildKit）](attestation-storage.md)。

## 证明清单格式

证明存储为清单，由镜像索引引用。每个_证明清单_引用单个_镜像清单_（镜像的一个平台变体）。证明清单包含单个层，即证明的"值"。

以下示例显示了证明清单的结构：

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "size": 167,
    "digest": "sha256:916d7437a36dd0e258e64d9c5a373ca5c9618eeb1555e79bd82066e593f9afae"
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "size": 1833349,
      "digest": "sha256:3138024b98ed5aa8e3008285a458cd25a987202f2500ce1a9d07d8e1420f5491",
      "annotations": {
        "in-toto.io/predicate-type": "https://spdx.dev/Document"
      }
    }
  ]
}
```

### 作为 OCI 工件的证明

您可以使用 `image` 和 `registry` 导出器的 [`oci-artifact` 选项](/manuals/build/exporters/image-registry.md#synopsis) 配置证明清单的格式。如果设置为 `true`，证明清单的结构将更改如下：

- 向证明清单添加 `artifactType` 字段，值为 `application/vnd.docker.attestation.manifest.v1+json`。
- `config` 字段是[空描述符]而不是"虚拟"配置。
- 还添加了 `subject` 字段，指向证明引用的镜像清单。

[空描述符]: https://github.com/opencontainers/image-spec/blob/main/manifest.md#guidance-for-an-empty-descriptor

以下示例显示了 OCI 工件格式的证明：

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "artifactType": "application/vnd.docker.attestation.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.empty.v1+json",
    "size": 2,
    "digest": "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "data": "e30="
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "size": 2208,
      "digest": "sha256:6d2f2c714a6bee3cf9e4d3cb9a966b629efea2dd8556ed81f19bd597b3325286",
      "annotations": {
        "in-toto.io/predicate-type": "https://slsa.dev/provenance/v0.2"
      }
    }
  ],
  "subject": {
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "size": 1054,
    "digest": "sha256:bc2046336420a2852ecf915786c20f73c4c1b50d7803aae1fd30c971a7d1cead",
    "platform": {
      "architecture": "amd64",
      "os": "linux"
    }
  }
}
```

## 下一步

了解更多关于可用证明类型及其使用方法的信息：

- [Provenance](slsa-provenance.md)
- [SBOM](sbom.md)
