---
title: 读取守护进程日志
description: 如何读取 Docker 守护进程的事件日志
keywords: docker, daemon, configuration, troubleshooting, logging, 守护进程, 日志, 故障排查
---

守护进程日志可以帮助您诊断问题。根据操作系统配置和使用的日志子系统，日志可能保存在以下几个位置之一：

| 操作系统                           | 位置                                                                                                                                 |
| :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| Linux                              | 使用命令 `journalctl -xu docker.service` (或读取 `/var/log/syslog` 或 `/var/log/messages`，取决于您的 Linux 发行版) |
| macOS (`dockerd` 日志)             | `~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log`                                                                         |
| macOS (`containerd` 日志)          | `~/Library/Containers/com.docker.docker/Data/log/vm/containerd.log`                                                                      |
| Windows (WSL2) (`dockerd` 日志)    | `%LOCALAPPDATA%\Docker\log\vm\dockerd.log`                                                                                               |
| Windows (WSL2) (`containerd` 日志) | `%LOCALAPPDATA%\Docker\log\vm\containerd.log`                                                                                            |
| Windows (Windows 容器)             | 日志位于 Windows 事件日志中                                                                                                        |

要在 macOS 上查看 `dockerd` 日志，请打开终端窗口，并使用带有 `-f` 标志的 `tail` 命令来“跟随”日志。日志将持续打印，直到您使用 `CTRL+c` 终止命令：

```console
$ tail -f ~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.497642089Z" level=debug msg="attach: stdout: begin"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.497714291Z" level=debug msg="attach: stderr: begin"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.499798390Z" level=debug msg="Calling POST /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/wait?condition=removed"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.518403686Z" level=debug msg="Calling GET /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/json"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.527074928Z" level=debug msg="Calling POST /v1.41/containers/35fc5ec0ffe1ad492d0a4fbf51fd6286a087b89d4dd66367fa3b7aec70b46a40/start"
2021-07-28T10:21:21Z dockerd time="2021-07-28T10:21:21.528203579Z" level=debug msg="container mounted via layerStore: &{/var/lib/docker/overlay2/6e76ffecede030507fcaa576404e141e5f87fc4d7e1760e9ce5b52acb24
...
^C
```

## 启用调试 (Debugging)

有两种方式可以启用调试。推荐的方法是在 `daemon.json` 文件中将 `debug` 键设置为 `true`。此方法适用于每个 Docker 平台。

1.  编辑 `daemon.json` 文件，该文件通常位于 `/etc/docker/`。如果该文件尚不存在，您可能需要创建它。在 macOS 或 Windows 上，请勿直接编辑该文件。相反，应通过 Docker Desktop 设置进行编辑。

2.  如果文件为空，添加以下内容：

    ```json
    {
      "debug": true
    }
    ```

    如果文件已包含 JSON 内容，只需添加键 `"debug": true`，注意如果它不是闭括号之前的最后一行，请在行尾添加逗号。同时验证如果设置了 `log-level` 键，它应被设置为 `info` 或 `debug`。`info` 是默认值，其他可能的值有 `debug`、`info`、`warn`、`error`、`fatal`。

3.  向守护进程发送 `HUP` 信号，使其重新加载配置。在 Linux 主机上，使用以下命令。

    ```console
    $ sudo kill -SIGHUP $(pidof dockerd)
    ```

    在 Windows 主机上，重启 Docker。

除了遵循此过程外，您还可以停止 Docker 守护进程并手动使用调试标志 `-D` 重新启动它。然而，这可能会导致 Docker 以与主机启动脚本创建的环境不同的环境重新启动，这可能会使调试变得更加困难。

## 强制记录堆栈跟踪 (Stack trace)

如果守护进程无响应，您可以通过向守护进程发送 `SIGUSR1` 信号来强制记录完整的堆栈跟踪。

- **Linux**:

  ```console
  $ sudo kill -SIGUSR1 $(pidof dockerd)
  ```

- **Windows Server**:

  下载 [docker-signal](https://github.com/moby/docker-signal)。

  获取 dockerd 的进程 ID：`Get-Process dockerd`。

  运行可执行文件，并带上标志 `--pid=<守护进程的 PID>`。

这会强制记录堆栈跟踪，但不会停止守护进程。守护进程日志将显示堆栈跟踪，或者如果堆栈跟踪被记录到文件中，则显示该文件的路径。

守护进程在处理 `SIGUSR1` 信号并将堆栈跟踪转储到日志后继续运行。堆栈跟踪可用于确定守护进程内所有 goroutine 和线程的状态。

## 查看堆栈跟踪

可以使用以下方法之一查看 Docker 守护进程日志：

- 在使用 `systemctl` 的 Linux 系统上运行 `journalctl -u docker.service`
- 在较旧的 Linux 系统上查看 `/var/log/messages`、`/var/log/daemon.log` 或 `/var/log/docker.log`

> [!NOTE]
>
> 在 Docker Desktop for Mac 或 Docker Desktop for Windows 上无法手动生成堆栈跟踪。但是，您可以点击 Docker 任务栏图标并选择 **Troubleshoot** (故障排查) 以在遇到问题时向 Docker 发送信息。

在 Docker 日志中查找类似以下的消息：

```text
...goroutine stacks written to /var/run/docker/goroutine-stacks-2017-06-02T193336z.log
```

Docker 保存这些堆栈跟踪和转储的位置取决于您的操作系统和配置。有时您可以直接从堆栈跟踪和转储中获得有用的诊断信息。否则，您可以将此信息提供给 Docker，以帮助诊断问题。
