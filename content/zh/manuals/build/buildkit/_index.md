---
title: BuildKit
weight: 100
description: BuildKit 简介和概览
keywords: build, buildkit
---

## 概览

[BuildKit](https://github.com/moby/buildkit) 是一个改进的后端，用于取代传统的构建器。从 23.0 版本开始，BuildKit 已成为 Docker Desktop 和 Docker Engine 用户的默认构建器。

BuildKit 提供了新功能并提高了构建性能。它还引入了对处理更复杂场景的支持：

- 检测并跳过执行未使用的构建阶段
- 并行构建相互独立的构建阶段
- 在构建之间仅增量传输 [构建上下文](../concepts/context.md) 中更改的文件
- 检测并跳过传输 [构建上下文](../concepts/context.md) 中未使用的文件
- 使用具有许多新功能的 [Dockerfile 前端](frontend.md) 实现
- 避免对其他 API 产生副作用（中间镜像和容器）
- 优先处理构建缓存以进行自动清理

除了许多新功能外，BuildKit 对当前体验的主要改进在于性能、存储管理和可扩展性。在性能方面，一项重大更新是全新的全并发构建图解算器。它可以在可能的情况下并行运行构建步骤，并优化掉对最终结果没有影响的命令。我们还优化了对本地源文件的访问。通过仅跟踪重复构建调用之间对这些文件所做的更新，在开始工作之前无需等待读取或上传本地文件。

## LLB

BuildKit 的核心是 [低级构建 (Low-Level Build, LLB)](https://github.com/moby/buildkit#exploring-llb) 定义格式。LLB 是一种中间二进制格式，允许开发人员扩展 BuildKit。LLB 定义了一个基于内容寻址的依赖图，可用于组合非常复杂的构建定义。它还支持 Dockerfile 中未暴露的功能，如直接数据挂载和嵌套调用。

{{< figure src="../images/buildkit-dag.svg" class="invertible" >}}

关于构建执行和缓存的所有内容都在 LLB 中定义。与传统构建器相比，其缓存模型已完全重写。LLB 不再使用启发式方法来比较镜像，而是直接跟踪构建图的校验和以及挂载到特定操作的内容。这使其速度更快、更精确且更具便携性。构建缓存甚至可以导出到镜像库，由任何主机上的后续调用按需拉取。

可以使用 [golang 客户端包](https://pkg.go.dev/github.com/moby/buildkit/client/llb) 直接生成 LLB，该包允许使用 Go 语言原语定义构建操作之间的关系。这为您提供了运行所能想象的任何事物的全部能力，但可能并不是大多数人定义构建方式。相反，大多数用户会使用前端组件或 LLB 嵌套调用来运行一组准备好的构建步骤。

## 前端 (Frontend)

前端是一个将人类可读的构建格式转换为 LLB 以便 BuildKit 执行的组件。前端可以作为镜像分发，用户可以针对特定版本的前端，以确保其定义中使用的功能可以正常工作。

例如，要使用 BuildKit 构建 [Dockerfile](/reference/dockerfile.md)，您需要 [使用外部 Dockerfile 前端](frontend.md)。

## 快速入门

对于 Docker Desktop 和 Docker Engine v23.0 及更高版本的用户，BuildKit 是默认构建器。

如果您安装了 Docker Desktop，则无需启用 BuildKit。如果您运行的是早于 23.0 的 Docker Engine 版本，则可以通过设置环境变量或在守护进程配置中将 BuildKit 设置为默认值来启用它。

要在运行 `docker build` 命令时设置 BuildKit 环境变量，请运行：

```console
$ DOCKER_BUILDKIT=1 docker build . 
```

> [!NOTE]
> 
> Buildx 始终使用 BuildKit。

要默认使用 Docker BuildKit，请按照以下方式编辑 `/etc/docker/daemon.json` 中的 Docker 守护进程配置，并重启守护进程。

```json
{
  "features": {
    "buildkit": true
  }
}
```

如果 `/etc/docker/daemon.json` 文件不存在，请创建一个名为 `daemon.json` 的新文件并添加以下内容。然后重启 Docker 守护进程。

## Windows 上的 BuildKit

> [!WARNING]
> 
> BuildKit 仅完全支持构建 Linux 容器。对 Windows 容器的支持是实验性的。

从 0.13 版本开始， BuildKit 对 Windows 容器 (WCOW) 提供实验性支持。本节将引导您完成试用步骤。我们感谢您通过 [在此处提交 issue](https://github.com/moby/buildkit/issues/new) 提供的任何反馈，尤其是关于 `buildkitd.exe` 的反馈。

### 已知限制

有关 Windows 上与 BuildKit 相关的已知 Bug 和限制的信息，请参阅 [GitHub issues](https://github.com/moby/buildkit/issues?q=is%3Aissue%20state%3Aopen%20label%3Aarea%2Fwindows-wcow)。

### 前提条件

- 架构：`amd64`、`arm64`（二进制文件可用，但尚未经过官方测试）。
- 支持的操作系统：Windows Server 2019、Windows Server 2022、Windows 11。
- 基础镜像：`ServerCore:ltsc2019`、`ServerCore:ltsc2022`、`NanoServer:ltsc2022`。请参阅 [此处的兼容性对照表](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility?tabs=windows-server-2019%2Cwindows-11#windows-server-host-os-compatibility)。
- Docker Desktop 4.29 或更高版本

### 步骤

> [!NOTE]
> 
> 以下命令需要在 PowerShell 终端中具备管理员（提权）权限。

1. 启用 **Hyper-V** 和 **Containers**（容器）Windows 功能。

   ```console
   > Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V, Containers -All
   ```

   如果您看到 `RestartNeeded` 为 `True`，请重启机器并重新以管理员身份打开 PowerShell 终端。否则，继续下一步。

2. 在 Docker Desktop 中切换到 Windows 容器。

   选择任务栏中的 Docker 图标，然后选择 **Switch to Windows containers...**。

3. 按照 [此处](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#installing-containerd-on-windows) 的安装说明安装 containerd 1.7.7 或更高版本。

4. 下载并解压最新的 BuildKit 发行版。

   ```powershell
   $version = "v0.22.0" # 指定发行版本，v0.13+
   $arch = "amd64" # 也有 arm64 二进制文件可用
   curl.exe -LO https://github.com/moby/buildkit/releases/download/$version/buildkit-$version.windows-$arch.tar.gz
   # containerd 指示中可能已有另一个 `.\bin` 目录
   # 您可以移动它们
   mv bin bin2
   tar.exe xvf .\buildkit-$version.windows-$arch.tar.gz
   ## x bin/
   ## x bin/buildctl.exe
   ## x bin/buildkitd.exe
   ```

5. 将 BuildKit 二进制文件安装到 `PATH`。

   ```powershell
   # 二进制文件解压到 bin 目录后
   # 将它们移动到 $Env:PATH 目录中的适当路径，或者：
   Copy-Item -Path ".\bin" -Destination "$Env:ProgramFiles\buildkit" -Recurse -Force
   # 将 `buildkitd.exe` 和 `buildctl.exe` 二进制文件添加到 $Env:PATH
   $Path = [Environment]::GetEnvironmentVariable("PATH", "Machine") + \
       [IO.Path]::PathSeparator + "$Env:ProgramFiles\buildkit"
   [Environment]::SetEnvironmentVariable( "Path", $Path, "Machine")
   $Env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + \
       [System.Environment]::GetEnvironmentVariable("Path","User")
   ```
6. 启动 BuildKit 守护进程。

   ```console
   > buildkitd.exe
   ```
   > [!NOTE]
   > 如果您正在运行由 _dockerd 管理的_ `containerd` 进程，请通过提供地址来使用它：
   > `buildkitd.exe --containerd-worker-addr "npipe:////./pipe/docker-containerd"`

7. 在另一个具备管理员权限的终端中，创建一个使用本地 BuildKit 守护进程的远程构建器。

   > [!NOTE]
   > 
   > 这需要 Docker Desktop 4.29 或更高版本。

   ```console
   > docker buildx create --name buildkit-exp --use --driver=remote npipe:////./pipe/buildkitd
   buildkit-exp
   ```

8. 通过运行 `docker buildx inspect` 验证构建器连接。

   ```console
   > docker buildx inspect
   ```

   输出应指示构建器平台为 Windows，且构建器的端点是一个命名管道（named pipe）。

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
   "
   ```

10. 构建镜像并将其推送到镜像库。

    ```console
    > docker buildx build --push -t <username>/hello-buildkit .
    ```

11. 推送到镜像库后，使用 `docker run` 运行该镜像。

    ```console
    > docker run <username>/hello-buildkit
    ```
