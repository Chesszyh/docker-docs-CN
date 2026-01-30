---
description: 增强容器隔离的优势
title: 主要功能和优势
keywords: set up, enhanced container isolation, rootless, security, features, Docker Desktop
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/features-benefits/
weight: 20
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

## 所有容器上的 Linux 用户命名空间

使用增强容器隔离，所有用户容器都利用 [Linux 用户命名空间](https://man7.org/linux/man-pages/man7/user_namespaces.7.html)来获得额外的隔离。这意味着容器中的 root 用户映射到 Docker Desktop Linux 虚拟机中的非特权用户。

例如：

```console
$ docker run -it --rm --name=first alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

输出 `0 100000 65536` 是 Linux 用户命名空间的签名。它意味着容器中的 root 用户（0）被映射到 Docker Desktop Linux 虚拟机中的非特权用户 100000，并且映射范围扩展了连续的 64K 个用户 ID。同样适用于组 ID。

每个容器获得一个独占的映射范围，由 Sysbox 管理。例如，如果启动第二个容器，映射范围是不同的：

```console
$ docker run -it --rm --name=second alpine
/ # cat /proc/self/uid_map
         0     165536      65536
```

相比之下，没有增强容器隔离时，容器的 root 用户实际上是主机上的 root（又称"真正的 root"），这适用于所有容器：

```console
$ docker run -it --rm alpine
/ # cat /proc/self/uid_map
         0       0     4294967295
```

通过使用 Linux 用户命名空间，增强容器隔离确保容器进程永远不会以用户 ID 0（真正的 root）在 Linux 虚拟机中运行。实际上，它们永远不会以 Linux 虚拟机中的任何有效用户 ID 运行。因此，它们的 Linux capabilities 被限制在容器内的资源，与常规容器相比，无论是容器到主机还是跨容器隔离都显著增强。

## 特权容器也得到保护

特权容器 `docker run --privileged ...` 是不安全的，因为它们使容器完全访问 Linux 内核。也就是说，容器以真正的 root 身份运行，启用所有 capabilities，禁用 seccomp 和 AppArmor 限制，暴露所有硬件设备等。

旨在保护开发人员机器上 Docker Desktop 安全的组织面临特权容器的挑战。这些容器，无论运行良性还是恶意工作负载，都可以控制 Docker Desktop 虚拟机内的 Linux 内核，可能修改与安全相关的设置，例如镜像仓库访问管理和网络代理。

使用增强容器隔离，特权容器不能再这样做。Linux 用户命名空间和 Sysbox 使用的其他安全技术的组合确保特权容器内的进程只能访问分配给容器的资源。

> [!NOTE]
>
> 增强容器隔离不会阻止用户启动特权容器，而是通过确保它们只能修改与容器关联的资源来安全地运行它们。修改全局内核设置的特权工作负载，例如加载内核模块或更改 Berkeley Packet Filters（BPF）设置，将无法正常工作，因为它们在尝试此类操作时会收到"权限被拒绝"错误。

例如，增强容器隔离确保特权容器无法访问通过 BPF 配置的 Linux 虚拟机中的 Docker Desktop 网络设置：

```console
$ docker run --privileged djs55/bpftool map show
Error: can't get next map: Operation not permitted
```

相比之下，没有增强容器隔离，特权容器可以轻松做到这一点：

```console
$ docker run --privileged djs55/bpftool map show
17: ringbuf  name blocked_packets  flags 0x0
        key 0B  value 0B  max_entries 16777216  memlock 0B
18: hash  name allowed_map  flags 0x0
        key 4B  value 4B  max_entries 10000  memlock 81920B
20: lpm_trie  name allowed_trie  flags 0x1
        key 8B  value 8B  max_entries 1024  memlock 16384B
```

请注意，某些高级容器工作负载需要特权容器，例如 Docker-in-Docker、Kubernetes-in-Docker 等。使用增强容器隔离，您仍然可以运行此类工作负载，但比以前安全得多。

## 容器不能与 Linux 虚拟机共享命名空间

启用增强容器隔离后，容器不能与主机共享 Linux 命名空间（例如，PID、network、uts 等），因为这实际上会破坏隔离。

例如，共享 PID 命名空间失败：

```console
$ docker run -it --rm --pid=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share namespaces [pid] with the host (because they use the linux user-namespace for isolation): unknown.
```

同样，共享网络命名空间失败：

```console
$ docker run -it --rm --network=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share a network namespace with the host (because they use the linux user-namespace for isolation): unknown.
```

此外，用于在容器上禁用用户命名空间的 `--userns=host` 标志会被忽略：

```console
$ docker run -it --rm --userns=host alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

最后，Docker build `--network=host` 和 Docker buildx entitlements（`network.host`、`security.insecure`）不允许使用。需要这些的构建将无法正常工作。

## 绑定挂载限制

启用增强容器隔离后，Docker Desktop 用户可以继续将主机目录绑定挂载到容器中，如通过 **Settings** > **Resources** > **File sharing** 配置的那样，但他们不再被允许将任意 Linux 虚拟机目录绑定挂载到容器中。

这可以防止容器修改 Docker Desktop Linux 虚拟机内的敏感文件，这些文件可能包含镜像仓库访问管理、代理、Docker Engine 配置等的配置。

例如，以下将 Docker Engine 的配置文件（Linux 虚拟机内的 `/etc/docker/daemon.json`）绑定挂载到容器中的操作是受限的，因此会失败：

```console
$ docker run -it --rm -v /etc/docker/daemon.json:/mnt/daemon.json alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: can't mount /etc/docker/daemon.json because it's configured as a restricted host mount: unknown
```

相比之下，没有增强容器隔离，此挂载可以工作，并使容器完全读写访问 Docker Engine 的配置。

当然，主机文件的绑定挂载继续正常工作。例如，假设用户配置 Docker Desktop 文件共享她的 `$HOME` 目录，她可以将其绑定挂载到容器中：

```console
$ docker run -it --rm -v $HOME:/mnt alpine
/ #
```

> [!NOTE]
>
> 默认情况下，增强容器隔离不允许将 Docker Engine socket（`/var/run/docker.sock`）绑定挂载到容器中，因为这样做实际上会授予容器对 Docker Engine 的控制权，从而破坏容器隔离。但是，由于某些合法用例需要这样做，可以为受信任的容器镜像放宽此限制。请参阅 [Docker socket 挂载权限](config.md#docker-socket-挂载权限)。

## 审查敏感系统调用

增强容器隔离的另一个功能是它拦截并审查容器内的一些高度敏感的系统调用，如 `mount` 和 `umount`。这确保具有执行这些系统调用能力的进程不能使用它们来突破容器。

例如，具有 `CAP_SYS_ADMIN`（执行 `mount` 系统调用所需）的容器不能使用该能力将只读绑定挂载更改为读写挂载：

```console
$ docker run -it --rm --cap-add SYS_ADMIN -v $HOME:/mnt:ro alpine
/ # mount -o remount,rw /mnt /mnt
mount: permission denied (are you root?)
```

由于 `$HOME` 目录作为只读挂载到容器的 `/mnt` 目录，即使容器进程有能力这样做，也无法从容器内将其更改为读写。这确保容器进程不能使用 `mount` 或 `umount` 来突破容器的根文件系统。

但请注意，在前面的示例中，容器仍然可以在容器内创建挂载，并根据需要以只读或读写方式挂载它们。这些挂载是允许的，因为它们发生在容器内，因此不会突破其根文件系统：

```text
/ # mkdir /root/tmpfs
/ # mount -t tmpfs tmpfs /root/tmpfs
/ # mount -o remount,ro /root/tmpfs /root/tmpfs

/ # findmnt | grep tmpfs
├─/root/tmpfs    tmpfs      tmpfs    ro,relatime,uid=100000,gid=100000

/ # mount -o remount,rw /root/tmpfs /root/tmpfs
/ # findmnt | grep tmpfs
├─/root/tmpfs    tmpfs      tmpfs    rw,relatime,uid=100000,gid=100000
```

此功能与用户命名空间一起，确保即使容器进程拥有所有 Linux capabilities，它们也不能用于突破容器。

最后，增强容器隔离以一种在绑大多数情况下不影响容器性能的方式进行系统调用审查。它拦截在大多数容器工作负载中很少使用的控制路径系统调用，但不拦截数据路径系统调用。

## 文件系统用户 ID 映射

如前所述，ECI 在所有容器上启用 Linux 用户命名空间。这确保容器的用户 ID 范围（0->64K）映射到 Docker Desktop Linux 虚拟机中的非特权"真实"用户 ID 范围（例如，100000->165535）。

此外，每个容器在 Linux 虚拟机中获得一个独占的真实用户 ID 范围（例如，容器 0 可能映射到 100000->165535，容器 2 到 165536->231071，容器 3 到 231072->296607，依此类推）。同样适用于组 ID。此外，如果容器停止并重新启动，不能保证它会收到与之前相同的映射。这是设计使然，进一步提高了安全性。

但是，这在将 Docker 卷挂载到容器中时会产生问题。写入此类卷的文件具有真实的用户/组 ID，因此由于每个容器不同的真实用户 ID/组 ID，它们将无法在容器的启动/停止/重启之间或容器之间访问。

为了解决这个问题，Sysbox 使用"文件系统用户 ID 重映射"，通过 Linux 内核的 ID 映射挂载功能（2021 年添加）或替代的 `shiftsfs` 模块。这些技术将从容器的真实用户 ID（例如，范围 100000->165535）的文件系统访问映射到 Docker Desktop Linux 虚拟机内的范围（0->65535）。这样，即使每个容器使用独占的用户 ID 范围，卷现在也可以在容器之间挂载或共享。用户无需担心容器的真实用户 ID。

尽管文件系统用户 ID 重映射可能导致容器以真实用户 ID 0 访问挂载到容器中的 Linux 虚拟机文件，但[受限挂载功能](#绑定挂载限制)确保敏感的 Linux 虚拟机文件无法挂载到容器中。

## Procfs 和 sysfs 模拟

增强容器隔离的另一个功能是在每个容器内，`/proc` 和 `/sys` 文件系统被部分模拟。这有几个目的，例如在容器内隐藏敏感的主机信息，以及命名空间化尚未被 Linux 内核本身命名空间化的主机内核资源。

作为一个简单的示例，启用增强容器隔离后，`/proc/uptime` 文件显示容器本身的正常运行时间，而不是 Docker Desktop Linux 虚拟机的：

```console
$ docker run -it --rm alpine
/ # cat /proc/uptime
5.86 5.86
```

相比之下，没有增强容器隔离，您会看到 Docker Desktop Linux 虚拟机的正常运行时间。虽然这是一个微不足道的示例，但它展示了增强容器隔离如何旨在防止 Linux 虚拟机的配置和信息泄漏到容器中，以使突破虚拟机更加困难。

此外，`/proc/sys` 下的其他几个未被 Linux 内核命名空间化的资源也在容器内被模拟。每个容器看到每个此类资源的单独视图，Sysbox 在编程相应的 Linux 内核设置时协调容器之间的值。

这样做的优势是使那些否则需要真正特权容器才能访问此类非命名空间化内核资源的容器工作负载能够在启用增强容器隔离的情况下运行，从而提高安全性。
