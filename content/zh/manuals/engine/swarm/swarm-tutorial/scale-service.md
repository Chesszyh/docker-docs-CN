---
description: Scale the service running in the swarm
keywords: tutorial, cluster management, swarm mode, scale, get started
title: 扩展 swarm 中的服务
weight: 50
notoc: true
---

一旦你已经[部署了服务](deploy-service.md)到 swarm，你就可以使用 Docker CLI 来扩展服务中的容器数量。在服务中运行的容器称为任务（task）。

1.  如果你还没有，打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行以下命令更改在 swarm 中运行的服务的期望状态：

    ```console
    $ docker service scale <SERVICE-ID>=<NUMBER-OF-TASKS>
    ```

    例如：

    ```console
    $ docker service scale helloworld=5

    helloworld scaled to 5
    ```

3.  运行 `docker service ps <SERVICE-ID>` 查看更新后的任务列表：

    ```console
    $ docker service ps helloworld

    NAME                                    IMAGE   NODE      DESIRED STATE  CURRENT STATE
    helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2   Running        Running 7 minutes
    helloworld.2.c7a7tcdq5s0uk3qr88mf8xco6  alpine  worker1   Running        Running 24 seconds
    helloworld.3.6crl09vdcalvtfehfh69ogfb1  alpine  worker1   Running        Running 24 seconds
    helloworld.4.auky6trawmdlcne8ad8phb0f1  alpine  manager1  Running        Running 24 seconds
    helloworld.5.ba19kca06l18zujfwxyc5lkyn  alpine  worker2   Running        Running 24 seconds
    ```

    你可以看到 swarm 创建了 4 个新任务，扩展到总共 5 个 Alpine Linux 运行实例。这些任务分布在 swarm 的三个节点上。一个正在 `manager1` 上运行。

4.  运行 `docker ps` 查看你连接的节点上运行的容器。以下示例显示在 `manager1` 上运行的任务：

    ```console
    $ docker ps

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    528d68040f95        alpine:latest       "ping docker.com"   About a minute ago   Up About a minute                       helloworld.4.auky6trawmdlcne8ad8phb0f1
    ```

    如果你想查看其他节点上运行的容器，请 ssh 到那些节点并运行 `docker ps` 命令。

## 下一步

在教程的这一点上，你已经完成了 `helloworld` 服务。接下来，你将删除该服务。

{{< button text="删除服务" url="delete-service.md" >}}
