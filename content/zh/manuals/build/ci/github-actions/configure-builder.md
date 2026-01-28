---
title: 配置您的 GitHub Actions 构建器
linkTitle: BuildKit configuration
description: 在使用 GitHub Actions 进行 CI 构建时配置 BuildKit 实例
keywords: ci, github actions, gha, buildkit, buildx
---

本页包含使用我们的 [Setup Buildx Action](https://github.com/docker/setup-buildx-action) 时配置 BuildKit 实例的说明。

## 版本固定

默认情况下，该 action 将尝试使用 GitHub Runner（构建客户端）上可用的最新版本 [Buildx](https://github.com/docker/buildx) 和最新版本的 [BuildKit](https://github.com/moby/buildkit)（构建服务器）。

要固定到特定版本的 Buildx，请使用 `version` 输入。例如，要固定到 Buildx v0.10.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    version: v0.10.0
```

要固定到特定版本的 BuildKit，请在 `driver-opts` 输入中使用 `image` 选项。例如，要固定到 BuildKit v0.11.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver-opts: image=moby/buildkit:v0.11.0
```

## BuildKit 容器日志

要在使用 `docker-container` 驱动程序时显示 BuildKit 容器日志，您必须[启用步骤调试日志](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging#enabling-step-debug-logging)，或在 [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action 中设置 `--debug` buildkitd 标志：

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

日志将在作业结束时可用：

![BuildKit 容器日志](images/buildkit-container-logs.png)

## BuildKit 守护进程配置

如果您使用的是 [`docker-container` 驱动程序](/manuals/build/builders/drivers/docker-container.md)（默认），您可以通过 `config` 或 `buildkitd-config-inline` 输入为构建器提供 [BuildKit 配置](../../buildkit/toml-configuration.md)：

### 镜像仓库镜像

您可以使用 `buildkitd-config-inline` 输入，通过工作流中的内联块直接配置镜像仓库镜像：

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

有关使用镜像仓库镜像的更多信息，请参阅[镜像仓库镜像](../../buildkit/configure.md#registry-mirror)。

### 最大并行度

您可以限制 BuildKit 求解器的并行度，这对于低功率机器特别有用。

您可以像前面的示例一样使用 `buildkitd-config-inline` 输入，或者如果您愿意，也可以使用仓库中的专用 BuildKit 配置文件，通过 `config` 输入：

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

## 向构建器追加额外节点

Buildx 支持在多台机器上运行构建。这对于在原生节点上构建[多平台镜像](../../building/multi-platform.md)非常有用，可以处理 QEMU 无法处理的更复杂情况。在原生节点上构建通常具有更好的性能，并允许您在多台机器之间分配构建任务。

您可以使用 `append` 选项向正在创建的构建器追加节点。它以 YAML 字符串文档的形式接受输入，以消除 GitHub Actions 固有的限制：您只能在输入字段中使用字符串：

| 名称              | 类型   | 描述                                                                                                                                                                                                                                                             |
| ----------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | String | [节点名称](/reference/cli/docker/buildx/create.md#node)。如果为空，则是其所属构建器的名称加上索引号后缀。如果您想在工作流的后续步骤中修改/删除节点，设置此值很有用。 |
| `endpoint`        | String | 要添加到构建器的节点的 [Docker 上下文或端点](/reference/cli/docker/buildx/create.md#description)                                                                                                                                      |
| `driver-opts`     | List   | 额外的[驱动程序特定选项](/reference/cli/docker/buildx/create.md#driver-opt)列表                                                                                                                                                         |
| `buildkitd-flags` | String | [buildkitd 守护进程标志](/reference/cli/docker/buildx/create.md#buildkitd-flags)                                                                                                                                                                    |
| `platforms`       | String | 节点的固定[平台](/reference/cli/docker/buildx/create.md#platform)。如果不为空，值优先于检测到的平台。                                                                                                             |

以下是使用 [`remote` 驱动程序](/manuals/build/builders/drivers/remote.md)和 [TLS 认证](#tls-authentication)的远程节点示例：

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

要能够使用 [`docker-container` 驱动程序](/manuals/build/builders/drivers/docker-container.md)连接到 SSH 端点，您必须在 GitHub Runner 上设置 SSH 私钥和配置：

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

您还可以使用 remote 驱动程序[设置远程 BuildKit 实例](/manuals/build/builders/drivers/remote.md#example-remote-buildkit-in-docker-container)。为了简化在工作流中的集成，您可以使用环境变量来设置使用 BuildKit 客户端证书进行 `tcp://` 的身份验证：

- `BUILDER_NODE_<idx>_AUTH_TLS_CACERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_CERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_KEY`

`<idx>` 占位符是节点在节点列表中的位置。

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

## 独立模式

如果您的 GitHub Runner 上没有安装 Docker CLI，Buildx 二进制文件会直接调用，而不是作为 Docker CLI 插件调用。如果您想在自托管运行器中使用 `kubernetes` 驱动程序，这可能很有用：

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

## 隔离的构建器

以下示例展示了如何为不同的作业选择不同的构建器。

这可能有用的一个场景是当您使用 monorepo，并且想要将不同的包指向特定的构建器。例如，某些包可能特别需要资源密集型的构建，需要更多计算能力。或者它们需要配备特定功能或硬件的构建器。

有关远程构建器的更多信息，请参阅 [`remote` 驱动程序](/manuals/build/builders/drivers/remote.md)和[追加构建器节点示例](#append-additional-nodes-to-the-builder)。

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
