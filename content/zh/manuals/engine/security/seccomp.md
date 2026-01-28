---
description: Enabling seccomp in Docker
keywords: seccomp, security, docker, documentation
title: Docker 的 Seccomp 安全配置文件
---

安全计算模式（`seccomp`）是一项 Linux 内核功能。你可以使用它来限制容器内可用的操作。`seccomp()` 系统调用对调用进程的 seccomp 状态进行操作。你可以使用此功能来限制应用程序的访问。

此功能仅在 Docker 使用 `seccomp` 构建且内核配置了 `CONFIG_SECCOMP` 启用时可用。要检查你的内核是否支持 `seccomp`：

```console
$ grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

## 为容器传递配置文件

默认的 `seccomp` 配置文件为使用 seccomp 运行容器提供了合理的默认值，并禁用了 300 多个系统调用中的约 44 个。它在提供广泛应用程序兼容性的同时提供适度的保护。默认的 Docker 配置文件可以在[这里](https://github.com/moby/moby/blob/master/profiles/seccomp/default.json)找到。

实际上，该配置文件是一个允许列表，默认拒绝访问系统调用，然后只允许特定的系统调用。该配置文件通过定义 `defaultAction` 为 `SCMP_ACT_ERRNO` 并仅为特定系统调用覆盖该操作来工作。`SCMP_ACT_ERRNO` 的效果是导致 `Permission Denied` 错误。接下来，配置文件定义了一个完全允许的特定系统调用列表，因为它们的 `action` 被覆盖为 `SCMP_ACT_ALLOW`。最后，一些特定规则针对个别系统调用（如 `personality` 等），以允许这些系统调用的特定参数变体。

`seccomp` 对于以最小权限运行 Docker 容器至关重要。不建议更改默认的 `seccomp` 配置文件。

当你运行容器时，它使用默认配置文件，除非你使用 `--security-opt` 选项覆盖它。例如，以下明确指定一个策略：

```console
$ docker run --rm \
             -it \
             --security-opt seccomp=/path/to/seccomp/profile.json \
             hello-world
```

### 默认配置文件阻止的重要系统调用

Docker 的默认 seccomp 配置文件是一个允许列表，指定了允许的调用。下表列出了因不在允许列表中而被有效阻止的重要（但不是全部）系统调用。该表包含每个系统调用被阻止而不是被允许列入白名单的原因。

| 系统调用 | 描述 |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `acct`              | 会计系统调用，可能让容器禁用自己的资源限制或进程会计。也受 `CAP_SYS_PACCT` 限制。 |
| `add_key`           | 防止容器使用内核密钥环，它不是命名空间化的。 |
| `bpf`               | 拒绝将可能持久的 BPF 程序加载到内核中，已受 `CAP_SYS_ADMIN` 限制。 |
| `clock_adjtime`     | 时间/日期不是命名空间化的。也受 `CAP_SYS_TIME` 限制。 |
| `clock_settime`     | 时间/日期不是命名空间化的。也受 `CAP_SYS_TIME` 限制。 |
| `clone`             | 拒绝克隆新命名空间。对于 CLONE\_\* 标志也受 `CAP_SYS_ADMIN` 限制，除了 `CLONE_NEWUSER`。 |
| `create_module`     | 拒绝操作和函数作用于内核模块。已过时。也受 `CAP_SYS_MODULE` 限制。 |
| `delete_module`     | 拒绝操作和函数作用于内核模块。也受 `CAP_SYS_MODULE` 限制。 |
| `finit_module`      | 拒绝操作和函数作用于内核模块。也受 `CAP_SYS_MODULE` 限制。 |
| `get_kernel_syms`   | 拒绝检索导出的内核和模块符号。已过时。 |
| `get_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 限制。 |
| `init_module`       | 拒绝操作和函数作用于内核模块。也受 `CAP_SYS_MODULE` 限制。 |
| `ioperm`            | 防止容器修改内核 I/O 权限级别。已受 `CAP_SYS_RAWIO` 限制。 |
| `iopl`              | 防止容器修改内核 I/O 权限级别。已受 `CAP_SYS_RAWIO` 限制。 |
| `kcmp`              | 限制进程检查能力，已通过删除 `CAP_SYS_PTRACE` 阻止。 |
| `kexec_file_load`   | `kexec_load` 的姐妹系统调用，做同样的事情，参数略有不同。也受 `CAP_SYS_BOOT` 限制。 |
| `kexec_load`        | 拒绝加载新内核以供稍后执行。也受 `CAP_SYS_BOOT` 限制。 |
| `keyctl`            | 防止容器使用内核密钥环，它不是命名空间化的。 |
| `lookup_dcookie`    | 跟踪/分析系统调用，可能泄露大量主机信息。也受 `CAP_SYS_ADMIN` 限制。 |
| `mbind`             | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 限制。 |
| `mount`             | 拒绝挂载，已受 `CAP_SYS_ADMIN` 限制。 |
| `move_pages`        | 修改内核内存和 NUMA 设置的系统调用。 |
| `nfsservctl`        | 拒绝与内核 NFS 守护进程交互。自 Linux 3.1 起已过时。 |
| `open_by_handle_at` | 旧容器逃逸的原因。也受 `CAP_DAC_READ_SEARCH` 限制。 |
| `perf_event_open`   | 跟踪/分析系统调用，可能泄露大量主机信息。 |
| `personality`       | 防止容器启用 BSD 仿真。本身不危险，但测试不充分，可能存在大量内核漏洞。 |
| `pivot_root`        | 拒绝 `pivot_root`，应该是特权操作。 |
| `process_vm_readv`  | 限制进程检查能力，已通过删除 `CAP_SYS_PTRACE` 阻止。 |
| `process_vm_writev` | 限制进程检查能力，已通过删除 `CAP_SYS_PTRACE` 阻止。 |
| `ptrace`            | 跟踪/分析系统调用。在 4.8 之前的 Linux 内核版本中被阻止，以避免 seccomp 绕过。跟踪/分析任意进程已通过删除 `CAP_SYS_PTRACE` 阻止，因为它可能泄露大量主机信息。 |
| `query_module`      | 拒绝操作和函数作用于内核模块。已过时。 |
| `quotactl`          | 配额系统调用，可能让容器禁用自己的资源限制或进程会计。也受 `CAP_SYS_ADMIN` 限制。 |
| `reboot`            | 不让容器重启主机。也受 `CAP_SYS_BOOT` 限制。 |
| `request_key`       | 防止容器使用内核密钥环，它不是命名空间化的。 |
| `set_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已受 `CAP_SYS_NICE` 限制。 |
| `setns`             | 拒绝将线程与命名空间关联。也受 `CAP_SYS_ADMIN` 限制。 |
| `settimeofday`      | 时间/日期不是命名空间化的。也受 `CAP_SYS_TIME` 限制。 |
| `stime`             | 时间/日期不是命名空间化的。也受 `CAP_SYS_TIME` 限制。 |
| `swapon`            | 拒绝开始/停止交换到文件/设备。也受 `CAP_SYS_ADMIN` 限制。 |
| `swapoff`           | 拒绝开始/停止交换到文件/设备。也受 `CAP_SYS_ADMIN` 限制。 |
| `sysfs`             | 已过时的系统调用。 |
| `_sysctl`           | 已过时，被 /proc/sys 替代。 |
| `umount`            | 应该是特权操作。也受 `CAP_SYS_ADMIN` 限制。 |
| `umount2`           | 应该是特权操作。也受 `CAP_SYS_ADMIN` 限制。 |
| `unshare`           | 拒绝为进程克隆新命名空间。也受 `CAP_SYS_ADMIN` 限制，`unshare --user` 例外。 |
| `uselib`            | 与共享库相关的旧系统调用，长时间未使用。 |
| `userfaultfd`       | 用户空间页面错误处理，主要用于进程迁移。 |
| `ustat`             | 已过时的系统调用。 |
| `vm86`              | 内核 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 限制。 |
| `vm86old`           | 内核 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 限制。 |

## 不使用默认 seccomp 配置文件运行

你可以传递 `unconfined` 来运行没有默认 seccomp 配置文件的容器。

```console
$ docker run --rm -it --security-opt seccomp=unconfined debian:latest \
    unshare --map-root-user --user sh -c whoami
```
