---
description: 在用户命名空间内隔离容器
keywords: security, namespaces, 安全, 命名空间
title: 使用用户命名空间隔离容器
---

Linux 命名空间为运行中的进程提供隔离，在运行进程不知情的情况下限制其对系统资源的访问。有关 Linux 命名空间的更多信息，请参阅 [Linux namespaces](https://www.linux.com/news/understanding-and-securing-linux-namespaces)。

防止容器内发生特权提升攻击的最佳方法是将容器应用程序配置为以非特权用户身份运行。对于进程必须在容器内以 `root` 用户运行的容器，您可以将此用户重新映射到 Docker 主机上一个特权较低的用户。映射后的用户会被分配一组 UID，这些 UID 在命名空间内作为 0 到 65536 的正常 UID 运行，但在主机机器本身上没有特权。

## 关于重新映射以及从属用户和组 ID

重新映射本身由两个文件处理：`/etc/subuid` 和 `/etc/subgid`。这两个文件的作用相同，但一个涉及用户 ID 范围，另一个涉及组 ID 范围。考虑 `/etc/subuid` 中的以下条目：

```none
testuser:231072:65536
```

这意味着为 `testuser` 分配了一个从属用户 ID 范围，从 `231072` 开始，接下来是序列中的 65536 个整数。UID `231072` 在命名空间内 (在这种情况下是在容器内) 被映射为 UID `0` (`root`)。UID `231073` 被映射为 UID `1`，依此类推。如果一个进程试图在命名空间之外提升特权，该进程在主机上是以一个不具备特权的大数字 UID 运行的，该 UID 甚至不对应于一个真实用户。这意味着该进程在主机系统上根本没有特权。

> [!NOTE]
>
> 通过在 `/etc/subuid` 或 `/etc/subgid` 文件中为同一个用户或组添加多个非重叠映射，可以为给定的用户或组分配多个从属范围。在这种情况下，Docker 仅使用前五个映射，这符合内核在 `/proc/self/uid_map` 和 `/proc/self/gid_map` 中仅限五个条目的限制。

当您将 Docker 配置为使用 `userns-remap` 特性时，您可以选择指定一个现有的用户和/或组，或者指定 `default`。如果您指定 `default`，则会创建并使用一个名为 `dockremap` 的用户和组。

> [!WARNING]
>
> 某些发行版不会自动将新组添加到 `/etc/subuid` 和 `/etc/subgid` 文件中。如果是这种情况，您可能需要手动编辑这些文件并分配不重叠的范围。这一步骤在 [前提条件](#prerequisites) 中有详细说明。

范围不重叠非常重要，这样进程就无法在不同的命名空间中获取访问权限。在大多数 Linux 发行版上，当您添加或删除用户时，系统实用工具会自动为您管理这些范围。

这种重新映射对容器是透明的，但在容器需要访问 Docker 主机上的资源的情况下 (例如绑定挂载到系统用户无法写入的文件系统区域) 会引入一些配置复杂性。从安全角度来看，最好避免这些情况。

## 前提条件

1.  从属 UID 和 GID 范围必须与现有用户关联，尽管这种关联是一个实现细节。该用户拥有 `/var/lib/docker/` 下带命名空间的存储目录。如果您不想使用现有用户，Docker 可以为您创建一个并使用它。如果您想使用现有的用户名或用户 ID，它必须已经存在。通常，这意味着相关条目需要位于 `/etc/passwd` 和 `/etc/group` 中，但如果您使用的是不同的身份验证后端，此要求可能会有不同的体现。

    要验证这一点，请使用 `id` 命令：

    ```console
    $ id testuser

    uid=1001(testuser) gid=1001(testuser) groups=1001(testuser)
    ```

2.  主机上处理命名空间重新映射的方法是使用两个文件：`/etc/subuid` 和 `/etc/subgid`。当您添加或删除用户或组时，通常会自动管理这些文件，但在某些发行版上，您可能需要手动管理这些文件。

    每个文件包含三个字段：用户名或用户 ID，后跟起始 UID 或 GID (在命名空间内被视为 UID 或 GID 0) 以及该用户可用的最大 UID 或 GID 数量。例如，给定以下条目：

    ```none
    testuser:231072:65536
    ```

    这意味着由 `testuser` 启动的用户命名空间进程由主机 UID `231072` (在命名空间内部看起来像 UID `0`) 到 296607 (`231072 + 65536 - 1`) 拥有。这些范围不应重叠，以确保命名空间进程无法访问彼此的命名空间。

    添加用户后，检查 `/etc/subuid` 和 `/etc/subgid` 以查看您的用户是否在每个文件中都有条目。如果没有，您需要添加它，并注意避免重叠。

    如果您想使用 Docker 自动创建的 `dockremap` 用户，请在配置并重启 Docker 后检查这些文件中的 `dockremap` 条目。

3.  如果 Docker 主机上有任何需要非特权用户写入的位置，请相应地调整这些位置的权限。如果您想使用 Docker 自动创建的 `dockremap` 用户，这也是正确的，但直到配置并重启 Docker 后您才能修改权限。

4.  启用 `userns-remap` 实际上会遮蔽 `/var/lib/docker/` 中现有的镜像和容器层，以及其他 Docker 对象。这是因为 Docker 需要调整这些资源的所有权，并实际上将它们存储在 `/var/lib/docker/` 下的一个子目录中。最好在全新的 Docker 安装上启用此特性，而不是在现有的安装上。

    同理，如果您禁用 `userns-remap`，您将无法访问在其启用期间创建的任何资源。

5.  检查用户命名空间的 [已知限制](#user-namespace-known-limitations)，以确保您的用例可行。

## 在守护进程上启用 userns-remap

您可以使用 `--userns-remap` 标志启动 `dockerd`，或者按照此过程使用 `daemon.json` 配置文件配置守护进程。推荐使用 `daemon.json` 方法。如果您使用该标志，请参考以下命令：

```console
$ dockerd --userns-remap="testuser:testuser"
```

1.  编辑 `/etc/docker/daemon.json`。假设该文件之前为空，以下条目使用名为 `testuser` 的用户和组启用 `userns-remap`。您可以通过 ID 或名称指定用户和组。如果组名或 ID 与用户名或 ID 不同，才需要指定组名或 ID。如果您同时提供用户名和组名 (或 ID)，请用冒号 (`:`) 分隔。假设 `testuser` 的 UID 和 GID 都是 `1001`，以下格式对该值都有效：

    - `testuser`
    - `testuser:testuser`
    - `1001`
    - `1001:1001`
    - `testuser:1001`
    - `1001:testuser`

    ```json
    {
      "userns-remap": "testuser"
    }
    ```

    > [!NOTE]
    >
    > 要使用 `dockremap` 用户并让 Docker 为您创建它，请将该值设置为 `default` 而不是 `testuser`。

    保存文件并重启 Docker。

2.  如果您使用的是 `dockremap` 用户，请使用 `id` 命令验证 Docker 是否已创建该用户。

    ```console
    $ id dockremap

    uid=112(dockremap) gid=116(dockremap) groups=116(dockremap)
    ```

    验证条目是否已添加到 `/etc/subuid` 和 `/etc/subgid`：

    ```console
    $ grep dockremap /etc/subuid

    dockremap:231072:65536

    $ grep dockremap /etc/subgid

    dockremap:231072:65536
    ```

    如果这些条目不存在，请以 `root` 用户身份编辑文件，并分配一个起始 UID 和 GID，该起始值应为当前已分配的最高值加上偏移量 (在本例中为 `65536`)。注意不要让范围发生任何重叠。

3.  使用 `docker image ls` 命令验证之前的镜像是否不可用。输出应该是空的。

4.  从 `hello-world` 镜像启动一个容器。

    ```console
    $ docker run hello-world
    ```

5.  验证 `/var/lib/docker/` 中是否存在以命名空间用户的 UID 和 GID 命名的命名空间目录，该目录由该 UID 和 GID 拥有，且不可被组或其他用户读取。某些子目录仍由 `root` 拥有且具有不同的权限。

    ```console
    $ sudo ls -ld /var/lib/docker/231072.231072/

    drwx------ 11 231072 231072 11 Jun 21 21:19 /var/lib/docker/231072.231072/

    $ sudo ls -l /var/lib/docker/231072.231072/

    total 14
    drwx------ 5 231072 231072 5 Jun 21 21:19 aufs
    drwx------ 3 231072 231072 3 Jun 21 21:21 containers
    drwx------ 3 root   root   3 Jun 21 21:19 image
    drwxr-x--- 3 root   root   3 Jun 21 21:19 network
    drwx------ 4 root   root   4 Jun 21 21:19 plugins
    drwx------ 2 root   root   2 Jun 21 21:19 swarm
    drwx------ 2 231072 231072 2 Jun 21 21:21 tmp
    drwx------ 2 root   root   2 Jun 21 21:19 trust
    drwx------ 2 231072 231072 3 Jun 21 21:19 volumes
    ```

    您的目录列表可能会有一些差异，特别是如果您使用与 `aufs` 不同的容器存储驱动程序。

    由重新映射用户拥有的目录将被使用，而不是 `/var/lib/docker/` 正下方的相同目录，并且未使用的版本 (例如此处示例中的 `/var/lib/docker/tmp/`) 可以被删除。当 `userns-remap` 启用时，Docker 不会使用它们。

## 为容器禁用命名空间重新映射

如果您在守护进程上启用了用户命名空间，默认情况下所有启动的容器都会启用用户命名空间。在某些情况下 (如特权容器)，您可能需要为特定容器禁用用户命名空间。请参阅 [用户命名空间已知限制](#user-namespace-known-limitations) 了解其中一些限制。

要为特定容器禁用用户命名空间，请在 `docker container create`、`docker container run` 或 `docker container exec` 命令中添加 `--userns=host` 标志。

使用此标志时会产生一个副作用：该容器将不会启用用户重新映射，但由于只读 (镜像) 层在容器之间共享，容器文件系统的所有权仍将被重新映射。

这意味着整个容器文件系统将属于守护进程配置 `--userns-remap` 中指定的用户 (在上述示例中为 `231072`)。这可能会导致容器内程序的意外行为。例如 `sudo` (它检查其二进制文件是否属于用户 `0`) 或带有 `setuid` 标志的二进制文件。

## 用户命名空间已知限制

以下标准 Docker 特性与启用了用户命名空间的 Docker 守护进程不兼容：

- 与主机共享 PID 或 NET 命名空间 (`--pid=host` 或 `--network=host`)。
- 无法感知或无法使用守护进程用户映射的外部 (卷或存储) 驱动程序。
- 在 `docker run` 上使用 `--privileged` 模式标志而不同时指定 `--userns=host`。

用户命名空间是一项高级特性，需要与其他功能协调。例如，如果卷是从主机挂载的，且您需要对卷内容进行读写访问，则必须预先安排文件所有权。

虽然用户命名空间容器进程内的 root 用户拥有容器内预期的许多超级用户特权，但 Linux 内核会根据其内部知晓这是一个用户命名空间进程而施加限制。一个显著的限制是无法使用 `mknod` 命令。当由 `root` 用户运行时，在容器内创建设备的权限会被拒绝。
