---
title: Docker Scout 镜像分析
description:
  Docker Scout 镜像分析提供了对镜像组成及其包含的漏洞的详细视图
keywords: scout, 扫描, 漏洞, 供应链, 安全, 分析
alias:
  - /scout/advanced-image-analysis/
  - /scout/image-analysis/
---

当您为一个仓库激活镜像分析时，Docker Scout 会自动分析您推送到该仓库的新镜像。

镜像分析会提取软件物料清单 (SBOM) 和其他镜像元数据，并将其与来自 [安全公告](/manuals/scout/deep-dive/advisory-db-sources.md) 的漏洞数据进行评估。

如果您使用 CLI 或 Docker Desktop 运行镜像分析作为一次性任务，Docker Scout 不会存储有关您镜像的任何数据。
但是，如果您为容器镜像仓库启用了 Docker Scout，Docker Scout 会在分析后保存镜像的元数据快照。
随着新的漏洞数据可用，Docker Scout 会使用元数据快照重新校准分析，这意味着您的镜像安全状态是实时更新的。
这种动态评估意味着当新的 CVE 信息披露时，无需重新分析镜像。

Docker Scout 镜像分析默认可用于 Docker Hub 仓库。
您还可以集成第三方注册表和其他服务。要了解更多信息，请参阅 [将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## 在仓库上激活 Docker Scout

Docker Personal 附带 1 个启用 Scout 的仓库。如果您需要额外的仓库，可以升级您的 Docker 订阅。
请参阅 [订阅和功能](../../subscription/details.md) 以了解每个订阅层级包含多少个启用 Scout 的仓库。

在第三方注册表的仓库上激活镜像分析之前，该注册表必须已为您 Docker 组织集成了 Docker Scout。
Docker Hub 默认已集成。有关更多信息，请参阅 [容器注册表集成](/manuals/scout/integrations/_index.md#container-registries)。

> [!NOTE]
> 
> 您必须在 Docker 组织中拥有 **Editor** (编辑器) 或 **Owner** (所有者) 角色才能在仓库上激活镜像分析。

激活镜像分析：

1. 转到 Docker Scout 控制面板中的 [仓库设置](https://scout.docker.com/settings/repos)。
2. 选择要启用的仓库。
3. 选择 **Enable image analysis**。

如果您的仓库中已经包含镜像，Docker Scout 会自动拉取并分析最新的镜像。

## 分析注册表镜像

要触发注册表中镜像的分析，请将镜像推送到集成了 Docker Scout 且已激活镜像分析的仓库。

> [!NOTE]
> 
> 除非镜像具有 SBOM 证明，否则 Docker Scout 平台上的镜像分析最大镜像文件限制为 10 GB。
> 参见 [最大镜像尺寸](#maximum-image-size)。

1. 使用您的 Docker ID 登录，可以使用 `docker login` 命令或 Docker Desktop 中的 **Sign in** 按钮。
2. 构建并推送您要分析的镜像。

   ```console
   $ docker build --push --tag <org>/<image:tag> --provenance=true --sbom=true .
   ```

   使用 `--provenance=true` 和 `--sbom=true` 标志进行构建会将 [构建证明](/manuals/build/metadata/attestations/_index.md) 附加到镜像上。Docker Scout 使用证明来提供更精细的分析结果。

   > [!NOTE]
   > 
   > 仅当您使用 [containerd 镜像存储](/manuals/desktop/features/containerd.md) 时，默认的 `docker` 驱动程序才支持构建证明。

3. 转到 Docker Scout 控制面板中的 [镜像页面](https://scout.docker.com/reports/images)。

   镜像在您将其推送到注册表后不久就会出现在列表中。分析结果可能需要几分钟才能显示。

## 在本地分析镜像

您可以使用 Docker Desktop 或 Docker CLI 的 `docker scout` 命令在本地分析镜像。

### Docker Desktop

> [!NOTE]
> 
> Docker Desktop 后台索引支持最大 10 GB 的镜像。
> 参见 [最大镜像尺寸](#maximum-image-size)。

要使用 Docker Desktop GUI 在本地分析镜像：

1. 拉取或构建您要分析的镜像。
2. 转到 Docker Dashboard 中的 **Images** 视图。
3. 在列表中选择您的一个本地镜像。

   这将打开 [镜像详情视图](./image-details-view.md)，显示 Docker Scout 对您所选镜像的分析所发现的软件包和漏洞分类。

### CLI

`docker scout` CLI 命令提供了一个从终端使用 Docker Scout 的命令行界面。

- `docker scout quickview`: 指定镜像的摘要，见 [Quickview](#quickview)
- `docker scout cves`: 指定镜像的本地分析，见 [CVEs](#cves)
- `docker scout compare`: 分析并比较两个镜像

默认情况下，结果会打印到标准输出。您还可以将结果以结构化格式导出到文件，例如静态分析结果交换格式 (SARIF)。

#### Quickview

`docker scout quickview` 命令提供给定镜像及其基础镜像中发现的漏洞的概览。

```console
$ docker scout quickview traefik:latest
    ✓ SBOM of image already cached, 311 packages indexed

  Your image  traefik:latest  │    0C     2H     8M     1L
  Base image  alpine:3        │    0C     0H     0M     0L
```

如果您的基础镜像已过时，`quickview` 命令还会显示更新基础镜像将如何改变镜像的漏洞暴露情况。

```console
$ docker scout quickview postgres:13.1
    ✓ Pulled
    ✓ Image stored for indexing
    ✓ Indexed 187 packages

  Your image  postgres:13.1                 │   17C    32H    35M    33L
  Base image  debian:buster-slim            │    9C    14H     9M    23L
  Refreshed base image  debian:buster-slim  │    0C     1H     6M    29L
                                            │    -9    -13     -3     +6
  Updated base image  debian:stable-slim    │    0C     0H     0M    17L
                                            │    -9    -14     -9     -6
```

#### CVEs

`docker scout cves` 命令为您提供镜像中所有漏洞的完整视图。该命令支持多个标志，可让您更精确地指定您感兴趣的漏洞，例如按严重性或软件包类型：

```console
$ docker scout cves --format only-packages --only-vuln-packages \
  --only-severity critical postgres:13.1
    ✓ SBOM of image already cached, 187 packages indexed
    ✗ Detected 10 vulnerable packages with a total of 17 vulnerabilities

     Name            Version         Type        Vulnerabilities
───────────────────────────────────────────────────────────────────────────
  dpkg        1.19.7                 deb      1C     0H     0M     0L
  glibc       2.28-10                deb      4C     0H     0M     0L
  gnutls28    3.6.7-4+deb10u6        deb      2C     0H     0M     0L
  libbsd      0.9.1-2                deb      1C     0H     0M     0L
  libksba     1.3.5-2                deb      2C     0H     0M     0L
  libtasn1-6  4.13-3                 deb      1C     0H     0M     0L
  lz4         1.8.3-1                deb      1C     0H     0M     0L
  openldap    2.4.47+dfsg-3+deb10u5  deb      1C     0H     0M     0L
  openssl     1.1.1d-0+deb10u4       deb      3C     0H     0M     0L
  zlib        1:1.2.11.dfsg-1        deb      1C     0H     0M     0L
```

有关这些命令及其使用方法的更多信息，请参阅 CLI 参考文档：

- [`docker scout quickview`](/reference/cli/docker/scout/quickview.md)
- [`docker scout cves`](/reference/cli/docker/scout/cves.md)

## 漏洞严重性评估

Docker Scout 根据来自 [公告源](/manuals/scout/deep-dive/advisory-db-sources.md) 的漏洞数据为漏洞分配严重性评级。公告会根据受漏洞影响的软件包类型进行排序和优先处理。例如，如果漏洞影响 OS 软件包，则分发维护者分配的严重性级别将被优先考虑。

如果首选公告源已为 CVE 分配了严重性评级，但没有 CVSS 评分，Docker Scout 会退而显示来自另一个源的 CVSS 评分。来自首选公告的严重性评级和来自备用公告的 CVSS 评分将一起显示。这意味着如果首选公告分配了 `LOW` 评级但没有 CVSS 评分，而备用公告分配了 9.8 的 CVSS 评分，那么漏洞可能具有 `LOW` 的严重性评级，同时 CVSS 评分为 9.8。

在任何来源中都未分配 CVSS 评分的漏洞被归类为 **Unspecified** (U) (未指定)。

Docker Scout 不实施专有的漏洞指标系统。所有指标均继承自与 Docker Scout 集成的安全公告。公告可能使用不同的分类阈值，但大多数公告都遵循 CVSS v3.0 规范，该规范根据下表将 CVSS 评分映射到严重性评级：

| CVSS 评分  | 严重性评级       |
| ---------- | ---------------- |
| 0.1 – 3.9  | **Low** (低) (L)      |
| 4.0 – 6.9  | **Medium** (中) (M)   |
| 7.0 – 8.9  | **High** (高) (H)     |
| 9.0 – 10.0 | **Critical** (危急) (C) |

有关更多信息，请参阅 [漏洞指标 (NIST)](https://nvd.nist.gov/vuln-metrics/cvss)。

请注意，考虑到前面描述的公告优先排序和回退机制，Docker Scout 中显示的严重性评级可能与此评级系统有所偏差。

## 最大镜像尺寸

Docker Scout 平台上的镜像分析以及由 Docker Desktop 中的后台索引触发的分析，镜像文件大小限制为 10 GB (未压缩)。要分析大于该限制的镜像，您可以：

- 在构建时附加 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md)
- 使用 [CLI](#cli) 在本地分析镜像

使用 CLI 在本地分析的镜像以及带有 SBOM 证明的镜像没有最大文件大小限制。
