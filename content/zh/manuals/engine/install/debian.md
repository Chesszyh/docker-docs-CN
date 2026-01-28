---
description: 了解如何在 Debian 上安装 Docker Engine。这些说明涵盖
  不同的安装方法、如何卸载以及后续步骤。
keywords: requirements, apt, installation, debian, install, uninstall, install debian, docker engine, install docker engine, upgrade, update
title: 在 Debian 上安装 Docker Engine
linkTitle: Debian
weight: 20
toc_max: 4
aliases:
- /engine/installation/debian/
- /engine/installation/linux/debian/
- /engine/installation/linux/docker-ce/debian/
- /install/linux/docker-ce/debian/
download-url-base: https://download.docker.com/linux/debian
---

要在 Debian 上开始使用 Docker Engine，请确保您
[满足前提条件](#prerequisites)，然后按照
[安装步骤](#installation-methods)进行操作。

## 前提条件

### 防火墙限制

> [!WARNING]
>
> 在安装 Docker 之前，请确保您考虑以下
> 安全影响和防火墙不兼容性。

- 如果您使用 ufw 或 firewalld 管理防火墙设置，请注意
  当您使用 Docker 暴露容器端口时，这些端口会绕过您的
  防火墙规则。有关更多信息，请参阅
  [Docker 和 ufw](/manuals/engine/network/packet-filtering-firewalls.md#docker-and-ufw)。
- Docker 仅与 `iptables-nft` 和 `iptables-legacy` 兼容。
  在安装了 Docker 的系统上不支持使用 `nft` 创建的防火墙规则。
  确保您使用的任何防火墙规则集都是使用 `iptables` 或 `ip6tables` 创建的，
  并将它们添加到 `DOCKER-USER` 链中，
  请参阅[数据包过滤和防火墙](/manuals/engine/network/packet-filtering-firewalls.md)。

### 操作系统要求

要安装 Docker Engine，您需要以下 Debian
版本之一的 64 位版本：

- Debian Trixie 13 (testing)
- Debian Bookworm 12 (stable)
- Debian Bullseye 11 (oldstable)

Docker Engine for Debian 与 x86_64（或 amd64）、armhf、arm64
和 ppc64le (ppc64el) 架构兼容。

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的软件包。

您的 Linux 发行版可能提供非官方的 Docker 软件包，这些软件包可能与
Docker 提供的官方软件包冲突。您必须在安装官方版本的 Docker Engine 之前
卸载这些软件包。

需要卸载的非官方软件包有：

- `docker.io`
- `docker-compose`
- `docker-doc`
- `podman-docker`

此外，Docker Engine 依赖于 `containerd` 和 `runc`。Docker Engine
将这些依赖项捆绑为一个包：`containerd.io`。如果您之前
安装了 `containerd` 或 `runc`，请卸载它们以避免
与 Docker Engine 捆绑的版本冲突。

运行以下命令卸载所有冲突的软件包：

```console
$ for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` 可能会报告您没有安装这些软件包。

卸载 Docker 时，存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络
不会被自动删除。如果您想从全新安装开始，
并且希望清理任何现有数据，请阅读
[卸载 Docker Engine](#uninstall-docker-engine) 部分。

## 安装方法

您可以根据需要以不同方式安装 Docker Engine：

- Docker Engine 与
  [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md) 捆绑在一起。这是
  最简单、最快速的入门方式。

- 从
  [Docker 的 `apt` 仓库](#install-using-the-repository)设置和安装 Docker Engine。

- [手动安装](#install-from-a-package)并手动管理升级。

- 使用[便捷脚本](#install-using-the-convenience-script)。仅
  推荐用于测试和开发环境。

### 使用 `apt` 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您
需要设置 Docker `apt` 仓库。之后，您可以从仓库安装和更新
Docker。

1. 设置 Docker 的 `apt` 仓库。

   ```bash
   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL {{% param "download-url-base" %}}/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] {{% param "download-url-base" %}} \
     $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```

   > [!NOTE]
   >
   > 如果您使用衍生发行版，例如 Kali Linux，
   > 您可能需要替换此命令中预期
   > 打印版本代号的部分：
   >
   > ```console
   > $(. /etc/os-release && echo "$VERSION_CODENAME")
   > ```
   >
   > 将此部分替换为相应 Debian 版本的代号，
   > 例如 `bookworm`。

2. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="Latest" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< tab name="Specific version" >}}

   要安装特定版本的 Docker Engine，首先列出仓库中的
   可用版本：

   ```console
   # List the available versions:
   $ apt-cache madison docker-ce | awk '{ print $3 }'

   5:{{% param "docker_ce_version" %}}-1~debian.12~bookworm
   5:{{% param "docker_ce_version_prev" %}}-1~debian.12~bookworm
   ...
   ```

   选择所需版本并安装：

   ```console
   $ VERSION_STRING=5:{{% param "docker_ce_version" %}}-1~debian.12~bookworm
   $ sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< /tabs >}}

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载一个测试镜像并在容器中运行它。当
   容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请按照
[安装说明](#install-using-the-repository)的步骤 2 进行操作，
选择您要安装的新版本。

### 从软件包安装 {#install-from-a-package}

如果您无法使用 Docker 的 `apt` 仓库安装 Docker Engine，可以
下载适用于您版本的 `deb` 文件并手动安装。每次要
升级 Docker Engine 时都需要下载新文件。

<!-- markdownlint-disable-next-line -->
1. 前往 [`{{% param "download-url-base" %}}/dists/`]({{% param "download-url-base" %}}/dists/)。

2. 在列表中选择您的 Debian 版本。

3. 前往 `pool/stable/` 并选择适用的架构（`amd64`、
   `armhf`、`arm64` 或 `s390x`）。

4. 下载 Docker Engine、CLI、containerd
   和 Docker Compose 软件包的以下 `deb` 文件：

   - `containerd.io_<version>_<arch>.deb`
   - `docker-ce_<version>_<arch>.deb`
   - `docker-ce-cli_<version>_<arch>.deb`
   - `docker-buildx-plugin_<version>_<arch>.deb`
   - `docker-compose-plugin_<version>_<arch>.deb`

5. 安装 `.deb` 软件包。将以下示例中的路径更新为
   您下载 Docker 软件包的位置。

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

   Docker 守护进程会自动启动。

6. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo service docker start
   $ sudo docker run hello-world
   ```

   此命令下载一个测试镜像并在容器中运行它。当
   容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件并重复
[安装过程](#install-from-a-package)，指向新文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   ```console
   $ sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件
   不会被自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. 删除源列表和密钥环

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.list
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

您必须手动删除任何已编辑的配置文件。

## 后续步骤

- 继续阅读 [Linux 安装后步骤](linux-postinstall.md)。
