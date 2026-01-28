---
description: Run the Docker daemon as a non-root user (Rootless mode)
keywords: security, namespaces, rootless
title: 无根模式
weight: 10
---

无根模式（Rootless mode）允许以非 root 用户身份运行 Docker 守护进程和容器，以缓解守护进程和容器运行时中的潜在漏洞。

无根模式在安装 Docker 守护进程期间也不需要 root 权限，只要满足[先决条件](#prerequisites)即可。

## 工作原理

无根模式在用户命名空间内执行 Docker 守护进程和容器。这与 [`userns-remap` 模式](userns-remap.md)非常相似，不同之处在于使用 `userns-remap` 模式时，守护进程本身以 root 权限运行，而在无根模式下，守护进程和容器都不以 root 权限运行。

无根模式不使用带有 `SETUID` 位或文件能力的二进制文件，除了 `newuidmap` 和 `newgidmap`，这两个命令是允许在用户命名空间中使用多个 UID/GID 所必需的。

## 先决条件

-  你必须在主机上安装 `newuidmap` 和 `newgidmap`。这些命令由大多数发行版上的 `uidmap` 包提供。

- `/etc/subuid` 和 `/etc/subgid` 应该为用户至少包含 65,536 个从属 UID/GID。在以下示例中，用户 `testuser` 拥有 65,536 个从属 UID/GID（231072-296607）。

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

### 发行版特定提示

> [!TIP]
>
> 我们建议你使用 Ubuntu 内核。

{{< tabs >}}
{{< tab name="Ubuntu" >}}
- 如果未安装 `dbus-user-session` 包，请安装它。运行 `sudo apt-get install -y dbus-user-session` 并重新登录。
- 如果未安装 `uidmap` 包，请安装它。运行 `sudo apt-get install -y uidmap`。
- 如果在用户未直接登录的终端中运行，你需要使用 `sudo apt-get install -y systemd-container` 安装 `systemd-container`，然后使用命令 `sudo machinectl shell TheUser@` 切换到 TheUser。

- `overlay2` 存储驱动默认启用（[Ubuntu 特定的内核补丁](https://kernel.ubuntu.com/git/ubuntu/ubuntu-bionic.git/commit/fs/overlayfs?id=3b7da90f28fe1ed4b79ef2d994c81efbc58f1144)）。

- Ubuntu 24.04 及更高版本默认启用受限的非特权用户命名空间，这会阻止非特权进程创建用户命名空间，除非配置了 AppArmor 配置文件以允许程序使用非特权用户命名空间。

  如果你使用 deb 包安装 `docker-ce-rootless-extras`（`apt-get install docker-ce-rootless-extras`），则 `rootlesskit` 的 AppArmor 配置文件已与 `apparmor` deb 包捆绑在一起。使用此安装方法，你不需要添加任何手动 AppArmor 配置。但是，如果你使用[安装脚本](https://get.docker.com/rootless)安装无根附加组件，则必须手动为 `rootlesskit` 添加 AppArmor 配置文件：

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
- 如果未安装 `dbus-user-session` 包，请安装它。运行 `sudo apt-get install -y dbus-user-session` 并重新登录。

- 对于 Debian 11，建议安装 `fuse-overlayfs`。运行 `sudo apt-get install -y fuse-overlayfs`。
  Debian 12 不需要此步骤。

- 无根 docker 需要大于 `v0.4.0` 版本的 `slirp4netns`（当未安装 `vpnkit` 时）。
  使用以下命令检查你是否有此版本

  ```console
  $ slirp4netns --version
  ```
  如果你没有此版本，请使用 `sudo apt-get install -y slirp4netns` 下载并安装，或从最新的 [release](https://github.com/rootless-containers/slirp4netns/releases) 下载。
{{< /tab >}}
{{< tab name="Arch Linux" >}}
- 建议安装 `fuse-overlayfs`。运行 `sudo pacman -S fuse-overlayfs`。

- 在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `kernel.unprivileged_userns_clone=1` 并运行 `sudo sysctl --system`
{{< /tab >}}
{{< tab name="openSUSE and SLES" >}}
- 对于 openSUSE 15 和 SLES 15，建议安装 `fuse-overlayfs`。运行 `sudo zypper install -y fuse-overlayfs`。
  openSUSE Tumbleweed 不需要此步骤。

- 需要执行 `sudo modprobe ip_tables iptable_mangle iptable_nat iptable_filter`。
  根据配置，其他发行版可能也需要此操作。

- 已知在 openSUSE 15 和 SLES 15 上可用。
{{< /tab >}}
{{< tab name="CentOS, RHEL, and Fedora" >}}
- 对于 RHEL 8 和类似发行版，建议安装 `fuse-overlayfs`。运行 `sudo dnf install -y fuse-overlayfs`。
  RHEL 9 和类似发行版不需要此步骤。

- 你可能需要 `sudo dnf install -y iptables`。
{{< /tab >}}
{{< /tabs >}}

## 已知限制

- 仅支持以下存储驱动：
  - `overlay2`（仅当运行内核 5.11 或更高版本，或 Ubuntu 风格内核时）
  - `fuse-overlayfs`（仅当运行内核 4.18 或更高版本，且已安装 `fuse-overlayfs` 时）
  - `btrfs`（仅当运行内核 4.18 或更高版本，或 `~/.local/share/docker` 以 `user_subvol_rm_allowed` 挂载选项挂载时）
  - `vfs`
- 仅当使用 cgroup v2 和 systemd 运行时才支持 Cgroup。参见[限制资源](#limiting-resources)。
- 不支持以下功能：
  - AppArmor
  - Checkpoint
  - Overlay 网络
  - 暴露 SCTP 端口
- 要使用 `ping` 命令，请参见[路由 ping 数据包](#routing-ping-packets)。
- 要暴露特权 TCP/UDP 端口（< 1024），请参见[暴露特权端口](#exposing-privileged-ports)。
- `docker inspect` 中显示的 `IPAddress` 是在 RootlessKit 的网络命名空间内的命名空间地址。
  这意味着如果不使用 `nsenter` 进入网络命名空间，该 IP 地址无法从主机访问。
- 主机网络（`docker run --net=host`）也是在 RootlessKit 内的命名空间中。
- 不支持将 NFS 挂载用作 docker 的"data-root"。此限制不是无根模式特有的。

## 安装

> [!NOTE]
>
> 如果系统级 Docker 守护进程已在运行，请考虑禁用它：
>```console
>$ sudo systemctl disable --now docker.service docker.socket
>$ sudo rm /var/run/docker.sock
>```
> 如果你选择不关闭 `docker` 服务和套接字，你将需要在下一节中使用 `--force`
> 参数。没有已知问题，但在你关闭并禁用之前，你仍在运行有根 Docker。

{{< tabs >}}
{{< tab name="With packages (RPM/DEB)" >}}

如果你使用 [RPM/DEB 包](/engine/install)安装了 Docker 20.10 或更高版本，你应该在 `/usr/bin` 中有 `dockerd-rootless-setuptool.sh`。

以非 root 用户身份运行 `dockerd-rootless-setuptool.sh install` 来设置守护进程：

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

如果 `dockerd-rootless-setuptool.sh` 不存在，你可能需要手动安装 `docker-ce-rootless-extras` 包，例如：

```console
$ sudo apt-get install -y docker-ce-rootless-extras
```

{{< /tab >}}
{{< tab name="Without packages" >}}

如果你没有权限运行包管理器如 `apt-get` 和 `dnf`，请考虑使用 [https://get.docker.com/rootless](https://get.docker.com/rootless) 上提供的安装脚本。
由于静态包不适用于 `s390x`，因此 `s390x` 不受支持。

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

二进制文件将安装在 `~/bin`。

{{< /tab >}}
{{< /tabs >}}

如果遇到错误，请参见[故障排除](#troubleshooting)。

## 卸载

要删除 Docker 守护进程的 systemd 服务，请运行 `dockerd-rootless-setuptool.sh uninstall`：

```console
$ dockerd-rootless-setuptool.sh uninstall
+ systemctl --user stop docker.service
+ systemctl --user disable docker.service
Removed /home/testuser/.config/systemd/user/default.target.wants/docker.service.
[INFO] Uninstalled docker.service
[INFO] This uninstallation tool does NOT remove Docker binaries and data.
[INFO] To remove data, run: `/usr/bin/rootlesskit rm -rf /home/testuser/.local/share/docker`
```

如果你已将 PATH 和 DOCKER_HOST 环境变量添加到 `~/.bashrc`，请取消设置它们。

要删除数据目录，请运行 `rootlesskit rm -rf ~/.local/share/docker`。

要删除二进制文件，如果你使用包管理器安装 Docker，请删除 `docker-ce-rootless-extras` 包。
如果你使用 https://get.docker.com/rootless 安装 Docker（[不使用包安装](#install)），请删除 `~/bin` 下的二进制文件：
```console
$ cd ~/bin
$ rm -f containerd containerd-shim containerd-shim-runc-v2 ctr docker docker-init docker-proxy dockerd dockerd-rootless-setuptool.sh dockerd-rootless.sh rootlesskit rootlesskit-docker-proxy runc vpnkit
```

## 使用

### 守护进程

{{< tabs >}}
{{< tab name="With systemd (Highly recommended)" >}}

systemd 单元文件安装在 `~/.config/systemd/user/docker.service`。

使用 `systemctl --user` 管理守护进程的生命周期：

```console
$ systemctl --user start docker
```

要在系统启动时启动守护进程，请启用 systemd 服务和 lingering：

```console
$ systemctl --user enable docker
$ sudo loginctl enable-linger $(whoami)
```

不支持将无根 Docker 作为系统级服务（`/etc/systemd/system/docker.service`）启动，即使使用 `User=` 指令也不行。

{{< /tab >}}
{{< tab name="Without systemd" >}}

要在没有 systemd 的情况下直接运行守护进程，你需要运行 `dockerd-rootless.sh` 而不是 `dockerd`。

必须设置以下环境变量：
- `$HOME`：主目录
- `$XDG_RUNTIME_DIR`：仅对预期用户可访问的临时目录，例如 `~/.docker/run`。
  该目录应在每次主机关机时删除。
  该目录可以在 tmpfs 上，但不应在 `/tmp` 下。
  将此目录放在 `/tmp` 下可能容易受到 TOCTOU 攻击。

{{< /tab >}}
{{< /tabs >}}

关于目录路径的说明：

- 套接字路径默认设置为 `$XDG_RUNTIME_DIR/docker.sock`。
  `$XDG_RUNTIME_DIR` 通常设置为 `/run/user/$UID`。
- 数据目录默认设置为 `~/.local/share/docker`。
  数据目录不应在 NFS 上。
- 守护进程配置目录默认设置为 `~/.config/docker`。
  此目录与客户端使用的 `~/.docker` 不同。

### 客户端

你需要明确指定套接字路径或 CLI 上下文。

要使用 `$DOCKER_HOST` 指定套接字路径：

```console
$ export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
$ docker run -d -p 8080:80 nginx
```

要使用 `docker context` 指定 CLI 上下文：

```console
$ docker context use rootless
rootless
Current context is now "rootless"
$ docker run -d -p 8080:80 nginx
```

## 最佳实践

### Docker 中的无根 Docker

要在"有根"Docker 中运行无根 Docker，请使用 `docker:<version>-dind-rootless` 镜像而不是 `docker:<version>-dind`。

```console
$ docker run -d --name dind-rootless --privileged docker:25.0-dind-rootless
```

`docker:<version>-dind-rootless` 镜像以非 root 用户（UID 1000）运行。但是，需要 `--privileged` 来禁用 seccomp、AppArmor 和挂载掩码。

### 通过 TCP 暴露 Docker API 套接字

要通过 TCP 暴露 Docker API 套接字，你需要使用 `DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp"` 启动 `dockerd-rootless.sh`。

```console
$ DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp" \
  dockerd-rootless.sh \
  -H tcp://0.0.0.0:2376 \
  --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem
```

### 通过 SSH 暴露 Docker API 套接字

要通过 SSH 暴露 Docker API 套接字，你需要确保在远程主机上设置了 `$DOCKER_HOST`。

```console
$ ssh -l <REMOTEUSER> <REMOTEHOST> 'echo $DOCKER_HOST'
unix:///run/user/1001/docker.sock
$ docker -H ssh://<REMOTEUSER>@<REMOTEHOST> run ...
```

### 路由 ping 数据包

在某些发行版上，`ping` 默认不工作。

在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `net.ipv4.ping_group_range = 0   2147483647` 并运行 `sudo sysctl --system` 以允许使用 `ping`。

### 暴露特权端口

要暴露特权端口（< 1024），请在 `rootlesskit` 二进制文件上设置 `CAP_NET_BIND_SERVICE` 并重启守护进程。

```console
$ sudo setcap cap_net_bind_service=ep $(which rootlesskit)
$ systemctl --user restart docker
```

或者在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `net.ipv4.ip_unprivileged_port_start=0` 并运行 `sudo sysctl --system`。

### 限制资源

使用与 cgroup 相关的 `docker run` 标志（如 `--cpus`、`--memory`、`--pids-limit`）限制资源仅在使用 cgroup v2 和 systemd 运行时才支持。
参见[更改 cgroup 版本](/manuals/engine/containers/runmetrics.md)以启用 cgroup v2。

如果 `docker info` 显示 `Cgroup Driver` 为 `none`，则不满足条件。
当这些条件不满足时，无根模式会忽略与 cgroup 相关的 `docker run` 标志。
参见[不使用 cgroup 限制资源](#limiting-resources-without-cgroup)以获取解决方法。

如果 `docker info` 显示 `Cgroup Driver` 为 `systemd`，则满足条件。
但是，通常默认情况下只有 `memory` 和 `pids` 控制器被委托给非 root 用户。

```console
$ cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.controllers
memory pids
```

要允许委托所有控制器，你需要按以下方式更改 systemd 配置：

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

即使 cgroup 不可用，你仍然可以使用传统的 `ulimit` 和 [`cpulimit`](https://github.com/opsengine/cpulimit)，尽管它们以进程粒度而不是容器粒度工作，并且可以被容器进程任意禁用。

例如：

- 要将 CPU 使用限制为 0.5 核（类似于 `docker run --cpus 0.5`）：
  `docker run <IMAGE> cpulimit --limit=50 --include-children <COMMAND>`
- 要将最大 VSZ 限制为 64MiB（类似于 `docker run --memory 64m`）：
  `docker run <IMAGE> sh -c "ulimit -v 65536; <COMMAND>"`

- 要将每个命名空间 UID 2000 的最大进程数限制为 100（类似于 `docker run --pids-limit=100`）：
  `docker run --user 2000 --ulimit nproc=100 <IMAGE> <COMMAND>`

## 故障排除

### 当系统上存在 systemd 时无法使用 systemd 安装

``` console
$ dockerd-rootless-setuptool.sh install
[INFO] systemd not detected, dockerd-rootless.sh needs to be started manually:
...
```
如果你通过 `sudo su` 切换到你的用户，`rootlesskit` 无法正确检测 systemd。对于无法登录的用户，你必须使用 `machinectl` 命令，它是 `systemd-container` 包的一部分。安装 `systemd-container` 后，使用以下命令切换到 `myuser`：
``` console
$ sudo machinectl shell myuser@
```
其中 `myuser@` 是你想要的用户名，@ 表示此机器。

### 启动 Docker 守护进程时的错误

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted**

当 `/proc/sys/kernel/unprivileged_userns_clone` 的值设置为 0 时，通常会发生此错误：

```console
$ cat /proc/sys/kernel/unprivileged_userns_clone
0
```

要解决此问题，请在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `kernel.unprivileged_userns_clone=1` 并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: no space left on device**

当 `/proc/sys/user/max_user_namespaces` 的值太小时，通常会发生此错误：

```console
$ cat /proc/sys/user/max_user_namespaces
0
```

要解决此问题，请在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `user.max_user_namespaces=28633` 并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to setup UID/GID map: failed to compute uid/gid map: No subuid ranges found for user 1001 ("testuser")**

当 `/etc/subuid` 和 `/etc/subgid` 未配置时会发生此错误。参见[先决条件](#prerequisites)。

**could not get XDG_RUNTIME_DIR**

当 `$XDG_RUNTIME_DIR` 未设置时会发生此错误。

在非 systemd 主机上，你需要创建一个目录然后设置路径：

```console
$ export XDG_RUNTIME_DIR=$HOME/.docker/xrd
$ rm -rf $XDG_RUNTIME_DIR
$ mkdir -p $XDG_RUNTIME_DIR
$ dockerd-rootless.sh
```

> [!NOTE]
>
> 你必须在每次注销时删除该目录。

在 systemd 主机上，使用 `pam_systemd` 登录主机（见下文）。
该值会自动设置为 `/run/user/$UID` 并在每次注销时清理。

**`systemctl --user` fails with "Failed to connect to bus: No such file or directory"**

当你使用 `sudo` 从 root 用户切换到非 root 用户时，通常会发生此错误：

```console
# sudo -iu testuser
$ systemctl --user start docker
Failed to connect to bus: No such file or directory
```

不要使用 `sudo -iu <USERNAME>`，你需要使用 `pam_systemd` 登录。例如：

- 通过图形控制台登录
- `ssh <USERNAME>@localhost`
- `machinectl shell <USERNAME>@`

**守护进程不会自动启动**

你需要 `sudo loginctl enable-linger $(whoami)` 来启用守护进程自动启动。参见[使用](#usage)。

**iptables failed: iptables -t nat -N DOCKER: Fatal: can't open lock file /run/xtables.lock: Permission denied**

当主机上启用 SELinux 时，较旧版本的 Docker 可能会发生此错误。

该问题已在 Docker 20.10.8 中修复。
较旧版本的 Docker 的已知解决方法是运行以下命令来禁用 `iptables` 的 SELinux：
```console
$ sudo dnf install -y policycoreutils-python-utils && sudo semanage permissive -a iptables_t
```

### `docker pull` 错误

**docker: failed to register layer: Error processing tar file(exit status 1): lchown &lt;FILE&gt;: invalid argument**

当 `/etc/subuid` 或 `/etc/subgid` 中可用条目数量不足时会发生此错误。所需条目数量因镜像而异。但是，65,536 个条目对于大多数镜像来说是足够的。参见[先决条件](#prerequisites)。

**docker: failed to register layer: ApplyLayer exit status 1 stdout:  stderr: lchown &lt;FILE&gt;: operation not permitted**

当 `~/.local/share/docker` 位于 NFS 上时，通常会发生此错误。

解决方法是在 `~/.config/docker/daemon.json` 中指定非 NFS 的 `data-root` 目录，如下所示：
```json
{"data-root":"/somewhere-out-of-nfs"}
```

### `docker run` 错误

**docker: Error response from daemon: OCI runtime create failed: ...: read unix @-&gt;/run/systemd/private: read: connection reset by peer: unknown.**

在 cgroup v2 主机上，当 dbus 守护进程未为用户运行时，通常会发生此错误。

```console
$ systemctl --user is-active dbus
inactive

$ docker run hello-world
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:385: applying cgroup configuration for process caused: error while starting unit "docker
-931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e.scope" with properties [{Name:Description Value:"libcontainer container 931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e"} {Name:Slice Value:"use
r.slice"} {Name:PIDs Value:@au [4529]} {Name:Delegate Value:true} {Name:MemoryAccounting Value:true} {Name:CPUAccounting Value:true} {Name:IOAccounting Value:true} {Name:TasksAccounting Value:true} {Name:DefaultDependencies Val
ue:false}]: read unix @->/run/systemd/private: read: connection reset by peer: unknown.
```

要解决此问题，请运行 `sudo apt-get install -y dbus-user-session` 或 `sudo dnf install -y dbus-daemon`，然后重新登录。

如果错误仍然发生，请尝试运行 `systemctl --user enable --now dbus`（不带 sudo）。

**`--cpus`、`--memory` 和 `--pids-limit` 被忽略**

这是 cgroup v1 模式下的预期行为。
要使用这些标志，需要将主机配置为启用 cgroup v2。
有关更多信息，请参见[限制资源](#limiting-resources)。

### 网络错误

本节提供无根模式下网络的故障排除技巧。

无根模式下的网络通过 RootlessKit 中的网络和端口驱动程序支持。网络性能和特性取决于你使用的网络和端口驱动程序的组合。如果你遇到与网络相关的意外行为或性能问题，请查看以下表格，该表格显示了 RootlessKit 支持的配置及其比较：

| 网络驱动 | 端口驱动 | 网络吞吐量 | 端口吞吐量 | 源 IP 传播 | 无 SUID | 备注 |
| -------------- | -------------- | -------------- | --------------- | --------------------- | ------- | ---------------------------------------------------------------------------- |
| `slirp4netns`  | `builtin`      | 慢           | 快 ✅         | ❌                    | ✅      | 典型设置中的默认值 |
| `vpnkit`       | `builtin`      | 慢           | 快 ✅         | ❌                    | ✅      | 当未安装 `slirp4netns` 时的默认值 |
| `slirp4netns`  | `slirp4netns`  | 慢           | 慢            | ✅                    | ✅      |                                                                              |
| `pasta`        | `implicit`     | 慢           | 快 ✅         | ✅                    | ✅      | 实验性；需要 pasta 版本 2023_12_04 或更高版本 |
| `lxc-user-nic` | `builtin`      | 快 ✅        | 快 ✅         | ❌                    | ❌      | 实验性 |
| `bypass4netns` | `bypass4netns` | 快 ✅        | 快 ✅         | ✅                    | ✅      | **注意：**未集成到 RootlessKit，因为它需要自定义 seccomp 配置文件 |

有关特定网络问题的故障排除信息，请参见：

- [`docker run -p` 失败并显示 `cannot expose privileged port`](#docker-run--p-fails-with-cannot-expose-privileged-port)
- [Ping 不工作](#ping-doesnt-work)
- [`docker inspect` 中显示的 `IPAddress` 不可访问](#ipaddress-shown-in-docker-inspect-is-unreachable)
- [`--net=host` 不在主机网络命名空间上监听端口](#--nethost-doesnt-listen-ports-on-the-host-network-namespace)
- [网络慢](#network-is-slow)
- [`docker run -p` 不传播源 IP 地址](#docker-run--p-does-not-propagate-source-ip-addresses)

#### `docker run -p` 失败并显示 `cannot expose privileged port`

当指定特权端口（< 1024）作为主机端口时，`docker run -p` 会失败并显示此错误。

```console
$ docker run -p 80:80 nginx:alpine
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_swanson (9e2e139a9d8fc92b37c36edfa6214a6e986fa2028c0cc359812f685173fa6df7): Error starting userland proxy: error while calling PortManager.AddPort(): cannot expose privileged port 80, you might need to add "net.ipv4.ip_unprivileged_port_start=0" (currently 1024) to /etc/sysctl.conf, or set CAP_NET_BIND_SERVICE on rootlesskit binary, or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied.
```

遇到此错误时，请考虑使用非特权端口代替。例如，使用 8080 代替 80。

```console
$ docker run -p 8080:80 nginx:alpine
```

要允许暴露特权端口，请参见[暴露特权端口](#exposing-privileged-ports)。

#### Ping 不工作

当 `/proc/sys/net/ipv4/ping_group_range` 设置为 `1 0` 时，ping 不工作：

```console
$ cat /proc/sys/net/ipv4/ping_group_range
1       0
```

有关详细信息，请参见[路由 ping 数据包](#routing-ping-packets)。

#### `docker inspect` 中显示的 `IPAddress` 不可访问

这是预期行为，因为守护进程在 RootlessKit 的网络命名空间内命名空间化。请改用 `docker run -p`。

#### `--net=host` 不在主机网络命名空间上监听端口

这是预期行为，因为守护进程在 RootlessKit 的网络命名空间内命名空间化。请改用 `docker run -p`。

#### 网络慢

如果安装了 slirp4netns v0.4.0 或更高版本，无根模式下的 Docker 使用 [slirp4netns](https://github.com/rootless-containers/slirp4netns) 作为默认网络栈。
如果未安装 slirp4netns，Docker 会回退到 [VPNKit](https://github.com/moby/vpnkit)。
安装 slirp4netns 可能会提高网络吞吐量。

有关 RootlessKit 网络驱动程序的更多信息，请参见 [RootlessKit 文档](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)。

此外，更改 MTU 值可能会提高吞吐量。
可以通过创建具有以下内容的 `~/.config/systemd/user/docker.service.d/override.conf` 来指定 MTU 值：

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

这是因为无根模式下的 Docker 默认使用 RootlessKit 的 `builtin` 端口驱动程序，它不支持源 IP 传播。要启用源 IP 传播，你可以：

- 使用 `slirp4netns` RootlessKit 端口驱动程序
- 使用 `pasta` RootlessKit 网络驱动程序，配合 `implicit` 端口驱动程序

`pasta` 网络驱动程序是实验性的，但与 `slirp4netns` 端口驱动程序相比提供了改进的吞吐量性能。`pasta` 驱动程序需要 Docker Engine 版本 25.0 或更高版本。

要更改 RootlessKit 网络配置：

1. 在 `~/.config/systemd/user/docker.service.d/override.conf` 创建一个文件。
2. 根据你想要使用的配置添加以下内容：

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

有关 RootlessKit 网络选项的更多信息，请参见：

- [网络驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)
- [端口驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/port.md)

### 调试技巧

**进入 `dockerd` 命名空间**

`dockerd-rootless.sh` 脚本在其自己的用户、挂载和网络命名空间中执行 `dockerd`。

为了调试，你可以通过运行 `nsenter -U --preserve-credentials -n -m -t $(cat $XDG_RUNTIME_DIR/docker.pid)` 进入命名空间。
