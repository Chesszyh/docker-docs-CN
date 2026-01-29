---
title: 自定义 Dockerfile 语法
description: 深入了解 Dockerfile 前端，并学习自定义前端
keywords: build, buildkit, dockerfile, 前端
---

## Dockerfile 前端

BuildKit 支持从容器镜像动态加载前端。要使用外部 Dockerfile 前端，您需要在 [Dockerfile](/reference/dockerfile.md) 的第一行设置 [`syntax` 指令](/reference/dockerfile.md#syntax)，指向您想要使用的特定镜像：

```dockerfile
# syntax=[remote image reference]
```

例如：

```dockerfile
# syntax=docker/dockerfile:1
# syntax=docker.io/docker/dockerfile:1
# syntax=example.com/user/repo:tag@sha256:abcdef...
```

您也可以使用预定义的 `BUILDKIT_SYNTAX` 构建参数在命令行上设置前端镜像引用：

```console
$ docker build --build-arg BUILDKIT_SYNTAX=docker/dockerfile:1 .
```

这定义了用于构建 Dockerfile 的语法位置。BuildKit 后端允许无缝使用以 Docker 镜像形式分发并在容器沙箱环境中执行的外部实现。

自定义 Dockerfile 实现允许您：

- 无需更新 Docker 守护进程即可自动获得 Bug 修复
- 确保所有用户都使用相同的实现来构建您的 Dockerfile
- 无需更新 Docker 守护进程即可使用最新功能
- 在新功能或第三方功能集成到 Docker 守护进程之前进行试用
- 使用 [替代构建定义，或创建您自己的定义](https://github.com/moby/buildkit#exploring-llb)
- 构建具有自定义功能的您自己的 Dockerfile 前端

> [!NOTE]
>
> BuildKit 附带了一个内置的 Dockerfile 前端，但建议使用外部镜像，以确保所有用户在构建器上使用相同的版本，并自动获取 Bug 修复，而无需等待 BuildKit 或 Docker Engine 的新版本。

## 官方发行版

Docker 在 Docker Hub 的 `docker/dockerfile` 仓库下发布了可用于构建 Dockerfile 的官方镜像版本。新镜像发布有两个频道：`stable`（稳定版）和 `labs`（实验版）。

### 稳定版频道 (Stable channel)

`stable` 频道遵循 [语义化版本控制 (semantic versioning)](https://semver.org)。例如：

- `docker/dockerfile:1` - 保持更新最新的 `1.x.x` 次要版本 *和* 补丁版本。
- `docker/dockerfile:1.2` - 保持更新最新的 `1.2.x` 补丁版本，一旦 `1.3.0` 版本发布即停止接收更新。
- `docker/dockerfile:1.2.1` - 不可变：永不更新。

我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新稳定发行版，并在版本 1 发行周期内接收“次要”和“补丁”更新。BuildKit 在执行构建时会自动检查语法更新，确保您使用的是最新版本。

如果使用特定版本（如 `1.2` 或 `1.2.1`），则需要手动更新 Dockerfile 才能继续接收 Bug 修复和新功能。旧版本的 Dockerfile 仍然与新版本的构建器兼容。

### Labs 频道

`labs` 频道提供了对 `stable` 频道中尚未提供的 Dockerfile 功能的早期访问。`labs` 镜像与稳定版同时发布，并遵循相同的版本模式，但使用 `-labs` 后缀，例如：

- `docker/dockerfile:labs` - `labs` 频道的最新发行版。
- `docker/dockerfile:1-labs` - 与 `dockerfile:1` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2-labs` - 与 `dockerfile:1.2` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2.1-labs` - 不可变：永不更新。与 `dockerfile:1.2.1` 相同，但启用了实验性功能。

选择最适合您需求的频道。如果您想从新功能中获益，请使用 `labs` 频道。`labs` 频道中的镜像包含 `stable` 频道中的所有功能，外加早期访问功能。`labs` 频道中的稳定功能遵循 [语义化版本控制](https://semver.org)，但早期访问功能不遵循，且较新的版本可能不向后兼容。请固定版本以避免处理破坏性变更。

## 其他资源

有关 `labs` 功能、master 构建和每夜功能发布的文档，请参阅 [GitHub 上的 BuildKit 源码库](https://github.com/moby/buildkit/blob/master/README.md) 中的描述。有关可用镜像的完整列表，请访问 Docker Hub 上的 [`docker/dockerfile` 仓库](https://hub.docker.com/r/docker/dockerfile)，以及用于开发构建的 [`docker/dockerfile-upstream` 仓库](https://hub.docker.com/r/docker/dockerfile-upstream)。
