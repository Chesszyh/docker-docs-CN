---
title: 安装 Docker Compose 独立版
linkTitle: 独立版
description: 在 Linux 和 Windows Server 上安装旧版 Docker Compose 独立工具的说明
keywords: install docker-compose, standalone docker compose, docker-compose windows server, install docker compose linux, legacy compose install
toc_max: 3
weight: 20
---

本页面包含如何从命令行在 Linux 或 Windows Server 上安装 Docker Compose 独立版的说明。

> [!WARNING]
>
> Docker Compose 独立版使用 `-compose` 语法而不是当前标准语法 `compose`。
> 例如，使用 Docker Compose 独立版时，您必须输入 `docker-compose up`，而不是 `docker compose up`。
> 仅在向后兼容时使用它。

## 在 Linux 上

1. 要下载并安装 Docker Compose 独立版，运行：

   ```console
   $ curl -SL https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
   ```

2. 为安装目标路径中的独立二进制文件应用可执行权限。

   ```console
   $ chmod +x /usr/local/bin/docker-compose
   ```

3. 使用 `docker-compose` 测试和执行 Docker Compose 命令。

> [!TIP]
>
> 如果安装后 `docker-compose` 命令失败，请检查您的路径。
> 您也可以创建一个到 `/usr/bin` 或您路径中任何其他目录的符号链接。
> 例如：
> ```console
> $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
> ```

## 在 Windows Server 上

如果您[直接在 Microsoft Windows Server 上运行 Docker 守护进程](/manuals/engine/install/binaries.md#install-server-and-client-binaries-on-windows)并想要安装 Docker Compose，请按照以下说明操作。

1.  以管理员身份运行 PowerShell。
    当询问您是否要允许此应用程序对您的设备进行更改时，选择**是**以继续安装。

2.  可选。确保 TLS1.2 已启用。
    GitHub 需要 TLS1.2 进行安全连接。如果您使用的是较旧版本的 Windows Server，例如 2016，或怀疑 TLS1.2 未启用，请在 PowerShell 中运行以下命令：

    ```powershell
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    ```

3. 下载最新版本的 Docker Compose（{{% param "compose_version" %}}）。运行以下命令：

    ```powershell
     Start-BitsTransfer -Source "https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-windows-x86_64.exe" -Destination $Env:ProgramFiles\Docker\docker-compose.exe
    ```

    要安装不同版本的 Docker Compose，将 `{{% param "compose_version" %}}` 替换为您想要使用的 Compose 版本。

    > [!NOTE]
    >
    > 在 Windows Server 2019 上，您可以将 Compose 可执行文件添加到 `$Env:ProgramFiles\Docker`。
     由于此目录已在系统 `PATH` 中注册，您可以在后续步骤中运行 `docker-compose --version` 命令，无需额外配置。

4.  测试安装。

    ```console
    $ docker-compose.exe version
    Docker Compose version {{% param "compose_version" %}}
    ```

## 下一步是什么？

- [了解 Compose 如何工作](/manuals/compose/intro/compose-application-model.md)
- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
