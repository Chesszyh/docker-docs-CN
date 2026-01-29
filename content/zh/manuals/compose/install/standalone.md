---
title: 安装独立版 Docker Compose
linkTitle: 独立版
description: 在 Linux 和 Windows Server 上安装旧版独立 Docker Compose 工具的说明
keywords: 安装 docker-compose, 独立版 docker compose, docker-compose windows server, linux 安装 docker compose, 旧版 compose 安装
toc_max: 3
weight: 20
---

本页包含了关于如何通过命令行在 Linux 或 Windows Server 上安装独立版 Docker Compose 的说明。

> [!WARNING]
>
> 独立版 Docker Compose 使用 `-compose` 语法，而不是当前的官方标准语法 `compose`。  
> 例如，使用独立版 Docker Compose 时，您必须输入 `docker-compose up`，而不是 `docker compose up`。请仅在需要向后兼容时使用它。

## 在 Linux 上

1. 要下载并安装独立版 Docker Compose，请运行：

   ```console
   $ curl -SL https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
   ```

2. 为安装目标路径下的独立版二进制文件授予执行权限。

   ```console
   $ chmod +x /usr/local/bin/docker-compose
   ```

3. 使用 `docker-compose` 测试并执行 Docker Compose 命令。

> [!TIP]
>
> 如果安装后 `docker-compose` 命令失败，请检查您的 path。
> 您也可以为 `/usr/bin` 或您路径中的任何其他目录创建一个符号链接。
> 例如：
> ```console
> $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
> ```

## 在 Windows Server 上

如果您 [直接在 Microsoft Windows Server 上运行 Docker 守护进程](/manuals/engine/install/binaries.md#在-Windows-上安装服务器和客户端二进制文件) 并想安装 Docker Compose，请遵循以下说明。

1.  以管理员身份运行 PowerShell。
    为了继续安装，当系统询问您是否允许此应用更改您的设备时，选择 **是 (Yes)**。

2.  可选。确保已启用 TLS1.2。 
    GitHub 要求使用 TLS1.2 进行安全连接。如果您使用的是较旧版本的 Windows Server（例如 2016），或者怀疑未启用 TLS1.2，请在 PowerShell 中运行以下命令：

    ```powershell
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    ```

3. 下载最新版本的 Docker Compose ({{% param "compose_version" %}})。运行以下命令：

    ```powershell
     Start-BitsTransfer -Source "https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-windows-x86_64.exe" -Destination $Env:ProgramFiles\Docker\docker-compose.exe
    ```

    要安装不同版本的 Docker Compose，请将 `{{% param "compose_version" %}}` 替换为您想要使用的版本。

    > [!NOTE]
    >
    > 在 Windows Server 2019 上，您可以将 Compose 可执行文件添加到 `$Env:ProgramFiles\Docker`。
     由于此目录已在系统 `PATH` 中注册，因此在后续步骤中，您无需进行任何额外配置即可运行 `docker-compose --version` 
     命令。

4.  测试安装。

    ```console
    $ docker-compose.exe version
    Docker Compose version {{% param "compose_version" %}}
    ```

## 下一步

- [了解 Compose 的工作原理](/manuals/compose/intro/compose-application-model.md)
- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
