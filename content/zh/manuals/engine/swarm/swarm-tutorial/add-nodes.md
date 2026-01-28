---
description: Add nodes to the swarm
keywords: tutorial, cluster management, swarm, get started
title: 向 swarm 添加节点
weight: 20
notoc: true
---

一旦你[创建了 swarm](create-swarm.md) 并有了管理节点，你就可以添加工作节点了。

1.  打开终端并 ssh 到你想要运行工作节点的机器。本教程使用名为 `worker1` 的机器。

2.  运行[创建 swarm](create-swarm.md) 教程步骤中 `docker swarm init` 输出产生的命令来创建加入现有 swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

    如果你没有可用的命令，可以在管理节点上运行以下命令来获取工作节点的加入命令：

    ```console
    $ docker swarm join-token worker

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377
    ```

3.  打开终端并 ssh 到你想要运行第二个工作节点的机器。本教程使用名为 `worker2` 的机器。

4.  运行[创建 swarm](create-swarm.md) 教程步骤中 `docker swarm init` 输出产生的命令来创建加入现有 swarm 的第二个工作节点：

    ```console
    $ docker swarm join \
      --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

5.  打开终端并 ssh 到管理节点运行的机器，然后运行 `docker node ls` 命令来查看工作节点：

    ```console
    $ docker node ls
    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
    9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
    ```

    `MANAGER` 列标识了 swarm 中的管理节点。`worker1` 和 `worker2` 在此列中的空状态将它们标识为工作节点。

    像 `docker node ls` 这样的 Swarm 管理命令只能在管理节点上工作。


## 下一步是什么？

现在你的 swarm 由一个管理节点和两个工作节点组成。接下来，你将部署一个服务。

{{< button text="部署服务" url="deploy-service.md" >}}
