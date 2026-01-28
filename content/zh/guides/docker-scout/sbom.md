---
title: 软件物料清单
description: 了解软件物料清单（SBOM）以及 Docker Scout 如何使用它。
keywords: scout, sbom, software bill of materials, analysis, composition
aliases:
  - /scout/concepts/sbom/
weight: 40
---

{{< youtube-embed PbS4y7C7h4A >}}

物料清单（BOM）是制造产品所需的材料、零件及其数量的列表。例如，计算机的物料清单可能列出主板、CPU、内存、电源、存储设备、机箱和其他组件，以及构建计算机所需的各组件数量。

软件物料清单（SBOM）是构成软件的所有组件的列表。这包括开源和第三方组件，以及为软件编写的任何自定义代码。SBOM 类似于实体产品的物料清单，但适用于软件。

在软件供应链安全的背景下，SBOM 可以帮助识别和降低软件中的安全和合规风险。通过准确了解软件中使用的组件，您可以快速识别和修补组件中的漏洞，或确定某个组件的许可证是否与您的项目不兼容。

## SBOM 的内容

SBOM 通常包含以下信息：

- SBOM 描述的软件名称，例如库或框架的名称。
- 软件版本。
- 软件分发所依据的许可证。
- 软件依赖的其他组件列表。

## Docker Scout 如何使用 SBOM

Docker Scout 使用 SBOM 来确定 Docker 镜像中使用的组件。当您分析镜像时，Docker Scout 将使用作为证明附加到镜像的 SBOM，或者通过分析镜像内容即时生成 SBOM。

SBOM 与[安全公告数据库](/manuals/scout/deep-dive/advisory-db-sources.md)进行交叉引用，以确定镜像中的任何组件是否存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>
