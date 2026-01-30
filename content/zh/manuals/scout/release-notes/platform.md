---
title: Docker Scout 发布说明
linkTitle: 平台发布说明
description: 了解 Docker Scout 的最新功能
keywords: docker scout, 发布说明, 更新日志, 功能, 变化, 增量, 新版本, 发布
aliases:
- /scout/release-notes/
tags: [发布说明]
---

<!-- vale Docker.We = NO -->

本页包含有关 Docker Scout 发布版本中新功能、改进、已知问题和错误修复的信息。这些发布说明涵盖了 Docker Scout 平台，包括控制面板 (Dashboard)。有关 CLI 的发布说明，请参阅 [Docker Scout CLI 发布说明](./cli.md)。

## 2024 年第四季度

2024 年第四季度发布的最新功能和改进。

### 2024-10-09

策略评估 (Policy Evaluation) 已从早期访问阶段正式进入正式发布 (GA) 阶段。

Docker Scout 控制面板 UI 更改：

- 在 Docker Scout 控制面板上，选择策略卡片现在将打开策略详情页面，而不是策略结果页面。
- 策略结果页面和策略详情侧面板现在为只读。策略操作 (编辑、禁用、删除) 现在可以从策略详情页面访问。

## 2024 年第三季度

2024 年第三季度发布的最新功能和改进。

### 2024-09-30

在此版本中，我们更改了自定义策略的工作方式。之前，自定义策略是通过复制现成的策略创建的。现在，您可以通过编辑 **策略类型 (policy type)** (作为模板) 中的默认策略来自定义策略。Docker Scout 中的默认策略也是基于这些类型实现的。

有关更多信息，请参阅 [策略类型](/manuals/scout/policy/_index.md#policy-types)。

### 2024-09-09

此版本更改了 Docker Scout 中 [健康评分 (health scores)](/manuals/scout/policy/scores.md) 的计算方式。健康评分计算现在会考虑您为组织配置的可选策略和自定义策略。

这意味着如果您启用、禁用或自定义了任何默认策略，Docker Scout 现在在计算您组织镜像的健康评分时会考虑这些策略。

如果您尚未为组织启用 Docker Scout，健康评分计算将基于现成的默认策略。

### 2024-08-13

此版本更改了现成的默认策略，使其与评估 Docker Scout [健康评分](/manuals/scout/policy/scores.md) 所用的策略配置保持一致。

现在的默认现成策略包括：

- **No high-profile vulnerabilities** (无高关注漏洞)
- **No fixable critical or high vulnerabilities** (无待修复的危急或高危漏洞)
- **Approved Base Images** (经批准的基础镜像)
- **Default non-root user** (默认非 root 用户)
- **Supply chain attestations** (供应链证明)
- **Up-to-Date Base Images** (最新的基础镜像)
- **No AGPL v3 licenses** (无 AGPL v3 许可证)

这些策略的配置现在与计算健康评分所用的配置相同。此前，现成策略的配置与健康评分策略的配置不同。

## 2024 年第二季度

2024 年第二季度发布的最新功能和改进。

### 2024-06-27

此版本在 Docker Scout 控制面板中引入了对 **例外 (Exceptions)** 的初步支持。例外允许您使用 VEX 文档抑制镜像中发现的漏洞 (误报)。将 VEX 文档作为证明 (attestations) 附加到镜像上，或将其嵌入到镜像文件系统中，Docker Scout 将自动检测并将 VEX 声明纳入镜像分析结果中。

新的 [Exceptions 页面](https://scout.docker.com/reports/vex/) 列出了影响您组织镜像的所有例外情况。您还可以转到 Docker Scout 控制面板中的镜像视图，查看适用于给定镜像的所有例外。

有关更多信息，请参阅 [管理漏洞例外](/manuals/scout/explore/exceptions.md)。

### 2024-05-06

新增 HTTP 端点，允许您使用 Prometheus 抓取 Docker Scout 的数据，以便使用 Grafana 创建您自己的漏洞和策略控制面板。
有关更多信息，请参阅 [Docker Scout 指标导出器](/manuals/scout/explore/metrics-exporter.md)。

## 2024 年第一季度

2024 年第一季度发布的最新功能和改进。

### 2024-03-29

**No high-profile vulnerabilities** 策略现在会报告 `xz` 后门漏洞 [CVE-2024-3094](https://scout.docker.com/v/CVE-2024-3094)。您 Docker 组织中任何包含带有后门的 `xz/liblzma` 版本的镜像都将不符合 **No high-profile vulnerabilities** 策略。

### 2024-03-20

**No fixable critical or high vulnerabilities** 策略现在支持 **Fixable vulnerabilities only** (仅限可修复漏洞) 配置选项，允许您决定是否仅标记具有可用修复版本的漏洞。

### 2024-03-14

移除了 **All critical vulnerabilities** (所有危急漏洞) 策略。
**No fixable critical or high vulnerabilities** 策略提供了类似的功能，并且将来会进行更新以支持更广泛的自定义，从而使已移除的 **All critical vulnerabilities** 策略变得冗余。

### 2024-01-26

**Azure Container Registry** 集成已从 [早期访问 (Early Access)](../../release-lifecycle.md#early-access-ea) 晋升为 [正式发布 (GA)](../../release-lifecycle.md#genera-availability-ga)。

有关更多信息和设置说明，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2024-01-23

新增 **Approved Base Images** 策略，允许您限制构建中允许使用的基础镜像。您可以使用模式定义允许的基础镜像。镜像引用不匹配指定模式的基础镜像会导致策略失败。

### 2024-01-12

新增 **Default non-root user** 策略，标记默认以具有完整系统管理权限的 `root` 超级用户身份运行的镜像。为您的镜像指定一个非 root 默认用户有助于增强运行时安全性。

### 2024-01-11

[Beta](../../release-lifecycle.md#beta) 发布了一个新的 GitHub 应用程序，用于将 Docker Scout 与您的源代码管理集成，以及一个帮助您改进策略合规性的修复功能。

修复 (Remediation) 是 Docker Scout 的一项新功能，可根据策略评估结果提供背景化的、建议的操作，指导您如何改进合规性。

GitHub 集成增强了修复功能。通过启用集成，Docker Scout 能够将分析结果与源代码连接起来。这种关于镜像如何构建的额外上下文被用于生成更好、更精确的建议。

有关 Docker Scout 可以提供以帮助您改进策略合规性的建议类型的更多信息，请参阅 [修复 (Remediation)](../policy/remediation.md)。

有关如何在源仓库上授权 Docker Scout GitHub 应用程序的更多信息，请参阅 [将 Docker Scout 与 GitHub 集成](../integrations/source-code-management/github.md)。

## 2023 年第四季度

2023 年第四季度发布的最新功能和改进。

### 2023-12-20

**Azure Container Registry** 集成已从 [Beta](../../release-lifecycle.md#beta) 晋升为 [早期访问 (Early Access)](../../release-lifecycle.md#early-access-ea)。

有关更多信息和设置说明，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-12-06

新增 [SonarQube](https://www.sonarsource.com/products/sonarqube/) 集成及相关策略。SonarQube 是一个用于持续检查代码质量的开源平台。此集成允许您将 SonarQube 的质量门禁作为 Docker Scout 中的策略评估添加进来。启用集成，推送镜像，并在新的 **SonarQube quality gates passed** 策略中查看出现的 SonarQube 质量门禁条件。

### 2023-12-01

[Beta](../../release-lifecycle.md#beta) 发布了新的 **Azure Container Registry** (ACR) 集成，允许 Docker Scout 自动拉取并分析 ACR 仓库中的镜像。

要了解有关集成以及如何开始的更多信息，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-11-21

新增 **可配置策略 (configurable policies)** 功能，使您能够根据自己的偏好调整现成的策略，或者如果它们不完全符合您的需求，可以将其完全禁用。如何为组织调整策略的一些示例包括：

- 更改漏洞相关策略使用的严重性阈值
- 自定义“高关注漏洞”列表
- 添加或删除要标记为“copyleft”的软件许可证

有关更多信息，请参阅 [可配置策略](../policy/configure.md)。

### 2023-11-10

新增 **供应链证明 (Supply chain attestations)** 策略，帮助您跟踪镜像是否使用 SBOM 和来源证明构建。为镜像添加证明是改进供应链行为的良好第一步，通常也是执行更多操作的前提。

### 2023-11-01

新增 **No high-profile vulnerabilities** 策略，确保您的制品不包含被公认为具有风险的精选漏洞列表。

### 2023-10-04

这标志着 Docker Scout 的正式发布 (GA)。

此版本包含以下新功能：

- [策略评估 (Policy Evaluation)](#policy-evaluation) (早期访问)
- [Amazon ECR 集成](#amazon-ecr-integration)
- [Sysdig 集成](#sysdig-integration)
- [JFrog Artifactory 集成](#jfrog-artifactory-integration)

#### 策略评估

策略评估是一项早期访问功能，可帮助您确保软件完整性并跟踪制品随时间推移的表现。此版本随附了四项现成策略，默认对所有组织启用。

![控制面板中的策略概览](../images/release-notes/policy-ea.webp)

- **Base images not up-to-date** 评估基础镜像是否过时且需要更新。最新的基础镜像有助于确保您的环境可靠且安全。
- **Critical and high vulnerabilities with fixes** 报告镜像中是否存在危急或高危严重程度的漏洞，且该漏洞具有可升级到的修复版本。
- **All critical vulnerabilities** 检查镜像中发现的任何危急严重程度的漏洞。
- **Packages with AGPLv3, GPLv3 license** 帮助您捕获镜像中可能不希望使用的 copyleft 许可证。

您可以使用 Docker Scout 控制面板和 `docker scout policy` CLI 命令查看和评估镜像的策略状态。有关更多信息，请参阅 [策略评估文档](/scout/policy/)。

#### Amazon ECR 集成

新的 Amazon Elastic Container Registry (ECR) 集成允许对托管在 ECR 仓库中的镜像进行分析。

您可以使用预配置的 CloudFormation 堆栈模板设置集成，该模板会在您的账户中引导必要的 AWS 资源。Docker Scout 会自动分析您推送到注册表的镜像，仅存储有关镜像内容的元数据，而不存储容器镜像本身。

该集成提供了一个简单的过程来添加额外的仓库、为特定仓库激活 Docker Scout 以及在需要时移除集成。要了解更多信息，请参阅 [Amazon ECR 集成文档](../integrations/registry/ecr.md)。

#### Sysdig 集成

新的 Sysdig 集成可为您的 Kubernetes 运行时环境提供实时安全见解。

启用此集成有助于您针对用于运行生产工作负载的镜像处理风险并确定其优先级。它还有助于减少监控噪音，通过使用 VEX 文档自动排除从未加载到内存中的程序中的漏洞。

有关更多信息和入门，请参阅 [Sysdig 集成文档](../integrations/environment/sysdig.md)。

#### JFrog Artifactory 集成

新的 JFrog Artifactory 集成允许在 Artifactory 注册表上进行自动镜像分析。

该集成涉及部署一个 Docker Scout Artifactory 代理，该代理会轮询新镜像、执行分析并将结果上传到 Docker Scout，同时保持镜像数据的完整性。

#### 已知限制

- 镜像分析仅适用于 Linux 镜像
- Docker Scout 无法处理压缩后大小超过 12GB 的镜像
- 创建镜像 SBOM (镜像分析的一部分) 的超时限制为 4 分钟
