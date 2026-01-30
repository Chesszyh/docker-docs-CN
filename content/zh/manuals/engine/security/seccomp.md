---
description: 在 Docker 中启用 seccomp
keywords: seccomp, security, docker, documentation, 安全, 文档
title: 适用于 Docker 的 Seccomp 安全配置文件
---

安全计算模式 (`seccomp`) 是 Linux 内核的一项特性。您可以使用它来限制容器内可用的操作。`seccomp()` 系统调用作用于调用进程的 seccomp 状态。您可以使用此功能来限制应用程序的访问权限。

仅当 Docker 在构建时包含了 `seccomp` 支持且内核配置中启用了 `CONFIG_SECCOMP` 时，此功能才可用。检查您的内核是否支持 `seccomp`：

```console
$ grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

## 为容器传递配置文件

默认的 `seccomp` 配置文件为运行带有 seccomp 的容器提供了一个合理的默认值，并在 300 多个系统调用中禁用了大约 44 个。它在提供广泛的应用程序兼容性的同时，提供了适度的保护。默认的 Docker 配置文件可以在 [这里](https://github.com/moby/moby/blob/master/profiles/seccomp/default.json) 找到。

实际上，该配置文件是一个白名单，默认情况下拒绝访问系统调用，然后允许特定的系统调用。该配置文件通过定义 `SCMP_ACT_ERRNO` 的 `defaultAction` 并在仅针对特定系统调用覆盖该操作来工作。`SCMP_ACT_ERRNO` 的效果是导致“权限被拒绝 (Permission Denied)”错误。接下来，配置文件定义了一个完全允许的系统调用的特定列表，因为它们的 `action` 被覆盖为 `SCMP_ACT_ALLOW`。最后，针对 `personality` 等某些系统调用制定了特定规则，以允许具有特定参数的这些系统调用的变体。

`seccomp` 对于以最小特权运行 Docker 容器非常有帮助。不建议更改默认的 `seccomp` 配置文件。

当您运行容器时，除非您使用 `--security-opt` 选项覆盖它，否则它将使用默认配置文件。例如，以下命令显式指定了一个策略：

```console
$ docker run --rm \
             -it \
             --security-opt seccomp=/path/to/seccomp/profile.json \
             hello-world
```

### 默认配置文件阻止的重要系统调用

Docker 的默认 seccomp 配置文件是一个白名单，指定了允许的调用。下表列出了由于不在白名单上而被有效阻止的重要 (但非全部) 系统调用。表中包含了每个系统调用被阻止而不是被列入白名单的原因。

| 系统调用 (Syscall)  | 描述                                                                                                                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `acct`              | 记账系统调用，可能允许容器禁用其自身的资源限制或进程记账。也受 `CAP_SYS_PACCT` 控制。                                                                                                          |
| `add_key`           | 防止容器使用未命名空间化的内核密钥环 (keyring)。                                                                                                                                                                     |
| `bpf`               | 拒绝将潜在持久化的 BPF 程序加载到内核中，已受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                |
| `clock_adjtime`     | 时间/日期未命名空间化。也受 `CAP_SYS_TIME` 控制。                                                                                                                                                                                     |
| `clock_settime`     | 时间/日期未命名空间化。也受 `CAP_SYS_TIME` 控制。                                                                                                                                                                                     |
| `clone`             | 拒绝克隆新的命名空间。对于 CLONE\_\* 标志，除了 `CLONE_NEWUSER` 之外，也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                        |
| `create_module`     | 拒绝在内核模块上进行操作和功能。已过时。也受 `CAP_SYS_MODULE` 控制。                                                                                                                                                   |
| `delete_module`     | 拒绝在内核模块上进行操作和功能。也受 `CAP_SYS_MODULE` 控制。                                                                                                                                                             |
| `finit_module`      | 拒绝在内核模块上进行操作和功能。也受 `CAP_SYS_MODULE` 控制。                                                                                                                                                             |
| `get_kernel_syms`   | 拒绝获取导出的内核和模块符号。已过时。                                                                                                                                                                                |
| `get_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 控制。                                                                                                                                                        |
| `init_module`       | 拒绝在内核模块上进行操作和功能。也受 `CAP_SYS_MODULE` 控制。                                                                                                                                                             |
| `ioperm`            | 防止容器修改内核 I/O 特权级别。已受 `CAP_SYS_RAWIO` 控制。                                                                                                                                               |
| `iopl`              | 防止容器修改内核 I/O 特权级别。已受 `CAP_SYS_RAWIO` 控制。                                                                                                                                               |
| `kcmp`              | 限制进程检查能力，已通过丢弃 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `kexec_file_load`   | 与 `kexec_load` 类似的系统调用，功能相同，参数略有不同。也受 `CAP_SYS_BOOT` 控制。                                                                                                                           |
| `kexec_load`        | 拒绝加载新内核供以后执行。也受 `CAP_SYS_BOOT` 控制。                                                                                                                                                                   |
| `keyctl`            | 防止容器使用未命名空间化的内核密钥环。                                                                                                                                                                     |
| `lookup_dcookie`    | 追踪/性能分析系统调用，可能会泄露主机上的大量信息。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                   |
| `mbind`             | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 控制。                                                                                                                                                        |
| `mount`             | 拒绝挂载，已受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                                               |
| `move_pages`        | 修改内核内存和 NUMA 设置的系统调用。                                                                                                                                                                                         |
| `nfsservctl`        | 拒绝与内核 NFS 守护进程交互。自 Linux 3.1 起已过时。                                                                                                                                                                         |
| `open_by_handle_at` | 曾导致旧版本的容器逃逸。也受 `CAP_DAC_READ_SEARCH` 控制。                                                                                                                                                                       |
| `perf_event_open`   | 追踪/性能分析系统调用，可能会泄露主机上的大量信息。                                                                                                                                                                  |
| `personality`       | 防止容器启用 BSD 仿真。本身并无危险，但测试较少，具有产生大量内核漏洞的潜在风险。                                                                                                     |
| `pivot_root`        | 拒绝 `pivot_root`，应为特权操作。                                                                                                                                                                                             |
| `process_vm_readv`  | 限制进程检查能力，已通过丢弃 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `process_vm_writev` | 限制进程检查能力，已通过丢弃 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `ptrace`            | 追踪/性能分析系统调用。在 4.8 之前的 Linux 内核版本中被阻止，以避免绕过 seccomp。追踪/分析任意进程的操作已通过丢弃 `CAP_SYS_PTRACE` 阻止，因为它可能会泄露主机上的大量信息。 |
| `query_module`      | 拒绝在内核模块上进行操作和功能。已过时。                                                                                                                                                                                   |
| `quotactl`          | 配额系统调用，可能允许容器禁用其自身的资源限制或进程记账。也受 `CAP_SYS_ADMIN` 控制。                                                                                                               |
| `reboot`            | 不允许容器重启主机。也受 `CAP_SYS_BOOT` 控制。                                                                                                                                                                            |
| `request_key`       | 防止容器使用未命名空间化的内核密钥环。                                                                                                                                                                     |
| `set_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 控制。                                                                                                                                                        |
| `setns`             | 拒绝将线程与命名空间关联。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                     |
| `settimeofday`      | 时间/日期未命名空间化。也受 `CAP_SYS_TIME` 控制。                                                                                                                                                                                     |
| `stime`             | 时间/日期未命名空间化。也受 `CAP_SYS_TIME` 控制。                                                                                                                                                                                     |
| `swapon`            | 拒绝开始/停止向文件/设备执行交换。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                        |
| `swapoff`           | 拒绝开始/停止向文件/设备执行交换。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                        |
| `sysfs`             | 已过时的系统调用。                                                                                                                                                                                                                              |
| `_sysctl`           | 已过时，被 /proc/sys 取代。                                                                                                                                                                                                               |
| `umount`            | 应为特权操作。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                               |
| `umount2`           | 应为特权操作。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                               |
| `unshare`           | 拒绝为进程克隆新的命名空间。除了 `unshare --user` 之外，也受 `CAP_SYS_ADMIN` 控制。                                                                                                                              |
| `uselib`            | 与共享库相关的旧系统调用，已长期未使用。                                                                                                                                                                             |
| `userfaultfd`       | 用户空间页错误处理，主要用于进程迁移。                                                                                                                                                                           |
| `ustat`             | 已过时的系统调用。                                                                                                                                                                                                                              |
| `vm86`              | 内核中的 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                        |
| `vm86old`           | 内核中的 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 控制。                                                                                                                                                                        |

## 不使用默认 seccomp 配置文件运行

您可以传递 `unconfined` 来运行不带默认 seccomp 配置文件的容器。

```console
$ docker run --rm -it --security-opt seccomp=unconfined debian:latest \
    unshare --map-root-user --user sh -c whoami
```
