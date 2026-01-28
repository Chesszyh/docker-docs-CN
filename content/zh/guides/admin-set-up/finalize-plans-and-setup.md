---
title: 最终确定计划并开始设置
description: 与 MDM 团队协作分发配置，并设置 SSO 和 Docker 产品试用。
weight: 20
---

## 第一步：将最终确定的设置文件发送给 MDM 团队

在按照模块一中概述的内容与相关团队就基准和安全配置达成一致后，使用 [Docker 管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)或 [`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)配置设置管理。

文件准备好后，与 MDM 团队协作部署您选择的设置，以及您选择的[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)方法。

> [!IMPORTANT]
>
> 强烈建议您首先与少数 Docker Desktop 开发人员一起测试，以验证功能是否按预期工作，然后再进行更广泛的部署。

## 第二步：管理您的组织

如果您有多个组织，建议您将它们合并为一个组织，或创建一个 [Docker 公司](/manuals/admin/company/_index.md)来管理多个组织。请与 Docker 客户成功和实施团队合作完成此操作。

## 第三步：开始设置

### 设置单点登录 SSO 域名验证

单点登录（SSO）允许开发人员使用其身份提供商（IdP）进行身份验证以访问 Docker。SSO 可用于整个公司及其所有关联组织，或用于拥有 Docker Business 订阅的单个组织。有关更多信息，请参阅[文档](/manuals/security/for-admins/single-sign-on/_index.md)。

您还可以启用 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 以进一步自动化用户的配置和取消配置。

### 设置订阅中包含的 Docker 产品权限

[Docker Build Cloud](/manuals/build-cloud/_index.md) 通过提供专用的远程构建器和共享缓存，显著减少本地和 CI 中的构建时间。借助云端的强大能力，开发人员的时间和本地资源得以释放，使您的团队能够专注于更重要的事情，如创新。要开始使用，请[设置云构建器](https://app.docker.com/build/)。

[Docker Scout](manuals/scout/_index.md) 是一个主动增强软件供应链安全性的解决方案。通过分析您的镜像，Docker Scout 编制组件清单，也称为软件物料清单（SBOM）。SBOM 与持续更新的漏洞数据库进行匹配，以查明安全弱点。要开始使用，请参阅[快速入门](/manuals/scout/quickstart.md)。

### 确保运行受支持版本的 Docker Desktop

> [!WARNING]
>
> 此步骤可能会影响使用旧版本 Docker Desktop 的用户体验。

现有用户可能正在运行过时或不受支持的 Docker Desktop 版本。强烈建议所有用户更新到受支持的版本。从最新版本发布起 6 个月内发布的 Docker Desktop 版本都受支持。

建议您使用 MDM 解决方案来管理用户的 Docker Desktop 版本。用户也可以直接从 Docker 或通过公司软件门户获取 Docker Desktop。
