---
linkTitle: 迁移到 Compose v2
Title: 从 Docker Compose v1 迁移到 v2
weight: 20
description: 从 Compose v1 迁移到 v2 的逐步指南，包括语法差异、环境处理和 CLI 变更
keywords: 迁移 docker compose, 升级 docker compose v2, docker compose 迁移, docker compose v1 vs v2, docker compose CLI 变更, docker-compose 转 docker compose
---

自 2023 年 7 月起，Compose v1 已停止接收更新。它也不再出现在 Docker Desktop 的新版本中。

Compose v2 最初发布于 2020 年，包含在所有当前受支持的 Docker Desktop 版本中。它提供了改进的 CLI 体验、通过 BuildKit 提升了构建性能，并持续进行新功能开发。

## 如何切换到 Compose v2？

最简单且推荐的方法是确保您拥有最新版本的 [Docker Desktop](/manuals/desktop/release-notes.md)，它捆绑了 Docker Engine 和包含 Compose v2 在内的 Docker CLI 平台。

在 Docker Desktop 中，Compose v2 始终可以通过 `docker compose` 访问。

对于 Linux 上的手动安装，您可以通过以下方式获取 Compose v2：
- [使用 Docker 的仓库](/manuals/compose/install/linux.md#使用仓库进行安装)（推荐）
- [手动下载并安装](/manuals/compose/install/linux.md#手动安装插件)

## Compose v1 与 Compose v2 有哪些区别？

### `docker-compose` vs `docker compose`

与 Compose v1 不同，Compose v2 集成到了 Docker CLI 平台中，推荐的命令行语法是 `docker compose`。

Docker CLI 平台提供了一组一致且可预测的选项和标志，例如 `DOCKER_HOST` 环境变量或 `--context` 命令行标志。

此更改允许您使用根 `docker` 命令的所有共享标志。例如，`docker --log-level=debug --tls compose up` 可以启用 Docker Engine 的调试日志，并确保连接使用了 TLS。

> [!TIP]
>
> 通过将连字符 (`-`) 替换为空格，将脚本更新为使用 Compose v2，即使用 `docker compose` 代替 `docker-compose`。

### 服务容器名称

Compose 根据项目名称、服务名称和缩放/副本计数生成容器名称。

在 Compose v1 中，使用下划线 (`_`) 作为单词分隔符。
在 Compose v2 中，使用连字符 (`-`) 作为单词分隔符。

下划线在 DNS 主机名中不是有效字符。通过改用连字符，Compose v2 确保可以通过一致、可预测的主机名在网络上访问服务容器。
 
例如，运行 Compose 命令 `-p myproject up --scale=1 svc`，Compose v1 会生成名为 `myproject_svc_1` 的容器，而 Compose v2 会生成名为 `myproject-svc-1` 的容器。

> [!TIP]
>
> 在 Compose v2 中，全局标志 `--compatibility` 或环境变量 `COMPOSE_COMPATIBILITY` 会保留 Compose v1 的行为，即使用下划线 (`_`) 作为单词分隔符。由于此选项必须在每次运行 Compose v2 命令时指定，因此建议仅在向 Compose v2 过渡期间将其作为临时措施使用。

### 命令行标志和子命令

Compose v2 支持几乎所有的 Compose V1 标志和子命令，因此在大多数情况下，它可以在脚本中作为直接替换件使用。

#### v2 中不支持的功能

以下功能在 Compose v1 中已弃用，在 Compose v2 中不支持：
* `docker-compose scale`。请改用 `docker compose up --scale`。
* `docker-compose rm --all`

#### v2 中的差异

以下功能在 Compose v1 和 v2 之间表现不同：

|                         | Compose v1                                                       | Compose v2                                                                    |
|-------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `--compatibility`       | 已弃用。根据旧版 schema 版本迁移 YAML 字段。 | 使用 `_` 作为容器名称的单词分隔符而不是 `-` ，以匹配 v1 行为。    |
| `ps --filter KEY-VALUE` | 未记录。允许通过任意服务属性进行过滤。  | 仅允许通过特定属性进行过滤，例如 `--filter=status=running`。 |

### 环境变量

Compose v1 中的环境变量行为没有正式文档记录，并且在某些边缘情况下表现不一致。

对于 Compose v2，[环境变量](/manuals/compose/how-tos/environment-variables/_index.md) 章节涵盖了 [优先级](/manuals/compose/how-tos/environment-variables/envvars-precedence.md) 以及 [`.env` 文件插值](/manuals/compose/how-tos/environment-variables/variable-interpolation.md)，并包含许多涵盖棘手情况（如嵌套引号转义）的示例。

检查以下各项：
- 您的项目是否使用了多级环境变量覆盖，例如 `.env` 文件和 `--env` CLI 标志。
- 任何 `.env` 文件值是否包含转义序列或嵌套引号。
- 任何 `.env` 文件值是否包含字面量 `$` 符号。这在 PHP 项目中很常见。
- 任何变量值是否使用了高级扩展语法，例如 `${VAR:?error}`。

> [!TIP]
>
> 在项目上运行 `docker compose config` 以预览 Compose v2 执行插值后的配置，从而验证数值是否如预期。
>
> 通常，通过确保字面量值（无插值）使用单引号，而应应用插值的值使用双引号，可以实现与 Compose v1 的向后兼容性。

## 这对我的 Compose v1 项目意味着什么？

对于大多数项目，切换到 Compose v2 不需要对 Compose YAML 或您的开发工作流进行任何更改。

建议您适应运行 Compose v2 的新首选方式，即使用 `docker compose` 而不是 `docker-compose`。这提供了额外的灵活性，并消除了对 `docker-compose` 兼容类别名的需求。 

然而，为了方便起见以及提高与第三方工具和脚本的兼容性，Docker Desktop 继续支持 `docker-compose` 别名，将命令重定向到 `docker compose`。

## 在切换之前，我还需要了解什么？

### 迁移正在运行的项目

在 v1 和 v2 中，在 Compose 项目上运行 up 会根据需要重新创建服务容器。它会将 Docker Engine 中的实际状态与解析后的项目配置（包括 Compose YAML、环境变量和命令行标志）进行比较。

由于 Compose v1 和 v2 对 [服务容器的命名方式不同](#服务容器名称)，在原本由 v1 启动且服务正在运行的项目上第一次使用 v2 运行 `up` 时，会导致服务容器以更新后的名称重新创建。

请注意，即使使用了 `--compatibility` 标志来保留 v1 的命名风格，Compose 在第一次由 v2 运行 `up` 时仍需重新创建原本由 v1 启动的服务容器，以迁移内部状态。

### 在 Docker-in-Docker 中使用 Compose v2

Compose v2 现在已包含在 [Docker Hub 上的 Docker 官方镜像](https://hub.docker.com/_/docker)中。

此外，一个新的 [Docker Hub 上的 docker/compose-bin 镜像](https://hub.docker.com/r/docker/compose-bin) 打包了最新版本的 Compose v2，供多阶段构建使用。

## 如果我想的话，还能继续使用 Compose v1 吗？

可以。您仍然可以下载并安装 Compose v1 软件包，但如果出现任何问题，您将无法获得来自 Docker 的支持。

>[!WARNING]
>
> 最后的 Compose v1 版本 1.29.2 发布于 2021 年 5 月 10 日。自那时起，这些软件包尚未接收过任何安全更新。使用风险自负。 

## 其他资源

- [PyPI 上的 docker-compose v1](https://pypi.org/project/docker-compose/1.29.2/)
- [Docker Hub 上的 docker/compose v1](https://hub.docker.com/r/docker/compose)
- [GitHub 上的 docker-compose v1 源码](https://github.com/docker/compose/releases/tag/1.29.2)
