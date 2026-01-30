---
description: Docker 安全公告
keywords: Docker, CVEs, security, notice, Log4J 2, Log4Shell, Text4Shell, announcements, 安全, 公告
title: Docker 安全公告
linkTitle: 安全公告
toc_min: 1
toc_max: 2
---

## Docker Desktop 4.43.0 安全更新：CVE-2025-6587

_最后更新于 2025 年 7 月 3 日_

Docker Desktop 中的一个漏洞已在 7 月 3 日发布的 [4.43.0](/manuals/desktop/release-notes.md#4430) 版本中修复：

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587) 漏洞，该漏洞曾导致敏感的系统环境变量被包含在 Docker Desktop 诊断日志中，从而可能造成机密泄露。

## Docker Desktop 4.41.0 安全更新：CVE-2025-3224、CVE-2025-4095 和 CVE-2025-3911

_最后更新于 2025 年 5 月 15 日_

Docker Desktop 中的三个漏洞已在 4 月 28 日发布的 [4.41.0](/manuals/desktop/release-notes.md#4410) 版本中修复。

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224) 漏洞，该漏洞允许能够访问用户机器的攻击者在 Docker Desktop 更新时执行特权提升。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095) 漏洞，该漏洞曾导致在使用 macOS 配置描述文件时未强制执行注册表访问管理 (RAM) 策略，允许用户从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911) 漏洞，该漏洞允许具有用户机器读取权限的攻击者从 Docker Desktop 日志文件中获取敏感信息，包括为运行中的容器配置的环境变量。

我们强烈建议您更新到 Docker Desktop [4.41.0](/manuals/desktop/release-notes.md#4410)。

## Docker Desktop 4.34.2 安全更新：CVE-2024-8695 和 CVE-2024-8696

_最后更新于 2024 年 9 月 13 日_

由 [Cure53](https://cure53.de/) 报告的两个与 Docker 扩展 (Extensions) 相关的 Docker Desktop 远程代码执行 (RCE) 漏洞，已在 9 月 12 日发布的 [4.34.2](/manuals/desktop/release-notes.md#4342) 版本中修复。

- [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)：通过精心构造的扩展描述/变更日志实现的远程代码执行 (RCE) 漏洞，可能被 4.34.2 之前的 Docker Desktop 中的恶意扩展利用。[危急 (Critical)]
- [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)：通过精心构造的扩展发布者 URL/附加 URL 实现的远程代码执行 (RCE) 漏洞，可能被 4.34.2 之前的 Docker Desktop 中的恶意扩展利用。[高危 (High)]

在扩展市场 (Extensions Marketplace) 中未发现利用这些漏洞的现有扩展。Docker 团队将密切监控并认真审查发布新扩展的任何请求。

我们强烈建议您更新到 Docker Desktop [4.34.2](/manuals/desktop/release-notes.md#4342)。如果您无法立即更新，可以 [禁用 Docker 扩展](/manuals/extensions/settings-feedback.md#turn-on-or-turn-off-extensions) 作为临时解决方法。

## 强制执行 SSO 时 CLI 密码登录的弃用

_最后更新于 2024 年 7 月_

在首次引入 [SSO 强制执行](/manuals/security/for-admins/single-sign-on/connect.md) 时，Docker 提供了一个宽限期，允许在向 Docker Hub 进行身份验证时继续在 Docker CLI 上使用密码。这是为了让组织能够更轻松地使用 SSO 强制执行。建议配置 SSO 的管理员鼓励使用 CLI 的用户 [切换到个人访问令牌 (Personal Access Tokens)](/security/for-admins/single-sign-on/#prerequisites)，以应对此宽限期的结束。

自 2024 年 9 月 16 日起，宽限期结束，当强制执行 SSO 时，将无法再通过 Docker CLI 使用密码向 Docker Hub 进行身份验证。受影响的用户需要切换到使用 PAT 才能继续登录。

在 Docker，我们希望为开发人员和组织提供最安全的体验，而此项弃用是朝着这一方向迈出的关键一步。

## SOC 2 Type 2 鉴证和 ISO 27001 认证

_最后更新于 2024 年 6 月_

Docker 很高兴地宣布，我们已经获得了 SOC 2 Type 2 鉴证和 ISO 27001 认证，没有任何例外或重大不符合项。

安全是 Docker 运营的基本支柱，它已融入我们的整体使命和公司战略中。Docker 的产品是我们用户社区的核心，我们的 SOC 2 Type 2 鉴证和 ISO 27001 认证体现了 Docker 对其用户群持续的安全承诺。

更多信息请参阅 [博客公告](https://www.docker.com/blog/docker-announces-soc-2-type-2-attestation-iso-27001-certification/)。

## Docker 安全公告：runc、BuildKit 和 Moby 中的多个漏洞

_最后更新于 2024 年 2 月 2 日_

在 Docker，我们优先考虑软件的安全性和完整性以及用户的信任。Snyk 实验室的安全研究人员发现并报告了容器生态系统中的四个安全漏洞。其中一个漏洞 [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) 涉及 runc 容器运行时，另外三个影响 BuildKit ([CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653))。我们要向社区保证，我们的团队已与报告者和开源维护者协作，正在努力协调并实施必要的修复。

我们致力于维护最高安全标准。我们已于 1 月 31 日发布了 runc、BuildKit 和 Moby 的补丁版本，并在 2 月 1 日发布了 Docker Desktop 的更新以解决这些漏洞。此外，我们最新的 BuildKit 和 Moby 发布版本还包含了针对 [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) 和 [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) 的修复，这两个漏洞分别是由于独立研究人员发现以及通过 Docker 内部研究计划发现的。

|                        | 受影响版本                |
|:-----------------------|:--------------------------|
| `runc`                 | <= 1.1.11                 |
| `BuildKit`             | <= 0.12.4                 |
| `Moby (Docker Engine)` | <= 25.0.1 且 <= 24.0.8   |
| `Docker Desktop`       | <= 4.27.0                 |

### 如果我使用的是受影响的版本，该怎么办？

如果您正在使用 runc、BuildKit、Moby 或 Docker Desktop 的受影响版本，请务必更新到下表链接中的最新版本：

|                        | 补丁版本                  |
|:-----------------------|:--------------------------|
| `runc`                 | >= [1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)                 |
| `BuildKit`             | >= [0.12.5](https://github.com/moby/buildkit/releases/tag/v0.12.5)                 |
| `Moby (Docker Engine)` | >= [25.0.2](https://github.com/moby/moby/releases/tag/v25.0.2) 且 >= [24.0.9](https://github.com/moby/moby/releases/tag/v24.0.9)   |
| `Docker Desktop`       | >= [4.27.1](/manuals/desktop/release-notes.md#4271)                 |


如果您无法立即更新到不受影响的版本，请遵循以下最佳实践以降低风险：

* 仅使用受信任的 Docker 镜像 (例如 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images))。
* 不要从不受信任的来源或不受信任的 Dockerfile 构建 Docker 镜像。
* 如果您是使用 Docker Desktop 的 Docker Business 客户且无法更新到 v4.27.1，请确保启用 [Hardened Docker Desktop](/manuals/security/for-admins/hardened-desktop/_index.md) 功能，例如：
  * [增强型容器隔离 (Enhanced Container Isolation)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)，它可以在从恶意镜像运行容器的情况下，减轻 CVE-2024-21626 的影响。
  * [镜像访问管理 (Image Access Management)](for-admins/hardened-desktop/image-access-management.md) 和 [注册表访问管理 (Registry Access Management)](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)，它们使组织能够控制其用户可以访问哪些镜像和仓库。
* 针对 CVE-2024-23650、CVE-2024-23651、CVE-2024-23652 和 CVE-2024-23653，避免使用来自不受信任来源的 BuildKit 前端。前端镜像通常指定为您 Dockerfile 上的 #syntax 行，或在使用 `buildctl build` 命令时配合 `--frontend` 标志。
* 要减轻 CVE-2024-24557 的影响，请确保在构建镜像时使用 BuildKit 或禁用缓存。从 CLI 可以通过 `DOCKER_BUILDKIT=1` 环境变量 (如果安装了 buildx 插件，则 Moby >= v23.0 默认启用) 或 `--no-cache` 标志来完成。如果您直接或通过客户端使用 HTTP API，可以通过将 [/build API 端点](https://docs.docker.com/reference/api/engine/version/v1.44/#tag/Image/operation/ImageBuild) 的 `nocache` 设置为 `true` 或 `version` 设置为 `2` 来完成同样的操作。

### 技术细节与影响

#### CVE-2024-21626 (高)

在 runc v1.1.11 及更早版本中，由于某些泄露的文件描述符，攻击者可以通过导致新产生的容器进程 (来自 `runc exec`) 在主机文件系统命名空间中拥有工作目录，或者通过诱导用户运行恶意镜像并允许容器进程通过 `runc run` 获得对主机文件系统的访问权限，从而获得对主机文件系统的访问权限。此类攻击还可以改写半任意的主机二进制文件，从而导致完全的容器逃逸。请注意，在使用更高级别的运行时 (如 Docker 或 Kubernetes) 时，此漏洞可以通过运行恶意容器镜像而无需额外配置，或在启动容器时传递特定的工作目录 (workdir) 选项来利用。对于 Docker，该漏洞也可以从 Dockerfile 内部被利用。

_此问题已在 runc v1.1.12 中修复。_

#### CVE-2024-23651 (高)

在 BuildKit <= v0.12.4 中，两个恶意构建步骤并行运行且共享具有子路径的相同缓存挂载时，可能会引起竞态条件，导致主机系统中的文件可被构建容器访问。这仅在用户尝试构建恶意项目的 Dockerfile 时发生。

_此问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23652 (高)

在 BuildKit <= v0.12.4 中，恶意的 BuildKit 前端或使用 `RUN --mount` 的 Dockerfile 可能会误导移除为挂载点创建的空文件的功能，从而移除主机系统上容器外部的文件。这仅在用户使用恶意的 Dockerfile 时发生。

_此问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23653 (高)

除了将容器作为构建步骤运行外，BuildKit 还提供用于运行基于构建镜像的交互式容器的 API。在 BuildKit <= v0.12.4 中，可以使用这些 API 请求 BuildKit 运行具有提升权限的容器。通常情况下，只有在通过 buildkitd 配置启用了特殊的 `security.insecure` 授权且由初始化构建请求的用户允许时，才允许运行此类容器。

_此问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23650 (中)

在 BuildKit <= v0.12.4 中，恶意的 BuildKit 客户端或前端可以构建一个请求，该请求可能导致 BuildKit 守护进程因崩溃 (panic) 而退出。

_此问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-24557 (中)

在 Moby <= v25.0.1 且 <= v24.0.8 中，如果镜像是基于 `FROM scratch` 构建的，经典构建器的缓存系统容易受到缓存投毒攻击。此外，某些指令 (最重要的是 `HEALTHCHECK` 和 `ONBUILD`) 的更改不会导致缓存未命中。掌握某人正在使用的 Dockerfile 知识的攻击者，可以通过使其拉取一个专门构造的镜像来毒化其缓存，该镜像将被视为某些构建步骤的有效缓存候选。

_此问题已在 Moby >= v25.0.2 且 >= v24.0.9 中修复。_

### 对 Docker 产品有何影响？

#### Docker Desktop

Docker Desktop v4.27.0 及更早版本受到影响。Docker Desktop v4.27.1 已于 2 月 1 日发布，包含了 runc、BuildKit 和 dockerd 二进制文件的补丁。除了更新到这一新版本外，我们鼓励所有 Docker 用户审慎地使用 Docker 镜像和 Dockerfile，并确保在构建中仅使用受信任的内容。

与往常一样，在更新前您应检查适用于您操作系统的 Docker Desktop 系统要求 ([Windows](/manuals/desktop/setup/install/windows-install.md#system-requirements), [Linux](/manuals/desktop/setup/install/linux/_index.md#general-system-requirements), [Mac](/manuals/desktop/setup/install/mac-install.md#system-requirements)) 以确保完全兼容。

#### Docker Build Cloud

任何新的 Docker Build Cloud 构建器实例都将预置最新的 Docker Engine 和 BuildKit 版本，因此不受这些 CVE 的影响。更新也已推送到现有的 Docker Build Cloud 构建器。

_没有其他 Docker 产品受到这些漏洞的影响。_

### 公告链接

* Runc
  * [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
* BuildKit
  * [CVE-2024-23650](https://github.com/moby/buildkit/security/advisories/GHSA-9p26-698r-w4hx)
  * [CVE-2024-23651](https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv)
  * [CVE-2024-23652](https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8)
  * [CVE-2024-23653](https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g)
* Moby
  * [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

## Text4Shell CVE-2022-42889

_最后更新于 2022 年 10 月_

[CVE-2022-42889](https://nvd.nist.gov/vuln/detail/CVE-2022-42889) 已在流行的 Apache Commons Text 库中被发现。该库 1.10.0 之前的版本受到此漏洞的影响。

我们强烈建议您更新到最新版本的 [Apache Commons Text](https://commons.apache.org/proper/commons-text/download_text.cgi)。

### 扫描 Docker Hub 上的镜像

在 UTC 时间 2021 年 10 月 21 日 12:00 之后触发的 Docker Hub 安全扫描现在可以正确识别 Text4Shell CVE。此日期之前的扫描目前不反映该漏洞的状态。因此，我们建议您通过向 Docker Hub 推送新镜像来触发扫描，以便在漏洞报告中查看 Text4Shell CVE 的状态。详细说明请参阅 [扫描 Docker Hub 上的镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

### 受 CVE-2022-42889 影响的 Docker 官方镜像

许多 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 包含受威胁的 Apache Commons Text 版本。以下列表列出了可能包含受影响版本的 Docker 官方镜像：

- [bonita](https://hub.docker.com/_/bonita) 
- [Couchbase](https://hub.docker.com/_/couchbase)
- [Geonetwork](https://hub.docker.com/_/geonetwork) 
- [neo4j](https://hub.docker.com/_/neo4j)
- [sliverpeas](https://hub.docker.com/_/sliverpeas)
- [solr](https://hub.docker.com/_/solr) 
- [xwiki](https://hub.docker.com/_/xwiki) 

我们已在这些镜像中将 Apache Commons Text 更新到最新版本。出于其他原因，其中一些镜像可能不易受攻击。我们建议您同时查阅上游网站发布的指南。

## Log4j 2 CVE-2021-44228

_最后更新于 2021 年 12 月_

[Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 漏洞存在于非常通用的 Java 日志库 Log4j 2 中，它允许远程执行代码，且通常通过攻击者容易获得的上下文进行攻击。例如，在 Minecraft 服务器中发现，可以像日志中输入命令，因为这些命令会被发送到日志记录器。由于该日志库使用极其广泛且可能很容易利用，这使得它成为一个非常严重的漏洞。许多开源维护者都在努力为软件生态系统提供修复和更新。

Log4j 2 的受影响版本包括 2.0 版到 2.14.1 版 (含)。第一个修复版本是 2.15.0。如果可以，我们强烈建议您更新到 [最新版本](https://logging.apache.org/log4j/2.x/download.html)。如果您使用的版本早于 2.0，则也不受影响。

即使您使用的是这些受影响版本，由于您的配置可能已经提供了缓解措施，或者您记录的内容不包含任何用户输入，您可能并不易受攻击。然而，在不深入了解所有可能进行日志记录的代码路径及其输入来源的情况下，这一点可能很难验证。因此，您可能希望升级所有使用受影响版本的代码。

> CVE-2021-45046
>
> 作为 [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 的更新，版本 2.15.0 中进行的修复并不完全。额外的漏洞已被发现并由 [CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046) 和 [CVE-2021-45105](https://nvd.nist.gov/vuln/detail/CVE-2021-45105) 追踪。为了更彻底地修复此漏洞，我们建议您尽可能更新到 2.17.0。

### 扫描 Docker Hub 上的镜像

在 UTC 时间 2021 年 12 月 13 日 17:00 之后触发的 Docker Hub 安全扫描现在可以正确识别 Log4j 2 CVE。此日期之前的扫描目前不反映该漏洞的状态。因此，我们建议您通过向 Docker Hub 推送新镜像来触发扫描，以便在漏洞报告中查看 Log4j 2 CVE 的状态。详细说明请参阅 [扫描 Docker Hub 上的镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

## 受 Log4j 2 CVE 影响的 Docker 官方镜像

_最后更新于 2021 年 12 月_

许多 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 包含受 Log4j 2 CVE-2021-44228 威胁的版本。下表列出了可能包含受影响版本 Log4j 2 的 Docker 官方镜像。我们已在这些镜像中将 Log4j 2 更新到最新版本。出于其他原因，其中一些镜像可能不易受攻击。我们建议您同时查阅上游网站发布的指南。

| 仓库                      | 补丁版本               | 额外文档                       |
|:------------------------|:-----------------------|:-----------------------|
| [couchbase](https://hub.docker.com/_/couchbase)    | 7.0.3 | [Couchbase 博客](https://blog.couchbase.com/what-to-know-about-the-log4j-vulnerability-cve-2021-44228/) |
| [Elasticsearch](https://hub.docker.com/_/elasticsearch)    | 6.8.22, 7.16.2 | [Elasticsearch 公告](https://www.elastic.co/blog/new-elasticsearch-and-logstash-releases-upgrade-apache-log4j2) |
| [Flink](https://hub.docker.com/_/flink)    | 1.11.6, 1.12.7, 1.13.5, 1.14.2  | [Flink 关于 Log4j CVE 的建议](https://flink.apache.org/2021/12/10/log4j-cve.html) |
| [Geonetwork](https://hub.docker.com/_/geonetwork)    | 3.10.10 | [Geonetwork GitHub 讨论](https://github.com/geonetwork/core-geonetwork/issues/6076) |
| [lightstreamer](https://hub.docker.com/_/lightstreamer)     | 等待信息 | 等待信息  |
| [logstash](https://hub.docker.com/_/logstash)    | 6.8.22, 7.16.2 | [Elasticsearch 公告](https://www.elastic.co/blog/new-elasticsearch-and-logstash-releases-upgrade-apache-log4j2) |
| [neo4j](https://hub.docker.com/_/neo4j)     | 4.4.2 | [Neo4j 公告](https://community.neo4j.com/t/log4j-cve-mitigation-for-neo4j/48856) |
| [solr](https://hub.docker.com/_/solr)    | 8.11.1 | [Solr 安全新闻](https://solr.apache.org/security.html#apache-solr-affected-by-apache-log4j-cve-2021-44228) |
| [sonarqube](https://hub.docker.com/_/sonarqube)    | 8.9.5, 9.2.2 | [SonarQube 公告](https://community.sonarsource.com/t/sonarqube-sonarcloud-and-the-log4j-vulnerability/54721) |
| [storm](https://hub.docker.com/_/storm)    | 等待信息 | 等待信息 |

> [!NOTE]
>
> 尽管 [xwiki](https://hub.docker.com/_/xwiki) 镜像可能会被某些扫描器检测为易受攻击，但作者认为该镜像不受 Log4j 2 CVE 的威胁，因为 API jar 包不包含该漏洞。
> [Nuxeo](https://hub.docker.com/_/nuxeo) 镜像已弃用，将不再更新。
