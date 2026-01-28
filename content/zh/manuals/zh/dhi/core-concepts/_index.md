---
title: 核心概念
description: 了解 Docker 强化镜像背后的核心概念，包括安全元数据、漏洞管理、镜像结构和验证。
weight: 30
params:
  grid_concepts_metadata:
    - title: Attestations
      description: Review the full set of signed attestations included with each Docker Hardened Image, such as SBOMs, VEX, build provenance, and scan results.
      icon: assignment
      link: /dhi/core-concepts/attestations/
    - title: Software Bill of Materials (SBOMs)
      description: Learn what SBOMs are, why they matter, and how Docker Hardened Images include signed SBOMs to support transparency and compliance.
      icon: list_alt
      link: /dhi/core-concepts/sbom/
    - title: Supply-chain Levels for Software Artifacts (SLSA)
      description: Learn how Docker Hardened Images comply with SLSA Build Level 3 and how to verify provenance for secure, tamper-resistant builds.
      icon: fact_check
      link: /dhi/core-concepts/slsa/
    - title: Image provenance
      description: Learn how build provenance metadata helps trace the origin of Docker Hardened Images and support compliance with SLSA.
      icon: track_changes
      link: /dhi/core-concepts/provenance/
    - title: FIPS
      description: Learn how Docker Hardened Images support FIPS 140 by using validated cryptographic modules and providing signed attestations for compliance audits.
      icon: verified
      link: /dhi/core-concepts/fips/

  grid_concepts_risk:
    - title: Common Vulnerabilities and Exposures (CVEs)
      description: Understand what CVEs are, how Docker Hardened Images reduce exposure, and how to scan images for vulnerabilities using popular tools.
      icon: error
      link: /dhi/core-concepts/cves/
    - title: Vulnerability Exploitability eXchange (VEX)
      description: Learn how VEX helps you prioritize real risks by identifying which vulnerabilities in Docker Hardened Images are actually exploitable.
      icon: warning
      link: /dhi/core-concepts/vex/
    - title: Software Supply Chain Security
      description: Learn how Docker Hardened Images help secure every stage of your software supply chain with signed metadata, provenance, and minimal attack surface.
      icon: shield
      link: /dhi/core-concepts/sscs/
    - title: Secure Software Development Lifecycle (SSDLC)
      description: See how Docker Hardened Images support a secure SDLC by integrating with scanning, signing, and debugging tools.
      icon: build_circle
      link: /dhi/core-concepts/ssdlc/

  grid_concepts_structure:
    - title: Distroless images
      description: Learn how Docker Hardened Images use distroless variants to minimize attack surface and remove unnecessary components.
      icon: layers_clear
      link: /dhi/core-concepts/distroless/
    - title: glibc and musl support in Docker Hardened Images
      description: Compare glibc and musl variants of DHIs to choose the right base image for your application's compatibility, size, and performance needs.
      icon: swap_vert
      link: /dhi/core-concepts/glibc-musl/
    - title: Image immutability
      description: Understand how image digests, read-only containers, and signed metadata ensure Docker Hardened Images are tamper-resistant and immutable.
      icon: do_not_disturb_on
      link: /dhi/core-concepts/immutability/
    - title: Image hardening
      description: Learn how Docker Hardened Images are designed for security, with minimal components, nonroot execution, and secure-by-default configurations.
      icon: security
      link: /dhi/core-concepts/hardening/

  grid_concepts_verification:
    - title: Digests
      description: Learn how to use immutable image digests to guarantee consistency and verify the exact Docker Hardened Image you're running.
      icon: fingerprint
      link: /dhi/core-concepts/digests/
    - title: Code signing
      description: Understand how Docker Hardened Images are cryptographically signed using Cosign to verify authenticity, integrity, and secure provenance.
      icon: key
      link: /dhi/core-concepts/signatures/
---

Docker 强化镜像（DHIs）建立在安全软件供应链实践的基础之上。本节解释该基础背后的核心概念，从签名证明和不可变摘要到 SLSA 和 VEX 等标准。

如果您想了解 Docker 强化镜像如何支持合规性、透明度和安全性，请从这里开始。

## 安全元数据和证明

{{< grid items="grid_concepts_metadata" >}}

## 漏洞和风险管理

{{< grid items="grid_concepts_risk" >}}

## 镜像结构和行为

{{< grid items="grid_concepts_structure" >}}

## 验证和可追溯性

{{< grid items="grid_concepts_verification" >}}
