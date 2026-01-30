---
description: 了解如何在 SLES 上安装 Docker Engine。这些说明涵盖了不同的安装方法、如何卸载以及后续步骤。
keywords: 要求, apt, 安装, 安装 docker engine, centos, rpm, sles, install, 卸载, 升级, 更新, s390x, ibm-z
title: 在 SLES (s390x) 上安装 Docker Engine
linkTitle: SLES (s390x)
weight: 70
toc_max: 4
alias:
- /ee/docker-ee/sles/
- /ee/docker-ee/suse/
- /engine/installation/linux/docker-ce/sles/
- /engine/installation/linux/docker-ee/sles/
- /engine/installation/linux/docker-ee/suse/
- /engine/installation/linux/sles/
- /engine/installation/linux/SUSE/
- /engine/installation/linux/suse/
- /engine/installation/sles/
- /engine/installation/SUSE/
- /install/linux/docker-ce/sles/
- /install/linux/docker-ee/sles/
- /install/linux/docker-ee/suse/
- /install/linux/sles/
- /installation/sles/
download-url-base: https://download.docker.com/linux/sles
---

> [!NOTE]
>
> 本页上的安装说明指的是针对 **s390x** 架构 (IBM Z) 的 SLES 软件包。SLES 不支持其他架构 (包括 x86_64)。

要在 SLES 上开始使用 Docker Engine，请确保您[满足前提条件](#prerequisites)，然后按照[安装步骤](#installation-methods)进行操作。

## 前提条件

### 操作系统要求

要安装 Docker Engine，您需要以下 SLES 版本之一的受维护版本：

- s390x (IBM Z) 上的 SLES 15-SP4
- s390x (IBM Z) 上的 SLES 15-SP5

您必须启用 [`SCC SUSE`](https://scc.suse.com/packages?name=SUSE%20Linux%20Enterprise%20Server&version=15.5&arch=s390x) 仓库。

您必须添加 [OpenSUSE `SELinux` 仓库](https://download.opensuse.org/repositories/security:/SELinux/)。该仓库默认不添加。运行以下命令添加它：

```console
$ opensuse_repo="https://download.opensuse.org/repositories/security:/SELinux/openSUSE_Factory/security:SELinux.repo"
$ sudo zypper addrepo $opensuse_repo
```

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的软件包。

您的 Linux 发行版可能会提供非官方的 Docker 软件包，这些软件包可能与 Docker 提供的官方软件包冲突。在安装官方版本的 Docker Engine 之前，您必须卸载这些软件包。

```console
$ sudo zypper remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  runc
```

`zypper` 可能会报告您没有安装这些软件包。

卸载 Docker 时，存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络不会自动移除。

## 安装方法

您可以根据需要以不同的方式安装 Docker Engine：

- 您可以[设置 Docker 的仓库](#install-using-the-repository)并从中安装，以便于安装和升级任务。这是推荐的方法。

- 您可以下载 RPM 软件包，[手动安装](#install-from-a-package)，并完全手动管理升级。这在无法访问互联网的离线系统上安装 Docker 时非常有用。

- 在测试和开发环境中，您可以使用自动化的[便利脚本](#install-using-the-convenience-script)来安装 Docker。

### 使用 rpm 仓库安装 {#install-using-the-repository}

在新的主机上首次安装 Docker Engine 之前，您需要设置 Docker 仓库。之后，您可以从仓库安装和更新 Docker。

#### 设置仓库

设置仓库。

```console
$ sudo zypper addrepo {{% param "download-url-base" %}}/docker-ce.repo
```

#### 安装 Docker Engine

1. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="最新版本" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo zypper install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   如果提示接受 GPG 密钥，请验证指纹是否匹配 `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`，如果是，请接受。

   此命令会安装 Docker，但不会启动 Docker。它还会创建一个 `docker` 组，但默认情况下不会向该组添加任何用户。

   {{< /tab >}}
   {{< tab name="特定版本" >}}

   要安装特定版本，请先列出仓库中可用的版本：

   ```console
   $ sudo zypper search -s --match-exact docker-ce | sort -r
 
     v  | docker-ce | package | 3:{{% param "docker_ce_version" %}}-1 | s390x | Docker CE Stable - s390x
     v  | docker-ce | package | 3:{{% param "docker_ce_version_prev" %}}-1 | s390x | Docker CE Stable - s390x
   ```

   返回的列表取决于启用了哪些仓库，并且特定于您的 SLES 版本。

   通过其完全限定的软件包名称安装特定版本，该名称由软件包名称 (`docker-ce`) 加上版本字符串 (第 2 列) 组成，中间用连字符 (`-`) 分隔。例如，`docker-ce-3:{{% param "docker_ce_version" %}}`。

   将 `<VERSION_STRING>` 替换为所需的版本，然后运行以下命令进行安装：

   ```console
   $ sudo zypper install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   此命令会安装 Docker，但不会启动 Docker。它还会创建一个 `docker` 组，但默认情况下不会向该组添加任何用户。
  
   {{< /tab >}}
   {{< /tabs >}}

2. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会将 Docker systemd 服务配置为在系统启动时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令会下载一个测试镜像并在容器中运行。当容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请按照[安装说明](#install-using-the-repository)操作，选择要安装的新版本。

### 从软件包安装

如果您无法使用 Docker 的 `rpm` 仓库安装 Docker Engine，可以下载对应版本的 `.rpm` 文件并手动安装。每次要升级 Docker Engine 时，都需要下载一个新文件。

1. 前往 [{{% param "download-url-base" %}}/]({{% param "download-url-base" %}}/) 并选择您的 SLES 版本。然后浏览到 `s390x/stable/Packages/` 并下载您要安装的 Docker 版本的 `.rpm` 文件。

2. 安装 Docker Engine，将以下路径更改为您下载 Docker 软件包的路径。

   ```console
   $ sudo zypper install /path/to/package.rpm
   ```

   Docker 已安装但未启动。`docker` 组已创建，但未向该组添加任何用户。

3. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会将 Docker systemd 服务配置为在系统启动时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

4. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令会下载一个测试镜像并在容器中运行。当容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件并重复[安装过程](#install-from-a-package)，使用 `zypper -y upgrade` 代替 `zypper -y install`，并指向新文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   ```console
   $ sudo zypper remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件不会自动移除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

您必须手动删除任何已编辑的配置文件。

## 后续步骤

- 继续阅读 [Linux 安装后的步骤](linux-postinstall.md)。
