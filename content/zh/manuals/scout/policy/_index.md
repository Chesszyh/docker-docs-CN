---
title: Docker Scout 策略评估入门
linkTitle: 策略评估
weight: 70
keywords: scout, supply chain, vulnerabilities, packages, cves, policy
description: |
  Docker Scout 中的策略（Policy）让您可以为构建产物定义供应链规则和阈值，
  并跟踪您的构建产物随时间推移相对于这些要求的表现
---

在软件供应链管理中，维护构建产物的安全性和可靠性是首要任务。Docker Scout 中的策略评估（Policy Evaluation）在现有分析能力之上引入了一层控制。它让您可以为构建产物定义供应链规则，并帮助您跟踪构建产物相对于规则和阈值随时间推移的表现。

了解如何使用策略评估来确保您的构建产物符合既定的最佳实践。

## 策略评估的工作原理

当您为仓库激活 Docker Scout 时，您推送的镜像会被[自动分析](/manuals/scout/explore/analysis.md)。分析为您提供关于镜像组成的洞察，包括它们包含哪些软件包以及暴露了哪些漏洞。策略评估建立在镜像分析功能之上，根据策略定义的规则解释分析结果。

策略定义了您的构建产物应满足的镜像质量标准。例如，**No AGPL v3 licenses** 策略会标记任何包含以 AGPL v3 许可证分发的软件包的镜像。如果镜像包含此类软件包，则该镜像不符合此策略。某些策略（如 **No AGPL v3 licenses** 策略）是可配置的。可配置策略让您可以调整标准以更好地匹配组织的需求。

在 Docker Scout 中，策略旨在帮助您逐步提升安全性和供应链状态。与其他专注于提供通过或失败状态的工具不同，Docker Scout 策略可视化地展示了即使您的构建产物（尚未）满足策略要求时，小的增量更改如何影响策略状态。通过跟踪失败差距随时间的变化，您可以更容易地看到您的构建产物相对于策略是在改善还是在恶化。

策略不一定与应用程序安全和漏洞相关。您也可以使用策略来衡量和跟踪供应链管理的其他方面，例如开源许可证使用情况和基础镜像的更新状态。

## 策略类型

在 Docker Scout 中，*策略（policy）*派生自*策略类型（policy type）*。策略类型是定义策略核心参数的模板。您可以将策略类型比作面向对象编程中的类，每个策略作为从其对应策略类型创建的实例。

Docker Scout 支持以下策略类型：

- [基于严重性的漏洞（Severity-Based Vulnerability）](#severity-based-vulnerability)
- [合规许可证（Compliant Licenses）](#compliant-licenses)
- [最新基础镜像（Up-to-Date Base Images）](#up-to-date-base-images)
- [高危漏洞（High-Profile Vulnerabilities）](#high-profile-vulnerabilities)
- [供应链证明（Supply Chain Attestations）](#supply-chain-attestations)
- [默认非 Root 用户（Default Non-Root User）](#default-non-root-user)
- [已批准的基础镜像（Approved Base Images）](#approved-base-images)
- [SonarQube 质量门禁（SonarQube Quality Gates）](#sonarqube-quality-gates)

Docker Scout 会自动为启用它的仓库提供默认策略，但 SonarQube Quality Gates 策略除外，该策略需要在使用前[与 SonarQube 集成](/manuals/scout/integrations/code-quality/sonarqube.md)。

您可以从任何支持的策略类型创建自定义策略，或者如果默认策略不适用于您的项目，也可以删除它。有关更多信息，请参阅[配置策略](./configure.md)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### Severity-Based Vulnerability

**Severity-Based Vulnerability**（基于严重性的漏洞）策略类型检查您的构建产物是否暴露于已知漏洞。

默认情况下，此策略仅标记有可用修复版本的严重（critical）和高（high）级别漏洞。实际上，这意味着对于未通过此策略的镜像，存在一个简单的修复方法：将有漏洞的软件包升级到包含漏洞修复的版本。

如果镜像包含一个或多个不符合指定策略标准的漏洞，则该镜像被视为不符合此策略。

您可以通过创建该策略的自定义版本来配置此策略的参数。在自定义版本中可配置以下策略参数：

- **Age**（年龄）：漏洞首次发布以来的最少天数

  仅标记具有一定最小年龄的漏洞的原因是，新发现的漏洞不应在您有机会处理它们之前导致评估失败。

<!-- vale Vale.Spelling = NO -->
- **Severities**（严重性）：要考虑的严重性级别（默认：`Critical, High`）
<!-- vale Vale.Spelling = YES -->

- **Fixable vulnerabilities only**（仅可修复的漏洞）：是否仅报告有可用修复版本的漏洞（默认启用）。

- **Package types**（软件包类型）：要考虑的软件包类型列表。

  此选项让您可以指定要包含在策略评估中的软件包类型，以 [PURL 软件包类型定义](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst)形式指定。默认情况下，策略考虑所有软件包类型。

有关配置策略的更多信息，请参阅[配置策略](./configure.md)。

### Compliant Licenses

**Compliant Licenses**（合规许可证）策略类型检查您的镜像是否包含以不适当许可证分发的软件包。如果镜像包含一个或多个具有此类许可证的软件包，则被视为不合规。

您可以配置此策略应关注的许可证列表，并通过指定允许列表（以 PURL 形式）添加例外。请参阅[配置策略](./configure.md)。

### Up-to-Date Base Images

**Up-to-Date Base Images**（最新基础镜像）策略类型检查您使用的基础镜像是否是最新的。

如果您用于构建镜像的标签指向的摘要与您正在使用的不同，则该镜像被视为不符合此策略。如果摘要不匹配，这意味着您使用的基础镜像已过期。

您的镜像需要来源证明（provenance attestations）才能成功评估此策略。有关更多信息，请参阅[无基础镜像数据](#no-base-image-data)。

### High-Profile Vulnerabilities

**High-Profile Vulnerabilities**（高危漏洞）策略类型检查您的镜像是否包含 Docker Scout 精选列表中的漏洞。此列表会随着新披露的、被广泛认为存在风险的漏洞而保持更新。

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

您可以通过配置策略来自定义此策略，以更改哪些 CVE 被视为高危。自定义配置选项包括：

- **Excluded CVEs**（排除的 CVE）：指定您希望此策略忽略的 CVE。

  默认：`[]`（不忽略任何高危 CVE）

- **CISA KEV**：启用对 CISA 已知被利用漏洞（KEV）目录中漏洞的跟踪

  [CISA KEV 目录](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)包括正在被积极利用的漏洞。启用后，该策略会标记包含 CISA KEV 目录中漏洞的镜像。

  默认启用。

有关策略配置的更多信息，请参阅[配置策略](./configure.md)。

### Supply Chain Attestations

**Supply Chain Attestations**（供应链证明）策略类型检查您的镜像是否具有 [SBOM](/manuals/build/metadata/attestations/sbom.md) 和[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。

如果镜像缺少 SBOM 证明或缺少具有 *max mode* 来源的来源证明，则被视为不合规。为确保合规，请更新您的构建命令以在构建时附加这些证明：

```console
$ docker buildx build --provenance=true --sbom=true -t <IMAGE> --push .
```

有关使用证明进行构建的更多信息，请参阅[证明](/manuals/build/metadata/attestations/_index.md)。

如果您使用 GitHub Actions 来构建和推送镜像，请了解如何[配置该操作](/manuals/build/ci/github-actions/attestations.md)以应用 SBOM 和来源证明。

### Default Non-Root User

默认情况下，容器以 `root` 超级用户身份运行，在容器内拥有完整的系统管理权限，除非 Dockerfile 指定了不同的默认用户。以特权用户运行容器会削弱其运行时安全性，因为这意味着容器中运行的任何代码都可以执行管理操作。

**Default Non-Root User**（默认非 Root 用户）策略类型检测设置为以默认 `root` 用户运行的镜像。要符合此策略，镜像必须在镜像配置中指定非 root 用户。如果镜像没有为运行时阶段指定非 root 默认用户，则不符合此策略。

对于不合规的镜像，评估结果会显示是否为镜像显式设置了 `root` 用户。这有助于您区分由隐式 `root` 用户的镜像引起的策略违规和故意设置 `root` 的镜像。

以下 Dockerfile 默认以 `root` 运行，尽管没有显式设置：

```Dockerfile
FROM alpine
RUN echo "Hi"
```

而在以下情况中，`root` 用户是显式设置的：

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> [!NOTE]
>
> 此策略仅检查镜像的默认用户，如镜像配置 blob 中所设置。即使您确实指定了非 root 默认用户，仍然可以在运行时覆盖默认用户，例如通过使用 `docker run` 命令的 `--user` 标志。

要使您的镜像符合此策略，请使用 [`USER`](/reference/dockerfile.md#user) Dockerfile 指令为运行时阶段设置一个没有 root 权限的默认用户。

以下 Dockerfile 代码片段展示了合规镜像和不合规镜像之间的区别。

{{< tabs >}}
{{< tab name="Non-compliant" >}}

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< tab name="Compliant" >}}

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

### Approved Base Images

**Approved Base Images**（已批准的基础镜像）策略类型确保您在构建中使用的基础镜像是经过维护且安全的。

此策略检查您构建中使用的基础镜像是否与策略配置中指定的任何模式匹配。下表显示了此策略的几个示例模式。

| 用例                                                           | 模式                             |
| --------------------------------------------------------------- | -------------------------------- |
| 允许来自 Docker Hub 的所有镜像                                   | `docker.io/*`                    |
| 允许所有 Docker 官方镜像                                         | `docker.io/library/*`            |
| 允许来自特定组织的镜像                                           | `docker.io/orgname/*`            |
| 允许特定仓库的标签                                               | `docker.io/orgname/repository:*` |
| 允许主机名为 `registry.example.com` 的镜像仓库上的镜像           | `registry.example.com/*`         |
| 允许 NodeJS 镜像的 slim 标签                                     | `docker.io/library/node:*-slim`  |

星号（`*`）匹配到其后的字符或镜像引用的末尾。请注意，需要 `docker.io` 前缀才能匹配 Docker Hub 镜像。这是 Docker Hub 的镜像仓库主机名。

此策略可通过以下选项进行配置：

- **Approved base image sources**（已批准的基础镜像来源）

  指定您要允许的镜像引用模式。策略根据这些模式评估基础镜像引用。

  默认：`[*]`（任何引用都是允许的基础镜像）

- **Only supported tags**（仅支持的标签）

  使用 Docker 官方镜像时仅允许受支持的标签。

  启用此选项后，使用官方镜像的不受支持标签作为基础镜像的镜像将触发策略违规。官方镜像的受支持标签列在 Docker Hub 上仓库概述的 **Supported tags** 部分。

  默认启用。

- **Only supported OS distributions**（仅支持的操作系统发行版）

  仅允许受支持的 Linux 发行版版本的 Docker 官方镜像。

  启用此选项后，使用已到达生命周期终止的不受支持 Linux 发行版（如 `ubuntu:18.04`）的镜像将触发策略违规。

  如果无法确定操作系统版本，启用此选项可能会导致策略报告无数据。

  默认启用。

您的镜像需要来源证明才能成功评估此策略。有关更多信息，请参阅[无基础镜像数据](#no-base-image-data)。

### SonarQube Quality Gates

**SonarQube Quality Gates**（SonarQube 质量门禁）策略类型建立在 [SonarQube 集成](../integrations/code-quality/sonarqube.md)之上，以评估源代码的质量。此策略通过将 SonarQube 代码分析结果引入 Docker Scout 来工作。

您使用 SonarQube 的[质量门禁](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/)来定义此策略的标准。SonarQube 根据您在 SonarQube 中定义的质量门禁评估您的源代码。Docker Scout 将 SonarQube 评估作为 Docker Scout 策略呈现。

Docker Scout 使用[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)或 `org.opencontainers.image.revision` OCI 注解将 SonarQube 分析结果与容器镜像关联。除了启用 SonarQube 集成外，您还必须确保您的镜像具有证明或标签。

![Git commit SHA 将镜像与 SonarQube 分析关联](../images/scout-sq-commit-sha.webp)

一旦您推送镜像并完成策略评估，SonarQube 质量门禁的结果将作为策略显示在 Docker Scout 仪表板和 CLI 中。

> [!NOTE]
>
> Docker Scout 只能访问启用集成后创建的 SonarQube 分析。Docker Scout 无法访问历史评估。在启用集成后触发 SonarQube 分析和策略评估以在 Docker Scout 中查看结果。

## 无基础镜像数据

在某些情况下，无法确定构建中使用的基础镜像的信息。在这种情况下，**Up-to-Date Base Images** 和 **Approved Base Images** 策略会被标记为 **No data**（无数据）。

出现此"无数据"状态的情况包括：

- Docker Scout 不知道您使用的基础镜像标签
- 您使用的基础镜像版本有多个标签，但并非所有标签都已过期

为确保 Docker Scout 始终了解您的基础镜像，您可以在构建时附加[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。Docker Scout 使用来源证明来找出基础镜像版本。
