---
title: 将 Scout 用于不同的制品类型
description: |
  某些 Docker Scout 命令支持镜像引用前缀，
  用于控制要分析的镜像或文件的位置。
keywords: scout, vulnerabilities, analyze, analysis, cli, packages, sbom, cve, security, local, source, code, supply chain
aliases:
  - /scout/image-prefix/
---

某些 Docker Scout CLI 命令支持使用前缀来指定要分析的制品（artifact）的位置或类型。

默认情况下，使用 `docker scout cves` 命令进行镜像分析时，会以 Docker Engine 本地镜像存储中的镜像为目标。以下命令在本地镜像存在时总是使用本地镜像：

```console
$ docker scout cves <image>
```

如果镜像在本地不存在，Docker 会在运行分析之前拉取镜像。再次分析同一镜像时，默认会使用相同的本地版本，即使该标签在镜像仓库中已经发生变化。

通过在镜像引用前添加 `registry://` 前缀，您可以强制 Docker Scout 分析镜像仓库版本的镜像：

```console
$ docker scout cves registry://<image>
```

## 支持的前缀

支持的前缀包括：

| 前缀                 | 描述                                                                 |
| -------------------- | -------------------------------------------------------------------- |
| `image://`（默认）   | 使用本地镜像，如果不存在则回退到镜像仓库查找                         |
| `local://`           | 使用本地镜像存储中的镜像（不进行镜像仓库查找）                       |
| `registry://`        | 使用镜像仓库中的镜像（不使用本地镜像）                               |
| `oci-dir://`         | 使用 OCI 布局目录                                                    |
| `archive://`         | 使用 tarball 归档文件，如通过 `docker save` 创建的文件               |
| `fs://`              | 使用本地目录或文件                                                   |

您可以在以下命令中使用前缀：

- `docker scout compare`
- `docker scout cves`
- `docker scout quickview`
- `docker scout recommendations`
- `docker scout sbom`

## 示例

本节包含一些示例，展示如何使用前缀为 `docker scout` 命令指定制品。

### 分析本地项目

`fs://` 前缀允许您直接分析本地源代码，而无需将其构建为容器镜像。以下 `docker scout quickview` 命令可让您快速查看当前工作目录中源代码的漏洞摘要：

```console
$ docker scout quickview fs://.
```

要查看本地源代码中发现的漏洞详情，可以使用 `docker scout cves --details fs://.` 命令。可以与其他标志组合使用，将结果缩小到您感兴趣的软件包和漏洞。

```console
$ docker scout cves --details --only-severity high fs://.
    ✓ File system read
    ✓ Indexed 323 packages
    ✗ Detected 1 vulnerable package with 1 vulnerability

​## Overview

                    │        Analyzed path
────────────────────┼──────────────────────────────
  Path              │  /Users/david/demo/scoutfs
    vulnerabilities │    0C     1H     0M     0L

​## Packages and Vulnerabilities

   0C     1H     0M     0L  fastify 3.29.0
pkg:npm/fastify@3.29.0

    ✗ HIGH CVE-2022-39288 [OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities]
      https://scout.docker.com/v/CVE-2022-39288

      fastify is a fast and low overhead web framework, for Node.js. Affected versions of
      fastify are subject to a denial of service via malicious use of the Content-Type
      header. An attacker can send an invalid Content-Type header that can cause the
      application to crash. This issue has been addressed in commit  fbb07e8d  and will be
      included in release version 4.8.1. Users are advised to upgrade. Users unable to
      upgrade may manually filter out http content with malicious Content-Type headers.

      Affected range : <4.8.1
      Fixed version  : 4.8.1
      CVSS Score     : 7.5
      CVSS Vector    : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H

1 vulnerability found in 1 package
  LOW       0
  MEDIUM    0
  HIGH      1
  CRITICAL  0
```

### 将本地项目与镜像进行比较

使用 `docker scout compare`，您可以将本地文件系统上源代码的分析结果与容器镜像的分析结果进行比较。以下示例将本地源代码（`fs://.`）与镜像仓库中的镜像 `registry://docker/scout-cli:latest` 进行比较。在这种情况下，比较的基准和目标都使用了前缀。

```console
$ docker scout compare fs://. --to registry://docker/scout-cli:latest --ignore-unchanged
WARN 'docker scout compare' is experimental and its behaviour might change in the future
    ✓ File system read
    ✓ Indexed 268 packages
    ✓ SBOM of image already cached, 234 packages indexed


  ## Overview

                           │              Analyzed File System              │              Comparison Image
  ─────────────────────────┼────────────────────────────────────────────────┼─────────────────────────────────────────────
    Path / Image reference │  /Users/david/src/docker/scout-cli-plugin      │  docker/scout-cli:latest
                           │                                                │  bb0b01303584
      platform             │                                                │ linux/arm64
      provenance           │ https://github.com/dvdksn/scout-cli-plugin.git │ https://github.com/docker/scout-cli-plugin
                           │  6ea3f7369dbdfec101ac7c0fa9d78ef05ffa6315      │  67cb4ef78bd69545af0e223ba5fb577b27094505
      vulnerabilities      │    0C     0H     1M     1L                     │    0C     0H     1M     1L
                           │                                                │
      size                 │ 7.4 MB (-14 MB)                                │ 21 MB
      packages             │ 268 (+34)                                      │ 234
                           │                                                │


  ## Packages and Vulnerabilities


    +   55 packages added
    -   21 packages removed
       213 packages unchanged
```

上面的示例为了简洁起见进行了截断。

### 查看镜像 tarball 的 SBOM

以下示例展示了如何使用 `archive://` 前缀获取使用 `docker save` 创建的镜像 tarball 的 SBOM。本例中的镜像是 `docker/scout-cli:latest`，SBOM 以 SPDX 格式导出到 `sbom.spdx.json` 文件。

```console
$ docker pull docker/scout-cli:latest
latest: Pulling from docker/scout-cli
257973a141f5: Download complete
1f2083724dd1: Download complete
5c8125a73507: Download complete
Digest: sha256:13318bb059b0f8b0b87b35ac7050782462b5d0ac3f96f9f23d165d8ed68d0894
$ docker save docker/scout-cli:latest -o scout-cli.tar
$ docker scout sbom --format spdx -o sbom.spdx.json archive://scout-cli.tar
```

## 了解更多

在 CLI 参考文档中阅读有关命令和支持标志的信息：

- [`docker scout quickview`](/reference/cli/docker/scout/quickview.md)
- [`docker scout cves`](/reference/cli/docker/scout/cves.md)
- [`docker scout compare`](/reference/cli/docker/scout/compare.md)
