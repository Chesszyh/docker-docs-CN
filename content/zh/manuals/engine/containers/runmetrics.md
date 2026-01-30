---
description: 了解如何衡量运行中的容器，以及各种不同的指标
keywords: docker, metrics, CPU, memory, disk, IO, run, runtime, stats, 指标, 运行时
title: 运行时指标 (Runtime metrics)
weight: 50
---

## Docker stats

您可以使用 `docker stats` 命令实时流式传输容器的运行时指标。该命令支持 CPU、内存使用情况、内存限制和网络 IO 指标。

以下是 `docker stats` 命令的示例输出：

```console
$ docker stats redis1 redis2

CONTAINER           CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O
redis1              0.07%               796 KB / 64 MB        1.21%               788 B / 648 B       3.568 MB / 512 KB
redis2              0.07%               2.746 MB / 64 MB      4.29%               1.266 KB / 648 B    12.4 MB / 0 B
```

[`docker stats`](/reference/cli/docker/container/stats.md) 参考页面包含有关 `docker stats` 命令的更多详情。

## 控制组 (Control groups)

Linux 容器依赖于 [控制组 (control groups, cgroups)](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt)，它不仅跟踪进程组，还公开有关 CPU、内存和块 IO 使用情况的指标。您可以访问这些指标，并同时获取网络使用指标。这对于“纯”LXC 容器以及 Docker 容器都是相关的。

控制组通过伪文件系统暴露。在现代发行版中，您应该可以在 `/sys/fs/cgroup` 下找到此文件系统。在该目录下，您会看到多个子目录，分别名为 `devices`、`freezer`、`blkio` 等。每个子目录实际上对应一个不同的 cgroup 层级。

在较旧的系统上，控制组可能挂载在 `/cgroup` 上，没有明显的层级。在这种情况下，您不会看到子目录，而是会看到该目录下的一堆文件，以及一些可能对应于现有容器的目录。

要找出您的控制组挂载在哪里，可以运行：

```console
$ grep cgroup /proc/mounts
```

### 枚举 cgroups

cgroups 的文件布局在 v1 和 v2 之间有显著不同。

如果您的系统上存在 `/sys/fs/cgroup/cgroup.controllers`，则您正在使用 v2，否则使用的是 v1。请参阅对应您 cgroup 版本的子章节。

以下发行版默认使用 cgroup v2：

- Fedora (自版本 31 起)
- Debian GNU/Linux (自版本 11 起)
- Ubuntu (自版本 21.10 起)

#### cgroup v1

您可以查看 `/proc/cgroups` 来了解系统已知的不同控制组子系统、它们所属的层级以及它们包含多少个组。

您还可以查看 `/proc/<pid>/cgroup` 来了解一个进程属于哪些控制组。控制组显示为相对于层级挂载点根目录的路径。`/` 表示进程尚未分配到组，而 `/lxc/pumpkin` 表示该进程是名为 `pumpkin` 的容器的成员。

#### cgroup v2

在 cgroup v2 主机上，`/proc/cgroups` 的内容没有实际意义。请查看 `/sys/fs/cgroup/cgroup.controllers` 以了解可用的控制器。

### 更改 cgroup 版本

更改 cgroup 版本需要重启整个系统。

在基于 systemd 的系统上，可以通过在内核命令行中添加 `systemd.unified_cgroup_hierarchy=1` 来启用 cgroup v2。要将 cgroup 版本还原为 v1，则需要设置为 `systemd.unified_cgroup_hierarchy=0`。

如果您的系统上提供了 `grubby` 命令 (例如在 Fedora 上)，可以按如下方式修改命令行：

```console
$ sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
```

如果没有 `grubby` 命令，请编辑 `/etc/default/grub` 中的 `GRUB_CMDLINE_LINUX` 行并运行 `sudo update-grub`。

### 在 cgroup v2 上运行 Docker

自 Docker 20.10 起支持 cgroup v2。在 cgroup v2 上运行 Docker 还需要满足以下条件：

- containerd: v1.4 或更高版本
- runc: v1.0.0-rc91 或更高版本
- 内核: v4.15 或更高版本 (建议 v5.2 或更高版本)

请注意，cgroup v2 模式的行为与 cgroup v1 模式略有不同：

- 默认的 cgroup 驱动程序 (`dockerd --exec-opt native.cgroupdriver`) 在 v2 上是 `systemd`，在 v1 上是 `cgroupfs`。
- 默认的 cgroup 命名空间模式 (`docker run --cgroupns`) 在 v2 上是 `private`，在 v1 上是 `host`。
- `docker run` 标志 `--oom-kill-disable` 和 `--kernel-memory` 在 v2 上会被忽略。

### 查找给定容器的 cgroup

对于每个容器，会在每个层级中创建一个 cgroup。在带有旧版 LXC 用户空间工具的旧系统上，cgroup 的名称就是容器的名称。在较新版本的 LXC 工具中，cgroup 是 `lxc/<container_name>`。

对于使用 cgroups 的 Docker 容器，cgroup 名称是容器的完整 ID 或长 ID。如果容器在 `docker ps` 中显示为 `ae836c95b4c3`，其长 ID 可能是类似于 `ae836c95b4c3c9e9179e0e91015512da89fdec91612f63cebae57df9a5444c79` 的内容。您可以使用 `docker inspect` 或 `docker ps --no-trunc` 来查找它。

综合以上信息，要查看 Docker 容器的内存指标，请查看以下路径：

- `/sys/fs/cgroup/memory/docker/<longid>/` (cgroup v1, `cgroupfs` 驱动程序)
- `/sys/fs/cgroup/memory/system.slice/docker-<longid>.scope/` (cgroup v1, `systemd` 驱动程序)
- `/sys/fs/cgroup/docker/<longid>/` (cgroup v2, `cgroupfs` 驱动程序)
- `/sys/fs/cgroup/system.slice/docker-<longid>.scope/` (cgroup v2, `systemd` 驱动程序)

### 来自 cgroups 的指标：内存、CPU、块 IO

> [!NOTE]
>
> 本节尚未针对 cgroup v2 进行更新。有关 cgroup v2 的更多信息，请参阅 [内核文档](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)。

对于每个子系统 (内存、CPU 和块 IO)，存在一个或多个包含统计信息的伪文件。

#### 内存指标：`memory.stat`

内存指标可以在 `memory` cgroup 中找到。内存控制组会增加一点开销，因为它会对主机上的内存使用情况进行非常精细的核算。因此，许多发行版选择默认不启用它。通常，要启用它，您只需添加一些内核命令行参数：`cgroup_enable=memory swapaccount=1`。

指标位于伪文件 `memory.stat` 中。其内容如下所示：

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

前半部分 (没有 `total_` 前缀) 包含与 cgroup 内进程相关的统计信息，不包括子 cgroup。后半部分 (带有 `total_` 前缀) 也包括子 cgroup。

有些指标是“量表 (gauges)”，即可以增加或减少的值。例如，`swap` 是 cgroup 成员使用的交换空间量。其他一些是“计数器 (counters)”，即只能增加的值，因为它们代表特定事件的发生次数。例如，`pgfault` 表示自创建 cgroup 以来的缺页中断次数。

`cache`
: 此控制组进程使用的可以精确关联到块设备上某个块的内存量。当您从磁盘读取文件或向磁盘写入文件时，此数值会增加。如果您使用“常规”I/O (`open`、`read`、`write` 系统调用) 以及映射文件 (使用 `mmap`)，就会出现这种情况。它还包括 `tmpfs` 挂载使用的内存，尽管原因尚不清楚。

`rss`
: 与磁盘上任何内容都不对应的内存量：栈 (stacks)、堆 (heaps) 和匿名内存映射。

`mapped_file`
: 表示控制组中进程映射的内存量。它不提供关于使用了多少内存的信息，而是告诉您它是如何被使用的。

`pgfault`, `pgmajfault`
: 分别表示 cgroup 进程触发“缺页中断”和“主缺页中断”的次数。当进程访问其虚拟内存空间中不存在或受保护的部分时，会发生缺页中断。前者可能在进程有 bug 并尝试访问无效地址时发生 (它会被发送 `SIGSEGV` 信号，通常会因著名的 `Segmentation fault` 消息而终止)。后者可能在进程从已换出到磁盘的内存区域或对应于映射文件的区域读取时发生：在这种情况下，内核从磁盘加载该页，并让 CPU 完成内存访问。当进程向写时复制内存区域写入时也可能发生：同样，内核抢占进程，复制内存页，并在进程自己的该页副本上恢复写入操作。当内核实际上需要从磁盘读取数据时，会发生“主 (Major)”缺页中断。当它只是复制现有页面或分配一个空页时，这是一个常规的 (或“次要 Minor”) 缺页中断。

`swap`
: 此 cgroup 进程当前使用的交换分区大小。

`active_anon`, `inactive_anon`
: 被内核分别识别为 *活跃 (active)* 和 *非活跃 (inactive)* 的匿名内存量。“匿名”内存是指 *未* 链接到磁盘页面的内存。换句话说，这相当于上面描述的 rss 计数器。事实上，rss 计数器的定义正是 `active_anon` + `inactive_anon` - `tmpfs` (其中 tmpfs 是此控制组挂载的 `tmpfs` 文件系统所消耗的内存量)。那么，“活跃”和“非活跃”有什么区别呢？页面最初是“活跃”的；内核会定期扫描内存，并将一些页面标记为“非活跃”。每当它们再次被访问时，它们会立即被重新标记为“活跃”。当内核内存几乎耗尽且需要换出到磁盘时，内核会换出“非活跃”页面。

`active_file`, `inactive_file`
: 缓存内存，其 *活跃* 和 *非活跃* 与上面的 *匿名 (anon)* 内存类似。确切的公式是 `cache` = `active_file` + `inactive_file` + `tmpfs`。内核在活跃和非活跃集合之间移动内存页的具体规则与匿名内存使用的规则不同，但基本原理是一样的。当内核需要回收内存时，从这个池中回收一个干净的 (=未修改的) 页面成本更低，因为它可以立即被回收 (而匿名页面和脏/修改过的页面需要先写入磁盘)。

`unevictable`
: 无法回收的内存量；通常，它计入已使用 `mlock` “锁定”的内存。它通常被加密框架使用，以确保密钥和其他敏感资料永远不会被换出到磁盘。

`memory_limit`, `memsw_limit`
: 这些实际上不是指标，而是对此 cgroup 应用的限制的提醒。第一个表示此控制组进程可以使用的最大物理内存量；第二个表示 RAM+交换分区的最大总量。

核算页面缓存中的内存非常复杂。如果两个不同控制组中的进程都读取同一个文件 (最终依赖于磁盘上的相同块)，则相应的内存开销将在这些控制组之间分摊。这很好，但也意味着当一个 cgroup 终止时，可能会增加另一个 cgroup 的内存使用量，因为它们不再分摊这些内存页的成本。

### CPU 指标：`cpuacct.stat`

既然我们已经介绍了内存指标，其他的相比之下就很简单了。CPU 指标在 `cpuacct` 控制器中。

对于每个容器，伪文件 `cpuacct.stat` 包含容器进程累计的 CPU 使用时间，分为 `user` (用户) 时间和 `system` (系统) 时间。区别在于：

- `user` 时间是进程直接控制 CPU、执行进程代码的时间量。
- `system` 时间是内核代表进程执行系统调用的时间。

这些时间以 1/100 秒的滴答 (ticks) 表示，也称为“用户滴答 (user jiffies)”。每秒有 `USER_HZ` 个 *“jiffies”*，在 x86 系统上，`USER_HZ` 是 100。从历史上看，这正好对应每秒调度程序的“滴答”数，但更高频率的调度和 [无滴答内核 (tickless kernels)](https://lwn.net/Articles/549580/) 已使得滴答数变得不再那么重要。

#### 块 IO 指标

块 IO 在 `blkio` 控制器中进行核算。不同的指标散布在不同的文件中。虽然您可以在内核文档的 [blkio-controller](https://www.kernel.org/doc/Documentation/cgroup-v1/blkio-controller.txt) 文件中找到深入的细节，但这里列出了最相关的几个：

`blkio.sectors`
: 包含 cgroup 成员进程读取和写入的 512 字节扇区数，按设备分类。读取和写入合并在一个计数器中。

`blkio.io_service_bytes`
: 表示 cgroup 读取和写入的字节数。每个设备有 4 个计数器，因为它对每个设备区分了同步 vs 异步 I/O 以及读取 vs 写入。

`blkio.io_serviced`
: 执行的 I/O 操作次数，无论大小。每个设备也有 4 个计数器。

`blkio.io_queued`
: 表示当前为此 cgroup 排队的 I/O 操作数。换句话说，如果 cgroup 没有执行任何 I/O，该值为零。反之则不然。也就是说，如果没有排队的 I/O，并不意味着 cgroup 是空闲的 (就 I/O 而言)。它可能正在一个本来就沉寂的设备上执行纯同步读取，因此该设备可以立即处理它们，而无需排队。此外，虽然这有助于确定哪个 cgroup 对 I/O 子系统施加了压力，但请记住这是一个相对量。即使一个进程组没有执行更多的 I/O，它的队列大小也可能仅仅因为其他设备导致的设备负载增加而增加。

### 网络指标

网络指标不直接通过控制组暴露。对此有一个很好的解释：网络接口存在于 *网络命名空间 (network namespaces)* 的上下文中。内核可能会累计一个进程组发送和接收的数据包及字节数，但这些指标不会很有用。您需要的是按接口分类的指标 (因为发生在本地 `lo` 接口上的流量并不真正算数)。但由于单个 cgroup 中的进程可以属于多个网络命名空间，因此这些指标将更难解读：多个网络命名空间意味着多个 `lo` 接口、可能多个 `eth0` 接口等；这就是为什么没有简单的方法通过控制组收集网络指标的原因。

相反，您可以从其他来源收集网络指标。

#### iptables

iptables (或者更确切地说，iptables 仅仅作为其接口的 netfilter 框架) 可以执行一些严肃的核算工作。

例如，您可以设置一条规则来核算 Web 服务器上的出站 HTTP 流量：

```console
$ iptables -I OUTPUT -p tcp --sport 80
```

没有 `-j` 或 `-g` 标志，因此该规则只是对匹配的数据包进行计数，然后转到下一条规则。

稍后，您可以使用以下命令检查计数器的值：

```console
$ iptables -nxvL OUTPUT
```

从技术上讲，`-n` 不是必需的，但它可以防止 iptables 执行 DNS 反向查询，这在此场景中可能没用。

计数器包括数据包和字节。如果您想为像这样的容器流量设置指标，可以执行一个 `for` 循环，为每个容器 IP 地址在 `FORWARD` 链中添加两条 `iptables` 规则 (每个方向一条)。这仅计量通过 NAT 层传输的流量；您还需要添加通过用户空间代理传输的流量。

然后，您需要定期检查这些计数器。如果您碰巧使用 `collectd`，有一个 [很棒的插件](https://collectd.org/wiki/index.php/Table_of_Plugins) 可以自动收集 iptables 计数器。

#### 接口级计数器

由于每个容器都有一个虚拟以太网接口，您可能想直接检查此接口的 TX 和 RX 计数器。每个容器都与您主机中的一个虚拟以太网接口相关联，名称类似于 `vethKk8Zqi`。不幸的是，找出哪个接口对应于哪个容器比较困难。

但目前，最好的方法是 *从容器内部* 检查指标。为此，您可以使用 **ip-netns 魔法**，在容器的网络命名空间内运行主机环境中的可执行文件。

`ip netns exec` 命令允许您在当前进程可见的任何网络命名空间内执行任何程序 (存在于主机系统中)。这意味着您的主机可以进入容器的网络命名空间，但您的容器无法访问主机或其他对等容器。不过，容器可以与其子容器交互。

该命令的确切格式为：

```console
$ ip netns exec <nsname> <command...>
```

例如：

```console
$ ip netns exec mycontainer netstat -i
```

`ip netns` 通过使用命名空间伪文件来查找 `mycontainer` 容器。每个进程属于一个网络命名空间、一个 PID 命名空间、一个 `mnt` 命名空间等，这些命名空间在 `/proc/<pid>/ns/` 下实体化。例如，PID 为 42 的进程的网络命名空间由伪文件 `/proc/42/ns/net` 实体化。

当您运行 `ip netns exec mycontainer ...` 时，它期望 `/var/run/netns/mycontainer` 是这些伪文件之一 (接受符号链接)。

换句话说，要在容器的网络命名空间内执行命令，我们需要：

- 找出我们要调查的容器内任何进程的 PID；
- 创建一个从 `/var/run/netns/<某个名称>` 到 `/proc/<该PID>/ns/net` 的符号链接；
- 执行 `ip netns exec <某个名称> ....`

查看 [枚举 Cgroups](#enumerate-cgroups) 了解如何查找您想测量其网络使用情况的容器内进程的 cgroup。从那里，您可以检查名为 `tasks` 的伪文件，它包含该 cgroup (因此也就是该容器) 中的所有 PID。选取其中任何一个 PID 即可。

综合起来，如果容器的“短 ID”保存在环境变量 `$CID` 中，那么您可以这样做：

```console
$ TASKS=/sys/fs/cgroup/devices/docker/$CID*/tasks
$ PID=$(head -n 1 $TASKS)
$ mkdir -p /var/run/netns
$ ln -sf /proc/$PID/ns/net /var/run/netns/$CID
$ ip netns exec $CID netstat -i
```

## 高性能指标收集技巧

每次想要更新指标时都运行一个新进程是 (相对) 昂贵的。如果您想以高分辨率和/或针对大量容器 (想想单台主机上有 1000 个容器) 收集指标，您不会希望每次都派生一个新进程。

以下是如何从单个进程收集指标的方法。您需要用 C (或任何允许您进行底层系统调用的语言) 编写您的指标收集器。您需要使用一个特殊的系统调用 `setns()`，它允许当前进程进入任何任意命名空间。但是，它需要一个指向命名空间伪文件的打开文件描述符 (记住：那就是 `/proc/<pid>/ns/net` 中的伪文件)。

然而，有一个陷阱：您不能保持此文件描述符一直打开。如果您这样做，当控制组的最后一个进程退出时，命名空间将不会被销毁，其网络资源 (如容器的虚拟接口) 会一直存在 (直到您关闭该文件描述符)。

正确的方法应该是跟踪每个容器的第一个 PID，并每次重新打开该命名空间伪文件。

## 在容器退出时收集指标

有时，您不关心实时指标收集，但在容器退出时，您想知道它使用了多少 CPU、内存等。

Docker 让这变得困难，因为它依赖于 `lxc-start`，而后者会仔细进行收尾清理工作。通常定期收集指标更容易，这也是 `collectd` LXC 插件的工作方式。

但是，如果您仍想在容器停止时收集统计信息，方法如下：

对于每个容器，启动一个收集进程，并通过将其 PID 写入 cgroup 的 `tasks` 文件将其移动到您想要监控的控制组中。收集进程应定期重新读取 `tasks` 文件，以检查它是否是该控制组中仅存的最后一个进程。(如果您还想按照上一节所述收集网络统计信息，您还应该将进程移动到适当的网络命名空间中。)

当容器退出时，`lxc-start` 会尝试删除控制组。它会失败，因为该控制组仍在使用中；但这没关系。您的进程现在应该检测到它是组中仅存的一个。现在正是收集您所需所有指标的最佳时机！

最后，您的进程应将其自身移回根控制组，并删除容器控制组。要删除控制组，只需 `rmdir` 它的目录即可。`rmdir` 一个仍包含文件的目录似乎违反直觉；但请记住这是一个伪文件系统，因此通常的规则不适用。清理完成后，收集进程可以安全退出。
