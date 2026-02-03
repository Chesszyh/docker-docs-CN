---
title: BuildKit
weight: 100
description: BuildKit 简介与概览
keywords: build, buildkit, 构建
---

## 概览

[BuildKit](https://github.com/moby/buildkit) 是用于替代旧版构建器的改进版后端。自 23.0 版本起，BuildKit 已成为 Docker Desktop 和 Docker Engine 用户的默认构建器。

BuildKit 提供了新功能并提升了构建性能。它还引入了对处理更复杂场景的支持：

- 自动检测并跳过执行未使用的构建阶段
- 并行构建独立的构建阶段
- 在不同构建任务之间，增量传输 [构建上下文](../concepts/context.md) 中仅发生更改的文件
- 自动检测并跳过传输 [构建上下文](../concepts/context.md) 中未使用的文件
- 使用具有许多新特性的 [Dockerfile 前端 (Dockerfile frontend)](frontend.md) 实现
- 避免对 API 的其他部分产生副作用（如中间镜像和容器）
- 为自动清理功能优先考虑构建缓存

除了许多新特性外，BuildKit 主要在性能、存储管理和扩展性方面提升了现有体验。在性能方面，一个重大更新是全新的全并发构建图求解器 (build graph solver)。它可以在可能的情况下并行运行构建步骤，并优化掉对最终结果没有影响的命令。我们还优化了对本地源文件的访问。通过仅跟踪重复构建调用之间这些文件的更新，无需等待本地文件被读取或上传即可开始工作。

## LLB

BuildKit 的核心是 [低级构建 (Low-Level Build, LLB)](https://github.com/moby/buildkit#exploring-llb) 定义格式。LLB 是一种中间二进制格式，允许开发人员扩展 BuildKit。LLB 定义了一个内容寻址的依赖图，可用于组合非常复杂的构建定义。它还支持 Dockerfile 中未暴露的特性，如直接数据挂载和嵌套调用。

{{< figure src="../images/buildkit-dag.svg" class="invertible" >}}

关于构建执行和缓存的所有内容都在 LLB 中定义。与旧版构建器相比，其缓存模型被完全重写。LLB 不再使用启发式方法来比较镜像，而是直接跟踪构建图的校验和以及挂载到特定操作的内容。这使其更加快速、精确且具有可移植性。构建缓存甚至可以导出到注册表，并在任何主机上的后续调用中按需拉取。

LLB 可以直接使用 [Golang 客户端包](https://pkg.go.dev/github.com/moby/buildkit/client/llb) 生成，该包允许使用 Go 语言原语定义构建操作之间的关系。这为您运行任何想象得到的操作提供了十足的动力，但这可能不是大多数人定义其构建任务的方式。相反，大多数用户将使用前端组件或 LLB 嵌套调用来运行一组准备好的构建步骤。

## 前端 (Frontend)

前端是一个将人类可读的构建格式转换为 LLB 的组件，以便 BuildKit 执行。前端可以以镜像的形式分发，用户可以针对特定版本的前端，以确保其定义中使用的特性能够正常工作。

例如，要使用 BuildKit 构建 [Dockerfile](/reference/dockerfile.md)，您需要 [使用一个外部 Dockerfile 前端](frontend.md)。

## 入门指南

BuildKit 是 Docker Desktop 和 Docker Engine v23.0 及更高版本用户的默认构建器。

如果您安装了 Docker Desktop，则无需启用 BuildKit。如果您运行的 Docker Engine 版本早于 23.0，可以通过设置环境变量或在守护进程配置中将 BuildKit 设为默认值来启用它。

要在运行 `docker build` 命令时设置 BuildKit 环境变量，请运行：

```console
$ DOCKER_BUILDKIT=1 docker build . 
```

> [!NOTE]
> 
> Buildx 始终使用 BuildKit。

要默认使用 Docker BuildKit，请按如下方式编辑 `/etc/docker/daemon.json` 中的 Docker 守护进程配置，并重启守护进程。

```json
{
  "features": {
    "buildkit": true
  }
}
```

如果 `/etc/docker/daemon.json` 文件不存在，请创建一个名为 `daemon.json` 的新文件，添加上述内容，然后重启 Docker 守护进程。

## Windows 上的 BuildKit

> [!WARNING]
> 
> BuildKit 目前仅完全支持构建 Linux 容器。对 Windows 容器的支持仍处于实验阶段。

自 0.13 版本起，BuildKit 对 Windows 容器 (WCOW) 提供了实验性支持。本节将引导您完成试用步骤。欢迎通过 [在此开启 issue](https://github.com/moby/buildkit/issues/new) 向我们反馈，特别是关于 `buildkitd.exe` 的反馈。

### 已知限制

有关 Windows 上 BuildKit 相关的已知 Bug 和限制的信息，请参阅 [GitHub issues](https://github.com/moby/buildkit/issues?q=is%3Aissue%20state%3Aopen%20label%3Aarea%2Fwindows-wcow)。

### 前提条件

- 架构：`amd64`、`arm64`（二进制文件可用但尚未正式测试）。
- 支持的操作系统：Windows Server 2019、Windows Server 2022、Windows 11。
- 基础镜像：`ServerCore:ltsc2019`、`ServerCore:ltsc2022`、`NanoServer:ltsc2022`。参见 [此处的一致性列表](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility?tabs=windows-server-2019%2Cwindows-11#windows-server-host-os-compatibility)。
- Docker Desktop 4.29 或更高版本

### 操作步骤

> [!NOTE]
> 
> 以下命令要求在 PowerShell 终端中具有管理员（提升的）权限。

1. 启用 **Hyper-V** 和 **Containers** Windows 特性。

   ```console
   > Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V, Containers -All
   ```

   如果看到 `RestartNeeded` 为 `True`，请重启您的机器并重新以管理员身份打开 PowerShell 终端。否则，继续下一步。

2. 在 Docker Desktop 中切换到 Windows 容器模式。

   点击任务栏中的 Docker 图标，然后选择 **Switch to Windows containers...**。

3. 按照 [此处的安装说明](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#installing-containerd-on-windows) 安装 containerd 1.7.7 或更高版本。

4. 下载并解压最新的 BuildKit 发布版本。

   ```powershell
   $version = "v0.22.0" # 指定发布版本，需 v0.13+
   $arch = "amd64" # 也有 arm64 二进制文件
   curl.exe -LO https://github.com/moby/buildkit/releases/download/$version/buildkit-$version.windows-$arch.tar.gz
   # 如果之前按照 containerd 的说明存在另一个 `.\bin` 目录
   # 您可以将其移走
   mv bin bin2
   tar.exe xvf .\buildkit-$version.windows-$arch.tar.gz
   ## x bin/
   ## x bin/buildctl.exe
   ## x bin/buildkitd.exe
   ```

5. 将 BuildKit 二进制文件添加到 `PATH`。

   ```powershell
   # 将 bin 目录下的二进制文件解压后
   # 移动到您的 $Env:PATH 目录中的适当路径，或者执行：
   Copy-Item -Path ".\bin" -Destination "$Env:ProgramFiles\buildkit" -Recurse -Force
   # 将 `buildkitd.exe` 和 `buildctl.exe` 二进制文件添加到 $Env:PATH
   $Path = [Environment]::GetEnvironmentVariable("PATH", "Machine") + `
       [IO.Path]::PathSeparator + "$Env:ProgramFiles\buildkit"
   [Environment]::SetEnvironmentVariable( "Path", $Path, "Machine")
   $Env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + `
       [System.Environment]::GetEnvironmentVariable("Path","User")
   ```
6. 启动 BuildKit 守护进程。

   ```console
   > buildkitd.exe
   ```
   > [!NOTE]
   > 如果您正在运行由 _dockerd 管理_ 的 `containerd` 进程，请改用该进程并提供地址：
   > `buildkitd.exe --containerd-worker-addr "npipe:////./pipe/docker-containerd"`

7. 在另一个具有管理员权限的终端中，创建一个使用本地 BuildKit 守护进程的远程构建器。

   > [!NOTE]
   > 
   > 这要求使用 Docker Desktop 4.29 或更高版本。

   ```console
   > docker buildx create --name buildkit-exp --use --driver=remote npipe:////./pipe/buildkitd
   buildkit-exp
   ```

8. 通过运行 `docker buildx inspect` 验证构建器连接。

   ```console
   > docker buildx inspect
   ```

   输出应指示构建器平台为 Windows，且构建器的端点是一个命名管道。

   ```text
   Name:          buildkit-exp
    Driver:        remote
    Last Activity: 2024-04-15 17:51:58 +0000 UTC
    Nodes:
    Name:             buildkit-exp0
    Endpoint:         npipe:////./pipe/buildkitd
    Status:           running
    BuildKit version: v0.13.1
    Platforms:        windows/amd64
   ...
   ```

9. 创建一个 Dockerfile 并构建 `hello-buildkit` 镜像。

   ```console
   > mkdir sample_dockerfile
   > cd sample_dockerfile
   > Set-Content Dockerfile @"
   FROM mcr.microsoft.com/windows/nanoserver:ltsc2022
   USER ContainerAdministrator
   COPY hello.txt C:/
   RUN echo "Goodbye!" >> hello.txt
   CMD ["cmd", "/C", "type C:\\hello.txt"]
   "@
   Set-Content hello.txt @"
   Hello from BuildKit!
   This message shows that your installation appears to be working correctly.
   "@
   ```

10. 构建并将镜像推送到注册表。

    ```console
    > docker buildx build --push -t <用户名>/hello-buildkit .
    ```

11. 推送到注册表后，使用 `docker run` 运行镜像。

    ```console
    > docker run <用户名>/hello-buildkit
    ```