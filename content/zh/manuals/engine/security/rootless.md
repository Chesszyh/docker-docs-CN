--- 
description: 以非 root 用户运行 Docker 守护进程 (无根模式)
keywords: security, namespaces, rootless, 安全, 命名空间, 无根模式
title: 无根模式 (Rootless mode)
weight: 10
---

无根模式允许以非 root 用户身份运行 Docker 守护进程和容器，以减轻守护进程和容器运行时中潜在的漏洞风险。

只要满足 [前提条件](#prerequisites)，即使在安装 Docker 守护进程期间，无根模式也不需要 root 权限。

## 工作原理

无根模式在用户命名空间内执行 Docker 守护进程和容器。这与 [`userns-remap` 模式](userns-remap.md) 非常相似，不同之处在于，在 `userns-remap` 模式下，守护进程本身是以 root 权限运行的，而在无根模式下，守护进程和容器都在没有 root 权限的情况下运行。

无根模式不使用带有 `SETUID` 位或文件能力 (file capabilities) 的二进制文件，但 `newuidmap` 和 `newgidmap` 除外，它们是允许在用户命名空间中使用多个 UID/GID 所必需的。

## 前提条件

- 您必须在主机上安装 `newuidmap` 和 `newgidmap`。在大多数发行版上，这些命令由 `uidmap` 软件包提供。

- `/etc/subuid` 和 `/etc/subgid` 应包含至少 65,536 个该用户的从属 UID/GID。在以下示例中，用户 `testuser` 拥有 65,536 个从属 UID/GID (231072-296607)。

```console
$ id -u
1001
$ whoami
testuser
$ grep ^$(whoami): /etc/subuid
testuser:231072:65536
$ grep ^$(whoami): /etc/subgid
testuser:231072:65536
```

### 各发行版提示

> [!TIP]
> 
> 我们建议您使用 Ubuntu 内核。

{{< tabs >}}
{{< tab name="Ubuntu" >}}
- 如果未安装 `dbus-user-session` 软件包，请安装。运行 `sudo apt-get install -y dbus-user-session` 并重新登录。
- 如果未安装 `uidmap` 软件包，请安装。运行 `sudo apt-get install -y uidmap`。
- 如果在非直接登录用户的终端中运行，您需要通过 `sudo apt-get install -y systemd-container` 安装 `systemd-container`，然后使用命令 `sudo machinectl shell TheUser@` 切换到该用户 (TheUser)。

- 默认启用 `overlay2` 存储驱动程序 ([Ubuntu 特有内核补丁](https://kernel.ubuntu.com/git/ubuntu/ubuntu-bionic.git/commit/fs/overlayfs?id=3b7da90f28fe1ed4b79ef2d994c81efbc58f1144))。

- Ubuntu 24.04 及更高版本默认启用了受限的非特权用户命名空间，这会阻止非特权进程创建用户命名空间，除非配置了 AppArmor 配置文件以允许程序使用非特权用户命名空间。

  如果您使用 deb 软件包安装 `docker-ce-rootless-extras` (`apt-get install docker-ce-rootless-extras`)，那么 `rootlesskit` 的 AppArmor 配置文件已随 `apparmor` deb 软件包一起提供。使用此安装方法，您无需手动添加任何 AppArmor 配置。但是，如果您使用 [安装脚本](https://get.docker.com/rootless) 安装无根模式扩展，则必须手动为 `rootlesskit` 添加 AppArmor 配置文件：

  1. 创建并安装当前登录用户的 AppArmor 配置文件：

     ```console
     $ filename=$(echo $HOME/bin/rootlesskit | sed -e s@^/@@ -e s@/@.@g)
     $ cat <<EOF > ~/${filename}
     abi <abi/4.0>,
     include <tunables/global>

     "$HOME/bin/rootlesskit" flags=(unconfined) {
       userns,

       include if exists <local/${filename}>
     }
     EOF
     $ sudo mv ~/${filename} /etc/apparmor.d/${filename}
     ```
  2. 重启 AppArmor。

     ```console
     $ systemctl restart apparmor.service
     ```

{{< /tab >}}
{{< tab name="Debian GNU/Linux" >}}
- 如果未安装 `dbus-user-session` 软件包，请安装。运行 `sudo apt-get install -y dbus-user-session` 并重新登录。

- 对于 Debian 11，建议安装 `fuse-overlayfs`。运行 `sudo apt-get install -y fuse-overlayfs`。Debian 12 不需要此步骤。

- 无根 Docker 需要版本大于 `v0.4.0` 的 `slirp4netns` (当未安装 `vpnkit` 时)。使用以下命令检查：
  
  ```console
  $ slirp4netns --version
  ```
  如果您没有此版本，请使用 `sudo apt-get install -y slirp4netns` 下载安装，或下载最新的 [发布版本](https://github.com/rootless-containers/slirp4netns/releases)。
{{< /tab >}}
{{< tab name="Arch Linux" >}}
- 建议安装 `fuse-overlayfs`。运行 `sudo pacman -S fuse-overlayfs`。

- 将 `kernel.unprivileged_userns_clone=1` 添加到 `/etc/sysctl.conf` (或 `/etc/sysctl.d`) 并运行 `sudo sysctl --system`。
{{< /tab >}}
{{< tab name="openSUSE and SLES" >}}
- 对于 openSUSE 15 和 SLES 15，建议安装 `fuse-overlayfs`。运行 `sudo zypper install -y fuse-overlayfs`。openSUSE Tumbleweed 不需要此步骤。

- 需要执行 `sudo modprobe ip_tables iptable_mangle iptable_nat iptable_filter`。根据配置，其他发行版可能也需要执行此操作。

- 已知可在 openSUSE 15 和 SLES 15 上工作。
{{< /tab >}}
{{< tab name="CentOS, RHEL, and Fedora" >}}
- 对于 RHEL 8 及类似发行版，建议安装 `fuse-overlayfs`。运行 `sudo dnf install -y fuse-overlayfs`。RHEL 9 及类似发行版不需要此步骤。

- 您可能需要执行 `sudo dnf install -y iptables`。
{{< /tab >}}
{{< /tabs >}}

## 已知限制

- 仅支持以下存储驱动程序：
  - `overlay2` (仅当运行内核 5.11 或更高版本，或 Ubuntu 系列内核时)
  - `fuse-overlayfs` (仅当运行内核 4.18 或更高版本，且安装了 `fuse-overlayfs` 时)
  - `btrfs` (仅当运行内核 4.18 或更高版本，或使用 `user_subvol_rm_allowed` 挂载选项挂载 `~/.local/share/docker` 时)
  - `vfs`
- 仅当配合 cgroup v2 和 systemd 运行时才支持 Cgroup。参见 [限制资源](#limiting-resources)。
- 不支持以下特性：
  - AppArmor
  - Checkpoint (检查点)
  - Overlay 网络
  - 暴露 SCTP 端口
- 要使用 `ping` 命令，请参阅 [路由 ping 数据包](#routing-ping-packets)。
- 要暴露特权 TCP/UDP 端口 (< 1024)，请参阅 [暴露特权端口](#exposing-privileged-ports)。
- `docker inspect` 中显示的 `IPAddress` 位于 RootlessKit 的网络命名空间内。这意味着如果不使用 `nsenter` 进入该网络命名空间，就无法从主机访问该 IP 地址。
- 主机网络 (`docker run --net=host`) 也在 RootlessKit 内部进行了命名空间化。
- 不支持将 NFS 挂载作为 docker 的 "data-root"。此限制并非无根模式特有。

## 安装

> [!NOTE]
> 
> 如果系统范围的 Docker 守护进程已在运行，请考虑禁用它：
>```console
>$ sudo systemctl disable --now docker.service docker.socket
>$ sudo rm /var/run/docker.sock
>```
> 如果您选择不关闭 `docker` 服务和套接字，则需要在下一节中使用 `--force` 参数。目前没有已知问题，但在关闭和禁用之前，您运行的仍是具有 root 权限的 Docker。

{{< tabs >}}
{{< tab name="使用软件包 (RPM/DEB)" >}}

如果您使用 [RPM/DEB 软件包](/engine/install) 安装了 Docker 20.10 或更高版本，则应在 `/usr/bin` 中拥有 `dockerd-rootless-setuptool.sh`。

以非 root 用户运行 `dockerd-rootless-setuptool.sh install` 以设置守护进程：

```console
$ dockerd-rootless-setuptool.sh install
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Make sure the following environment variables are set (or add them to ~/.bashrc):

export PATH=/usr/bin:$PATH
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

如果 `dockerd-rootless-setuptool.sh` 不存在，您可能需要手动安装 `docker-ce-rootless-extras` 软件包，例如：

```console
$ sudo apt-get install -y docker-ce-rootless-extras
```

{{< /tab >}}
{{< tab name="不使用软件包" >}}

如果您没有权限运行 `apt-get` 和 `dnf` 等软件包管理器，请考虑使用可从 [https://get.docker.com/rootless](https://get.docker.com/rootless) 获取的安装脚本。由于 `s390x` 暂无静态包，因此 `s390x` 不受支持。

```console
$ curl -fsSL https://get.docker.com/rootless | sh
...
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Make sure the following environment variables are set (or add them to ~/.bashrc):

export PATH=/home/testuser/bin:$PATH
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

二进制文件将安装在 `~/bin` 目录下。

{{< /tab >}}
{{< /tabs >}}

如果遇到错误，请参阅 [故障排查](#troubleshooting)。

## 卸载

要移除 Docker 守护进程的 systemd 服务，运行 `dockerd-rootless-setuptool.sh uninstall`：

```console
$ dockerd-rootless-setuptool.sh uninstall
+ systemctl --user stop docker.service
+ systemctl --user disable docker.service
Removed /home/testuser/.config/systemd/user/default.target.wants/docker.service.
[INFO] Uninstalled docker.service
[INFO] This uninstallation tool does NOT remove Docker binaries and data.
[INFO] To remove data, run: `/usr/bin/rootlesskit rm -rf /home/testuser/.local/share/docker`
```

如果您已将 PATH 和 DOCKER_HOST 环境变量添加到 `~/.bashrc`，请将其取消设置。

要移除数据目录，运行 `rootlesskit rm -rf ~/.local/share/docker`。

要移除二进制文件，如果您使用软件包管理器安装了 Docker，请移除 `docker-ce-rootless-extras` 软件包。如果您使用 https://get.docker.com/rootless 安装了 Docker ([不使用软件包安装](#install))，请移除 `~/bin` 下的二进制文件：
```console
$ cd ~/bin
$ rm -f containerd containerd-shim containerd-shim-runc-v2 ctr docker docker-init docker-proxy dockerd dockerd-rootless-setuptool.sh dockerd-rootless.sh rootlesskit rootlesskit-docker-proxy runc vpnkit
```

## 使用方法

### 守护进程 (Daemon)

{{< tabs >}}
{{< tab name="使用 systemd (强烈推荐)" >}}

systemd 单元文件安装为 `~/.config/systemd/user/docker.service`。

使用 `systemctl --user` 来管理守护进程的生命周期：

```console
$ systemctl --user start docker
```

要在系统启动时启动守护进程，请启用 systemd 服务并开启 lingering：

```console
$ systemctl --user enable docker
$ sudo loginctl enable-linger $(whoami)
```

不支持将无根 Docker 作为系统范围的服务 (`/etc/systemd/system/docker.service`) 启动，即使使用了 `User=` 指令也是如此。

{{< /tab >}}
{{< tab name="不使用 systemd" >}}

要在没有 systemd 的情况下直接运行守护进程，您需要运行 `dockerd-rootless.sh` 而不是 `dockerd`。

必须设置以下环境变量：
- `$HOME`: 主目录
- `$XDG_RUNTIME_DIR`: 一个仅供预期用户访问的临时目录，例如 `~/.docker/run`。该目录应在每次主机关闭时移除。该目录可以位于 tmpfs 上，但不应位于 `/tmp` 下。将此目录放在 `/tmp` 下可能会容易受到 TOCTOU 攻击。

{{< /tab >}}
{{< /tabs >}}

关于目录路径的说明：

- 套接字路径默认设置为 `$XDG_RUNTIME_DIR/docker.sock`。`$XDG_RUNTIME_DIR` 通常设置为 `/run/user/$UID`。
- 数据目录默认设置为 `~/.local/share/docker`。数据目录不应位于 NFS 上。
- 守护进程配置目录默认设置为 `~/.config/docker`。此目录与客户端使用的 `~/.docker` 不同。

### 客户端 (Client)

您需要显式指定套接字路径或 CLI 上下文 (context)。

使用 `$DOCKER_HOST` 指定套接字路径：

```console
$ export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
$ docker run -d -p 8080:80 nginx
```

使用 `docker context` 指定 CLI 上下文：

```console
$ docker context use rootless
rootless
Current context is now "rootless"
$ docker run -d -p 8080:80 nginx
```

## 最佳实践

### 无根 Docker-in-Docker

要在“有根 (rootful)” Docker 内部运行无根 Docker，请使用 `docker:<version>-dind-rootless` 镜像而不是 `docker:<version>-dind`。

```console
$ docker run -d --name dind-rootless --privileged docker:25.0-dind-rootless
```

`docker:<version>-dind-rootless` 镜像以非 root 用户 (UID 1000) 运行。但是，为了禁用 seccomp、AppArmor 和挂载掩码，仍然需要 `--privileged` 标志。

### 通过 TCP 暴露 Docker API 套接字

要通过 TCP 暴露 Docker API 套接字，您需要带参数 `DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp"` 启动 `dockerd-rootless.sh`。

```console
$ DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp" \
  dockerd-rootless.sh \
  -H tcp://0.0.0.0:2376 \
  --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem
```

### 通过 SSH 暴露 Docker API 套接字

要通过 SSH 暴露 Docker API 套接字，您需要确保在远程主机上设置了 `$DOCKER_HOST`。

```console
$ ssh -l <REMOTEUSER> <REMOTEHOST> 'echo $DOCKER_HOST'
unix:///run/user/1001/docker.sock
$ docker -H ssh://<REMOTEUSER>@<REMOTEHOST> run ...
```

### 路由 ping 数据包

在某些发行版上，`ping` 默认无法工作。

将 `net.ipv4.ping_group_range = 0   2147483647` 添加到 `/etc/sysctl.conf` (或 `/etc/sysctl.d`) 并运行 `sudo sysctl --system` 以允许使用 `ping`。

### 暴露特权端口

要暴露特权端口 (< 1024)，请在 `rootlesskit` 二进制文件上设置 `CAP_NET_BIND_SERVICE` 并重启守护进程。

```console
$ sudo setcap cap_net_bind_service=ep $(which rootlesskit)
$ systemctl --user restart docker
```

或者将 `net.ipv4.ip_unprivileged_port_start=0` 添加到 `/etc/sysctl.conf` (或 `/etc/sysctl.d`) 并运行 `sudo sysctl --system`。

### 限制资源

仅在配合 cgroup v2 和 systemd 运行时，才支持通过 cgroup 相关的 `docker run` 标志 (如 `--cpus`、`--memory`、`--pids-limit`) 限制资源。参见 [更改 cgroup 版本](/manuals/engine/containers/runmetrics.md) 以启用 cgroup v2。

如果 `docker info` 显示 `Cgroup Driver` 为 `none`，则不满足条件。当不满足这些条件时，无根模式会忽略 cgroup 相关的 `docker run` 标志。参见 [不使用 cgroup 限制资源](#limiting-resources-without-cgroup) 了解变通方法。

如果 `docker info` 显示 `Cgroup Driver` 为 `systemd`，则满足条件。然而，通常默认情况下只有 `memory` 和 `pids` 控制器被委托给非 root 用户。

```console
$ cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.controllers
memory pids
```

要允许委托所有控制器，您需要按如下方式更改 systemd 配置：

```console
# mkdir -p /etc/systemd/system/user@.service.d
# cat > /etc/systemd/system/user@.service.d/delegate.conf << EOF
[Service]
Delegate=cpu cpuset io memory pids
EOF
# systemctl daemon-reload
```

> [!NOTE]
> 
> 委托 `cpuset` 需要 systemd 244 或更高版本。

#### 不使用 cgroup 限制资源

即使在 cgroup 不可用的情况下，您仍然可以使用传统的 `ulimit` 和 [`cpulimit`](https://github.com/opsengine/cpulimit)，尽管它们是在进程粒度而不是容器粒度下工作的，并且可以由容器进程任意禁用。

例如：

- 将 CPU 使用率限制为 0.5 核 (类似于 `docker run --cpus 0.5`)：
  `docker run <IMAGE> cpulimit --limit=50 --include-children <COMMAND>`
- 将最大 VSZ 限制为 64MiB (类似于 `docker run --memory 64m`)：
  `docker run <IMAGE> sh -c "ulimit -v 65536; <COMMAND>"`

- 针对命名空间 UID 2000，将最大进程数限制为 100 (类似于 `docker run --pids-limit=100`)：
  `docker run --user 2000 --ulimit nproc=100 <IMAGE> <COMMAND>`

## 故障排查

### 系统中存在 systemd 却无法通过 systemd 安装

``` console
$ dockerd-rootless-setuptool.sh install
[INFO] systemd not detected, dockerd-rootless.sh needs to be started manually:
...
```
如果您通过 `sudo su` 切换到您的用户，`rootlesskit` 可能无法正确检测到 systemd。对于无法直接登录的用户，您必须使用 `systemd-container` 软件包中的 `machinectl` 命令。安装 `systemd-container` 后，使用以下命令切换到 `myuser`：
``` console
$ sudo machinectl shell myuser@
```
其中 `myuser@` 是您想要的用户名，@ 表示这台机器。

### 启动 Docker 守护进程时的错误

**[rootlesskit:parent] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted**

此错误通常发生在 `/proc/sys/kernel/unprivileged_userns_clone` 的值被设置为 0 时：

```console
$ cat /proc/sys/kernel/unprivileged_userns_clone
0
```

要修复此问题，请将 `kernel.unprivileged_userns_clone=1` 添加到 `/etc/sysctl.conf` (或 `/etc/sysctl.d`) 并运行 `sudo sysctl --system`。

**[rootlesskit:parent] error: failed to start the child: fork/exec /proc/self/exe: no space left on device**

此错误通常发生在 `/proc/sys/user/max_user_namespaces` 的值太小时：

```console
$ cat /proc/sys/user/max_user_namespaces
0
```

要修复此问题，请将 `user.max_user_namespaces=28633` 添加到 `/etc/sysctl.conf` (或 `/etc/sysctl.d`) 并运行 `sudo sysctl --system`。

**[rootlesskit:parent] error: failed to setup UID/GID map: failed to compute uid/gid map: No subuid ranges found for user 1001 ("testuser")**

当未配置 `/etc/subuid` 和 `/etc/subgid` 时会发生此错误。参见 [前提条件](#prerequisites)。

**could not get XDG_RUNTIME_DIR**

当未设置 `$XDG_RUNTIME_DIR` 时会发生此错误。

在非 systemd 主机上，您需要创建一个目录然后设置路径：

```console
$ export XDG_RUNTIME_DIR=$HOME/.docker/xrd
$ rm -rf $XDG_RUNTIME_DIR
$ mkdir -p $XDG_RUNTIME_DIR
$ dockerd-rootless.sh
```

> [!NOTE]
> 
> 每次注销时必须移除该目录。

在 systemd 主机上，使用 `pam_systemd` 登录到主机 (见下文)。该值会自动设置为 `/run/user/$UID` 并在每次注销时清理。

**`systemctl --user` 失败并提示 "Failed to connect to bus: No such file or directory"**

此错误通常发生在您通过 `sudo` 从 root 用户切换到非 root 用户时：

```console
# sudo -iu testuser
$ systemctl --user start docker
Failed to connect to bus: No such file or directory
```

您需要使用 `pam_systemd` 登录，而不是使用 `sudo -iu <USERNAME>`。例如：

- 通过图形控制台登录
- `ssh <USERNAME>@localhost`
- `machinectl shell <USERNAME>@`

**守护进程未自动启动**

您需要执行 `sudo loginctl enable-linger $(whoami)` 以允许守护进程自动启动。参见 [使用方法](#usage)。

**iptables failed: iptables -t nat -N DOCKER: Fatal: can't open lock file /run/xtables.lock: Permission denied**

当主机启用了 SELinux 时，旧版本的 Docker 可能会发生此错误。

此问题已在 Docker 20.10.8 中修复。对于旧版本的 Docker，一个已知的变通方法是运行以下命令以为 `iptables` 禁用 SELinux：
```console
$ sudo dnf install -y policycoreutils-python-utils && sudo semanage permissive -a iptables_t
```

### `docker pull` 错误

**docker: failed to register layer: Error processing tar file(exit status 1): lchown <FILE>: invalid argument**

当 `/etc/subuid` 或 `/etc/subgid` 中可用的条目数不足时，会发生此错误。所需的条目数因镜像而异。但是，对于大多数镜像，65,536 个条目就足够了。参见 [前提条件](#prerequisites)。

**docker: failed to register layer: ApplyLayer exit status 1 stdout:  stderr: lchown <FILE>: operation not permitted**

此错误通常发生在 `~/.local/share/docker` 位于 NFS 上时。

变通方法是在 `~/.config/docker/daemon.json` 中指定一个非 NFS 的 `data-root` 目录，如下所示：
```json
{"data-root":"/somewhere-out-of-nfs"}
```

### `docker run` 错误

**docker: Error response from daemon: OCI runtime create failed: ...: read unix @->/run/systemd/private: read: connection reset by peer: unknown.**

此错误通常发生在 cgroup v2 主机上，且该用户的 dbus 守护进程未运行时。

```console
$ systemctl --user is-active dbus
inactive

$ docker run hello-world
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:385: applying cgroup configuration for process caused: error while starting unit "docker
-931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e.scope" with properties [{Name:Description Value:"libcontainer container 931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e"} {Name:Slice Value:"use
r.slice"} {Name:PIDs Value:@au [4529]} {Name:Delegate Value:true} {Name:MemoryAccounting Value:true} {Name:CPUAccounting Value:true} {Name:IOAccounting Value:true} {Name:TasksAccounting Value:true} {Name:DefaultDependencies Val
ue:false}]: read unix @->/run/systemd/private: read: connection reset by peer: unknown.
```

要修复此问题，请运行 `sudo apt-get install -y dbus-user-session` 或 `sudo dnf install -y dbus-daemon`，然后重新登录。

如果错误仍然发生，尝试运行 `systemctl --user enable --now dbus` (不使用 sudo)。

**`--cpus`, `--memory`, 和 `--pids-limit` 被忽略**

这是 cgroup v1 模式下的预期行为。要使用这些标志，主机需要配置为启用 cgroup v2。有关更多信息，请参阅 [限制资源](#limiting-resources)。

### 网络错误

本节提供在无根模式下有关联网的故障排查提示。

无根模式下的联网通过 RootlessKit 中的网络和端口驱动程序支持。网络性能和特性取决于您使用的网络和端口驱动程序的组合。如果您遇到与联网相关的意外行为或性能问题，请查看下表，该表显示了 RootlessKit 支持的配置及其对比：

| 网络驱动程序   | 端口驱动程序   | 网络吞吐量 | 端口吞吐量 | 源 IP 传播 | 无 SUID | 备注                                                                         |
| -------------- | -------------- | ---------- | ---------- | ---------- | ------- | ---------------------------------------------------------------------------- |
| `slirp4netns`  | `builtin`      | 慢         | 快 ✅      | ❌         | ✅      | 典型设置中的默认值                                                           |
| `vpnkit`       | `builtin`      | 慢         | 快 ✅      | ❌         | ✅      | 当未安装 `slirp4netns` 时的默认值                                            |
| `slirp4netns`  | `slirp4netns`  | 慢         | 慢         | ✅         | ✅      |                                                                              |
| `pasta`        | `implicit`     | 慢         | 快 ✅      | ✅         | ✅      | 实验性；需要 pasta 2023_12_04 或更高版本                                     |
| `lxc-user-nic` | `builtin`      | 快 ✅      | 快 ✅      | ❌         | ❌      | 实验性                                                                       |
| `bypass4netns` | `bypass4netns` | 快 ✅      | 快 ✅      | ✅         | ✅      | **备注：** 未集成到 RootlessKit，因为它需要自定义 seccomp 配置文件 |

有关排查特定网络问题的信息，请参阅：

- [`docker run -p` 失败并提示 `cannot expose privileged port`](#docker-run--p-fails-with-cannot-expose-privileged-port)
- [Ping 无法工作](#ping-doesnt-work)
- [`docker inspect` 中显示的 `IPAddress` 无法访问](#ipaddress-shown-in-docker-inspect-is-unreachable)
- [`--net=host` 未在主机网络命名空间上监听端口](#--nethost-doesnt-listen-ports-on-the-host-network-namespace)
- [网络缓慢](#network-is-slow)
- [`docker run -p` 不传播源 IP 地址](#docker-run--p-does-not-propagate-source-ip-addresses)

#### `docker run -p` 失败并提示 `cannot expose privileged port`

当指定特权端口 (< 1024) 作为主机端口时，`docker run -p` 会失败并报错。

```console
$ docker run -p 80:80 nginx:alpine
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_swanson (9e2e139a9d8fc92b37c36edfa6214a6e986fa2028c0cc359812f685173fa6df7): Error starting userland proxy: error while calling PortManager.AddPort(): cannot expose privileged port 80, you might need to add "net.ipv4.ip_unprivileged_port_start=0" (currently 1024) to /etc/sysctl.conf, or set CAP_NET_BIND_SERVICE on rootlesskit binary, or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied.
```

当您遇到此错误时，请考虑使用非特权端口。例如，使用 8080 而不是 80。

```console
$ docker run -p 8080:80 nginx:alpine
```

要允许暴露特权端口，请参阅 [暴露特权端口](#exposing-privileged-ports)。

#### Ping 无法工作

当 `/proc/sys/net/ipv4/ping_group_range` 设置为 `1 0` 时，Ping 无法工作：

```console
$ cat /proc/sys/net/ipv4/ping_group_range
1       0
```

有关详情，请参阅 [路由 ping 数据包](#routing-ping-packets)。

#### `docker inspect` 中显示的 `IPAddress` 无法访问

这是预期行为，因为守护进程位于 RootlessKit 的网络命名空间内。请改用 `docker run -p`。

#### `--net=host` 未在主机网络命名空间上监听端口

这是预期行为，因为守护进程位于 RootlessKit 的网络命名空间内。请改用 `docker run -p`。

#### 网络缓慢

如果安装了 slirp4netns v0.4.0 或更高版本，无根模式下的 Docker 默认使用 [slirp4netns](https://github.com/rootless-containers/slirp4netns) 作为网络栈。如果未安装 slirp4netns，Docker 会回退到 [VPNKit](https://github.com/moby/vpnkit)。安装 slirp4netns 可能会提高网络吞吐量。

有关 RootlessKit 网络驱动程序的更多信息，请参阅 [RootlessKit 文档](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)。

此外，更改 MTU 值也可能会提高吞吐量。可以通过创建 `~/.config/systemd/user/docker.service.d/override.conf` 并包含以下内容来指定 MTU 值：

```systemd
[Service]
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_MTU=<INTEGER>"
```

然后重启守护进程：
```console
$ systemctl --user daemon-reload
$ systemctl --user restart docker
```

#### `docker run -p` 不传播源 IP 地址

这是因为无根模式下的 Docker 默认使用 RootlessKit 的 `builtin` 端口驱动程序，该驱动程序不支持源 IP 传播。要启用源 IP 传播，您可以：

- 使用 `slirp4netns` RootlessKit 端口驱动程序
- 使用 `pasta` RootlessKit 网络驱动程序，配合 `implicit` 端口驱动程序

`pasta` 网络驱动程序是实验性的，但与 `slirp4netns` 端口驱动程序相比，它提供了更高的吞吐量性能。`pasta` 驱动程序需要 Docker Engine 25.0 或更高版本。

要更改 RootlessKit 网络配置：

1. 在 `~/.config/systemd/user/docker.service.d/override.conf` 创建一个文件。
2. 根据您想要使用的配置添加以下内容：

   - `slirp4netns`

      ```systemd
      [Service]
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=slirp4netns"
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=slirp4netns"
      ```

   - `pasta` 网络驱动程序配合 `implicit` 端口驱动程序

      ```systemd
      [Service]
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=pasta"
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=implicit"
      ```

3. 重启守护进程：

   ```console
   $ systemctl --user daemon-reload
   $ systemctl --user restart docker
   ```

有关 RootlessKit 联网选项的更多信息，请参阅：

- [网络驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)
- [端口驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/port.md)

### 调试技巧

**进入 `dockerd` 命名空间**

`dockerd-rootless.sh` 脚本在它自己的用户、挂载和网络命名空间中执行 `dockerd`。

为了调试，您可以通过运行以下命令进入这些命名空间：
`nsenter -U --preserve-credentials -n -m -t $(cat $XDG_RUNTIME_DIR/docker.pid)`。
