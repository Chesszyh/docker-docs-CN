---
title: FIPS
description: 了解 Docker 强化镜像如何通过使用经过验证的加密模块来支持 FIPS 140，帮助组织满足合规要求。
keywords: docker fips, fips 140 images, fips docker images, docker compliance, secure container images
---

## 什么是 FIPS 140？

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) 是美国政府标准，定义了保护敏感信息的加密模块的安全要求。它广泛用于政府、医疗保健和金融服务等受监管环境。

FIPS 认证由 [NIST 加密模块验证计划（CMVP）](https://csrc.nist.gov/projects/cryptographic-module-validation-program)管理，确保加密模块符合严格的安全标准。

## 为什么 FIPS 合规性很重要

在必须保护敏感数据的许多受监管环境中，FIPS 140 合规性是必需的或强烈推荐的，例如政府、医疗保健、金融和国防领域。这些标准确保加密操作使用经过审查、可信的算法在安全模块中执行。

使用依赖于经过验证的加密模块的软件组件可以帮助组织：

- 满足联邦和行业要求，例如 FedRAMP，它要求或强烈推荐 FIPS 140 验证的加密。
- 展示审计就绪性，提供安全、基于标准的加密实践的可验证证据。
- 降低安全风险，通过阻止未批准或不安全的算法（例如 MD5）并确保跨环境的一致行为。

## Docker 强化镜像如何支持 FIPS 合规性

Docker 强化镜像（DHIs）包含使用经过 FIPS 140 验证的加密模块的变体。这些镜像旨在通过整合符合标准的组件来帮助组织满足合规要求。

- FIPS 镜像变体使用已经过 FIPS 140 验证的加密模块。
- 这些变体由 Docker 构建和维护，以支持具有法规或合规需求的环境。
- Docker 提供签名的测试证明，记录经过验证的加密模块的使用。这些证明可以支持内部审计和合规报告。

> [!NOTE]
>
> 使用 FIPS 镜像变体有助于满足合规要求，但不会使应用程序或系统完全合规。合规性取决于镜像在更广泛系统中的集成和使用方式。

## 识别支持 FIPS 的镜像

支持 FIPS 的 Docker 强化镜像在 Docker 强化镜像目录中标记为 **FIPS** 合规。

要查找具有 FIPS 镜像变体的 DHI 仓库，请[探索镜像](../how-to/explore.md)并：

- 在目录页面上使用 **FIPS** 过滤器
- 在单个镜像列表中查找 **FIPS** 合规标记

这些指示器帮助您快速定位支持基于 FIPS 合规需求的仓库。包含 FIPS 支持的镜像变体将具有以 `-fips` 结尾的标签，例如 `3.13-fips`。

## 使用证明验证 FIPS 相关测试

Docker 强化镜像包含签名的[测试证明](../core-concepts/attestations.md)，记录自动化镜像验证的结果。对于 FIPS 变体，这包括验证镜像是否使用 FIPS 验证的加密模块的测试用例。

您可以使用 Docker Scout CLI 检索和检查此证明：

```console
$ docker scout attest get \
  --predicate-type https://scout.docker.com/tests/v0.1 \
  --predicate \
  <your-namespace>/dhi-<image>:<tag> --platform <platform>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://scout.docker.com/tests/v0.1 \
  --predicate \
  docs/dhi-python:3.13-fips --platform linux/amd64
```

输出是结构化的 JSON 报告。单个测试输出在 `stdout` 等字段下以 base64 编码。您可以解码它们以查看原始测试输出。

要解码并查看测试结果：

```console
$ docker scout attest get \
  --predicate-type https://scout.docker.com/tests/v0.1 \
  --predicate \
  docs/dhi-python:3.13-fips --platform linux/amd64 \
  | jq -r '.results.tests[].extra.stdout' \
  | base64 -d
```
