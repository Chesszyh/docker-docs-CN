---
title: Wasm 工作负载 
weight: 90
description: 了解如何在 Docker Desktop 中运行 Wasm 工作负载
keywords: Docker, WebAssembly, wasm, containerd, engine
toc_max: 3
alias: 
- /desktop/wasm/
params:
  sidebar:
    badge:
      color: blue
      text: Beta
---

{{< summary-bar feature_name="Wasm 工作负载" >}}

WebAssembly (Wasm) 是 Linux 和 Windows 容器的一种快速、轻量级的替代方案。借助于 Docker Desktop，您现在可以让 Wasm 工作负载与传统容器并行运行。

本页提供了关于在 Docker 中运行 Wasm 应用程序及 Linux 容器能力的信息。

> [!TIP]
> 
> 欲了解更多关于 Wasm 用例和权衡的信息，请参阅 [Docker Wasm 技术预览博客文章](https://www.docker.com/blog/docker-wasm-technical-preview/)。

## 开启 Wasm 工作负载

Wasm 工作负载需要开启 [containerd 镜像库](containerd.md) 功能。如果您尚未开始使用 containerd 镜像库，那么预先存在的镜像和容器将无法访问。

1. 导航到 Docker Desktop 中的 **Settings**（设置）。
2. 在 **General**（常规）选项卡中，勾选 **Use containerd for pulling and storing images**。
3. 前往 **Features in development**（开发中的功能）并勾选 **Enable Wasm**（启用 Wasm）选项。
4. 选择 **Apply**（应用）以保存设置。
5. 在确认对话框中，选择 **Install**（安装）以安装 Wasm 运行时。

Docker Desktop 会下载并安装以下运行时： 
- `io.containerd.slight.v1`
- `io.containerd.spin.v2`
- `io.containerd.wasmedge.v1`
- `io.containerd.wasmtime.v1`
- `io.containerd.lunatic.v1`
- `io.containerd.wws.v1`
- `io.containerd.wasmer.v1`

## 使用示例

### 使用 `docker run` 运行 Wasm 应用程序

以下 `docker run` 命令将在您的系统上启动一个 Wasm 容器：

```console
$ docker run \
  --runtime=io.containerd.wasmedge.v1 \
  --platform=wasi/wasm \
  secondstate/rust-example-hello
```

运行此命令后，您可以访问 [http://localhost:8080/](http://localhost:8080/) 查看此示例模块输出的 "Hello world"。

如果您收到错误消息，请参阅 [故障排除部分](#故障排除) 以寻求帮助。

请注意此命令中使用的 `--runtime` 和 `--platform` 标志：

- `--runtime=io.containerd.wasmedge.v1`：告知 Docker 引擎您希望使用 Wasm containerd shim 而不是标准的 Linux 容器运行时。
- `--platform=wasi/wasm`：指定您要使用的镜像架构。通过利用 Wasm 架构，您无需为不同的机器架构构建单独的镜像。Wasm 运行时负责将 Wasm 二进制文件转换为机器指令的最后一步。

### 使用 Docker Compose 运行 Wasm 应用程序

可以使用以下 Docker Compose 文件运行相同的应用程序：

```yaml
services:
  app:
    image: secondstate/rust-example-hello
    platform: wasi/wasm
    runtime: io.containerd.wasmedge.v1
```

使用常规的 Docker Compose 命令启动应用程序：

   ```console
   $ docker compose up
   ```

### 使用 Wasm 运行多服务应用程序

网络的工作方式与您对 Linux 容器的预期相同，这为您提供了在单个应用程序栈中将 Wasm 应用程序与其他容器化工作负载（如数据库）相结合的灵活性。

在以下示例中，Wasm 应用程序利用了运行在容器中的 MariaDB 数据库。

1. 克隆仓库。

   ```console
   $ git clone https://github.com/second-state/microservice-rust-mysql.git
   Cloning into 'microservice-rust-mysql'...
   remote: Enumerating objects: 75, done.
   remote: Counting objects: 100% (75/75), done.
   remote: Compressing objects: 100% (42/42), done.
   remote: Total 75 (delta 29), reused 48 (delta 14), pack-reused 0
   Receiving objects: 100% (75/75), 19.09 KiB | 1.74 MiB/s, done.
   Resolving deltas: 100% (29/29), done.
   ```

2. 进入克隆的项目并使用 Docker Compose 启动项目。

   ```console
   $ cd microservice-rust-mysql
   $ docker compose up
   [+] Running 0/1
   ⠿ server Warning                                                                                                  0.4s
   [+] Building 4.8s (13/15)
   ...
   microservice-rust-mysql-db-1      | 2022-10-19 19:54:45 0 [Note] mariadbd: ready for connections.
   microservice-rust-mysql-db-1      | Version: '10.9.3-MariaDB-1:10.9.3+maria~ubu2204'  socket: '/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
   ```

   如果您从另一个终端窗口运行 `docker image ls`，可以在镜像库中看到 Wasm 镜像。

   ```console
   $ docker image ls
   REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
   server       latest    2c798ddecfa1   2 minutes ago   3MB
   ```

   检查该镜像会显示其具有 `wasi/wasm` 平台，即操作系统和架构的组合：

   ```console
   $ docker image inspect server | grep -A 3 "Architecture"
           "Architecture": "wasm",
           "Os": "wasi",
           "Size": 3001146,
           "VirtualSize": 3001146,
   ```

3. 在浏览器中打开 URL `http://localhost:8090` 并创建几个示例订单。所有这些操作都在与 Wasm 服务器进行交互。

4. 完成后，在启动应用程序的终端中按 `Ctrl+C` 停止所有内容。

### 构建并推送 Wasm 模块

1. 创建一个用于构建 Wasm 应用程序的 Dockerfile。

   具体操作方式取决于您使用的编程语言。

2. 在 `Dockerfile` 的一个单独阶段中，提取模块并将其设置为 `ENTRYPOINT`。

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM scratch
   COPY --from=build /build/hello_world.wasm /hello_world.wasm
   ENTRYPOINT [ "/hello_world.wasm" ]
   ```

3. 构建并推送镜像，指定 `wasi/wasm` 架构。Buildx 使得通过单条命令完成此操作变得非常容易。

   ```console
   $ docker buildx build --platform wasi/wasm -t username/hello-world .
   ...
   => exporting to image                                                                             0.0s
   => => exporting layers                                                                            0.0s
   => => exporting manifest sha256:2ca02b5be86607511da8dc688234a5a00ab4d58294ab9f6beaba48ab3ba8de56  0.0s
   => => exporting config sha256:a45b465c3b6760a1a9fd2eda9112bc7e3169c9722bf9e77cf8c20b37295f954b    0.0s
   => => naming to docker.io/username/hello-world:latest                                            0.0s
   => => unpacking to docker.io/username/hello-world:latest                                         0.0s
   $ docker push username/hello-world
   ```

## 故障排除

本节包含如何解决常见问题的说明。

### 指定了未知的运行时 (Unknown runtime specified)

如果您尝试在没有 [containerd 镜像库](./containerd.md) 的情况下运行 Wasm 容器，将显示类似以下的错误：

```text
docker: Error response from daemon: Unknown runtime specified io.containerd.wasmedge.v1.
```

在 Docker Desktop 设置中 [开启 containerd 功能](./containerd.md#启用-containerd-镜像库) 并重试。

### 启动 shim 失败：无法解析运行时路径 (Failed to start shim: failed to resolve runtime path)

如果您使用不支持运行 Wasm 工作负载的旧版 Docker Desktop，您将看到类似以下的错误消息：

```text
docker: Error response from daemon: failed to start shim: failed to resolve runtime path: runtime "io.containerd.wasmedge.v1" binary not installed "containerd-shim-wasmedge-v1": file does not exist: unknown.
```

将您的 Docker Desktop 更新到最新版本并重试。

## 已知问题

- Docker Compose 在中断时可能无法干净地退出。作为变通方法，请通过发送 SIGKILL (`killall -9 docker-compose`) 来清理 `docker-compose` 进程。
- 推送到 Docker Hub 时可能会提示 `server message: insufficient_scope: authorization failed` 错误，即使已经通过 Docker Desktop 登录。作为变通方法，请在 CLI 中运行 `docker login`。