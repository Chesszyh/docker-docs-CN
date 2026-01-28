---
title: 常见漏洞和暴露（CVE）
linktitle: CVE
description: 了解什么是 CVE、Docker 强化镜像如何减少暴露，以及如何使用流行工具扫描镜像中的漏洞。
keywords: docker cve scan, grype vulnerability scanner, trivy image scan, vex attestation, secure container images
---

## 什么是 CVE？

CVE 是软件或硬件中公开披露的网络安全漏洞。每个 CVE 都被分配一个唯一标识符（例如 CVE-2024-12345）并包含标准化描述，允许组织一致地跟踪和解决漏洞。

在 Docker 的上下文中，CVE 通常涉及基础镜像或应用程序依赖项中的问题。这些漏洞的范围从小错误到关键安全风险，如远程代码执行或权限提升。

## 为什么 CVE 很重要？

定期扫描和更新 Docker 镜像以缓解 CVE 对于维护安全和合规的环境至关重要。忽略 CVE 可能导致严重的安全漏洞，包括：

- 未授权访问：漏洞利用可能使攻击者获得对系统的未授权访问。
- 数据泄露：敏感信息可能被暴露或窃取。
- 服务中断：漏洞可能被利用来中断服务或导致停机。
- 合规违规：未能解决已知漏洞可能导致不符合行业法规和标准。

## Docker 强化镜像如何帮助缓解 CVE

Docker 强化镜像（DHIs）从一开始就致力于最小化 CVE 风险。通过采用安全优先的方法，DHIs 在 CVE 缓解方面提供了几个优势：

- 减少攻击面：DHIs 使用 distroless 方法构建，剥离了不必要的组件和包。与传统镜像相比，镜像大小减少高达 95%，这限制了潜在漏洞的数量，使攻击者更难利用不需要的软件。

- 更快的 CVE 修复：由 Docker 以企业级 SLA 维护，DHIs 持续更新以解决已知漏洞。关键和高严重性 CVE 会被快速修补，确保您的容器保持安全，无需手动干预。

- 主动漏洞管理：通过使用 DHIs，组织可以主动管理漏洞。镜像附带 CVE 和漏洞暴露（VEX）数据源，使团队能够及时了解潜在威胁并采取必要行动。

## 扫描镜像中的 CVE

定期扫描 Docker 镜像中的 CVE 对于维护安全的容器化环境至关重要。虽然 Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中，但 Grype 和 Trivy 等工具也提供替代扫描功能。以下是使用每个工具扫描 Docker 镜像中 CVE 的说明。

### Docker Scout

Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要和直接的修复指南链接。

#### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker 强化镜像，请运行以下命令：

```console
$ docker scout cves <your-namespace>/dhi-<image>:<tag>
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

### Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，可根据 NVD 和发行版公告等漏洞数据库检查容器镜像。

#### 使用 Grype 扫描 DHI

安装 Grype 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker 强化镜像：

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

### Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他制品的开源漏洞扫描器。它检测操作系统包和应用程序依赖项中的漏洞。

#### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker 强化镜像：

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

## 使用 VEX 过滤已知不可利用的 CVE

Docker 强化镜像包含签名的 [VEX（漏洞可利用性交换）](./vex.md) 证明，用于标识与镜像运行时行为无关的漏洞。

使用 Docker Scout 时，这些 VEX 声明会自动应用，无需手动配置。

要为支持 VEX 的工具手动检索 VEX 证明：

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

这将创建一个包含指定镜像 VEX 声明的 `vex.json` 文件。然后，您可以将此文件与支持 VEX 的工具一起使用，以过滤掉已知不可利用的 CVE。

例如，使用 Grype 和 Trivy，您可以使用 `--vex` 标志在扫描期间应用 VEX 声明：

```console
$ grype <your-namespace>/dhi-<image>:<tag> --vex vex.json
```
