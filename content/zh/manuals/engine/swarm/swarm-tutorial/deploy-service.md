---
description: 向 Swarm 部署一个服务
keywords: tutorial, cluster management, swarm mode, get started, 教程, 服务, 部署
title: 向 Swarm 部署一个服务
weight: 30
notoc: true
---

[创建 Swarm](create-swarm.md) 后，您就可以向 Swarm 部署服务了。在本教程中，您还 [添加了工作节点](add-nodes.md)，但这并不是部署服务的必要条件。

1.  打开终端并 SSH 登录到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行以下命令：

    ```console
    $ docker service create --replicas 1 --name helloworld alpine ping docker.com

    9uk4639qpg7npwf3fn2aasksr
    ```

    * `docker service create` 命令创建服务。
    * `--name` 标志将服务命名为 `helloworld`。
    * `--replicas` 标志指定期望状态为 1 个运行实例。
    * 参数 `alpine ping docker.com` 定义了该服务为一个 Alpine Linux 容器，执行 `ping docker.com` 命令。

3.  运行 `docker service ls` 查看运行中的服务列表：

    ```console
    $ docker service ls

    ID            NAME        SCALE  IMAGE   COMMAND
    9uk4639qpg7n  helloworld  1/1    alpine  ping docker.com
    ```

## 下一步

现在您已经准备好检查该服务了。

{{< button text="检查服务" url="inspect-service.md" >}}
