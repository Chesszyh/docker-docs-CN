---
description: 在 Linux 上使用软件包仓库或手动方法安装 Docker Compose 插件的分步说明。
keywords: install docker compose linux, docker compose plugin, docker-compose-plugin linux, docker compose v2, docker compose manual install, linux docker compose
toc_max: 3
title: 安装 Docker Compose 插件
linkTitle: 插件
aliases:
- /compose/compose-plugin/
- /compose/compose-linux/
- /compose/install/compose-plugin/
weight: 10
---

本页面包含如何从命令行在 Linux 上安装 Docker Compose 插件的说明。

要在 Linux 上安装 Docker Compose 插件，您可以：
- [在您的 Linux 系统上设置 Docker 的仓库](#使用仓库安装)。
- [手动安装](#手动安装插件)。

> [!NOTE]
>
> 这些说明假设您已经安装了 Docker Engine 和 Docker CLI，现在想要安装 Docker Compose 插件。

## 使用仓库安装

1. 设置仓库。在以下位置找到特定发行版的说明：

    [Ubuntu](/manuals/engine/install/ubuntu.md#install-using-the-repository) |
    [CentOS](/manuals/engine/install/centos.md#set-up-the-repository) |
    [Debian](/manuals/engine/install/debian.md#install-using-the-repository) |
    [Raspberry Pi OS](/manuals/engine/install/raspberry-pi-os.md#install-using-the-repository) |
    [Fedora](/manuals/engine/install/fedora.md#set-up-the-repository) |
    [RHEL](/manuals/engine/install/rhel.md#set-up-the-repository) |
    [SLES](/manuals/engine/install/sles.md#set-up-the-repository)。

2. 更新软件包索引，并安装最新版本的 Docker Compose：

    * 对于 Ubuntu 和 Debian，运行：

        ```console
        $ sudo apt-get update
        $ sudo apt-get install docker-compose-plugin
        ```
    * 对于基于 RPM 的发行版，运行：

        ```console
        $ sudo yum update
        $ sudo yum install docker-compose-plugin
        ```

3.  通过检查版本验证 Docker Compose 已正确安装。

    ```console
    $ docker compose version
    ```

### 更新 Docker Compose

要更新 Docker Compose 插件，运行以下命令：

* 对于 Ubuntu 和 Debian，运行：

    ```console
    $ sudo apt-get update
    $ sudo apt-get install docker-compose-plugin
    ```
* 对于基于 RPM 的发行版，运行：

    ```console
    $ sudo yum update
    $ sudo yum install docker-compose-plugin
    ```

## 手动安装插件

> [!WARNING]
>
> 手动安装不会自动更新。为了便于维护，请使用 Docker 仓库方法。

1.  要下载并安装 Docker Compose CLI 插件，运行：

    ```console
    $ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
    $ mkdir -p $DOCKER_CONFIG/cli-plugins
    $ curl -SL https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
    ```

    此命令为活动用户下载并安装最新版本的 Docker Compose 到 `$HOME` 目录下。

    安装时：
    - 要为系统上的_所有用户_安装 Docker Compose，将 `~/.docker/cli-plugins` 替换为 `/usr/local/lib/docker/cli-plugins`。
    - 要安装不同版本的 Compose，将 `{{% param "compose_version" %}}` 替换为您想要使用的 Compose 版本。
    - 对于不同的架构，将 `x86_64` 替换为[您想要的架构](https://github.com/docker/compose/releases)。


2. 为二进制文件应用可执行权限：

    ```console
    $ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
    ```
    或者，如果您选择为所有用户安装 Compose：

    ```console
    $ sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    ```

3. 测试安装。

    ```console
    $ docker compose version
    ```

## 下一步是什么？

- [了解 Compose 如何工作](/manuals/compose/intro/compose-application-model.md)
- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
