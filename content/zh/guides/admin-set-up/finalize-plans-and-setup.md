---
title: 敲定计划并开始设置
description: 与你的 MDM 团队协作，分发配置并设置 SSO 和 Docker 产品试用。
weight: 20
---

## 第一步：将最终确定的设置文件发送给 MDM 团队

在与相关团队就你的基线和安全配置达成一致后（如模块一中所述），使用 [Docker 管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)或 [`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)配置设置管理。

文件准备就绪后，与你的 MDM 团队协作，部署你选择的设置以及你选择的[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)方法。

> [!IMPORTANT]
>
> 强烈建议你首先与少数 Docker Desktop 开发人员一起测试此功能，以验证其功能是否按预期工作，然后再进行更广泛的部署。

## 第二步：管理你的组织

如果你有多个组织，建议你将它们合并为一个组织或创建一个 [Docker 公司](/manuals/admin/company/_index.md)来管理多个组织。与 Docker 客户成功和实施团队合作以实现此目标。

## 第三步：开始设置

### ��置单点登录 SSO 域验证

单点登录 (SSO) 允许开发人员使用其身份提供商 (IdP) 进行身份验证以访问 Docker。SSO 可用于整个公司及其所有关联组织，或拥有 Docker Business 订阅的单个组织。有关更多信息，请参阅[文档](/manuals/security/for-admins/single-sign-on/_index.md)。

你还可以启用 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 以进一步自动化用户的配置和取消配置。

### 设置订阅中包含的 Docker 产品权益

[Docker Build Cloud](/manuals/build-cloud/_index.md) 通过提供专用的远程构建器和共享缓存，显着减少了本地和 CI 中的构建时间。在云的支持下，开发人员的时间和本地资源得以释放，因此你的团队可以专注于更重要的事情，例如创新。要开始使用，请[设置云构建器](https://app.docker.com/build/)。

[Docker Scout](manuals/scout/_index.md) 是一个主动增强你的软件供应链安全性的解决方案。通过分析你的镜像，Docker Scout 会编译一个组件清单，也称为软件物料清单 (SBOM)。SBOM 会与不断更新的漏洞数据库进行匹配，以查明安全漏洞。要开始使用，请参阅[快速入门](/manuals/scout/quickstart.md)。

### 确保你正在运行受支持的 Docker Desktop 版本

> [!WARNING]
>
> 此步骤可能会影响使用旧版本 Docker Desktop 的用户的体验。

现有用户可能正在运行过时或不受支持的 Docker Desktop 版本。强烈建议所有用户更新到受支持的版本。支持从最新版本发布起 6 个月内的 Docker Desktop 版本。

建议你使用 MDM 解决方案来管理用户的 Docker Desktop 版本。用户也可以直接从 Docker 或通过公司软件门户获取 Docker Desktop。
