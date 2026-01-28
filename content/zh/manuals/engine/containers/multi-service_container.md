---
description: 了解如何在单个容器中运行多个进程
keywords: docker, supervisor, process management
title: 在容器中运行多个进程
weight: 20
aliases:
  - /articles/using_supervisord/
  - /engine/admin/multi-service_container/
  - /engine/admin/using_supervisord/
  - /engine/articles/using_supervisord/
  - /config/containers/multi-service_container/
---

容器的主运行进程是 `Dockerfile` 末尾的 `ENTRYPOINT` 和/或 `CMD`。最佳实践是通过每个容器使用一个服务来分离关注点。该服务可能会派生出多个进程（例如，Apache Web 服务器会启动多个工作进程）。拥有多个进程是可以的，但为了充分利用 Docker 的优势，应避免让一个容器负责整体应用程序的多个方面。您可以使用用户定义的网络和共享卷来连接多个容器。

容器的主进程负责管理它启动的所有进程。在某些情况下，主进程设计不够完善，在容器退出时无法优雅地处理子进程的"回收"（停止）。如果您的进程属于这种情况，可以在运行容器时使用 `--init` 选项。`--init` 标志会在容器中插入一个微型 init 进程作为主进程，并在容器退出时处理所有进程的回收。以这种方式处理进程优于使用完整的 init 进程（如 `sysvinit` 或 `systemd`）来处理容器内的进程生命周期。

如果您需要在一个容器中运行多个服务，可以通过几种不同的方式来实现。

## 使用包装脚本

将所有命令放入一个包装脚本中，包含测试和调试信息。将包装脚本作为您的 `CMD` 运行。以下是一个简单的示例。首先是包装脚本：

```bash
#!/bin/bash

# Start the first process
./my_first_process &

# Start the second process
./my_second_process &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
```

然后是 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_first_process my_first_process
COPY my_second_process my_second_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## 使用 Bash 作业控制

如果您有一个需要首先启动并保持运行的主进程，但临时需要运行一些其他进程（可能是为了与主进程交互），那么您可以使用 bash 的作业控制。首先是包装脚本：

```bash
#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
./my_main_process &

# Start the helper process
./my_helper_process

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns


# now we bring the primary process back into the foreground
# and leave it there
fg %1
```

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_main_process my_main_process
COPY my_helper_process my_helper_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## 使用进程管理器

使用像 `supervisord` 这样的进程管理器。这比其他选项更复杂，因为它需要您将 `supervisord` 及其配置打包到镜像中（或基于包含 `supervisord` 的镜像），以及它管理的不同应用程序。然后启动 `supervisord`，它会为您管理进程。

以下 Dockerfile 示例展示了这种方法。该示例假设以下文件存在于构建上下文的根目录：

- `supervisord.conf`
- `my_first_process`
- `my_second_process`

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY my_first_process my_first_process
COPY my_second_process my_second_process
CMD ["/usr/bin/supervisord"]
```

如果您想确保两个进程的 `stdout` 和 `stderr` 输出到容器日志，可以在 `supervisord.conf` 文件中添加以下内容：

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

[program:app]
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
redirect_stderr=true
```
