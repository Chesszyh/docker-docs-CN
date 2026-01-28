---
title: Docker Scout
weight: 40
keywords: scout, supply chain, vulnerabilities, packages, cves, scan, analysis, analyze
description:
  获取 Docker Scout 概述，主动增强您的软件供应链安全
aliases:
  - /engine/scan/
params:
  sidebar:
    group: Products
grid:
  - title: 快速入门
    link: /scout/quickstart/
    description: 了解 Docker Scout 的功能以及如何开始使用。
    icon: explore
  - title: 镜像分析
    link: /scout/image-analysis/
    description: 揭示并深入了解镜像的组成。
    icon: radar
  - title: 安全公告数据库
    link: /scout/advisory-db-sources/
    description: 了解 Docker Scout 使用的信息来源。
    icon: database
  - title: 集成
    description: |
      将 Docker Scout 与您的 CI、镜像仓库和其他第三方服务连接。
    link: /scout/integrations/
    icon: multiple_stop
  - title: 仪表板
    link: /scout/dashboard/
    description: |
      Docker Scout 的 Web 界面。
    icon: dashboard
  - title: 策略
    link: /scout/policy/
    description: |
      确保您的制品符合供应链最佳实践。
    icon: policy
  - title: 升级
    link: /subscription/change/
    description: |
      个人订阅包含最多 1 个仓库。如需更多，请升级。
    icon: upgrade
---

容器镜像由层和软件包组成，这些都容易受到漏洞的影响。
这些漏洞可能会危及容器和应用程序的安全。

Docker Scout 是一种主动增强软件供应链安全的解决方案。
通过分析您的镜像，Docker Scout 编制组件清单，也称为软件物料清单（Software Bill of Materials，SBOM）。
SBOM 与持续更新的漏洞数据库进行匹配，以精确定位安全弱点。

Docker Scout 是一个独立的服务和平台，您可以通过
Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout 仪表板与之交互。
Docker Scout 还支持与第三方系统的集成，例如容器镜像仓库和 CI 平台。

{{< grid >}}
