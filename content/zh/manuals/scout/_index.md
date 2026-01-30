---
title: Docker Scout
weight: 40
keywords: scout, 供应链, 漏洞, 软件包, cves, 扫描, 分析
description:
  了解 Docker Scout 概览，主动增强软件供应链安全
aliases:
  - /engine/scan/
params:
  sidebar:
    group: 产品
grid:
  - title: 快速入门
    link: /scout/quickstart/
    description: 了解 Docker Scout 的功能以及如何开始使用。
    icon: explore
  - title: 镜像分析
    link: /scout/image-analysis/
    description: 揭示并深入研究镜像的组成。
    icon: radar
  - title: 咨询数据库
    link: /scout/advisory-db-sources/
    description: 了解 Docker Scout 使用的信息源。
    icon: database
  - title: 集成
    description: |
      将 Docker Scout 与您的 CI、注册表和其他第三方服务连接。
    link: /scout/integrations/
    icon: multiple_stop
  - title: 控制面板
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
      个人订阅最多包含 1 个仓库。升级以获得更多。
    icon: upgrade
---

容器镜像由层和软件包组成，这些内容容易受到漏洞的影响。
这些漏洞可能会损害容器和应用程序的安全。

Docker Scout 是一个用于主动增强软件供应链安全的解决方案。
通过分析您的镜像，Docker Scout 会编译一份组件清单，也称为软件物料清单 (SBOM)。
SBOM 将与不断更新的漏洞数据库进行匹配，以查明安全漏洞。

Docker Scout 是一个独立的系统和平台，您可以使用 Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout Dashboard 与之交互。
Docker Scout 还支持与第三方系统集成，例如容器注册表和 CI 平台。

{{< grid >}}
