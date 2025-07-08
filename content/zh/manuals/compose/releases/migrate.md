---
linkTitle: 迁移到 Compose v2
Title: 从 Docker Compose v1 迁移到 v2
weight: 20
description: 从 Compose v1 迁移到 v2 的分步指南，包括语法差异、环境处理和 CLI 变更。
keywords: migrate docker compose, upgrade docker compose v2, docker compose migration, docker compose v1 vs v2, docker compose CLI changes, docker-compose to docker compose, 迁移, 升级, 差异
aliases:
- /compose/compose-v2/
- /compose/cli-command-compatibility/
- /compose/migrate/
---

从 2023 年 7 月起，Compose v1 停止接收更新。它也不再包含在 Docker Desktop 的新版本中。

Compose v2 于 2020 年首次发布，包含在所有当前支持的 Docker Desktop 版本中。它提供了改进的 CLI 体验、通过 BuildKit 改进的构建性能以及持续的新功能开发。

## 如何切换到 Compose v2？

最简单且推荐的方法是确保您拥有最新版本的 [Docker Desktop](/manuals/desktop/release-notes.md)，它捆绑了包括 Compose v2 在内的 Docker Engine 和 Docker CLI 平台。

使用 Docker Desktop，Compose v2 始终可以通过 `docker compose` 访问。

对于 Linux 上的手动安装，您可以通过以下任一方式获取 Compose v2：
- [使用 Docker 的仓库](/manuals/compose/install/linux.md#install-using-the-repository) (推荐)
- [手动下载和安装](/manuals/compose/install/linux.md#install-the-plugin-manually)

## Compose v1 和 Compose v2 有什么区别？

### `docker-compose` vs `docker compose`

与 Compose v1 不同，Compose v2 集成到 Docker CLI 平台中，推荐的命令行语法是 `docker compose`。

Docker CLI 平台提供了一套一致且可预测的选项和标志，例如 `DOCKER_HOST` 环境变量或 `--context` 命令行标志。

这一更改使您可以在根 `docker` 命令上使用所有共享标志。
例如，`docker --log-level=debug --tls compose up` 可以从 Docker Engine 启用调试日志记录，并确保连接使用 TLS。

> [!TIP]
>
> 通过将连字符 (`-`) 替换为空格，使用 `docker compose` 而不是 `docker-compose` 来更新脚本以使用 Compose v2。

### 服务容器名称

Compose 根据项目名称、服务名称和扩展/副本计数生成容器名称。

在 Compose v1 中，下划线 (`_`) 用作单词分隔符。
在 Compose v2 中，连字符 (`-`) 用作单词分隔符。

下划线在 DNS 主机名中不是有效字符。
通过使用连字符，Compose v2 确保服务容器可以通��一致、可预测的主机名通过网络访问。
 
例如，运行 Compose 命令 `-p myproject up --scale=1 svc` 会在 Compose v1 中产生一个名为 `myproject_svc_1` 的容器，在 Compose v2 中产生一个名为 `myproject-svc-1` 的容器。

> [!TIP]
>
> 在 Compose v2 中，全局 `--compatibility` 标志或 `COMPOSE_COMPATIBILITY` 环境变量会保留 Compose v1 的行为，即使用下划线 (`_`) 作为单词分隔符。
由于每次运行 Compose v2 命令都必须指定此选项，因此建议您仅在过渡到 Compose v2 期间将其用作临时措施。

### 命令行标志和子命令

Compose v2 支持几乎所有的 Compose V1 标志和子命令，因此在大多数情况下，它可以作为脚本中的直接替代品。

#### v2 中不支持

以下内容在 Compose v1 中已弃用，在 Compose v2 中不受支持：
* `docker-compose scale`。请改用 `docker compose up --scale`。
* `docker-compose rm --all`

#### v2 中的不同之处

以下行为在 Compose v1 和 v2 之间有所不同：

|                         | Compose v1                                                       | Compose v2                                                                    |
|-------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `--compatibility`       | 已弃用。根据旧版模式版本迁移 YAML 字段。 | 使用 `_` 作为容器名称的单词分隔符，而不是 `-`，以匹配 v1。    |
| `ps --filter KEY-VALUE` | 未记录。允许按任意服务属性进行筛选。  | 仅允许按特定属性进行筛选，例如 `--filter=status=running`。 |

### 环境变量

Compose v1 中的环境变量行为没有正式记录，在某些边缘情况下表现不一致。

对于 Compose v2，[环境变量](/manuals/compose/how-tos/environment-variables/_index.md) 部分涵盖了[优先级](/manuals/compose/how-tos/environment-variables/envvars-precedence.md)和 [`.env` 文件插值](/manuals/compose/how-tos/environment-variables/variable-interpolation.md)，并包括许多涵盖棘手情况的示例，例如转义嵌套引号。

检查：
- 您的项目是否使用多级环境变量覆盖，例如 `.env` 文件和 `--env` CLI 标志。
- 任何 `.env` 文件值是否具有转义序列或嵌套引号。
- 任何 `.env` 文件值是否包含文字 `$` 符号。这在 PHP 项目中很常见。
- 任何变量值是否使用高级扩展语法，例如 `${VAR:?error}`。

> [!TIP]
>
> 在项目上运行 `docker compose config` 以在 Compose v2 执行插值后预览配置，以验证值是否按预期显示。
>
> 通常可以通过确保文字值（无插值）使用单引号，而应应用插值的值使用双引号来保持与 Compose v1 的向后兼容性。

## 这对我的使用 Compose v1 的项目意味着什么？

对于大多数项目，切换到 Compose v2 不需要对 Compose YAML 或您的开发工作流程进行任何更改。

建议您适应运行 Compose v2 的新首选方式，即使用 `docker compose` 而不是 `docker-compose`。
这提供了额外的灵活性，并消除了对 `docker-compose` 兼容性别名的要求。

但是，Docker Desktop 继续支持 `docker-compose` 别名，以将命令重定向到 `docker compose`，以方便并提高与第三方工具和脚本的兼容性。

## 在切换之前我还需要知道什么吗？

### 迁移正在运行的项目

在 v1 和 v2 中，在 Compose 项目上运行 `up` 会根据需要重新创建服务容器。它将 Docker Engine 中的实际状态与解析的项目配置进行比较，后者包括 Compose YAML、环境变量和命令行标志。

由于 Compose v1 和 v2 [对服务容器的命名方式不同](#service-container-names)，因此首次在最初由 v1 启动的正在运行服务的项目上使用 v2 运行 `up` 时，会导致服务容器以更新的名称重新创建。

请注意，即使使用 `--compatibility` 标志来保留 v1 命名样式，Compose 仍需要在 v2 首次运行 `up` 时重新创建最初由 v1 启动的服务容器，以迁移内部状态。

### 在 Docker-in-Docker 中使用 Compose v2

Compose v2 现在包含在 [Docker Hub 上的 Docker 官方镜像](https://hub.docker.com/_/docker)中。

此外，[Docker Hub 上的新 docker/compose-bin 镜像](https://hub.docker.com/r/docker/compose-bin)打包了最新版本的 Compose v2，可用于多阶段构建。

## 如果我愿意，我还可以使用 Compose v1 吗？

可以。您仍然可以下载和安装 Compose v1 软件包，但如果出现任何问题，您将无法获得 Docker 的支持。

>[!WARNING]
>
> 最终的 Compose v1 版本 1.29.2 发布于 2021 年 5 月 10 日。此后这些软件包未收到任何安全更新。使用风险自负。

## 其他资源

- [PyPI 上的 docker-compose v1](https://pypi.org/project/docker-compose/1.29.2/)
- [Docker Hub 上的 docker/compose v1](https://hub.docker.com/r/docker/compose)
- [GitHub 上的 docker-compose v1 源代码](https://github.com/docker/compose/releases/tag/1.29.2)
