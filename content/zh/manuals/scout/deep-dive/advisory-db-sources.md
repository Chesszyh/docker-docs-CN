---
description: 了解更多关于 Docker Scout 分析背后的咨询数据库和 CVE 到软件包匹配服务的详细信息。
keywords: scout, 扫描, 分析, 漏洞, Hub, 供应链, 安全, 软件包, 仓库, 生态系统
title: 咨询数据库源和匹配服务
aliases:
  /scout/advisory-db-sources/
---

可靠的信息源是 Docker Scout 对软件制品进行相关且准确评估的关键。鉴于行业中来源和方法的多样性，漏洞评估结果出现差异是可能发生的。本页描述了 Docker Scout 咨询数据库及其 CVE 到软件包的匹配方法是如何工作的，以应对这些差异。

## 咨询数据库源

Docker Scout 汇总了来自多个来源的漏洞数据。数据会持续更新，以确保实时使用最新的可用信息来表示您的安全状况。

Docker Scout 使用以下软件包仓库和安全跟踪器：

<!-- vale off -->

- [AlmaLinux Security Advisory](https://errata.almalinux.org/)
- [Alpine secdb](https://secdb.alpinelinux.org/)
- [Amazon Linux Security Center](https://alas.aws.amazon.com/)
- [Bitnami Vulnerability Database](https://github.com/bitnami/vulndb)
- [CISA Known Exploited Vulnerability Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [CISA Vulnrichment](https://github.com/cisagov/vulnrichment)
- [Chainguard Security Feed](https://packages.cgr.dev/chainguard/osv/all.json)
- [Debian Security Bug Tracker](https://security-tracker.debian.org/tracker/)
- [Exploit Prediction Scoring System (EPSS)](https://api.first.org/epss/)
- [GitHub Advisory Database](https://github.com/advisories/)
- [GitLab Advisory Database](https://gitlab.com/gitlab-org/advisories-community/)
- [Golang VulnDB](https://github.com/golang/vulndb)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Oracle Linux Security](https://linux.oracle.com/security/)
- [Photon OS 3.0 Security Advisories](https://github.com/vmware/photon/wiki/Security-Updates-3)
- [Python Packaging Advisory Database](https://github.com/pypa/advisory-database)
- [RedHat Security Data](https://www.redhat.com/security/data/metrics/)
- [Rocky Linux Security Advisory](https://errata.rockylinux.org/)
- [RustSec Advisory Database](https://github.com/rustsec/advisory-db)
- [SUSE Security CVRF](http://ftp.suse.com/pub/projects/security/cvrf/)
- [Ubuntu CVE Tracker](https://people.canonical.com/~ubuntu-security/cve/)
- [Wolfi Security Feed](https://packages.wolfi.dev/os/security.json)
- [inTheWild, a community-driven open database of vulnerability exploitation](https://github.com/gmatuz/inthewilddb)

<!-- vale on -->

当您为 Docker 组织启用 Docker Scout 时，Docker Scout 平台会预配一个新的数据库实例。该数据库存储软件物料清单 (SBOM) 和关于您镜像的其他元数据。当安全公告包含有关漏洞的新信息时，您的 SBOM 会与 CVE 信息进行交叉引用，以检测该漏洞如何影响您。

有关镜像分析工作原理的更多详情，请参阅 [镜像分析页面](/manuals/scout/explore/analysis.md)。

## 漏洞匹配

传统工具通常依赖广泛的 [通用产品枚举 (CPE)](https://en.wikipedia.org/wiki/Common_Platform_Enumeration) 匹配，这可能导致许多误报结果。

Docker Scout 使用 [软件包 URL (PURLs)](https://github.com/package-url/purl-spec) 将软件包与 CVE 进行匹配，从而实现对漏洞的更精确识别。PURL 显著降低了误报的可能性，只关注真正受影响的软件包。

## 支持的软件包生态系统

Docker Scout 支持以下软件包生态系统：

- .NET
- GitHub 软件包
- Go
- Java
- JavaScript
- PHP
- Python
- RPM
- Ruby
- `alpm` (Arch Linux)
- `apk` (Alpine Linux)
- `deb` (Debian Linux 及其衍生版)
