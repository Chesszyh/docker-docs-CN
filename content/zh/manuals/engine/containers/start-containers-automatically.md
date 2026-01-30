---
description: 如何自动启动容器
keywords: containers, restart, policies, automation, administration, 容器, 重启策略, 自动化, 管理
title: 自动启动容器
weight: 10
aliases:
  - /engine/articles/host_integration/
  - /engine/admin/host_integration/
  - /engine/admin/start-containers-automatically/
  - /config/containers/start-containers-automatically/
---

Docker 提供了 [重启策略 (restart policies)](/manuals/engine/containers/run.md#restart-policies---restart) 来控制在容器退出或 Docker 重启时是否自动启动容器。重启策略会按正确的顺序启动已链接的容器。Docker 建议您使用重启策略，并避免使用进程管理器来启动容器。

重启策略与 `dockerd` 命令的 `--live-restore` 标志不同。使用 `--live-restore` 允许您在 Docker 升级期间保持容器运行，尽管网络和用户输入会中断。

## 使用重启策略

要配置容器的重启策略，请在执行 `docker run` 命令时使用 `--restart` 标志。`--restart` 标志的值可以是以下任何一种：

| 标志                       | 描述                                                                                                                                                                                                                                                                                                                                                           |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no`                       | 不自动重启容器。(默认值)                                                                                                                                                                                                                                                                                                                  |
| `on-failure[:max-retries]` | 如果容器因错误退出 (表现为非零退出代码)，则重启容器。可选地，使用 `:max-retries` 选项限制 Docker 守护进程尝试重启容器的次数。`on-failure` 策略仅在容器因失败退出时才会触发重启。如果守护进程重启，它不会重启该容器。 |
| `always`                   | 如果容器停止，始终重启它。如果是手动停止的，只有在 Docker 守护进程重启或容器本身被手动重启时，它才会重启。(参见 [重启策略详情](#restart-policy-details) 中的第二点)                                                                                                                |
| `unless-stopped`           | 类似于 `always`，不同之处在于当容器被停止 (手动或其他方式) 时，即使在 Docker 守护进程重启后也不会重启。                                                                                                                                                                                                                         |

以下命令启动一个 Redis 容器，并将其配置为除非容器被显式停止或守护进程重启，否则始终重启。

```console
$ docker run -d --restart unless-stopped redis
```

以下命令为已运行的名为 `redis` 的容器更改重启策略。

```console
$ docker update --restart unless-stopped redis
```

以下命令确保所有运行中的容器都会重启。

```console
$ docker update --restart unless-stopped $(docker ps -q)
```

### 重启策略详情

使用重启策略时，请记住以下几点：

- 重启策略仅在容器成功启动后才会生效。在这种情况下，“成功启动”意味着容器已运行至少 10 秒且 Docker 已开始对其进行监控。这可以防止根本无法启动的容器陷入重启循环。

- 如果您手动停止一个容器，重启策略将被忽略，直到 Docker 守护进程重启或容器被手动重启。这可以防止重启循环。

- 重启策略仅适用于容器。要为 Swarm 服务配置重启策略，请参阅 [与服务重启相关的标志](/reference/cli/docker/service/create.md)。

### 重启前台容器

当您在前台运行容器时，停止容器会导致附加的 CLI 也随之退出，而不管容器的重启策略如何。以下示例说明了此行为。

1. 创建一个打印数字 1 到 5 然后退出的 Dockerfile。

   ```dockerfile
   FROM busybox:latest
   COPY --chmod=755 <<"EOF" /start.sh
   echo "Starting..."
   for i in $(seq 1 5); do
     echo "$i"
     sleep 1
   done
   echo "Exiting..."
   exit 1
   EOF
   ENTRYPOINT /start.sh
   ```

2. 从 Dockerfile 构建镜像。

   ```console
   $ docker build -t startstop .
   ```

3. 从镜像运行一个容器，并将其重启策略指定为 `always`。

   容器将数字 1 到 5 打印到 stdout，然后退出。这会导致附加的 CLI 也随之退出。

   ```console
   $ docker run --restart always startstop
   Starting...
   1
   2
   3
   4
   5
   Exiting...
   $
   ```

4. 运行 `docker ps` 显示容器由于重启策略仍在运行或正在重启。然而，CLI 会话已经退出。它无法在初始容器退出后继续存在。

   ```console
   $ docker ps
   CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS     NAMES
   081991b35afe   startstop   "/bin/sh -c /start.sh"   9 seconds ago   Up 4 seconds             gallant_easley
   ```

5. 您可以在重启之间使用 `docker container attach` 命令将您的终端重新附加到容器。下次容器退出时，它将再次脱离。

   ```console
   $ docker container attach 081991b35afe
   4
   5
   Exiting...
   $
   ```

## 使用进程管理器

如果重启策略不符合您的需求 (例如当 Docker 之外的进程依赖于 Docker 容器时)，您可以改用 [systemd](https://systemd.io/) 或 [supervisor](http://supervisord.org/) 等进程管理器。

> [!WARNING]
>
> 不要将 Docker 重启策略与主机级的进程管理器结合使用，因为这会产生冲突。

要使用进程管理器，请配置它使用您平时手动启动容器时所用的相同 `docker start` 或 `docker service` 命令来启动您的容器或服务。有关更多详情，请咨询特定进程管理器的文档。

### 在容器内部使用进程管理器

进程管理器也可以在容器内部运行，以检查某个进程是否正在运行，如果不是则启动/重启它。

> [!WARNING]
>
> 它们不能感知 Docker，而只能监控容器内的操作系统进程。Docker 不推荐这种方法，因为它是平台相关的，并且在给定的 Linux 发行版版本之间可能存在差异。
