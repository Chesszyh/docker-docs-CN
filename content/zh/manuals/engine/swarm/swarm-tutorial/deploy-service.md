---
description: Deploy a service to the swarm
keywords: tutorial, cluster management, swarm mode, get started
title: 部署服务到 swarm
weight: 30
notoc: true
---

[创建 swarm](create-swarm.md) 后，你可以将服务部署到 swarm。在本教程中，你还[添加了工作节点](add-nodes.md)，但这不是部署服务的必要条件。

1.  打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行以下命令：

    ```console
    $ docker service create --replicas 1 --name helloworld alpine ping docker.com

    9uk4639qpg7npwf3fn2aasksr
    ```

    * `docker service create` 命令创建服务。
    * `--name` 标志将服务命名为 `helloworld`。
    * `--replicas` 标志指定期望状态为 1 个运行实例。
    * 参数 `alpine ping docker.com` 将服务定义为执行命令 `ping docker.com` 的 Alpine Linux 容器。

3.  运行 `docker service ls` 查看正在运行的服务列表：

    ```console
    $ docker service ls

    ID            NAME        SCALE  IMAGE   COMMAND
    9uk4639qpg7n  helloworld  1/1    alpine  ping docker.com
    ```

## 下一步

现在你可以检查服务了。

{{< button text="检查服务" url="inspect-service.md" >}}
