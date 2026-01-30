---
title: Docker 守护进程故障排查
description: 了解如何排查 Docker 守护进程中的错误和错误配置
keywords: |
  docker, daemon, configuration, troubleshooting, error, fail to start,
  networking, dns resolver, ip forwarding, dnsmasq, firewall,
  Cannot connect to the Docker daemon. Is 'docker daemon' running on this host?,
  故障排查, 守护进程, 错误, 启动失败, 联网
---

本页介绍了在遇到问题时如何对守护进程进行故障排查和调试。

您可以开启守护进程的调试功能，以了解守护进程的运行时活动并辅助故障排查。如果守护进程无响应，您还可以通过向 Docker 守护进程发送 `SIGUSR` 信号，[强制将所有线程的完整堆栈跟踪](logs.md#force-a-stack-trace-to-be-logged) 添加到守护进程日志中。

## 守护进程 (Daemon)

### 无法连接到 Docker 守护进程

```text
Cannot connect to the Docker daemon. Is 'docker daemon' running on this host?
```

此错误可能表示：

- 您的系统上未运行 Docker 守护进程。启动守护进程并尝试再次运行命令。
- 您的 Docker 客户端正尝试连接到另一台主机上的 Docker 守护进程，且该主机无法访问。

### 检查 Docker 是否正在运行

检查 Docker 是否正在运行且与操作系统无关的方法是向 Docker 询问，使用 `docker info` 命令。

您也可以使用操作系统工具，例如 `sudo systemctl is-active docker` 或 `sudo status docker` 或 `sudo service docker status`，或者使用 Windows 工具检查服务状态。

最后，您可以使用 `ps` 或 `top` 等命令在进程列表中查找 `dockerd` 进程。

#### 检查您的客户端连接到了哪台主机

要查看您的客户端连接到了哪台主机，请检查环境中 `DOCKER_HOST` 变量的值。

```console
$ env | grep DOCKER_HOST
```

如果此命令返回了一个值，则说明 Docker 客户端被设置为连接到运行在该主机上的 Docker 守护进程。如果未设置，则 Docker 客户端被设置为连接到本地主机上运行的 Docker 守护进程。如果设置错误，请使用以下命令取消设置：

```console
$ unset DOCKER_HOST
```

您可能需要编辑 `~/.bashrc` 或 `~/.profile` 等文件中的环境，以防止 `DOCKER_HOST` 变量被错误设置。

如果 `DOCKER_HOST` 设置符合预期，请验证远程主机上是否正在运行 Docker 守护进程，以及是否有防火墙或网络中断阻止了您的连接。

### 排查 `daemon.json` 与启动脚本之间的冲突

如果您使用了 `daemon.json` 文件，同时也手动或使用启动脚本向 `dockerd` 命令传递了选项，且这些选项发生冲突，Docker 将无法启动并报错，例如：

```text
unable to configure the Docker daemon with file /etc/docker/daemon.json:
the following directives are specified both as a flag and in the configuration
file: hosts: (from flag: [unix:///var/run/docker.sock], from file: [tcp://127.0.0.1:2376])
```

如果您看到类似的错误且您是手动带标志启动守护进程的，您可能需要调整您的标志或 `daemon.json` 以消除冲突。

> [!NOTE]
> 
> 如果您看到有关 `hosts` 的这条特定错误消息，请继续阅读 [下一节](#configure-the-daemon-host-with-systemd) 了解解决方法。

如果您是使用操作系统的 init 脚本启动 Docker 的，您可能需要以特定于操作系统的方式覆盖这些脚本中的默认值。

#### 使用 systemd 配置守护进程主机

一个难以排查的配置冲突示例是，当您想要指定一个与默认地址不同的守护进程地址时。Docker 默认监听在套接字 (socket) 上。在使用了 `systemd` 的 Debian 和 Ubuntu 系统上，这意味着启动 `dockerd` 时始终会使用主机标志 `-H`。如果您在 `daemon.json` 中指定了 `hosts` 条目，这会导致配置冲突并导致 Docker 守护进程启动失败。

要解决此问题，请创建一个新文件 `/etc/systemd/system/docker.service.d/docker.conf`，内容如下，以移除默认启动守护进程时使用的 `-H` 参数。

```systemd
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
```

在其他情况下，您可能也需要为 Docker 配置 `systemd`，例如 [配置 HTTP 或 HTTPS 代理](./proxy.md)。

> [!NOTE]
> 
> 如果您覆盖了此选项，但在 `daemon.json` 中没有指定 `hosts` 条目，或者在手动启动 Docker 时没有指定 `-H` 标志，Docker 将无法启动。

在尝试启动 Docker 之前运行 `sudo systemctl daemon-reload`。如果 Docker 启动成功，它现在将监听 `daemon.json` 的 `hosts` 键中指定的 IP 地址，而不是套接字。

> [!IMPORTANT]
> 
> 在 Docker Desktop for Windows 或 Docker Desktop for Mac 上不支持在 `daemon.json` 中设置 `hosts`。

### 内存不足 (OOM) 问题

如果您的容器尝试使用的内存超过了系统可用内存，您可能会遇到内存不足 (Out of Memory, OOM) 异常，容器或 Docker 守护进程可能会被内核 OOM 杀手停止。为了防止这种情况发生，请确保您的应用程序运行在具有充足内存的主机上，并参阅 [了解运行内存不足的风险](../containers/resource_constraints.md#understand-the-risks-of-running-out-of-memory)。

### 内核兼容性

如果您的内核版本早于 3.10，或者缺少内核模块，Docker 无法正常运行。要检查内核兼容性，您可以下载并运行 [`check-config.sh`](https://raw.githubusercontent.com/docker/docker/master/contrib/check-config.sh) 脚本。

```console
$ curl https://raw.githubusercontent.com/docker/docker/master/contrib/check-config.sh > check-config.sh

$ bash ./check-config.sh
```

该脚本仅在 Linux 上运行。

### 内核 cgroup 交换限制能力 (Swap limit capabilities) 

在 Ubuntu 或 Debian 主机上，处理镜像时可能会看到类似于以下的消息。

```text
WARNING: Your kernel does not support swap limit capabilities. Limitation discarded.
```

如果您不需要这些能力，可以忽略该警告。

您可以按照以下说明在 Ubuntu 或 Debian 上启用这些能力。即使 Docker 未运行，内存和交换核算也会产生约 1% 的总可用内存开销和 10% 的整体性能下降。

1. 以具有 `sudo` 特权的用户身份登录 Ubuntu 或 Debian 主机。

2. 编辑 `/etc/default/grub` 文件。添加或编辑 `GRUB_CMDLINE_LINUX` 行以添加以下两个键值对：

   ```text
   GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
   ```

   保存并关闭文件。

3. 更新 GRUB 引导加载程序。

   ```console
   $ sudo update-grub
   ```

   如果您的 GRUB 配置文件语法不正确，则会发生错误。在这种情况下，请重复步骤 2 和 3。

   更改将在重启系统后生效。

## 联网 (Networking)

### IP 转发问题

如果您使用 systemd 219 或更高版本中的 `systemd-network` 手动配置网络，Docker 容器可能无法访问您的网络。从 systemd 版本 220 开始，给定网络 (`net.ipv4.conf.<interface>.forwarding`) 的转发设置默认为关闭。此设置会阻止 IP 转发。它还与 Docker 在容器内启用 `net.ipv4.conf.all.forwarding` 设置的行为冲突。

要在 RHEL、CentOS 或 Fedora 上解决此问题，请编辑 Docker 主机上 `/usr/lib/systemd/network/` 中的 `<interface>.network` 文件，例如 `/usr/lib/systemd/network/80-container-host0.network`。

在 `[Network]` 部分内添加以下代码块：

```systemd
[Network]
... 
IPForward=kernel
# 或者
IPForward=true
```

此配置允许按照预期从容器进行 IP 转发。

### DNS 解析器问题

```console
DNS resolver found in resolv.conf and containers can't use it
```

Linux 桌面环境通常运行有一个网络管理器程序，该程序使用 `dnsmasq` 通过将 DNS 请求添加到 `/etc/resolv.conf` 来缓存它们。`dnsmasq` 实例运行在回环地址上，如 `127.0.0.1` 或 `127.0.1.1`。它可以加快 DNS 查找速度并提供 DHCP 服务。这种配置在 Docker 容器内不起作用。Docker 容器使用自己的网络命名空间，并将 `127.0.0.1` 等回环地址解析为它自己，而它不太可能在自己的回环地址上运行 DNS 服务器。

如果 Docker 检测到 `/etc/resolv.conf` 中引用的 DNS 服务器不是功能完备的 DNS 服务器，则会出现以下警告：

```text
WARNING: Local (127.0.0.1) DNS resolver found in resolv.conf and containers
can't use it. Using default external servers : [8.8.8.8 8.8.4.4]
```

如果您看到此警告，首先检查您是否使用了 `dnsmasq`：

```console
$ ps aux | grep dnsmasq
```

如果您的容器需要解析网络内部的主机，则公共域名服务器是不够的。您有两个选择：

- 指定 Docker 使用的 DNS 服务器。
- 关闭 `dnsmasq`。

  关闭 `dnsmasq` 会将实际 DNS 域名服务器的 IP 地址添加到 `/etc/resolv.conf` 中，但您会失去 `dnsmasq` 的好处。

您只需要使用其中一种方法。

### 为 Docker 指定 DNS 服务器

配置文件的默认位置是 `/etc/docker/daemon.json`。您可以使用 `--config-file` 守护进程标志更改配置文件的位置。以下说明假设配置文件的位置是 `/etc/docker/daemon.json`。

1. 创建或编辑 Docker 守护进程配置文件 (默认为 `/etc/docker/daemon.json`)，该文件控制 Docker 守护进程的配置。

   ```console
   $ sudo nano /etc/docker/daemon.json
   ```

2. 添加一个 `dns` 键，其值为一个或多个 DNS 服务器 IP 地址。

   ```json
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   ```

   如果文件已有内容，您只需要添加或编辑 `dns` 行。如果您的内部 DNS 服务器无法解析公共 IP 地址，请至少包含一个可以解析的 DNS 服务器。这样做可以让您连接到 Docker Hub，并让您的容器解析互联网域名。

   保存并关闭文件。

3. 重启 Docker 守护进程。

   ```console
   $ sudo service docker restart
   ```

4. 通过尝试拉取镜像来验证 Docker 是否可以解析外部 IP 地址：

   ```console
   $ docker pull hello-world
   ```

5. 必要时，通过 ping 内部主机名来验证 Docker 容器是否可以解析它。

   ```console
   $ docker run --rm -it alpine ping -c4 <my_internal_host>

   PING google.com (192.168.1.2): 56 data bytes
   64 bytes from 192.168.1.2: seq=0 ttl=41 time=7.597 ms
   64 bytes from 192.168.1.2: seq=1 ttl=41 time=7.635 ms
   64 bytes from 192.168.1.2: seq=2 ttl=41 time=7.660 ms
   64 bytes from 192.168.1.2: seq=3 ttl=41 time=7.677 ms
   ```

### 关闭 `dnsmasq`

{{< tabs >}}
{{< tab name="Ubuntu" >}}

如果您不想将 Docker 守护进程的配置更改为使用特定的 IP 地址，请按照以下说明在 NetworkManager 中关闭 `dnsmasq`。

1. 编辑 `/etc/NetworkManager/NetworkManager.conf` 文件。

2. 通过在行首添加 `#` 字符来注释掉 `dns=dnsmasq` 行。

   ```text
   # dns=dnsmasq
   ```

   保存并关闭文件。

3. 重启 NetworkManager 和 Docker。或者，您可以重启系统。

   ```console
   $ sudo systemctl restart network-manager
   $ sudo systemctl restart docker
   ```

{{< /tab >}}
{{< tab name="RHEL, CentOS, or Fedora" >}}

要在 RHEL、CentOS 或 Fedora 上关闭 `dnsmasq`：

1. 关闭 `dnsmasq` 服务：

   ```console
   $ sudo systemctl stop dnsmasq
   $ sudo systemctl disable dnsmasq
   ```

2. 参考 [Red Hat 文档](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/configuring-the-order-of-dns-servers_configuring-and-managing-networking) 手动配置 DNS 服务器。

{{< /tab >}}
{{< /tabs >}}

### Docker 网络消失

如果 Docker 网络 (如 `docker0` 网桥或自定义网络) 随机消失或出现运行异常，可能是因为另一个服务正在干扰或修改 Docker 接口。已知管理主机网络接口的工具由于有时会不当地修改 Docker 接口而导致此问题。

根据主机上存在的网络管理工具，请参考以下部分了解如何将网络管理器配置为不管理 Docker 接口：

- 如果安装了 `netscript`，请考虑 [卸载它](#uninstall-netscript)
- 配置网络管理器 [将 Docker 接口视为不管理的](#un-manage-docker-interfaces)
- 如果您使用的是 Netplan，您可能需要 [应用自定义 Netplan 配置](#prevent-netplan-from-overriding-network-configuration)

#### 卸载 `netscript`

如果您的系统上安装了 `netscript`，您很可能可以通过卸载它来修复此问题。例如，在基于 Debian 的系统上：

```console
$ sudo apt-get remove netscript-2.4
```

#### 不管理 Docker 接口

在某些情况下，网络管理器会默认尝试管理 Docker 接口。您可以尝试通过编辑系统的网络配置设置，显式地将 Docker 网络标记为不管理的。

{{< tabs >}}
{{< tab name="NetworkManager" >}}

如果您使用的是 `NetworkManager`，请在 `/etc/network/interfaces` 下编辑系统网络配置。

1. 在 `/etc/network/interfaces.d/20-docker0` 创建一个文件，内容如下：

   ```text
   iface docker0 inet manual
   ```

   注意，此示例配置仅“不管理”默认的 `docker0` 网桥，而不包括自定义网络。

2. 重启 `NetworkManager` 使配置更改生效。

   ```console
   $ systemctl restart NetworkManager
   ```

3. 验证 `docker0` 接口是否处于 `unmanaged` 状态。

   ```console
   $ nmcli device
   ```

{{< /tab >}}
{{< tab name="systemd-networkd" >}}

如果您是在使用 `systemd-networkd` 作为联网守护进程的系统上运行 Docker，请通过在 `/etc/systemd/network` 下创建配置文件，将 Docker 接口配置为不管理的：

1. 创建 `/etc/systemd/network/docker.network`，内容如下：

   ```ini
   # 确保 Docker 接口不被管理

   [Match]
   Name=docker0 br-* veth*

   [Link]
   Unmanaged=yes

   ```

2. 重新加载配置。

   ```console
   $ sudo systemctl restart systemd-networkd
   ```

3. 重启 Docker 守护进程。

   ```console
   $ sudo systemctl restart docker
   ```

4. 验证 Docker 接口是否处于 `unmanaged` 状态。

   ```console
   $ networkctl
   ```

{{< /tab >}}
{{< /tabs >}}

### 防止 Netplan 覆盖网络配置

在通过 [`cloud-init`](https://cloudinit.readthedocs.io/en/latest/index.html) 使用 [Netplan](https://netplan.io/) 的系统上，您可能需要应用自定义配置以防止 `netplan` 覆盖网络管理器配置：

1. 按照 [不管理 Docker 接口](#un-manage-docker-interfaces) 中的步骤创建网络管理器配置。
2. 在 `/etc/netplan/50-cloud-init.yml` 下创建一个 `netplan` 配置文件。

   以下示例配置文件是一个起点。根据您想要不管理的接口对其进行调整。配置不正确可能会导致网络连接问题。

   ```yaml {title="/etc/netplan/50-cloud-init.yml"}
   network:
     ethernets:
       all:
         dhcp4: true
         dhcp6: true
         match:
           # 编辑此过滤器以匹配适合您系统的任何内容
           name: en*
     renderer: networkd
     version: 2
   ```

3. 应用新的 Netplan 配置。

   ```console
   $ sudo netplan apply
   ```

4. 重启 Docker 守护进程：

   ```console
   $ sudo systemctl restart docker
   ```

5. 验证 Docker 接口是否处于 `unmanaged` 状态。

   ```console
   $ networkctl
   ```

## 卷 (Volumes)

### 无法移除文件系统

```text
Error: Unable to remove filesystem
```

一些基于容器的实用程序 (如 [Google cAdvisor](https://github.com/google/cadvisor)) 会将 Docker 系统目录 (如 `/var/lib/docker/`) 挂载到容器中。例如，`cadvisor` 的文档指导您按如下方式运行 `cadvisor` 容器：

```console
$ sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:latest
```

当您绑定挂载 `/var/lib/docker/` 时，这实际上会将所有其他正在运行的容器的所有资源作为文件系统挂载到挂载了 `/var/lib/docker/` 的容器中。当您尝试移除任何这些容器时，移除尝试可能会失败，并出现类似于以下的错误：

```none
Error: Unable to remove filesystem for
74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515: 
remove /var/lib/docker/containers/74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515/shm: 
Device or resource busy
```

如果绑定挂载 `/var/lib/docker/` 的容器对 `/var/lib/docker/` 内的文件系统句柄使用了 `statfs` 或 `fstatfs` 且未关闭它们，就会出现该问题。

通常，我们建议不要以这种方式绑定挂载 `/var/lib/docker`。但是，`cAdvisor` 需要此绑定挂载来实现核心功能。

如果您不确定是哪个进程导致错误中提到的路径处于繁忙状态并阻止其被移除，您可以使用 `lsof` 命令来查找其进程。例如，对于上面的错误：

```console
$ sudo lsof /var/lib/docker/containers/74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515/shm
```

要解决此问题，请停止绑定挂载 `/var/lib/docker` 的容器，然后再次尝试移除另一个容器。

