---
title: 自定义 Dockerfile 语法
description: 深入了解 Dockerfile 前端，并学习如何使用自定义前端
keywords: build, buildkit, dockerfile, frontend, 前端, 语法
aliases:
  - /build/buildkit/dockerfile-frontend/
  - /build/dockerfile/frontend/
---

## Dockerfile 前端

BuildKit 支持从容器镜像动态加载前端。要使用外部 Dockerfile 前端，您的 [Dockerfile](/reference/dockerfile.md) 第一行需要设置 [`syntax` 指令](/reference/dockerfile.md#syntax)，指向您想要使用的特定镜像：

```dockerfile
# syntax=[远程镜像引用]
```

例如：

```dockerfile
# syntax=docker/dockerfile:1
# syntax=docker.io/docker/dockerfile:1
# syntax=example.com/user/repo:tag@sha256:abcdef...
```

您还可以使用预定义的 `BUILDKIT_SYNTAX` 构建参数在命令行设置前端镜像引用：

```console
$ docker build --build-arg BUILDKIT_SYNTAX=docker/dockerfile:1 .
```

这定义了用于构建该 Dockerfile 的语法定义所在的位置。BuildKit 后端允许无缝地使用外部实现，这些实现以 Docker 镜像的形式分发，并在容器沙箱环境中执行。

自定义 Dockerfile 实现允许您：

- 无需更新 Docker 守护进程即可自动获得 Bug 修复
- 确保所有用户都使用相同的实现来构建您的 Dockerfile
- 无需更新 Docker 守护进程即可使用最新特性
- 在新特性或第三方特性被集成进 Docker 守护进程之前提前试用
- 使用 [替代的构建定义，或创建您自己的定义](https://github.com/moby/buildkit#exploring-llb)
- 构建您自己的带有自定义特性的 Dockerfile 前端

> [!NOTE]
>
> 虽然 BuildKit 随附了内置的 Dockerfile 前端，但建议使用外部镜像，以确保所有用户在构建器上使用相同版本，并自动获取 Bug 修复，而无需等待新版本的 BuildKit 或 Docker Engine。

## 官方发布

Docker 在 Docker Hub 的 `docker/dockerfile` 存储库下发布可用于构建 Dockerfile 的官方版本镜像。有两个发布新镜像的频道：`stable` 和 `labs`。

### Stable（稳定）频道

`stable` 频道遵循 [语义化版本规范 (semantic versioning)](https://semver.org)。例如：

- `docker/dockerfile:1`：保持更新至最新的 `1.x.x` 次要版本 *及* 修订版本发布。
- `docker/dockerfile:1.2`：保持更新至最新的 `1.2.x` 修订版本发布，并在 `1.3.0` 版本发布后停止接收更新。
- `docker/dockerfile:1.2.1`：不可变：永不更新。

建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新稳定发布，并在版本 1 的发布周期内接收“次要”和“修订”更新。BuildKit 在执行构建时会自动检查语法的更新，确保您使用的是最新版本。

如果使用了特定版本，如 `1.2` 或 `1.2.1`，则需要手动更新 Dockerfile 才能继续接收 Bug 修复和新特性。旧版本的 Dockerfile 仍与新版本的构建器保持兼容。

### Labs（实验）频道

`labs` 频道提供了对 `stable` 频道中尚未提供的 Dockerfile 特性的早期访问。`labs` 镜像与稳定版同时发布，遵循相同的版本模式，但使用 `-labs` 后缀，例如：

- `docker/dockerfile:labs`：`labs` 频道的最新发布。
- `docker/dockerfile:1-labs`：与 `dockerfile:1` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2-labs`：与 `dockerfile:1.2` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2.1-labs`：不可变：永不更新。与 `dockerfile:1.2.1` 相同，但启用了实验性功能。

请选择最适合您需求的频道。如果您想从新特性中受益，请使用 `labs` 频道。`labs` 频道中的镜像包含 `stable` 频道中的所有特性，以及早期访问特性。`labs` 频道中的稳定特性遵循 [语义化版本规范](https://semver.org)，但早期访问特性则不遵循，且较新版本可能不向后兼容。请固定版本以避免受到重大变更 (breaking changes) 的影响。

## 其他资源

有关 `labs` 特性、master 分支构建以及每夜特性发布的文档，请参阅 [GitHub 上的 BuildKit 源码仓库](https://github.com/moby/buildkit/blob/master/README.md) 中的描述。欲查看可用镜像的完整列表，请访问 [Docker Hub 上的 `docker/dockerfile` 仓库](https://hub.docker.com/r/docker/dockerfile)；欲查看开发版构建，请访问 [Docker Hub 上的 `docker/dockerfile-upstream` 仓库](https://hub.docker.com/r/docker/dockerfile-upstream)。