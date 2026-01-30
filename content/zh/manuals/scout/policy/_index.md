---
title: 开始使用 Docker Scout 策略评估
linkTitle: 策略评估
weight: 70
keywords: scout, 供应链, 漏洞, 软件包, cves, 策略
description: |
  Docker Scout 中的策略允许您为制品定义供应链规则和阈值，并跟踪制品随时间推移在这些要求下的表现
---

在软件供应链管理中，保持制品的安全性和可靠性是重中之重。Docker Scout 中的策略评估 (Policy Evaluation) 在现有分析能力的基础上增加了一层控制。它允许您为制品定义供应链规则，并帮助您跟踪制品随时间推移在规则和阈值下的表现。

了解如何使用策略评估来确保您的制品符合既定的最佳实践。

## 策略评估的工作原理

当您为仓库激活 Docker Scout 时，您推送的镜像会被 [自动分析](/manuals/scout/explore/analysis.md)。分析让您深入了解镜像的组成，包括包含哪些软件包以及暴露在哪些漏洞之下。策略评估建立在镜像分析功能之上，根据策略定义的规则解读分析结果。

策略定义了您的制品应满足的镜像质量标准。例如，**No AGPL v3 licenses** 策略会标记任何包含在 AGPL v3 许可证下分发的软件包的镜像。如果镜像包含此类软件包，则该镜像不符合此策略。某些策略 (如 **No AGPL v3 licenses** 策略) 是可配置的。可配置策略允许您调整标准，以更好地满足组织的需求。

在 Docker Scout 中，策略旨在帮助您逐步提高安全和供应链地位。其他工具通常只提供“通过”或“失败”状态，而 Docker Scout 策略则通过可视化方式展示即使制品 (尚未) 满足策略要求时，微小的增量变化如何影响策略状态。通过跟踪失败差距随时间的变化，您可以更轻松地看到制品相对于策略是在改进还是在恶化。

策略不一定非要与应用程序安全和漏洞相关。您还可以使用策略来衡量和跟踪供应链管理的其他方面，例如开源许可证的使用情况和基础镜像的最新状态。

## 策略类型

在 Docker Scout 中，*策略 (policy)* 源自 *策略类型 (policy type)*。策略类型是定义策略核心参数的模板。您可以将策略类型比作面向对象编程中的“类”，每个策略则是根据其对应的策略类型创建的“实例”。

Docker Scout 支持以下策略类型：

- [Severity-Based Vulnerability](#severity-based-vulnerability) (基于严重性的漏洞)
- [Compliant Licenses](#compliant-licenses) (合规许可证)
- [Up-to-Date Base Images](#up-to-date-base-images) (最新的基础镜像)
- [High-Profile Vulnerabilities](#high-profile-vulnerabilities) (高关注漏洞)
- [Supply Chain Attestations](#supply-chain-attestations) (供应链证明)
- [Default Non-Root User](#default-non-root-user) (默认非 Root 用户)
- [Approved Base Images](#approved-base-images) (经批准的基础镜像)
- [SonarQube Quality Gates](#sonarqube-quality-gates) (SonarQube 质量门禁)

Docker Scout 会自动为启用了该功能的仓库提供默认策略，但 SonarQube Quality Gates 策略除外，该策略在使用前需要 [与 SonarQube 集成](/manuals/scout/integrations/code-quality/sonarqube.md)。

您可以从任何支持的策略类型中创建自定义策略，或者删除不适用于您项目的默认策略。有关更多信息，请参阅 [配置策略](./configure.md)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### Severity-Based Vulnerability (基于严重性的漏洞)

**Severity-Based Vulnerability** 策略类型检查您的制品是否暴露于已知漏洞。

默认情况下，此策略仅标记存在修复版本的危急 (critical) 和高危 (high) 漏洞。从本质上讲，这意味着对于未通过此策略的镜像，您可以部署一种简单的修复方法：将有漏洞的软件包升级到包含该漏洞修复程序的版本。

如果镜像包含一个或多个不符合指定策略标准的漏洞，则该镜像被视为不符合此策略。

您可以通过创建该策略的自定义版本来配置其参数。在自定义版本中，以下策略参数是可配置的：

- **Age** (存在时间)：漏洞首次发布后的最小天数。

  仅标记达到一定最小存在时间的漏洞的理由是，新发现的漏洞在您有机会解决之前不应导致评估失败。

<!-- vale Vale.Spelling = NO -->
- **Severities** (严重性)：要考虑的严重性级别 (默认：`Critical, High`)。
<!-- vale Vale.Spelling = YES -->

- **Fixable vulnerabilities only** (仅限可修复的漏洞)：是否仅报告存在修复版本的漏洞 (默认启用)。

- **Package types** (软件包类型)：要考虑的软件包类型列表。

  此选项允许您指定想要包含在策略评估中的软件包类型 (采用 [PURL 软件包类型定义](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst))。默认情况下，策略会考虑所有软件包类型。

有关配置策略的更多信息，请参阅 [配置策略](./configure.md)。

### Compliant Licenses (合规许可证)

**Compliant Licenses** 策略类型检查您的镜像是否包含在不当许可证下分发的软件包。如果镜像包含一个或多个带此类许可证的软件包，则被视为不合规。

您可以配置此策略应注意的许可证列表，并通过指定允许列表 (以 PURL 的形式) 来添加例外。参见 [配置策略](./configure.md)。

### Up-to-Date Base Images (最新的基础镜像)

**Up-to-Date Base Images** 策略类型检查您使用的基础镜像是否是最新的。

如果您用于构建镜像的标签指向的摘要与您正在使用的摘要不同，则镜像被视为不符合此策略。如果摘要不匹配，则表示您正在使用的基础镜像已过时。

您的镜像需要来源证明 (provenance attestations) 才能成功进行此策略评估。有关更多信息，请参阅 [无基础镜像数据](#no-base-image-data)。

### High-Profile Vulnerabilities (高关注漏洞)

**High-Profile Vulnerabilities** 策略类型检查您的镜像是否包含 Docker Scout 精选列表中的漏洞。此列表会根据公认风险较高的最新披露漏洞保持更新。

该列表包括以下漏洞：

- [CVE-2014-0160 (OpenSSL Heartbleed)](https://scout.docker.com/v/CVE-2014-0160)
- [CVE-2021-44228 (Log4Shell)](https://scout.docker.com/v/CVE-2021-44228)
- [CVE-2023-38545 (cURL SOCKS5 heap buffer overflow)](https://scout.docker.com/v/CVE-2023-38545)
- [CVE-2023-44487 (HTTP/2 Rapid Reset)](https://scout.docker.com/v/CVE-2023-44487)
- [CVE-2024-3094 (XZ backdoor)](https://scout.docker.com/v/CVE-2024-3094)
- [CVE-2024-47176 (OpenPrinting - `cups-browsed`)](https://scout.docker.com/v/CVE-2024-47176)
- [CVE-2024-47076 (OpenPrinting - `libcupsfilters`)](https://scout.docker.com/v/CVE-2024-47076)
- [CVE-2024-47175 (OpenPrinting - `libppd`)](https://scout.docker.com/v/CVE-2024-47175)
- [CVE-2024-47177 (OpenPrinting - `cups-filters`)](https://scout.docker.com/v/CVE-2024-47177)

您可以通过配置策略来自定义哪些 CVE 被视为高关注。自定义配置选项包括：

- **Excluded CVEs** (排除的 CVE)：指定您希望此策略忽略的 CVE。

  默认值：`[]` (不忽略任何高关注 CVE)

- **CISA KEV**：启用对 CISA 已知利用漏洞 (KEV) 目录中漏洞的跟踪。

  [CISA KEV 目录](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) 包含了在野被积极利用的漏洞。启用后，策略将标记包含 CISA KEV 目录中漏洞的镜像。

  默认启用。

有关策略配置的更多信息，请参阅 [配置策略](./configure.md)。

### Supply Chain Attestations (供应链证明)

**Supply Chain Attestations** 策略类型检查您的镜像是否具有 [SBOM](/manuals/build/metadata/attestations/sbom.md) 和 [来源 (provenance)](/manuals/build/metadata/attestations/slsa-provenance.md) 证明。

如果镜像缺少 SBOM 证明或带有 *max mode* 来源证明，则被视为不合规。为了确保合规，请更新您的构建命令以在构建时附加这些证明：

```console
$ docker buildx build --provenance=true --sbom=true -t <IMAGE> --push .
```

有关构建证明的更多信息，请参阅 [证明 (Attestations)](/manuals/build/metadata/attestations/_index.md)。

如果您使用 GitHub Actions 来构建和推送镜像，请了解如何 [配置该 Action](/manuals/build/ci/github-actions/attestations.md) 以应用 SBOM 和来源证明。

### Default Non-Root User (默认非 Root 用户)

默认情况下，容器以具有完整系统管理权限的 `root` 超级用户身份在容器内运行，除非 Dockerfile 指定了不同的默认用户。以特权用户身份运行容器会削弱其运行时安全性，因为这意味着容器中运行的任何代码都可以执行管理操作。

**Default Non-Root User** 策略类型检测设置为以默认 `root` 用户身份运行的镜像。为了符合此策略，镜像必须在镜像配置中指定一个非 root 用户。如果镜像没有为运行时阶段指定非 root 默认用户，则不符合此策略。

对于不合规的镜像，评估结果会显示镜像是否显式设置了 `root` 用户。这有助于您区分由镜像隐式使用 `root` 用户引起的策略冲突，以及有意设置 `root` 用户引起的策略冲突。

以下 Dockerfile 尽管没有明确设置，但默认以 `root` 运行：

```Dockerfile
FROM alpine
RUN echo "Hi"
```

而在以下情况下，`root` 用户是明确设置的：

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> [!NOTE]
>
> 此策略仅检查镜像配置 blob 中设置的镜像默认用户。即使您确实指定了非 root 默认用户，在运行时仍然可以覆盖默认用户，例如通过在 `docker run` 命令中使用 `--user` 标志。

要使镜像符合此策略，请使用 [`USER`](/reference/dockerfile.md#user) Dockerfile 指令在运行时阶段设置一个不具有 root 权限的默认用户。

以下 Dockerfile 片段显示了合规镜像和不合规镜像之间的区别。

{{< tabs >}}
{{< tab name="不合规" >}}

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< tab name="合规" >}}

```dockerfile {hl_lines=7}
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
USER nonroot
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< /tabs >}}

### Approved Base Images (经批准的基础镜像)

**Approved Base Images** 策略类型确保您在构建中使用的基础镜像经过维护且安全。

此策略检查您构建中使用的基础镜像是否符合策略配置中指定的任何模式。下表显示了此策略的一些示例模式。

| 用例                                                            | 模式                             |
| --------------------------------------------------------------- | -------------------------------- |
| 允许来自 Docker Hub 的所有镜像                                  | `docker.io/*`                    |
| 允许所有 Docker 官方镜像 (Docker Official Images)                | `docker.io/library/*`            |
| 允许来自特定组织的镜像                                          | `docker.io/orgname/*`            |
| 允许特定仓库的标签                                              | `docker.io/orgname/repository:*` |
| 允许主机名为 `registry.example.com` 的注册表上的镜像            | `registry.example.com/*`         |
| 允许 NodeJS 镜像的 slim 标签                                    | `docker.io/library/node:*-slim`  |

星号 (`*`) 匹配到其后的字符或镜像引用的末尾。请注意，必须使用 `docker.io` 前缀才能匹配 Docker Hub 镜像。这是 Docker Hub 的注册表主机名。

此策略可配置以下选项：

- **Approved base image sources** (经批准的基础镜像源)

  指定您想要允许的镜像引用模式。策略会根据这些模式评估基础镜像引用。

  默认值：`[*]` (任何引用都是允许的基础镜像)

- **Only supported tags** (仅限支持的标签)

  使用 Docker 官方镜像时，仅允许受支持的标签。

  启用此选项后，使用官方镜像的不受支持标签作为其基础镜像的镜像会触发策略冲突。官方镜像的受支持标签列在 Docker Hub 上仓库概览的 **Supported tags** 部分。

  默认启用。

- **Only supported OS distributions** (仅限支持的操作系统发行版)

  仅允许受支持的 Linux 发行版版本的 Docker 官方镜像。

  启用此选项后，使用已达到生命周期终点的分发版 (如 `ubuntu:18.04`) 的镜像将触发策略冲突。

  如果无法确定操作系统版本，启用此选项可能会导致策略报告“无数据”。

  默认启用。

您的镜像需要来源证明才能成功进行此策略评估。有关更多信息，请参阅 [无基础镜像数据](#no-base-image-data)。

### SonarQube Quality Gates (SonarQube 质量门禁)

**SonarQube Quality Gates** 策略类型基于 [SonarQube 集成](../integrations/code-quality/sonarqube.md) 来评估源代码的质量。此策略通过将 SonarQube 代码分析结果摄取到 Docker Scout 中来工作。

您使用 SonarQube 的 [质量门禁 (quality gates)](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/) 来定义此策略的标准。SonarQube 会根据您在 SonarQube 中定义的质量门禁来评估源代码。Docker Scout 将 SonarQube 评估呈现为 Docker Scout 策略。

Docker Scout 使用 [来源 (provenance)](/manuals/build/metadata/attestations/slsa-provenance.md) 证明或 `org.opencontainers.image.revision` OCI 注释来将 SonarQube 分析结果与容器镜像链接起来。除了启用 SonarQube 集成外，您还必须确保镜像具有上述证明或标签。

![Git commit SHA 将镜像与 SonarQube 分析关联](../images/scout-sq-commit-sha.webp)

一旦您推送镜像并且策略评估完成，SonarQube 质量门禁的结果将作为一项策略显示在 Docker Scout 控制面板和 CLI 中。

> [!NOTE]
>
> Docker Scout 只能访问启用集成后创建的 SonarQube 分析。Docker Scout 无法访问历史评估。启用集成后，请触发 SonarQube 分析和策略评估，以便在 Docker Scout 中查看结果。

## 无基础镜像数据

在某些情况下，无法确定构建中使用的基础镜像信息。在这种情况下，**Up-to-Date Base Images** 和 **Approved Base Images** 策略会被标记为 **No data** (无数据)。

出现这种“无数据”状态的情况包括：

- Docker Scout 不知道您使用了哪个基础镜像标签。
- 您使用的基础镜像版本有多个标签，但并非所有标签都已过时。

为了确保 Docker Scout 始终了解您的基础镜像，您可以在构建时附加 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。Docker Scout 使用来源证明来查明基础镜像版本。
