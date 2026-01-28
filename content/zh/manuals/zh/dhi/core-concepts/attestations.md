---
title: 证明
description: 查看每个 Docker 强化镜像包含的完整签名证明集，如 SBOM、VEX、构建来源证明和扫描结果。
keywords: container image attestations, signed sbom, build provenance, slsa compliance, vex document
---

Docker 强化镜像（DHIs）包含全面的签名安全证明，用于验证镜像的构建过程、内容和安全状况。这些证明是安全软件供应链实践的核心部分，帮助用户验证镜像是可信和符合策略的。

## 什么是证明？

证明（Attestation）是一份签名声明，提供关于镜像的可验证信息，例如它是如何构建的、包含什么内容以及通过了哪些安全检查。证明通常使用 Sigstore 工具（如 Cosign）签名，使其具有防篡改性和加密可验证性。

证明遵循标准化格式（如 [in-toto](https://in-toto.io/)、[CycloneDX](https://cyclonedx.org/) 和 [SLSA](https://slsa.dev/)），并作为 OCI 兼容元数据附加到镜像上。它们可以在镜像构建期间自动生成，或手动添加以记录额外的测试、扫描结果或自定义来源证明。

## 为什么证明很重要？

证明通过以下方式提供对软件供应链的关键可见性：

- 记录镜像中包含*什么*（例如 SBOM）
- 验证*如何*构建的（例如构建来源证明）
- 捕获*通过或未通过哪些安全扫描*（例如 CVE 报告、密钥扫描、测试结果）
- 帮助组织执行合规性和安全策略
- 支持运行时信任决策和 CI/CD 策略门控

它们对于满足 SLSA 等行业标准至关重要，并通过使构建和安全数据透明且可验证来帮助团队降低供应链攻击的风险。

## Docker 强化镜像如何使用证明

所有 DHIs 都使用 [SLSA Build Level 3](https://slsa.dev/spec/latest/levels) 实践构建，每个镜像变体都发布有完整的签名证明集。这些证明允许用户：

- 验证镜像是在安全环境中从可信来源构建的
- 以多种格式查看 SBOM 以了解组件级别的详细信息
- 查看扫描结果以检查漏洞或嵌入的密钥
- 确认每个镜像的构建和部署历史

证明会自动发布并与您 Docker Hub 组织中的每个镜像同步的 DHI 关联。它们可以使用 [Docker Scout](../how-to/verify.md) 或 [Cosign](https://docs.sigstore.dev/cosign/overview) 等工具检查，并可被 CI/CD 工具或安全平台使用。

## 可用的证明

以下证明可用于每个镜像变体。

| 证明类型 | 描述 | 谓词类型 URI |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| CycloneDX SBOM | [CycloneDX](https://cyclonedx.org/) 格式的软件物料清单，列出组件、库和版本。 | `https://cyclonedx.org/bom/v1.5` |
| SPDX SBOM | [SPDX](https://spdx.dev/) 格式的 SBOM，在开源生态系统中被广泛采用。 | `https://spdx.dev/Document` |
| Scout SBOM | 由 Docker Scout 生成和签名的 SBOM，包含额外的 Docker 特定元数据。 | `https://scout.docker.com/sbom/v0.1` |
| CVEs（in-toto 格式） | 基于包和发行版扫描，影响镜像组件的已知漏洞（CVE）列表。 | `https://in-toto.io/attestation/vulns/v0.1` |
| CVEs（Scout 格式） | 由 Docker Scout 生成的漏洞报告，列出已知 CVE 和严重性数据。 | `https://scout.docker.com/vulnerabilities/v0.1` |
| VEX | [漏洞可利用性交换（VEX）](https://openvex.dev/)文档，标识不适用于镜像的漏洞并解释原因（例如，不可达或不存在）。 | `https://openvex.dev/ns/v0.2.0` |
| 密钥扫描 | 扫描意外包含的密钥（如凭据、令牌或私钥）的结果。 | `https://scout.docker.com/secrets/v0.1` |
| 病毒扫描 | 对镜像层执行的防病毒扫描结果。 | `https://scout.docker.com/virus/v0.1` |
| 测试 | 对镜像运行的自动化测试记录，如功能检查或验证脚本。 | `https://scout.docker.com/tests/v0.1` |
| Scout 健康评分 | 来自 Docker Scout 的签名证明，总结镜像的整体安全和质量状况。 | `https://scout.docker.com/health/v0.1` |
| 构建来源证明（Scout） | 由 Docker Scout 生成的来源元数据，包括源 Git 提交、构建参数和环境详情。 | `https://scout.docker.com/provenance/v0.1` |
| SLSA 来源证明 | 标准 [SLSA](https://slsa.dev/) 来源声明，描述镜像的构建方式，包括构建工具、参数和来源。 | `https://slsa.dev/provenance/v0.2` |
| SLSA 验证摘要 | 指示镜像是否符合 SLSA 要求的摘要证明。 | `https://slsa.dev/verification_summary/v1` |

## 查看和验证证明

要查看和验证镜像的证明，请参阅[验证 Docker 强化镜像](../how-to/verify.md)。

## 添加您自己的证明

除了 Docker 强化镜像提供的全面证明外，您还可以在构建派生镜像时添加自己的签名证明。如果您正在基于 DHI 构建新应用程序并希望在软件供应链中保持透明度、可追溯性和信任，这特别有用。

通过附加 SBOM、构建来源证明或自定义元数据等证明，您可以满足合规要求、通过安全审计并支持 Docker Scout 等策略评估工具。

这些证明随后可以使用 Cosign 或 Docker Scout 等工具在下游进行验证。

要了解如何在构建过程中附加自定义证明，请参阅[构建证明](/manuals/build/metadata/attestations.md)。
