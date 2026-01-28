---
description: Initialize the swarm
keywords: tutorial, cluster management, swarm mode, get started, docker engine
title: 创建 swarm
weight: 10
notoc: true
---

完成[教程设置](index.md)步骤后，你就可以创建 swarm 了。确保主机上的 Docker 引擎守护进程已启动。

1.  打开终端并 ssh 到你想要运行管理节点的机器。本教程使用名为 `manager1` 的机器。

2.  运行以下命令创建新的 swarm：

    ```console
    $ docker swarm init --advertise-addr <MANAGER-IP>
    ```

    在本教程中，以下命令在 `manager1` 机器上创建 swarm：

    ```console
    $ docker swarm init --advertise-addr 192.168.99.100
    Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

    `--advertise-addr` 标志将管理节点配置为发布其地址为 `192.168.99.100`。swarm 中的其他节点必须能够通过该 IP 地址访问管理节点。

    输出包含将新节点加入 swarm 的命令。节点将作为管理节点或工作节点加入，具体取决于 `--token` 标志的值。

3.  运行 `docker info` 查看 swarm 的当前状态：

    ```console
    $ docker info

    Containers: 2
    Running: 0
    Paused: 0
    Stopped: 2
      ...snip...
    Swarm: active
      NodeID: dxn1zf6l61qsb1josjja83ngz
      Is Manager: true
      Managers: 1
      Nodes: 1
      ...snip...
    ```

4.  运行 `docker node ls` 命令查看节点信息：

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader

    ```

    节点 ID 旁边的 `*` 表示你当前连接在该节点上。

    Docker 引擎 Swarm 模式会自动使用机器主机名命名节点。本教程将在后续步骤中介绍其他列。

## 下一步

接下来，你将再向集群添加两个节点。

{{< button text="再添加两个节点" url="add-nodes.md" >}}
