---
description: Enabling AppArmor in Docker
keywords: AppArmor, security, docker, documentation
title: Docker 的 AppArmor 安全配置文件
---

AppArmor（Application Armor，应用程序防护）是一个 Linux 安全模块，用于保护操作系统及其应用程序免受安全威胁。要使用它，系统管理员需要为每个程序关联一个 AppArmor 安全配置文件。Docker 期望找到一个已加载并强制执行的 AppArmor 策略。

Docker 会自动生成并加载一个名为 `docker-default` 的容器默认配置文件。Docker 二进制文件在 `tmpfs` 中生成此配置文件，然后将其加载到内核中。

> [!NOTE]
>
> 此配置文件用于容器，而不是 Docker 守护进程。

Docker 引擎守护进程的配置文件存在，但目前未随 `deb` 包一起安装。如果你对守护进程配置文件的源代码感兴趣，它位于 Docker 引擎源代码仓库的 [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) 目录中。

## 理解策略

`docker-default` 配置文件是运行容器的默认配置。它提供适度的保护，同时提供广泛的应用程序兼容性。该配置文件从以下[模板](https://github.com/moby/moby/blob/master/profiles/apparmor/template.go)生成。

当你运行容器时，它会使用 `docker-default` 策略，除非你使用 `security-opt` 选项覆盖它。例如，以下命令明确指定默认策略：

```console
$ docker run --rm -it --security-opt apparmor=docker-default hello-world
```

## 加载和卸载配置文件

要将新配置文件加载到 AppArmor 中供容器使用：

```console
$ apparmor_parser -r -W /path/to/your_profile
```

然后，使用 `--security-opt` 运行自定义配置文件：

```console
$ docker run --rm -it --security-opt apparmor=your_profile hello-world
```

要从 AppArmor 卸载配置文件：

```console
# unload the profile
$ apparmor_parser -R /path/to/profile
```

### 编写配置文件的资源

AppArmor 中的文件通配语法与其他一些通配实现略有不同。强烈建议你查看以下有关 AppArmor 配置文件语法的资源。

- [快速配置文件语言](https://gitlab.com/apparmor/apparmor/wikis/QuickProfileLanguage)
- [通配语法](https://gitlab.com/apparmor/apparmor/wikis/AppArmor_Core_Policy_Reference#AppArmor_globbing_syntax)

## Nginx 示例配置文件

在此示例中，你将为 Nginx 创建一个自定义 AppArmor 配置文件。以下是自定义配置文件。

```c
#include <tunables/global>


profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,


  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

1. 将自定义配置文件保存到磁盘上的 `/etc/apparmor.d/containers/docker-nginx` 文件中。

   此示例中的文件路径不是必需的。在生产环境中，你可以使用其他路径。

2. 加载配置文件。

   ```console
   $ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
   ```

3. 使用该配置文件运行容器。

   要以分离模式运行 nginx：

   ```console
   $ docker run --security-opt "apparmor=docker-nginx" \
        -p 80:80 -d --name apparmor-nginx nginx
   ```

4. 进入正在运行的容器。

   ```console
   $ docker container exec -it apparmor-nginx bash
   ```

5. 尝试一些操作来测试配置文件。

   ```console
   root@6da5a2a930b9:~# ping 8.8.8.8
   ping: Lacking privilege for raw socket.

   root@6da5a2a930b9:/# top
   bash: /usr/bin/top: Permission denied

   root@6da5a2a930b9:~# touch ~/thing
   touch: cannot touch 'thing': Permission denied

   root@6da5a2a930b9:/# sh
   bash: /bin/sh: Permission denied

   root@6da5a2a930b9:/# dash
   bash: /bin/dash: Permission denied
   ```


你刚刚部署了一个使用自定义 apparmor 配置文件保护的容器。


## 调试 AppArmor

你可以使用 `dmesg` 调试问题，使用 `aa-status` 检查已加载的配置文件。

### 使用 dmesg

以下是一些有用的技巧，可帮助你调试可能遇到的与 AppArmor 相关的问题。

AppArmor 向 `dmesg` 发送非常详细的消息。通常 AppArmor 日志行如下所示：

```text
[ 5442.864673] audit: type=1400 audit(1453830992.845:37): apparmor="ALLOWED" operation="open" profile="/usr/bin/docker" name="/home/jessie/docker/man/man1/docker-attach.1" pid=10923 comm="docker" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
```

在上面的示例中，你可以看到 `profile=/usr/bin/docker`。这意味着用户加载了 `docker-engine`（Docker 引擎守护进程）配置文件。

查看另一行日志：

```text
[ 3256.689120] type=1400 audit(1405454041.341:73): apparmor="DENIED" operation="ptrace" profile="docker-default" pid=17651 comm="docker" requested_mask="receive" denied_mask="receive"
```

这次配置文件是 `docker-default`，它是默认在容器上运行的配置文件，除非处于 `privileged` 模式。这一行显示 apparmor 拒绝了容器中的 `ptrace`。这正是预期的行为。

### 使用 aa-status

如果你需要检查加载了哪些配置文件，可以使用 `aa-status`。输出如下所示：

```console
$ sudo aa-status
apparmor module is loaded.
14 profiles are loaded.
1 profiles are in enforce mode.
   docker-default
13 profiles are in complain mode.
   /usr/bin/docker
   /usr/bin/docker///bin/cat
   /usr/bin/docker///bin/ps
   /usr/bin/docker///sbin/apparmor_parser
   /usr/bin/docker///sbin/auplink
   /usr/bin/docker///sbin/blkid
   /usr/bin/docker///sbin/iptables
   /usr/bin/docker///sbin/mke2fs
   /usr/bin/docker///sbin/modprobe
   /usr/bin/docker///sbin/tune2fs
   /usr/bin/docker///sbin/xtables-multi
   /usr/bin/docker///sbin/zfs
   /usr/bin/docker///usr/bin/xz
38 processes have profiles defined.
37 processes are in enforce mode.
   docker-default (6044)
   ...
   docker-default (31899)
1 processes are in complain mode.
   /usr/bin/docker (29756)
0 processes are unconfined but have a profile defined.
```

上面的输出显示，在各种容器 PID 上运行的 `docker-default` 配置文件处于 `enforce` 模式。这意味着 AppArmor 正在积极阻止和审计 `dmesg` 中任何超出 `docker-default` 配置文件范围的行为。

上面的输出还显示 `/usr/bin/docker`（Docker 引擎守护进程）配置文件正在 `complain` 模式下运行。这意味着 AppArmor 只将超出配置文件范围的活动记录到 `dmesg`。（Ubuntu Trusty 除外，其中某些有趣的行为是强制执行的。）

## 为 Docker 的 AppArmor 代码做贡献

高级用户和包管理者可以在 Docker 引擎源代码仓库的 [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) 下找到 `/usr/bin/docker`（Docker 引擎守护进程）的配置文件。

容器的 `docker-default` 配置文件位于 [profiles/apparmor](https://github.com/moby/moby/tree/master/profiles/apparmor)。
