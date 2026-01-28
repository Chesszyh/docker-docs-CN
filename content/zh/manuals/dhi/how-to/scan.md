---
title: 扫描 Docker Hardened Images
linktitle: 扫描镜像
description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
keywords: scan container image, docker scout cves, grype scanner, trivy container scanner, vex attestation
weight: 45
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

Docker Hardened Images（DHI）被设计为默认安全，但与任何容器镜像一样，定期扫描它们作为漏洞管理流程的一部分非常重要。

您可以使用与标准镜像相同的工具来扫描 DHI，例如 Docker Scout、Grype 和 Trivy。DHI 遵循相同的格式和标准，以便与您的安全工具兼容。在扫描镜像之前，镜像必须已镜像到您在 Docker Hub 上的组织中。

> [!NOTE]
>
> [Docker Scout](/manuals/scout/_index.md) 会自动为 Docker Hub 上所有镜像的 Docker Hardened Image 仓库启用，无需额外费用。您可以直接在 Docker Hub UI 中您组织的仓库下查看扫描结果。

## Docker Scout

Docker Scout 集成在 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要和直接指向修复指南的链接。

### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker Hardened Image，请运行以下命令：

```console
$ docker scout cves <your-namespace>/dhi-<image>:<tag> --platform <platform>
```

示例输出：

```plaintext
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v VEX statements obtained from attestation
    v No vulnerable package detected
    ...
```

有关更详细的过滤和 JSON 输出，请参阅 [Docker Scout CLI 参考](../../../reference/cli/docker/scout/_index.md)。

### 使用 Docker Scout 在 CI/CD 中自动化 DHI 扫描

将 Docker Scout 集成到您的 CI/CD 流水线中，可以在构建过程中自动验证从 Docker Hardened Images 构建的镜像是否没有已知漏洞。这种主动方法确保了您的镜像在整个开发生命周期中持续保持安全完整性。

#### 示例 GitHub Actions 工作流

以下是一个示例 GitHub Actions 工作流，用于构建镜像并使用 Docker Scout 进行扫描：

```yaml {collapse="true"}
name: DHI Vulnerability Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ "**" ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }} .

      - name: Run Docker Scout CVE scan
        uses: docker/scout-action@v1
        with:
          command: cves
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }}
          only-severities: critical,high
          exit-code: true
```

`exit-code: true` 参数确保如果检测到任何关键或高危漏洞，工作流将失败，防止部署不安全的镜像。

有关在 CI 中使用 Docker Scout 的更多详情，请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，可根据漏洞数据库（如 NVD 和发行版公告）检查容器镜像。

### 使用 Grype 扫描 DHI

安装 Grype 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull <your-namespace>/dhi-<image>:<tag>
$ grype <your-namespace>/dhi-<image>:<tag>
```

示例输出：

```plaintext
NAME               INSTALLED              FIXED-IN     TYPE  VULNERABILITY     SEVERITY    EPSS%  RISK
libperl5.36        5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl               5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl-base          5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
...
```

您应该包含 `--vex` 标志以在扫描期间应用 VEX 声明，这会过滤掉已知不可利用的 CVE。有关更多信息，请参阅 [VEX 部分](#使用-vex-过滤已知不可利用的-cve)。

## Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他制品的开源漏洞扫描器。它可以检测操作系统软件包和应用依赖项中的漏洞。

### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull <your-namespace>/dhi-<image>:<tag>
$ trivy image <your-namespace>/dhi-<image>:<tag>
```

示例输出：

```plaintext
Report Summary

┌──────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                                    Target                                    │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ <namespace>/dhi-<image>:<tag> (debian 12.11)                                 │   debian   │       66        │    -    │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ opt/python-3.13.4/lib/python3.13/site-packages/pip-25.1.1.dist-info/METADATA │ python-pkg │        0        │    -    │
└──────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┴─────────┘
```

您应该包含 `--vex` 标志以在扫描期间应用 VEX 声明，这会过滤掉已知不可利用的 CVE。有关更多信息，请参阅 [VEX 部分](#使用-vex-过滤已知不可利用的-cve)。

## 使用 VEX 过滤已知不可利用的 CVE

Docker Hardened Images 包含签名的 VEX（Vulnerability Exploitability eXchange，漏洞可利用性交换）证明，用于标识与镜像运行时行为无关的漏洞。

使用 Docker Scout 时，这些 VEX 声明会自动应用，无需手动配置。

要为支持 VEX 的工具手动创建 JSON 文件 VEX 证明：

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --predicate \
  <your-namespace>/dhi-<image>:<tag> --platform <platform> > vex.json
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --predicate \
  docs/dhi-python:3.13 --platform linux/amd64 > vex.json
```

这将创建一个包含指定镜像 VEX 声明的 `vex.json` 文件。然后，您可以将此文件与支持 VEX 的工具一起使用，以过滤已知不可利用的 CVE。

例如，使用 Grype 和 Trivy，您可以使用 `--vex` 标志在扫描期间应用 VEX 声明：

```console
$ grype <your-namespace>/dhi-<image>:<tag> --vex vex.json
```
