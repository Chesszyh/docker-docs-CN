---
title: 自定义 Dockerfile 语法
description: 深入了解 Dockerfile 前端，并学习自定义前端
keywords: build, buildkit, dockerfile, frontend
aliases:
  - /build/buildkit/dockerfile-frontend/
  - /build/dockerfile/frontend/
---

## Dockerfile 前端

BuildKit 支持从容器镜像动态加载前端。要使用
外部 Dockerfile 前端，您的 [Dockerfile](/reference/dockerfile.md) 的第一行
需要设置指向您要使用的特定镜像的 [`syntax` 指令](/reference/dockerfile.md#syntax)：

```dockerfile
# syntax=[remote image reference]
```

例如：

```dockerfile
# syntax=docker/dockerfile:1
# syntax=docker.io/docker/dockerfile:1
# syntax=example.com/user/repo:tag@sha256:abcdef...
```

您还可以使用预定义的 `BUILDKIT_SYNTAX` 构建参数在命令行上设置
前端镜像引用：

```console
$ docker build --build-arg BUILDKIT_SYNTAX=docker/dockerfile:1 .
```

这定义了用于构建 Dockerfile 的 Dockerfile 语法的位置。BuildKit 后端允许无缝使用作为 Docker 镜像分发并在容器沙箱环境中执行的外部
实现。

自定义 Dockerfile 实现允许您：

- 无需更新 Docker 守护进程即可自动获取错误修复
- 确保所有用户使用相同的实现来构建您的 Dockerfile
- 无需更新 Docker 守护进程即可使用最新功能
- 在第三方功能集成到 Docker 守护进程之前试用新功能或第三方功能
- 使用[替代构建定义，或创建您自己的](https://github.com/moby/buildkit#exploring-llb)
- 构建具有自定义功能的您自己的 Dockerfile 前端

> [!NOTE]
>
> BuildKit 附带内置的 Dockerfile 前端，但建议
> 使用外部镜像以确保构建器上的所有用户使用相同版本，
> 并无需等待 BuildKit 或 Docker Engine 的新版本即可自动获取错误修复。

## 官方发布

Docker 在 Docker Hub 的 `docker/dockerfile` 仓库下分发可用于构建
Dockerfile 的镜像的官方版本。有两个
发布新镜像的通道：`stable` 和 `labs`。

### Stable 通道

`stable` 通道遵循[语义版本控制](https://semver.org)。
例如：

- `docker/dockerfile:1` - 保持更新为最新的 `1.x.x` 次要版本 _和_ 补丁
  版本。
- `docker/dockerfile:1.2` - 保持更新为最新的 `1.2.x` 补丁版本，
  在 `1.3.0` 版本发布后停止接收更新。
- `docker/dockerfile:1.2.1` - 不可变：永不更新。

我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新
stable 版本，并在版本 1 发布周期内接收"次要"和"补丁"
更新。BuildKit 在执行构建时会自动检查
语法的更新，确保您使用最新版本。

如果使用特定版本，如 `1.2` 或 `1.2.1`，则需要手动更新 Dockerfile
以继续接收错误修复和新功能。旧
版本的 Dockerfile 与新版本的构建器保持兼容。

### Labs 通道

`labs` 通道提供对 `stable` 通道中尚不可用的 Dockerfile 功能的早期访问。`labs` 镜像与 stable 版本同时发布，
并遵循相同的版本模式，但使用 `-labs`
后缀，例如：

- `docker/dockerfile:labs` - `labs` 通道的最新版本。
- `docker/dockerfile:1-labs` - 与 `dockerfile:1` 相同，启用了实验性
  功能。
- `docker/dockerfile:1.2-labs` - 与 `dockerfile:1.2` 相同，启用了实验性
  功能。
- `docker/dockerfile:1.2.1-labs` - 不可变：永不更新。与
  `dockerfile:1.2.1` 相同，启用了实验性功能。

选择最适合您需求的通道。如果您想从
新功能中受益，请使用 `labs` 通道。`labs` 通道中的镜像包含
`stable` 通道中的所有功能，以及早期访问功能。
`labs` 通道中的 stable 功能遵循[语义版本控制](https://semver.org)，
但早期访问功能不遵循，较新的版本可能不向后
兼容。固定版本以避免处理破坏性更改。

## 其他资源

有关 `labs` 功能、master 构建和 nightly 功能
发布的文档，请参阅 [GitHub 上 BuildKit 源代码仓库](https://github.com/moby/buildkit/blob/master/README.md)中的描述。
有关可用镜像的完整列表，请访问 [Docker Hub 上的 `docker/dockerfile` 仓库](https://hub.docker.com/r/docker/dockerfile)，
以及 [Docker Hub 上的 `docker/dockerfile-upstream` 仓库](https://hub.docker.com/r/docker/dockerfile-upstream)
获取开发构建。
