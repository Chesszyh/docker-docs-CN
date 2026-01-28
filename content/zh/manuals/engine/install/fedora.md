---
description: 了解如何在 Fedora 上安装 Docker Engine。这些说明涵盖
  不同的安装方法、如何卸载以及后续步骤。
keywords: requirements, dnf, installation, fedora, install fedora, install docker engine, rpm, install, uninstall, upgrade,
  update
title: 在 Fedora 上安装 Docker Engine
linkTitle: Fedora
weight: 40
toc_max: 4
aliases:
- /engine/installation/fedora/
- /engine/installation/linux/fedora/
- /engine/installation/linux/docker-ce/fedora/
- /install/linux/docker-ce/fedora/
download-url-base: https://download.docker.com/linux/fedora
---

要在 Fedora 上开始使用 Docker Engine，请确保您
[满足前提条件](#prerequisites)，然后按照
[安装步骤](#installation-methods)进行操作。

## 前提条件

### 操作系统要求

要安装 Docker Engine，您需要以下
Fedora 版本之一的受维护版本：

- Fedora 42
- Fedora 41

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的软件包。

您的 Linux 发行版可能提供非官方的 Docker 软件包，这些软件包可能与
Docker 提供的官方软件包冲突。您必须在安装官方版本的 Docker Engine 之前
卸载这些软件包。

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

`dnf` 可能会报告您没有安装这些软件包。

卸载 Docker 时，存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络
不会被自动删除。

## 安装方法

您可以根据需要以不同方式安装 Docker Engine：

- 您可以
  [设置 Docker 的仓库](#install-using-the-repository)并从中安装，
  以便于安装和升级任务。这是
  推荐的方法。

- 您可以下载 RPM 软件包，
  [手动安装](#install-from-a-package)，并完全手动管理
  升级。这在诸如在无法访问互联网的隔离系统上安装
  Docker 等情况下很有用。

- 在测试和开发环境中，您可以使用自动化
  [便捷脚本](#install-using-the-convenience-script)来安装 Docker。

### 使用 rpm 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您
需要设置 Docker 仓库。之后，您可以从仓库安装和更新
Docker。

#### 设置仓库

安装 `dnf-plugins-core` 软件包（提供管理
DNF 仓库的命令）并设置仓库。

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf-3 config-manager --add-repo {{% param "download-url-base" %}}/docker-ce.repo
```

#### 安装 Docker Engine

1. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="Latest" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   如果提示接受 GPG 密钥，请验证指纹是否匹配
   `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`，如果匹配，则接受它。

   此命令会安装 Docker，但不会启动 Docker。它还会创建一个
   `docker` 组，但默认情况下不会向该组添加任何用户。

   {{< /tab >}}
   {{< tab name="Specific version" >}}

   要安装特定版本，首先列出仓库中的可用版本：

   ```console
   $ dnf list docker-ce --showduplicates | sort -r

   docker-ce.x86_64    3:{{% param "docker_ce_version" %}}-1.fc41    docker-ce-stable
   docker-ce.x86_64    3:{{% param "docker_ce_version_prev" %}}-1.fc41    docker-ce-stable
   <...>
   ```

   返回的列表取决于启用了哪些仓库，并且特定于
   您的 Fedora 版本（在此示例中由 `.fc40` 后缀表示）。

   通过完全限定的软件包名称安装特定版本，即
   软件包名称（`docker-ce`）加上版本字符串（第 2 列），
   用连字符（`-`）分隔。例如，`docker-ce-3:{{% param "docker_ce_version" %}}-1.fc41`。

   将 `<VERSION_STRING>` 替换为所需版本，然后运行以下
   命令进行安装：

   ```console
   $ sudo dnf install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   此命令会安装 Docker，但不会启动 Docker。它还会创建一个
   `docker` 组，但默认情况下不会向该组添加任何用户。

   {{< /tab >}}
   {{< /tabs >}}

2. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会配置 Docker systemd 服务在您
   启动系统时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo
   systemctl start docker`。

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载一个测试镜像并在容器中运行它。当
   容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请按照[安装说明](#install-using-the-repository)进行操作，
选择您要安装的新版本。

### 从软件包安装 {#install-from-a-package}

如果您无法使用 Docker 的 `rpm` 仓库安装 Docker Engine，可以
下载适用于您版本的 `.rpm` 文件并手动安装。每次要
升级 Docker Engine 时都需要下载新文件。

<!-- markdownlint-disable-next-line -->
1. 前往 [{{% param "download-url-base" %}}/]({{% param "download-url-base" %}}/)
   并选择您的 Fedora 版本。然后浏览到 `x86_64/stable/Packages/`
   并下载您要安装的 Docker 版本的 `.rpm` 文件。

2. 安装 Docker Engine，将以下路径更改为您下载
   Docker 软件包的路径。

   ```console
   $ sudo dnf install /path/to/package.rpm
   ```

   Docker 已安装但未启动。`docker` 组已创建，但没有
   用户被添加到该组。

3. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会配置 Docker systemd 服务在您
   启动系统时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo
   systemctl start docker`。

4. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载一个测试镜像并在容器中运行它。当
   容器运行时，它会打印一条确认消息并退出。

您现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件并重复
[安装过程](#install-from-a-package)，使用 `dnf upgrade`
代替 `dnf install`，并指向新文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   ```console
   $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件
   不会被自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

您必须手动删除任何已编辑的配置文件。

## 后续步骤

- 继续阅读 [Linux 安装后步骤](linux-postinstall.md)。
