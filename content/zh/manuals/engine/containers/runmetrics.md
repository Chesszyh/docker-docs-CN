---
description: 了解如何测量运行中的容器，以及不同的指标
keywords: docker, metrics, CPU, memory, disk, IO, run, runtime, stats
title: 运行时指标
weight: 50
aliases:
  - /articles/runmetrics/
  - /engine/articles/run_metrics/
  - /engine/articles/runmetrics/
  - /engine/admin/runmetrics/
  - /config/containers/runmetrics/
---

## Docker stats

您可以使用 `docker stats` 命令实时流式传输容器的运行时指标。该命令支持 CPU、内存使用量、内存限制和网络 I/O 指标。

以下是 `docker stats` 命令的示例输出

```console
$ docker stats redis1 redis2

CONTAINER           CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O
redis1              0.07%               796 KB / 64 MB        1.21%               788 B / 648 B       3.568 MB / 512 KB
redis2              0.07%               2.746 MB / 64 MB      4.29%               1.266 KB / 648 B    12.4 MB / 0 B
```

[`docker stats`](/reference/cli/docker/container/stats.md) 参考页面提供了有关 `docker stats` 命令的更多详细信息。

## 控制组（Control groups）

Linux 容器依赖于[控制组](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt)，它不仅跟踪进程组，还暴露有关 CPU、内存和块 I/O 使用情况的指标。您可以访问这些指标并获取网络使用指标。这适用于"纯" LXC 容器以及 Docker 容器。

控制组通过伪文件系统暴露。在现代发行版中，您应该在 `/sys/fs/cgroup` 下找到此文件系统。在该目录下，您会看到多个子目录，称为 `devices`、`freezer`、`blkio` 等。每个子目录实际上对应于不同的 cgroup 层次结构。

在旧系统上，控制组可能挂载在 `/cgroup` 上，没有明确的层次结构。在这种情况下，您看到的不是子目录，而是该目录中的一堆文件，可能还有一些对应于现有容器的目录。

要找出控制组的挂载位置，您可以运行：

```console
$ grep cgroup /proc/mounts
```

### 枚举 cgroups

cgroups 的文件布局在 v1 和 v2 之间有很大差异。

如果您的系统上存在 `/sys/fs/cgroup/cgroup.controllers`，则您使用的是 v2，否则使用的是 v1。请参阅与您的 cgroup 版本对应的子节。

以下发行版默认使用 cgroup v2：

- Fedora（自版本 31 起）
- Debian GNU/Linux（自版本 11 起）
- Ubuntu（自版本 21.10 起）

#### cgroup v1

您可以查看 `/proc/cgroups` 以查看系统已知的不同控制组子系统、它们所属的层次结构以及它们包含多少个组。

您还可以查看 `/proc/<pid>/cgroup` 以查看进程属于哪些控制组。控制组显示为相对于层次结构挂载点的路径。`/` 表示进程未被分配到某个组，而 `/lxc/pumpkin` 表示进程是名为 `pumpkin` 的容器的成员。

#### cgroup v2

在 cgroup v2 主机上，`/proc/cgroups` 的内容没有意义。请查看 `/sys/fs/cgroup/cgroup.controllers` 以获取可用的控制器。

### 更改 cgroup 版本

更改 cgroup 版本需要重新启动整个系统。

在基于 systemd 的系统上，可以通过在内核命令行中添加 `systemd.unified_cgroup_hierarchy=1` 来启用 cgroup v2。要将 cgroup 版本恢复为 v1，您需要将其设置为 `systemd.unified_cgroup_hierarchy=0`。

如果您的系统上有 `grubby` 命令可用（例如在 Fedora 上），可以按如下方式修改命令行：

```console
$ sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
```

如果 `grubby` 命令不可用，请编辑 `/etc/default/grub` 中的 `GRUB_CMDLINE_LINUX` 行并运行 `sudo update-grub`。

### 在 cgroup v2 上运行 Docker

Docker 自 Docker 20.10 起支持 cgroup v2。在 cgroup v2 上运行 Docker 还需要满足以下条件：

- containerd：v1.4 或更高版本
- runc：v1.0.0-rc91 或更高版本
- 内核：v4.15 或更高版本（建议使用 v5.2 或更高版本）

请注意，cgroup v2 模式的行为与 cgroup v1 模式略有不同：

- 默认 cgroup 驱动程序（`dockerd --exec-opt native.cgroupdriver`）在 v2 上是 `systemd`，在 v1 上是 `cgroupfs`。
- 默认 cgroup 命名空间模式（`docker run --cgroupns`）在 v2 上是 `private`，在 v1 上是 `host`。
- `docker run` 标志 `--oom-kill-disable` 和 `--kernel-memory` 在 v2 上被忽略。

### 查找给定容器的 cgroup

对于每个容器，在每个层次结构中都会创建一个 cgroup。在使用旧版本 LXC 用户空间工具的旧系统上，cgroup 的名称是容器的名称。使用更新版本的 LXC 工具，cgroup 是 `lxc/<container_name>`。

对于使用 cgroups 的 Docker 容器，cgroup 名称是容器的完整 ID 或长 ID。如果一个容器在 `docker ps` 中显示为 ae836c95b4c3，其长 ID 可能类似于 `ae836c95b4c3c9e9179e0e91015512da89fdec91612f63cebae57df9a5444c79`。您可以使用 `docker inspect` 或 `docker ps --no-trunc` 查找它。

将所有内容放在一起查看 Docker 容器的内存指标，请查看以下路径：

- `/sys/fs/cgroup/memory/docker/<longid>/`：cgroup v1，`cgroupfs` 驱动程序
- `/sys/fs/cgroup/memory/system.slice/docker-<longid>.scope/`：cgroup v1，`systemd` 驱动程序
- `/sys/fs/cgroup/docker/<longid>/`：cgroup v2，`cgroupfs` 驱动程序
- `/sys/fs/cgroup/system.slice/docker-<longid>.scope/`：cgroup v2，`systemd` 驱动程序

### 来自 cgroups 的指标：内存、CPU、块 I/O

> [!NOTE]
>
> 本节尚未针对 cgroup v2 更新。有关 cgroup v2 的更多信息，请参阅[内核文档](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)。

对于每个子系统（内存、CPU 和块 I/O），存在一个或多个包含统计信息的伪文件。

#### 内存指标：`memory.stat`

内存指标位于 `memory` cgroup 中。内存控制组会增加一些开销，因为它对主机上的内存使用进行非常细粒度的记账。因此，许多发行版默认选择不启用它。通常，要启用它，您只需添加一些内核命令行参数：`cgroup_enable=memory swapaccount=1`。

指标位于伪文件 `memory.stat` 中。以下是它的样子：

    cache 11492564992
    rss 1930993664
    mapped_file 306728960
    pgpgin 406632648
    pgpgout 403355412
    swap 0
    pgfault 728281223
    pgmajfault 1724
    inactive_anon 46608384
    active_anon 1884520448
    inactive_file 7003344896
    active_file 4489052160
    unevictable 32768
    hierarchical_memory_limit 9223372036854775807
    hierarchical_memsw_limit 9223372036854775807
    total_cache 11492564992
    total_rss 1930993664
    total_mapped_file 306728960
    total_pgpgin 406632648
    total_pgpgout 403355412
    total_swap 0
    total_pgfault 728281223
    total_pgmajfault 1724
    total_inactive_anon 46608384
    total_active_anon 1884520448
    total_inactive_file 7003344896
    total_active_file 4489052160
    total_unevictable 32768

前半部分（没有 `total_` 前缀）包含与 cgroup 内进程相关的统计信息，不包括子 cgroups。后半部分（带有 `total_` 前缀）也包括子 cgroups。

一些指标是"计量器"，即可以增加或减少的值。例如，`swap` 是 cgroup 成员使用的交换空间量。另一些是"计数器"，即只能增加的值，因为它们代表特定事件的发生次数。例如，`pgfault` 表示自 cgroup 创建以来的页面错误数量。

`cache`
: 此控制组进程使用的内存量，可以精确地与块设备上的块关联。当您从磁盘读取和写入文件时，此数量会增加。如果您使用"传统" I/O（`open`、`read`、`write` 系统调用）以及映射文件（使用 `mmap`），都会是这种情况。它还计算 `tmpfs` 挂载使用的内存，尽管原因不明确。

`rss`
: 不对应磁盘上任何内容的内存量：堆栈、堆和匿名内存映射。

`mapped_file`
: 表示控制组中进程映射的内存量。它不会告诉您使用了多少内存；而是告诉您内存是如何使用的。

`pgfault`、`pgmajfault`
: 分别表示 cgroup 进程触发"页面错误"和"主要错误"的次数。当进程访问其虚拟内存空间中不存在或受保护的部分时，会发生页面错误。前者可能发生在进程有 bug 并尝试访问无效地址时（它会收到 `SIGSEGV` 信号，通常会以著名的 `Segmentation fault` 消息终止）。后者可能发生在进程从已被交换出的内存区域读取，或对应于映射文件时：在这种情况下，内核从磁盘加载页面，并让 CPU 完成内存访问。当进程写入写时复制内存区域时也会发生：同样，内核会抢占进程、复制内存页面，并在进程自己的页面副本上恢复写操作。当内核实际需要从磁盘读取数据时，会发生"主要"错误。当它只是复制现有页面或分配空页面时，是常规（或"次要"）错误。

`swap`
: 此 cgroup 中进程当前使用的交换空间量。

`active_anon`、`inactive_anon`
: 被内核分别标识为_活动_和_非活动_的匿名内存量。"匿名"内存是_不_链接到磁盘页面的内存。换句话说，它相当于上面描述的 rss 计数器。事实上，rss 计数器的定义是 `active_anon` + `inactive_anon` - `tmpfs`（其中 tmpfs 是此控制组挂载的 `tmpfs` 文件系统使用的内存量）。那么，"活动"和"非活动"之间有什么区别？页面最初是"活动的"；内核会定期扫描内存，并将某些页面标记为"非活动"。每当再次访问它们时，它们会立即重新标记为"活动"。当内核几乎耗尽内存，需要将页面交换到磁盘时，内核会交换"非活动"页面。

`active_file`、`inactive_file`
: 缓存内存，_活动_和_非活动_与上面的_匿名_内存类似。确切的公式是 `cache` = `active_file` + `inactive_file` + `tmpfs`。内核用于在活动和非活动集之间移动内存页面的确切规则与匿名内存使用的规则不同，但一般原则相同。当内核需要回收内存时，从此池中回收干净（=未修改）页面更便宜，因为可以立即回收（而匿名页面和脏/已修改页面需要先写入磁盘）。

`unevictable`
: 无法回收的内存量；通常，它计算使用 `mlock` "锁定"的内存。加密框架经常使用它来确保密钥和其他敏感材料永远不会被交换到磁盘。

`memory_limit`、`memsw_limit`
: 这些实际上不是指标，而是应用于此 cgroup 的限制的提醒。第一个表示此控制组进程可以使用的最大物理内存量；第二个表示 RAM+交换空间的最大量。

页面缓存中的内存记账非常复杂。如果不同控制组中的两个进程都读取同一个文件（最终依赖于磁盘上的相同块），相应的内存费用会在控制组之间分摊。这很好，但也意味着当一个 cgroup 终止时，它可能会增加另一个 cgroup 的内存使用量，因为它们不再分摊这些内存页面的成本。

### CPU 指标：`cpuacct.stat`

既然我们已经介绍了内存指标，其他一切相比之下就简单了。CPU 指标位于 `cpuacct` 控制器中。

对于每个容器，伪文件 `cpuacct.stat` 包含容器进程累积的 CPU 使用量，分为 `user`（用户）和 `system`（系统）时间。区别在于：

- `user` 时间是进程直接控制 CPU、执行进程代码的时间量。
- `system` 时间是内核代表进程执行系统调用的时间。

这些时间以 1/100 秒的滴答数表示，也称为"用户 jiffies"。每秒有 `USER_HZ` 个_"jiffies"_，在 x86 系统上，`USER_HZ` 是 100。从历史上看，这正好对应于每秒调度器"滴答"的数量，但更高频率的调度和[无滴答内核](https://lwn.net/Articles/549580/)使得滴答数量变得无关紧要。

#### 块 I/O 指标

块 I/O 记账在 `blkio` 控制器中。不同的指标分散在不同的文件中。虽然您可以在内核文档的 [blkio-controller](https://www.kernel.org/doc/Documentation/cgroup-v1/blkio-controller.txt) 文件中找到详细信息，但以下是最相关的简短列表：

`blkio.sectors`
: 包含 cgroup 成员进程按设备读取和写入的 512 字节扇区数。读取和写入合并在一个计数器中。

`blkio.io_service_bytes`
: 表示 cgroup 读取和写入的字节数。每个设备有 4 个计数器，因为对于每个设备，它区分同步与异步 I/O 以及读取与写入。

`blkio.io_serviced`
: 执行的 I/O 操作数量，不考虑其大小。每个设备也有 4 个计数器。

`blkio.io_queued`
: 表示此 cgroup 当前排队的 I/O 操作数量。换句话说，如果 cgroup 没有进行任何 I/O，这是零。反过来则不成立。换句话说，如果没有排队的 I/O，并不意味着 cgroup 处于空闲状态（I/O 方面）。它可能在一个空闲的设备上进行纯同步读取，因此可以立即处理，无需排队。此外，虽然它有助于找出哪个 cgroup 给 I/O 子系统带来压力，但请记住这是一个相对量。即使一个进程组没有执行更多 I/O，其队列大小也可能增加，只是因为其他设备导致设备负载增加。

### 网络指标

网络指标不直接由控制组暴露。这有一个很好的解释：网络接口存在于_网络命名空间_的上下文中。内核可能可以累积进程组发送和接收的数据包和字节的指标，但这些指标不会很有用。您想要的是每个接口的指标（因为本地 `lo` 接口上发生的流量并不真正算数）。但由于单个 cgroup 中的进程可以属于多个网络命名空间，这些指标会更难解释：多个网络命名空间意味着多个 `lo` 接口，可能有多个 `eth0` 接口等；因此这就是为什么没有简单的方法用控制组收集网络指标的原因。

相反，您可以从其他来源收集网络指标。

#### iptables

iptables（或更确切地说，iptables 只是其接口的 netfilter 框架）可以进行一些严肃的记账。

例如，您可以设置一条规则来记录 Web 服务器上的出站 HTTP 流量：

```console
$ iptables -I OUTPUT -p tcp --sport 80
```

没有 `-j` 或 `-g` 标志，所以规则只是计算匹配的数据包并转到下一条规则。

稍后，您可以检查计数器的值：

```console
$ iptables -nxvL OUTPUT
```

从技术上讲，`-n` 不是必需的，但它可以防止 iptables 进行 DNS 反向查找，这在此场景中可能是无用的。

计数器包括数据包和字节。如果您想为容器流量设置这样的指标，可以执行一个 `for` 循环，为每个容器 IP 地址添加两条 `iptables` 规则（每个方向一条），在 `FORWARD` 链中。这只测量通过 NAT 层的流量；您还需要添加通过用户空间代理的流量。

然后，您需要定期检查这些计数器。如果您使用 `collectd`，有一个[不错的插件](https://collectd.org/wiki/index.php/Table_of_Plugins)可以自动收集 iptables 计数器。

#### 接口级计数器

由于每个容器都有一个虚拟以太网接口，您可能想直接检查此接口的 TX 和 RX 计数器。每个容器在您的主机中都关联一个虚拟以太网接口，名称类似于 `vethKk8Zqi`。不幸的是，找出哪个接口对应于哪个容器是困难的。

但目前，最好的方法是_从容器内部_检查指标。为此，您可以使用 **ip-netns magic** 在容器的网络命名空间内从主机环境运行可执行文件。

`ip-netns exec` 命令允许您在当前进程可见的任何网络命名空间中执行任何程序（存在于主机系统中）。这意味着您的主机可以进入容器的网络命名空间，但您的容器无法访问主机或其他对等容器。但是，容器可以与其子容器交互。

命令的确切格式是：

```console
$ ip netns exec <nsname> <command...>
```

例如：

```console
$ ip netns exec mycontainer netstat -i
```

`ip netns` 通过使用命名空间伪文件找到 `mycontainer` 容器。每个进程属于一个网络命名空间、一个 PID 命名空间、一个 `mnt` 命名空间等，这些命名空间在 `/proc/<pid>/ns/` 下具体化。例如，PID 42 的网络命名空间由伪文件 `/proc/42/ns/net` 具体化。

当您运行 `ip netns exec mycontainer ...` 时，它期望 `/var/run/netns/mycontainer` 是这些伪文件之一。（接受符号链接。）

换句话说，要在容器的网络命名空间中执行命令，我们需要：

- 找出我们要调查的容器内任何进程的 PID；
- 创建从 `/var/run/netns/<somename>` 到 `/proc/<thepid>/ns/net` 的符号链接
- 执行 `ip netns exec <somename> ....`

查看[枚举 Cgroups](#枚举-cgroups) 了解如何找到要测量网络使用情况的容器内进程的 cgroup。从那里，您可以检查名为 `tasks` 的伪文件，其中包含 cgroup（因此也是容器）中的所有 PID。选择任何一个 PID。

将所有内容放在一起，如果容器的"短 ID"保存在环境变量 `$CID` 中，那么您可以这样做：

```console
$ TASKS=/sys/fs/cgroup/devices/docker/$CID*/tasks
$ PID=$(head -n 1 $TASKS)
$ mkdir -p /var/run/netns
$ ln -sf /proc/$PID/ns/net /var/run/netns/$CID
$ ip netns exec $CID netstat -i
```

## 高性能指标收集技巧

每次要更新指标时运行一个新进程（相对）开销很大。如果您想以高分辨率收集指标，和/或在大量容器上收集（想想单个主机上的 1000 个容器），您不希望每次都 fork 一个新进程。

以下是如何从单个进程收集指标。您需要用 C（或任何允许您进行低级系统调用的语言）编写指标收集器。您需要使用一个特殊的系统调用 `setns()`，它允许当前进程进入任意命名空间。但是，它需要一个打开的文件描述符指向命名空间伪文件（记住：那是 `/proc/<pid>/ns/net` 中的伪文件）。

但是，有一个陷阱：您不能保持此文件描述符打开。如果这样做，当控制组的最后一个进程退出时，命名空间不会被销毁，其网络资源（如容器的虚拟接口）会永远保留（或直到您关闭该文件描述符）。

正确的方法是跟踪每个容器的第一个 PID，并每次重新打开命名空间伪文件。

## 容器退出时收集指标

有时，您不关心实时指标收集，但当容器退出时，您想知道它使用了多少 CPU、内存等。

Docker 使这变得困难，因为它依赖于 `lxc-start`，它会在自己之后仔细清理。通常更容易定期收集指标，这就是 `collectd` LXC 插件的工作方式。

但是，如果您仍想在容器停止时收集统计信息，以下是方法：

对于每个容器，启动一个收集进程，并通过将其 PID 写入 cgroup 的 tasks 文件，将其移动到要监控的控制组中。收集进程应定期重新读取 tasks 文件，以检查它是否是控制组中的最后一个进程。（如果您还想按上一节所述收集网络统计信息，您还应该将进程移动到适当的网络命名空间。）

当容器退出时，`lxc-start` 尝试删除控制组。它会失败，因为控制组仍在使用中；但这没关系。您的进程现在应该检测到它是组中唯一剩下的进程。现在是收集所需所有指标的正确时机！

最后，您的进程应该将自己移回根控制组，并删除容器控制组。要删除控制组，只需 `rmdir` 其目录。`rmdir` 一个仍包含文件的目录是违反直觉的；但请记住，这是一个伪文件系统，所以通常的规则不适用。清理完成后，收集进程可以安全退出。
