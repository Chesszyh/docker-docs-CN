---
description: 从 Swarm 中移除服务
keywords: tutorial, cluster management, swarm, service, get started, 教程, 移除服务
title: 删除 Swarm 上运行的服务
weight: 60
notoc: true
---

本教程后续步骤不再使用 `helloworld` 服务，因此您现在可以将该服务从 Swarm 中删除。

1.  如果您还没有这样做，请打开终端并 SSH 登录到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service rm helloworld` 来移除 `helloworld` 服务。

    ```console
    $ docker service rm helloworld

    helloworld
    ```

3.  运行 `docker service inspect <SERVICE-ID>` 来验证 Swarm 管理节点是否已移除该服务。CLI 会返回一条消息，提示找不到该服务：

    ```console
    $ docker service inspect helloworld
    []
    Status: Error: no such service: helloworld, Code: 1
    ```

4.  即使服务已不存在，任务容器仍需要几秒钟的时间进行清理。您可以在各个节点上使用 `docker ps` 来验证任务是否已被移除。

    ```console
    $ docker ps

    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
    db1651f50347        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.5.9lkmos2beppihw95vdwxy1j3w
    43bf6e532a92        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.3.a71i8rp6fua79ad43ycocl4t2
    5a0fb65d8fa7        alpine:latest       "ping docker.com"        44 minutes ago      Up 45 seconds                 helloworld.2.2jpgensh7d935qdc857pxulfr
    afb0ba67076f        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.4.1c47o7tluz7drve4vkm2m5olx
    688172d3bfaa        alpine:latest       "ping docker.com"        45 minutes ago      Up About a minute             helloworld.1.74nbhb3fhud8jfrhigd7s29we

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES

    ```

## 下一步

接下来，您将设置一个新服务并应用滚动更新。

{{< button text="应用滚动更新" url="rolling-update.md" >}}
