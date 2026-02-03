---
title: SBOM 证明 (SBOM attestations)
keywords: build, attestations, sbom, spdx, metadata, packages, 软件物料清单, 证明
description: |
  SBOM 证明描述了镜像包含的软件产物以及用于创建该镜像的产物。
aliases:
  - /build/attestations/sbom/
---

SBOM 证明通过验证镜像包含的软件产物以及用于创建镜像的产物，有助于确保 [软件供应链透明度](/guides/docker-scout/s3c.md)。用于描述软件产物的 [SBOM](/guides/docker-scout/sbom.md) 中包含的元数据可能包括：

- 产物名称
- 版本号
- 许可证类型
- 作者
- 唯一的软件包标识符

在构建期间对镜像内容进行索引，相比于仅扫描最终镜像具有更多优势。当扫描作为构建的一部分发生时，您可以检测到用于构建镜像的软件，而这些软件可能不会出现在最终镜像中。

Docker 通过使用 BuildKit 和证明，支持通过符合 SLSA 标准的构建过程生成 SBOM 并进行证明。由 [BuildKit](/manuals/build/buildkit/_index.md) 生成的 SBOM 遵循 SPDX 标准，并使用由 [in-toto SPDX 谓词 (predicate)](https://github.com/in-toto/attestation/blob/main/spec/predicates/spdx.md) 定义的格式，以 JSON 编码的 SPDX 文档形式附加到最终镜像上。在本页中，您将学习如何使用 Docker 工具创建、管理和验证 SBOM 证明。

## 创建 SBOM 证明

要创建 SBOM 证明，请向 `docker buildx build` 命令传递 `--attest type=sbom` 选项：

```console
$ docker buildx build --tag <命名空间>/<镜像名>:<版本> \
    --attest type=sbom --push .
```

或者，您也可以使用简写的 `--sbom=true` 选项来代替 `--attest type=sbom`。

有关如何使用 GitHub Actions 添加 SBOM 证明的示例，请参阅 [使用 GitHub Actions 添加证明](/manuals/build/ci/github-actions/attestations.md)。

## 验证 SBOM 证明

在将镜像推送到注册表之前，务必验证为该镜像生成的 SBOM。

要进行验证，您可以使用 `local` 导出器构建镜像。使用 `local` 导出器构建会将构建结果保存到您的本地文件系统，而不是创建镜像。证明会以 JSON 文件的形式写入到导出目录的根目录下。

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
```

SBOM 文件出现在输出目录的根目录下，名为 `sbom.spdx.json`：

```console
$ ls -1 ./out | grep sbom
sbom.spdx.json
```

## 参数 (Arguments)

默认情况下，BuildKit 仅扫描镜像的最终阶段。生成的 SBOM 不包含在早期阶段安装的或存在于构建上下文中的构建时依赖项。这可能会导致您忽视这些依赖项中的漏洞，从而影响最终构建产物的安全性。

例如，您可能会使用 [多阶段构建](/manuals/build/building/multi-stage.md)，并在最终阶段使用 `FROM scratch` 语句以减小镜像体积。

```dockerfile
FROM alpine AS build
# 构建软件 ...

FROM scratch
COPY --from=build /path/to/bin /bin
ENTRYPOINT [ "/bin" ]
```

扫描使用此 Dockerfile 示例构建的镜像将无法发现 `build` 阶段中使用的构建时依赖项。

要在 SBOM 中包含来自 Dockerfile 的构建时依赖项，您可以设置构建参数 `BUILDKIT_SBOM_SCAN_CONTEXT` 和 `BUILDKIT_SBOM_SCAN_STAGE`。这会扩展扫描范围，使其包含构建上下文和其他阶段。

您可以将这些参数设置为全局参数（在声明 Dockerfile 语法指令后、第一个 `FROM` 命令之前定义），也可以在每个阶段中单独设置。如果设置为全局参数，其值将传递到 Dockerfile 中的每个阶段。

`BUILDKIT_SBOM_SCAN_CONTEXT` 和 `BUILDKIT_SBOM_SCAN_STAGE` 构建参数是特殊值。您不能使用这些参数进行变量替换，也不能在 Dockerfile 内部使用环境变量来设置它们。设置这些值的唯一方法是在 Dockerfile 中使用显式的 `ARG` 命令。

### 扫描构建上下文

要扫描构建上下文，请将 `BUILDKIT_SBOM_SCAN_CONTEXT` 设置为 `true`。

```dockerfile
# syntax=docker/dockerfile:1
ARG BUILDKIT_SBOM_SCAN_CONTEXT=true
FROM alpine AS build
# ...
```

您可以使用 `--build-arg` CLI 选项来覆盖 Dockerfile 中指定的值。

```console
$ docker buildx build --tag <镜像名>:<版本> \
    --attest type=sbom \
    --build-arg BUILDKIT_SBOM_SCAN_CONTEXT=false .
```

请注意，如果仅作为 CLI 参数传递而未在 Dockerfile 中使用 `ARG` 声明，则该选项不会生效。您必须在 Dockerfile 中指定 `ARG`，然后才能通过 `--build-arg` 覆盖上下文扫描行为。

### 扫描构建阶段

要扫描除最终阶段以外的其他阶段，请将 `BUILDKIT_SBOM_SCAN_STAGE` 参数设置为 true（可以全局设置，也可以在想要扫描的特定阶段中设置）。下表展示了该参数的不同可能设置。

| 值 | 说明 |
| ----------------------------------- | ------------------------------------------------------ |
| `BUILDKIT_SBOM_SCAN_STAGE=true` | 为当前阶段开启扫描 |
| `BUILDKIT_SBOM_SCAN_STAGE=false` | 为当前阶段禁用扫描 |
| `BUILDKIT_SBOM_SCAN_STAGE=base,bin` | 为名为 `base` 和 `bin` 的阶段开启扫描 |

仅会被构建的阶段才会被扫描。如果某些阶段不是目标阶段的依赖项，则它们既不会被构建，也不会被扫描。

以下 Dockerfile 示例使用多阶段构建来配合 [Hugo](https://gohugo.io/) 构建一个静态网站。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine as hugo
ARG BUILDKIT_SBOM_SCAN_STAGE=true
WORKDIR /src
COPY <<config.yml ./
title: My Hugo website
config.yml
RUN apk add --upgrade hugo && hugo

FROM scratch
COPY --from=hugo /src/public /
```

在 `hugo` 阶段设置 `ARG BUILDKIT_SBOM_SCAN_STAGE=true` 确保了最终的 SBOM 中包含用于创建网站的 Alpine Linux 和 Hugo 的信息。

使用 `local` 导出器构建此镜像会创建两个 JSON 文件：

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
$ ls -1 out | grep sbom
sbom-hugo.spdx.json
sbom.spdx.json
```

## 检查 SBOM

要探索通过 `image` 导出器导出的已创建 SBOM，您可以使用 [`imagetools inspect`](/reference/cli/docker/buildx/imagetools/inspect.md) 命令。

使用 `--format` 选项，您可以为输出指定一个模板。所有与 SBOM 相关的数据都在 `.SBOM` 属性下。例如，要获取 SPDX 格式的原始 SBOM 内容：

```console
$ docker buildx imagetools inspect <命名空间>/<镜像名>:<版本> \
    --format "{{ json .SBOM.SPDX }}"
{
  "SPDXID": "SPDXRef-DOCUMENT",
  ...
}
```

> [!TIP]
> 
> 如果镜像是多平台的，您可以使用 `--format '{{ json (index .SBOM "linux/amd64").SPDX }}'` 来检查特定平台的索引。

您还可以利用 Go 模板的完整功能构建更复杂的表达式。例如，列出所有已安装的软件包及其版本标识符：

```console
$ docker buildx imagetools inspect <命名空间>/<镜像名>:<版本> \
    --format "{{ range .SBOM.SPDX.packages }}{{ .name }}@{{ .versionInfo }}{{ println }}{{ end }}"
adduser@3.118ubuntu2
apt@2.0.9
base-files@11ubuntu5.6
base-passwd@3.5.47
...
```

## SBOM 生成器 (Generator)

BuildKit 使用扫描器插件生成 SBOM。默认使用的是 [BuildKit Syft 扫描器](https://github.com/docker/buildkit-syft-scanner) 插件。该插件构建在 [Anchore 的 Syft](https://github.com/anchore/syft) 之上，Syft 是一款用于生成 SBOM 的开源工具。

您可以通过 `generator` 选项选择不同的插件，指定一个实现了 [BuildKit SBOM 扫描器协议](https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md) 的镜像。

```console
$ docker buildx build --attest type=sbom,generator=<镜像名> .
```

> [!TIP]
> 
> 也可以使用 Docker Scout SBOM 生成器。参见 [Docker Scout SBOMs](/manuals/scout/how-tos/view-create-sboms.md)。

## SBOM 证明示例

以下 JSON 示例展示了一个 SBOM 证明的可能样貌。

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "pkg:docker/<注册表>/<镜像名>@<标签/摘要>?platform=<平台>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
      "created": "2022-12-16T15:27:25.517047753Z",
      "creators": ["Organization: Anchore, Inc", "Tool: syft-v0.60.3"],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core/sbom-cba61a72-fa95-4b60-b63f-03169eac25ca",
    "name": "/run/src/core/sbom",
    "packages": [
      {
        "SPDXID": "SPDXRef-b074348b8f56ea64",
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:org:repo:\\(devel\\):*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/org/repo@(devel)",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/org/repo",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "(devel)"
      },
      {
        "SPDXID": "SPDXRef-1b96f57f8fed62d8",
        "checksums": [
          {
            "algorithm": "SHA256",
            "checksumValue": "0c13f1f3c1636491f716c2027c301f21f9dbed7c4a2185461ba94e3e58443408"
          }
        ],
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go-chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go_chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/go-chi/chi/v5@v5.0.0",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/go-chi/chi/v5",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "v5.0.0"
      }
    ],
    "relationships": [
      {
        "relatedSpdxElement": "SPDXRef-1b96f57f8fed62d8",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      },
      {
        "relatedSpdxElement": "SPDXRef-b074348b8f56ea64",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      }
    ],
    "spdxVersion": "SPDX-2.2"
  }
}