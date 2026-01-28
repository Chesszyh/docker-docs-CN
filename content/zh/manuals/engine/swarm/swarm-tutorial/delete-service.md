---
description: Remove the service from the swarm
keywords: tutorial, cluster management, swarm, service, get started
title: 删除在 swarm 上运行的服务
weight: 60
notoc: true
---

教程的剩余步骤不使用 `helloworld` 服务，所以现在你可以从 swarm 中删除该服务。

1.  如果你还没有，打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service rm helloworld` 删除 `helloworld` 服务。

    ```console
    $ docker service rm helloworld

    helloworld
    ```

3.  运行 `docker service inspect <SERVICE-ID>` 验证 swarm 管理节点已删除该服务。CLI 返回一条消息表示未找到该服务：

    ```console
    $ docker service inspect helloworld
    []
    Status: Error: no such service: helloworld, Code: 1
    ```

4.  即使服务不再存在，任务容器也需要几秒钟来清理。你可以在节点上使用 `docker ps` 来验证任务何时被删除。

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

接下来，你将设置一个新服务并应用滚动更新。

{{< button text="应用滚动更新" url="rolling-update.md" >}}
