---
description: 向 Swarm 添加节点
keywords: tutorial, cluster management, swarm, get started, 教程, 节点
title: 向 Swarm 添加节点
weight: 20
notoc: true
---

一旦您使用管理节点 [创建了一个 Swarm](create-swarm.md)，就可以准备添加工作节点了。

1.  打开终端并 SSH 登录到您想要运行工作节点的机器。本教程使用名称 `worker1`。

2.  运行 [创建一个 Swarm](create-swarm.md) 教程步骤中 `docker swarm init` 输出的命令，以创建一个加入现有 Swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

    如果您找不到该命令，可以在管理节点上运行以下命令来检索工作节点的 join 命令：

    ```console
    $ docker swarm join-token worker

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377
    ```

3.  打开终端并 SSH 登录到您想要运行第二个工作节点的机器。本教程使用名称 `worker2`。

4.  运行 [创建一个 Swarm](create-swarm.md) 教程步骤中 `docker swarm init` 输出的命令，以创建一个加入现有 Swarm 的第二个工作节点：

    ```console
    $ docker swarm join \
      --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

5.  打开终端并 SSH 登录到运行管理节点的机器，运行 `docker node ls` 命令查看工作节点：

    ```console
    $ docker node ls
    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
    9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
    ```

    `MANAGER STATUS` 列标识了 Swarm 中的管理节点。对于 `worker1` 和 `worker2`，该列为空状态，标识它们为工作节点。

    像 `docker node ls` 这样的 Swarm 管理命令只能在管理节点上运行。


## 下一步

现在您的 Swarm 由一个管理节点和两个工作节点组成。下一步，您将部署一个服务。

{{< button text="部署一个服务" url="deploy-service.md" >}}
