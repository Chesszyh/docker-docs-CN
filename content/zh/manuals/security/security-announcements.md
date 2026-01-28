---
description: Docker 安全公告
keywords: Docker, CVEs, security, notice, Log4J 2, Log4Shell, Text4Shell, announcements
title: Docker 安全公告
linkTitle: 安全公告
toc_min: 1
toc_max: 2
---

## Docker Desktop 4.43.0 安全更新：CVE-2025-6587

_最后更新于 2025 年 7 月 3 日_

Docker Desktop 中的一个漏洞已于 7 月 3 日在 [4.43.0](/manuals/desktop/release-notes.md#4430) 版本中修复：

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，该漏洞导致敏感系统环境变量被包含在 Docker Desktop 诊断日志中，可能导致密钥泄露。

## Docker Desktop 4.41.0 安全更新：CVE-2025-3224、CVE-2025-4095 和 CVE-2025-3911

_最后更新于 2025 年 5 月 15 日_

Docker Desktop 中的三个漏洞已于 4 月 28 日在 [4.41.0](/manuals/desktop/release-notes.md#4410) 版本中修复。

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224)，该漏洞允许能够访问用户计算机的攻击者在 Docker Desktop 更新时执行权限提升。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095)，该漏洞导致在使用 MacOS 配置文件时 Registry Access Management (RAM) 策略未被强制执行，允许用户从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911)，该漏洞允许对用户计算机具有读取权限的攻击者从 Docker Desktop 日志文件中获取敏感信息，包括为运行中容器配置的环境变量。

我们强烈建议您更新到 Docker Desktop [4.41.0](/manuals/desktop/release-notes.md#4410)。

## Docker Desktop 4.34.2 安全更新：CVE-2024-8695 和 CVE-2024-8696

_最后更新于 2024 年 9 月 13 日_

[Cure53](https://cure53.de/) 报告了 Docker Desktop 中与 Docker Extensions 相关的两个远程代码执行 (RCE) 漏洞，这些漏洞已于 9 月 12 日在 [4.34.2](/manuals/desktop/release-notes.md#4342) 版本中修复。

- [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)：在 Docker Desktop 4.34.2 之前的版本中，通过精心构造的扩展描述/变更日志可能导致远程代码执行 (RCE) 漏洞，可被恶意扩展利用。[严重]
- [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)：在 Docker Desktop 4.34.2 之前的版本中，通过精心构造的扩展 publisher-url/additional-urls 可能导致远程代码执行 (RCE) 漏洞，可被恶意扩展利用。[高危]

在 Extensions Marketplace 中未发现利用这些漏洞的现有扩展。Docker 团队将密切监控并认真审查任何发布新扩展的请求。

我们强烈建议您更新到 Docker Desktop [4.34.2](/manuals/desktop/release-notes.md#4342)。如果您无法及时更新，可以[禁用 Docker Extensions](/manuals/extensions/settings-feedback.md#turn-on-or-turn-off-extensions) 作为临时解决方案。

## 强制 SSO 时弃用 CLI 密码登录

_最后更新于 2024 年 7 月_

当 [SSO 强制执行](/manuals/security/for-admins/single-sign-on/connect.md) 首次引入时，Docker 提供了一个宽限期，允许在通过 Docker CLI 认证到 Docker Hub 时继续使用密码。这样做是为了让组织更容易使用 SSO 强制执行。建议配置 SSO 的管理员鼓励使用 CLI 的用户[切换到个人访问令牌](/security/for-admins/single-sign-on/#prerequisites)，以便在宽限期结束之前做好准备。

2024 年 9 月 16 日，宽限期将结束，在强制执行 SSO 时，密码将无法再通过 Docker CLI 认证到 Docker Hub。受影响的用户必须切换到使用 PAT 才能继续登录。

在 Docker，我们希望为开发人员和组织提供最安全的体验，这次弃用是朝着这个方向迈出的重要一步。

## SOC 2 Type 2 认证和 ISO 27001 认证

_最后更新于 2024 年 6 月_

Docker 很高兴地宣布，我们已获得 SOC 2 Type 2 认证和 ISO 27001 认证，且没有例外或重大不符合项。

安全是 Docker 运营的基本支柱，这已融入到我们的整体使命和公司战略中。Docker 的产品是我们用户社区的核心，我们的 SOC 2 Type 2 认证和 ISO 27001 认证证明了 Docker 对用户群安全的持续承诺。

如需更多信息，请参阅[博客公告](https://www.docker.com/blog/docker-announces-soc-2-type-2-attestation-iso-27001-certification/)。

## Docker 安全公告：runc、BuildKit 和 Moby 中的多个漏洞

_最后更新于 2024 年 2 月 2 日_

在 Docker，我们优先考虑软件的安全性和完整性以及用户的信任。Snyk Labs 的安全研究人员在容器生态系统中识别并报告了四个安全漏洞。其中一个漏洞 [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) 涉及 runc 容器运行时，另外三个影响 BuildKit（[CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)）。我们向社区保证，我们的团队与报告者和开源维护者合作，一直在努力协调和实施必要的修复措施。

我们致力于维护最高的安全标准。我们已于 1 月 31 日发布了 runc、BuildKit 和 Moby 的补丁版本，并于 2 月 1 日发布了 Docker Desktop 更新以解决这些漏洞。此外，我们最新的 BuildKit 和 Moby 版本还包含了对 [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) 和 [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) 的修复，这两个漏洞分别由独立研究人员和 Docker 内部研究团队发现。

|                        | 受影响版本         |
|:-----------------------|:--------------------------|
| `runc`                 | <= 1.1.11                 |
| `BuildKit`             | <= 0.12.4                 |
| `Moby (Docker Engine)` | <= 25.0.1 and <= 24.0.8   |
| `Docker Desktop`       | <= 4.27.0                 |

### 如果我使用的是受影响的版本，我应该怎么做？

如果您正在使用受影响版本的 runc、BuildKit、Moby 或 Docker Desktop，请确保更新到以下表格中链接的最新版本：

|                        | 已修补版本          |
|:-----------------------|:--------------------------|
| `runc`                 | >= [1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)                 |
| `BuildKit`             | >= [0.12.5](https://github.com/moby/buildkit/releases/tag/v0.12.5)                 |
| `Moby (Docker Engine)` | >= [25.0.2](https://github.com/moby/moby/releases/tag/v25.0.2) and >= [24.0.9](https://github.com/moby/moby/releases/tag/v24.0.9)   |
| `Docker Desktop`       | >= [4.27.1](/manuals/desktop/release-notes.md#4271)                 |


如果您无法及时更新到不受影响的版本，请遵循以下最佳实践以降低风险：

* 仅使用受信任的 Docker 镜像（例如 [Docker Official Images](../docker-hub/image-library/trusted-content.md#docker-official-images)）。
* 不要从不受信任的来源或不受信任的 Dockerfile 构建 Docker 镜像。
* 如果您是使用 Docker Desktop 的 Docker Business 客户且无法更新到 v4.27.1，请确保启用 [Hardened Docker Desktop](/manuals/security/for-admins/hardened-desktop/_index.md) 功能，例如：
  * [Enhanced Container Isolation](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)（增强容器隔离），可在从恶意镜像运行容器时减轻 CVE-2024-21626 的影响。
  * [Image Access Management](for-admins/hardened-desktop/image-access-management.md)（镜像访问管理）和 [Registry Access Management](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)（注册表访问管理），可让组织控制其用户可以访问哪些镜像和仓库。
* 对于 CVE-2024-23650、CVE-2024-23651、CVE-2024-23652 和 CVE-2024-23653，避免使用来自不受信任来源的 BuildKit 前端。前端镜像通常在 Dockerfile 的 #syntax 行中指定，或者在使用 `buildctl build` 命令时通过 `--frontend` 标志指定。
* 为了缓解 CVE-2024-24557，请确保使用 BuildKit 或在构建镜像时禁用缓存。从 CLI 可以通过 `DOCKER_BUILDKIT=1` 环境变量（对于安装了 buildx 插件的 Moby >= v23.0 是默认值）或 `--no-cache` 标志来实现。如果您直接或通过客户端使用 HTTP API，可以通过为 [/build API 端点](https://docs.docker.com/reference/api/engine/version/v1.44/#tag/Image/operation/ImageBuild) 将 `nocache` 设置为 `true` 或将 `version` 设置为 `2` 来实现相同效果。

### 技术细节和影响

#### CVE-2024-21626（高危）

在 runc v1.1.11 及更早版本中，由于某些文件描述符泄漏，攻击者可以通过使新生成的容器进程（来自 `runc exec`）的工作目录位于主机文件系统命名空间中来获取对主机文件系统的访问权限，或者通过诱骗用户运行恶意镜像并允许容器进程通过 `runc run` 获取对主机文件系统的访问权限。攻击还可以被改造为覆盖半任意的主机二进制文件，从而实现完全的容器逃逸。请注意，在使用更高级别的运行时（如 Docker 或 Kubernetes）时，此漏洞可以通过运行恶意容器镜像而无需额外配置来利用，或者在启动容器时通过传递特定的 workdir 选项来利用。在 Docker 的情况下，该漏洞也可以从 Dockerfile 中被利用。

_该问题已在 runc v1.1.12 中修复。_

#### CVE-2024-23651（高危）

在 BuildKit <= v0.12.4 中，两个共享相同带有子路径的缓存挂载的恶意构建步骤并行运行时可能导致竞争条件，从而使主机系统的文件可被构建容器访问。这仅在用户尝试构建恶意项目的 Dockerfile 时才会发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23652（高危）

在 BuildKit <= v0.12.4 中，恶意的 BuildKit 前端或使用 `RUN --mount` 的 Dockerfile 可能会欺骗用于删除为挂载点创建的空文件的功能，使其删除容器外部的主机系统文件。这仅在用户使用恶意 Dockerfile 时才会发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23653（高危）

除了将容器作为构建步骤运行外，BuildKit 还提供用于基于构建镜像运行交互式容器的 API。在 BuildKit <= v0.12.4 中，可以使用这些 API 请求 BuildKit 以提升的权限运行容器。通常，只有在 buildkitd 配置中启用了特殊的 `security.insecure` 授权且用户初始化构建请求时允许的情况下，才允许运行此类容器。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23650（中危）

在 BuildKit <= v0.12.4 中，恶意的 BuildKit 客户端或前端可能构造一个请求，导致 BuildKit 守护进程崩溃并出现 panic。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-24557（中危）

在 Moby <= v25.0.1 和 <= v24.0.8 中，如果镜像是 FROM scratch 构建的，传统构建器缓存系统容易受到缓存投毒攻击。此外，对某些指令的更改（最重要的是 `HEALTHCHECK` 和 `ONBUILD`）不会导致缓存未命中。了解某人正在使用的 Dockerfile 的攻击者可以通过让他们拉取一个特制的镜像来投毒他们的缓存，该镜像将被视为某些构建步骤的有效缓存候选。

_该问题已在 Moby >= v25.0.2 和 >= v24.0.9 中修复。_

### Docker 产品如何受到影响？

#### Docker Desktop

Docker Desktop v4.27.0 及更早版本受到影响。Docker Desktop v4.27.1 于 2 月 1 日发布，包含 runc、BuildKit 和 dockerd 二进制文件的补丁。除了更新到此新版本外，我们鼓励所有 Docker 用户谨慎使用 Docker 镜像和 Dockerfile，并确保在构建中仅使用受信任的内容。

一如既往，在更新之前，您应该检查您的操作系统的 Docker Desktop 系统要求（[Windows](/manuals/desktop/setup/install/windows-install.md#system-requirements)、[Linux](/manuals/desktop/setup/install/linux/_index.md#general-system-requirements)、[Mac](/manuals/desktop/setup/install/mac-install.md#system-requirements)）以确保完全兼容。

#### Docker Build Cloud

任何新的 Docker Build Cloud 构建器实例都将配置最新的 Docker Engine 和 BuildKit 版本，因此不会受到这些 CVE 的影响。现有的 Docker Build Cloud 构建器也已推出更新。

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

[CVE-2022-42889](https://nvd.nist.gov/vuln/detail/CVE-2022-42889) 已在流行的 Apache Commons Text 库中被发现。1.10.0 之前的此库版本受到此漏洞的影响。

我们强烈建议您更新到 [Apache Commons Text](https://commons.apache.org/proper/commons-text/download_text.cgi) 的最新版本。

### 在 Docker Hub 上扫描镜像

2021 年 10 月 21 日 1200 UTC 之后触发的 Docker Hub 安全扫描现在可以正确识别 Text4Shell CVE。此日期之前的扫描当前不反映此漏洞的状态。因此，我们建议您通过将新镜像推送到 Docker Hub 来触发扫描，以在漏洞报告中查看 Text4Shell CVE 的状态。有关详细说明，请参阅[在 Docker Hub 上扫描镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

### 受 CVE-2022-42889 影响的 Docker 官方镜像

多个 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 包含易受攻击版本的 Apache Commons Text。以下列出了可能包含易受攻击版本的 Apache Commons Text 的 Docker 官方镜像：

- [bonita](https://hub.docker.com/_/bonita)
- [Couchbase](https://hub.docker.com/_/couchbase)
- [Geonetwork](https://hub.docker.com/_/geonetwork)
- [neo4j](https://hub.docker.com/_/neo4j)
- [sliverpeas](https://hub.docker.com/_/sliverpeas)
- [solr](https://hub.docker.com/_/solr)
- [xwiki](https://hub.docker.com/_/xwiki)

我们已将这些镜像中的 Apache Commons Text 更新到最新版本。由于其他原因，其中一些镜像可能不受攻击。我们建议您也查看上游网站上发布的指南。

## Log4j 2 CVE-2021-44228

_最后更新于 2021 年 12 月_

[Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 是在 Log4j 2（一个非常常见的 Java 日志库）中发现的漏洞，允许远程代码执行，通常从攻击者容易获得的上下文中进行。例如，它在 Minecraft 服务器中被发现，允许将命令输入到聊天日志中，然后这些命令被发送到日志记录器。这使其成为一个非常严重的漏洞，因为该日志库使用如此广泛，而且利用起来可能很简单。许多开源维护者正在努力修复和更新软件生态系统。

Log4j 2 的易受攻击版本是 2.0 到 2.14.1（含）版本。第一个修复版本是 2.15.0。我们强烈建议您尽可能更新到[最新版本](https://logging.apache.org/log4j/2.x/download.html)。如果您使用的是 2.0 之前的版本，您也不会受到影响。

如果您使用的是这些版本，您可能不会受到影响，因为您的配置可能已经缓解了这一点，或者您记录的内容可能不包含任何用户输入。然而，如果不详细了解所有可能记录日志的代码路径以及它们可能从哪里获取输入，这可能很难验证。因此，您可能会希望升级所有使用易受攻击版本的代码。

> CVE-2021-45046
>
> 作为 [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 的更新，2.15.0 版本中的修复是不完整的。已识别出其他问题，并通过 [CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046) 和 [CVE-2021-45105](https://nvd.nist.gov/vuln/detail/CVE-2021-45105) 进行跟踪。为了更完整地修复此漏洞，我们建议在可能的情况下更新到 2.17.0。

### 在 Docker Hub 上扫描镜像

2021 年 12 月 13 日 1700 UTC 之后触发的 Docker Hub 安全扫描现在可以正确识别 Log4j 2 CVE。此日期之前的扫描当前不反映此漏洞的状态。因此，我们建议您通过将新镜像推送到 Docker Hub 来触发扫描，以在漏洞报告中查看 Log4j 2 CVE 的状态。有关详细说明，请参阅[在 Docker Hub 上扫描镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

## 受 Log4j 2 CVE 影响的 Docker 官方镜像

_最后更新于 2021 年 12 月_

多个 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 包含易受攻击版本的 Log4j 2 CVE-2021-44228。下表列出了可能包含易受攻击版本的 Log4j 2 的 Docker 官方镜像。我们已将这些镜像中的 Log4j 2 更新到最新版本。由于其他原因，其中一些镜像可能不受攻击。我们建议您也查看上游网站上发布的指南。

| 仓库                | 已修补版本         | 额外文档       |
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
> 虽然 [xwiki](https://hub.docker.com/_/xwiki) 镜像可能被某些扫描器检测为易受攻击，但作者认为这些镜像不受 Log4j 2 CVE 影响，因为 API jar 不包含该漏洞。
> [Nuxeo](https://hub.docker.com/_/nuxeo) 镜像已被弃用，将不会更新。
