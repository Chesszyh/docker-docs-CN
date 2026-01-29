---
title: Docker Compose 发行说明
linkTitle: 发行说明
weight: 10
description: 了解最新 Docker Compose 版本的特性、Bug 修复和重大变更
keywords: 发行说明, compose
tags: [发行说明]
toc_max: 2
aliases:
- /release-notes/docker-compose/
- /compose/release-notes/
---

有关更详细的信息，请参阅 [Compose 仓库中的发行说明](https://github.com/docker/compose/releases/)。

## 2.38.1

{{< release-date date="2025-06-30" >}}

### Bug 修复和增强

- 为服务 `models` 配置增加了对 `model_variable` 的支持

### 更新

- 依赖升级：将 compose-go 提升至 v2.7.1

## 2.38.0

{{< release-date date="2025-06-30" >}}

### Bug 修复和增强

- 引入了对 LLM 配置的 `models` 支持
- 添加了 `volumes` 命令
- 移除了对绑定挂载的 `publish` 限制
- 修复了将 Docker 套接字挂载到不需要它的容器的问题
- 修复了 bake 在输出时挂起的问题

### 更新

- 依赖升级：将 compose-go 提升至 v2.7.0
- 依赖升级：将 docker engine 和 cli 提升至 v28.3.0

## 2.37.3

{{< release-date date="2025-06-24" >}}

### Bug 修复和增强

- 为 Bake 添加了对 `cache_to` 的支持
- 修复了 Bake 集成的问题
- 修复了影响 `run` 命令的多个问题

### 更新

- 依赖升级：将 buildkit 提升至 v0.23.1

## 2.37.2

{{< release-date date="2025-06-20" >}}

### Bug 修复和增强

- 引入 `use_api_socket`
- 修复了 `compose images` JSON 输出格式
- 修复了在没有 watch 支持的项目上使用 `w` 快捷键时的 panic
- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误

### 更新

- 依赖升级：将 compose-go 提升至 v2.6.5
- 依赖升级：将 buildx 提升至 v0.25.0
- 依赖升级：将 buildkit 提升至 v0.23.0

## 2.37.1

{{< release-date date="2025-06-12" >}}

### Bug 修复和增强

- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误
- 将 `compose images` JSON 输出恢复为数组格式

## 2.37.0

{{< release-date date="2025-06-05" >}}

### Bug 修复和增强

- 修复了随机端口分配的问题
- 修复了在内循环期间不需要时重新创建容器的问题
- 修复了 `up --build` 期间使用 `additional_context` 的问题

### 更新

- 依赖升级：将 compose-go 提升至 v2.6.4
- 依赖升级：将 buildx 提升至 v0.24.0
- 依赖升级：将 buildkit 提升至 v0.22.0

## 2.36.2

{{< release-date date="2025-05-23" >}}

### Bug 修复和增强

- Compose Bridge 功能现在成为 Compose 的一部分
- 改进了 `docker compose images` 命令的显示
- 将 `bake` 提升为 Compose 的默认构建工具
- 修复了围绕构建流程的问题
- 修复了 `watch` 重新构建镜像后依赖服务的重启问题

### 更新

- 依赖升级：将 docker engine 和 cli 提升至 v28.2.2

## 2.36.1

{{< release-date date="2025-05-19" >}}

### Bug 修复和增强

- 引入了对 `provider` 服务 `options` 属性中数组的支持
- 在扩展协议中添加了 `debug` 消息
- 修复了尝试发布带有 `provider` 服务的 Compose 应用程序时的问题
- 修复了带有 `service.provider` 的 Compose 应用程序的构建问题
- 为 `config` 命令引入了 `--lock-image-digests`

### 更新

- 依赖升级：将 compose-go 提升至 v2.6.3
- 依赖升级：将 containerd 提升至 2.1.0

## 2.36.0

{{< release-date date="2025-05-07" >}}

### Bug 修复和增强

- 引入了 `networks.interface_name`
- 增加了对 `COMPOSE_PROGRESS` 环境变量的支持
- 将 `service.provider` 添加到外部二进制文件
- 引入了构建 `--check` 标志
- 修复了解析 Compose 文件时的多个 panic 问题

### 更新

- 依赖升级：将 compose-go 提升至 v2.6.2
- 依赖升级：将 docker engine 和 cli 提升至 v28.1.0
- 依赖升级：将 containerd 提升至 2.0.5
- 依赖升级：将 buildkit 提升至 v0.21.1

## 2.35.1

{{< release-date date="2025-04-17" >}}

### Bug 修复和增强

- 修复了绑定挂载的一个问题

### 更新

- 依赖升级：将 compose-go 提升至 v2.6.0
- 依赖升级：将 docker engine 和 cli 提升至 v28.0.4
- 依赖升级：将 buildx 提升至 v0.22.0

## 2.35.0

{{< release-date date="2025-04-10" >}}

### Bug 修复和增强

- 增加了对 [Docker Model Runner](/manuals/ai/model-runner.md) 的支持，以便轻松将 AI 模型集成到您的 Compose 应用程序中
- 增加了 `build --print` 命令，通过显示等效的 bake 文件来帮助调试复杂的构建配置
- 增加了 `volume.type=image` ，为容器镜像提供更灵活的卷管理
- 为 `run` 命令增加了 `--quiet` 选项，以便在运行容器时获得更整洁的输出
- 增加了 `config --no-env-resolution` 选项，以查看不带环境变量替换的原始配置
- 修复了 `depends_on` 的行为，以防止在依赖项更改时重新创建不必要的容器
- 修复了使用 `include` 时由环境变量定义的 secret 的支持
- 修复了卷挂载处理，以确保绑定挂载在所有场景下都能正确工作

### 更新

- 依赖升级：将 docker engine 和 cli 提升至 v28.1.0
- 依赖升级：将 buildx 提升至 v0.23.0
- 依赖升级：将 buildkit 提升至 v0.21.0

## 2.34.0

{{< release-date date="2025-03-14" >}}

### Bug 修复和增强

- 增加了对刷新 `pull_policy` 值 `daily`、`weekly` 和 `every_<duration>` 的支持
- 在 `watch` 定义中引入了 `include` 属性以匹配文件模式
- 在 `docker compose run` 命令的标志中引入了 `--env-from-file`
- 将 `publish` 提升为 Compose 的常规命令
- 修复了一个 Bug，即在选择服务后才加载 `env_file`

### 更新

- 依赖升级：将 docker engine 和 cli 提升至 v28.0.1
- 依赖升级：将 buildkit 提升至 v0.17.1
- 依赖升级：将 compose-go 提升至 v2.4.9
- 依赖升级：将 buildx 提升至 v0.21.2

## 2.33.1

{{< release-date date="2025-02-21" >}}

### Bug 修复和增强

- 增加了对 `gw_priority`、`enable_ipv4` 的支持（需要 Docker v28.0）
- 修复了导航菜单的一个问题
- 改进了对只读服务使用非文件 secret/config 时的错误消息

### 更新

- 依赖升级：将 docker engine 和 cli 提升至 v28.0.0

## 2.33.0

{{< release-date date="2025-02-13" >}}

### Bug 修复和增强

- 引入了一个提示以促进 [Bake](/build/bake/) 的使用
- 引入了对引用另一个服务的 `additional_context` 属性的支持
- 增加了对 `BUILDKIT_PROGRESS` 的支持
- Compose 现在会在发布的 Compose 应用程序包含环境变量时向您发出警告
- 增加了 `--with-env` 标志以发布带有环境变量的 Compose 应用程序
- 更新了 `ls --quiet` 的帮助描述
- 修复了将构建委托给 Bake 时的多个问题
- 更新了 `stats` 命令中的帮助信息
- 修复了对 "builtin" seccomp 配置文件的支持
- 修复了多个服务的 `watch` 支持
- 移除了旧版指标系统使用的按错误类型的退出代码
- 修复了 `compatibility` 的测试覆盖率
- 移除了发送到 OpenTelemetry 的原始 os.Args
- 启用了 copyloopvar linter
- 修复了二进制文件的来源并生成 SBOM
- 现在使用 docs 上游验证的主分支
- 添加了 codeowners 文件
- 在测试矩阵中添加了 Docker Engine v28.x

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.8
- 依赖升级：将 buildx 提升至 v0.20.1
- 依赖升级：将 docker 提升至 v27.5.1
- 依赖升级：将 golangci-lint 提升至 v1.63.4
- 依赖升级：将 golang.org/x/sys 从 0.28.0 提升至 0.30.0
- 依赖升级：将 github.com/moby/term 提升至 v0.5.2
- 依赖升级：将 github.com/otiai10/copy 从 1.14.0 提升至 1.14.1
- 依赖升级：将 github.com/jonboulle/clockwork 从 0.4.0 提升至 0.5.0
- 依赖升级：将 github.com/spf13/pflag 从 1.0.5 提升至 1.0.6
- 依赖升级：将 golang.org/x/sync 从 0.10.0 提升至 0.11.0
- 依赖升级：将 gotest.tools/v3 从 3.5.1 提升至 3.5.2

## 2.32.4

{{< release-date date="2025-01-16" >}}

### Bug 修复和增强

- 修复了使用 `docker compose version` 时 Compose 版本无法正确显示的问题

## 2.32.3

{{< release-date date="2025-01-13" >}}

> [!NOTE]
>
> 来自 Compose GitHub 仓库的二进制文件可能无法正确显示版本号。如果您在开发或 CI 流程中依赖 `docker compose version` ，请升级到 Compose 2.32.4 版本。

### Bug 修复和增强

- 修复了 Compose 会用主网络 MAC 地址覆盖服务级 MAC 地址的问题
- 修复了并发构建期间的日志渲染问题

## 2.32.2

{{< release-date date="2025-01-07" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.7
- 依赖升级：将 golang 提升至 v1.22.10

### Bug 修复和增强

- 为 `docker compose run` 命令添加了 `--pull` 标志
- 修复了一个 Bug，即 `watch` 模式的 `restart` 操作无法监控绑定挂载
- 修复了使用匿名卷时重新创建容器的问题

## 2.32.1

{{< release-date date="2024-12-16" >}}

### Bug 修复和增强

- 修复了在不需要时重新创建容器的 Bug

## 2.32.0

{{< release-date date="2024-12-13" >}}

### 更新

- 依赖升级：将 docker + buildx 提升至最新版本
- 依赖升级：将 otel 依赖提升至 v1.28.0 和 v0.53.0
- 依赖升级：将 golang.org/x/sys 提升至 0.28.0
- 依赖升级：将 golang.org/x/crypto 提升至 0.31.0
- 依赖升级：将 google.golang.org/grpc 提升至 1.68.1
- 依赖升级：将 golang.org/x/sync 提升至 0.10.0
- 依赖升级：将 xx 提升至 v1.6.1

### Bug 修复和增强

- 改进了使用 [Bake](/manuals/build/bake.md) 构建时的支持
- 增加了 `restart` 和 `sync+exec` watch 操作
- 当卷或网络配置更改时，Compose 现在会重新创建容器
- 修复了对 `mac_address` 的支持
- 修复了 `pull --quiet` 以仅隐藏进度，而不隐藏全局状态
- 修复了一个问题，即现在仅 `rebuild` watch 操作需要构建声明
- 当通过 Compose 菜单启用时，Compose 现在会记录 `watch` 配置错误


## 2.31.0

{{< release-date date="2024-11-28" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.5
- 依赖升级：将 docker engine 和 cli 提升至 v27.4.0-rc.2
- 依赖升级：将 buildx 提升至 v0.18.0
- 依赖升级：将 buildkit 提升至 v0.17.1

### Bug 修复和增强

- 增加了使用 Docker Buildx Bake 构建 Docker Compose 服务的能力
- 增加了 `commit` 命令，从运行中的容器创建新镜像
- 修复了无法检测到网络更改的问题
- 修复了容器按顺序停止导致重启过程变慢的问题


## 2.30.3

{{< release-date date="2024-11-07" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.4

### Bug 修复和增强

- 修复了使用 `--watch` 时不应重启的服务却被重启的问题
- 改进了在 Compose 文件中多次使用同一个 YAML 锚点的修复方案


## 2.30.2

{{< release-date date="2024-11-05" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.3

### Bug 修复和增强

- 修复了在更新服务配置文件（profiles）时重新创建服务的问题
- 修复了在 Compose 文件中多次使用同一个 YAML 锚点时的回归问题

## 2.30.1

{{< release-date date="2024-10-30" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.2

### Bug 修复和增强

- 修复了使用 stdin 作为 `-f` 标志输入时的回归问题
- 修复了在 Compose 文件中多次使用同一个 YAML 锚点时的回归问题

## 2.30.0

{{< release-date date="2024-10-29" >}}

### 更新

- 依赖升级：将 compose-go 提升至 v2.4.1
- 依赖升级：将 docker engine 和 cli 提升至 v27.3.1

### Bug 修复和增强

- 引入了对服务钩子（service hooks）的支持。
- 增加了 alpha 版本的 `generate` 命令。
- 增加了 `export` 命令。
- 增加了对在 Compose 文件中使用 `devices` 的 CDI 设备请求支持。
- 进行了大量 Bug 修复。

... (此处省略历史版本)
