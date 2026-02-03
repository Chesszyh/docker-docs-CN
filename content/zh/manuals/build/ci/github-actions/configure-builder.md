---
title: 配置 GitHub Actions 构建器
linkTitle: BuildKit 配置
description: 配置用于 GitHub Actions CI 构建的 BuildKit 实例
keywords: ci, github actions, gha, buildkit, buildx, 配置
---

本页包含关于在使用我们的 [Setup Buildx Action](https://github.com/docker/setup-buildx-action) 时如何配置 BuildKit 实例的说明。

## 版本固定 (Version pinning)

默认情况下，该 Action 会尝试使用 GitHub 运行器（构建客户端）上可用的最新版本 [Buildx](https://github.com/docker/buildx) 和最新发布的 [BuildKit](https://github.com/moby/buildkit)（构建服务器）。

要固定特定版本的 Buildx，请使用 `version` 输入项。例如，固定到 Buildx v0.10.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    version: v0.10.0
```

要固定特定版本的 BuildKit，请在 `driver-opts` 输入项中使用 `image` 选项。例如，固定到 BuildKit v0.11.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver-opts: image=moby/buildkit:v0.11.0
```

## BuildKit 容器日志

在使用 `docker-container` 驱动程序时，要显示 BuildKit 容器日志，您必须 [开启步骤调试日志记录](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging#enabling-step-debug-logging)，或者在 [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) Action 中设置 `--debug` buildkitd 标志：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          buildkitd-flags: --debug
      
      - name: Build
        uses: docker/build-push-action@v6
```

日志将在任务结束时可用：

![BuildKit 容器日志](images/buildkit-container-logs.png)

## BuildKit 守护进程配置

如果您正在使用 [`docker-container` 驱动](/manuals/build/builders/drivers/docker-container.md)（默认），可以通过 `config` 或 `buildkitd-config-inline` 输入项为您的构建器提供 [BuildKit 配置](../../buildkit/toml-configuration.md)：

### 注册表镜像站 (Registry mirror)

您可以使用 `buildkitd-config-inline` 输入项，直接在工作流中通过内联块配置注册表镜像站：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          buildkitd-config-inline: |
            [registry."docker.io"]
              mirrors = ["mirror.gcr.io"]
```

有关使用注册表镜像站的更多信息，请参阅 [注册表镜像站](../../buildkit/configure.md#注册表镜像站)。

### 最大并行度 (Max parallelism)

您可以限制 BuildKit 求解器的并行度，这对于低性能机器特别有用。

您可以像前面的示例一样使用 `buildkitd-config-inline` 输入项，也可以根据需要使用 `config` 输入项引用存储库中专用的 BuildKit 配置文件：

```toml
# .github/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          config: .github/buildkitd.toml
```

## 为构建器追加额外节点

Buildx 支持在多台机器上运行构建。这对于在原生节点上构建 [多平台镜像](../../building/multi-platform.md) 非常有用，特别是一些 QEMU 无法处理的复杂案例。在原生节点上构建通常性能更好，并允许您跨多台机器分配构建任务。

您可以使用 `append` 选项为您创建的构建器追加节点。它以 YAML 字符串文档的形式接收输入，以避开 GitHub Actions 固有的限制（输入字段仅限使用字符串）：

| 名称 | 类型 | 说明 |
| ----------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | 字符串 | [节点名称](/reference/cli/docker/buildx/create.md#node)。如果为空，则使用其所属构建器的名称并加上索引数字后缀。如果您想在工作流的后续步骤中修改/移除节点，设置此项会很有用。 |
| `endpoint`        | 字符串 | 要添加到构建器的节点的 [Docker 上下文或端点](/reference/cli/docker/buildx/create.md#description)。 |
| `driver-opts`     | 列表 | 额外的 [驱动特定选项](/reference/cli/docker/buildx/create.md#driver-opt) 列表。 |
| `buildkitd-flags` | 字符串 | buildkitd 守护进程的 [标志 (Flags)](/reference/cli/docker/buildx/create.md#buildkitd-flags)。 |
| `platforms`       | 字符串 | 该节点的固定 [平台 (platforms)](/reference/cli/docker/buildx/create.md#platform)。如果不为空，则这些值优先级高于自动检测到的值。 |

以下是一个使用 [`remote` 驱动](/manuals/build/builders/drivers/remote.md) 和 [TLS 身份验证](#tls-身份验证) 的远程节点示例：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: remote
          endpoint: tcp://oneprovider:1234
          append: |
            - endpoint: tcp://graviton2:1234
              platforms: linux/arm64
            - endpoint: tcp://linuxone:1234
              platforms: linux/s390x
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.ONEPROVIDER_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.ONEPROVIDER_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.ONEPROVIDER_KEY }}
          BUILDER_NODE_1_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_1_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_1_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
          BUILDER_NODE_2_AUTH_TLS_CACERT: ${{ secrets.LINUXONE_CA }}
          BUILDER_NODE_2_AUTH_TLS_CERT: ${{ secrets.LINUXONE_CERT }}
          BUILDER_NODE_2_AUTH_TLS_KEY: ${{ secrets.LINUXONE_KEY }}
```

## 远程构建器的身份验证

以下示例展示了如何使用 SSH 或 TLS 处理远程构建器的身份验证。

### SSH 身份验证

为了能够使用 [`docker-container` 驱动](/manuals/build/builders/drivers/docker-container.md) 连接到 SSH 端点，您必须在 GitHub 运行器上设置 SSH 私钥和配置：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: graviton2
          private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          private-key-name: aws_graviton2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          endpoint: ssh://me@graviton2
```

### TLS 身份验证

您还可以使用远程驱动 [设置一个远程 BuildKit 实例](/manuals/build/builders/drivers/remote.md#示例在-docker-容器中运行远程-buildkit)。为了方便集成到您的工作流中，您可以使用环境变量为 `tcp://` 端点设置基于 BuildKit 客户端证书的身份验证：

- `BUILDER_NODE_<idx>_AUTH_TLS_CACERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_CERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_KEY`

`<idx>` 占位符是该节点在节点列表中的索引位置。

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: remote
          endpoint: tcp://graviton2:1234
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
```

## 独立模式 (Standalone mode)

如果 GitHub 运行器上没有安装 Docker CLI，Buildx 二进制文件将被直接调用，而不是作为 Docker CLI 插件调用。这在您想在自托管运行器中使用 `kubernetes` 驱动程序时非常有用：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: kubernetes
      
      - name: Build
        run: |
          buildx build .
```

## 隔离的构建器 (Isolated builders)

以下示例展示了如何为不同的任务选择不同的构建器。

这种做法的一个典型场景是当您使用单体仓库 (monorepo) 时，希望将不同的包指定给特定的构建器。例如，某些包的构建可能特别消耗资源，需要更多的计算能力；或者它们需要一个具备特定能力或硬件的构建器。

有关远程构建器的更多信息，请参阅 [`remote` 驱动](/manuals/build/builders/drivers/remote.md) 和 [追加构建器节点示例](#为构建器追加额外节点)。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up builder1
        uses: docker/setup-buildx-action@v3
        id: builder1
      
      - name: Set up builder2
        uses: docker/setup-buildx-action@v3
        id: builder2
      
      - name: Build against builder1
        uses: docker/build-push-action@v6
        with:
          builder: ${{ steps.builder1.outputs.name }}
          target: mytarget1
      
      - name: Build against builder2
        uses: docker/build-push-action@v6
        with:
          builder: ${{ steps.builder2.outputs.name }}
          target: mytarget2
```