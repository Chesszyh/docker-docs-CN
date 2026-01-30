---
description: 初始化 Swarm
keywords: tutorial, cluster management, swarm mode, get started, docker engine, 教程, 初始化, Swarm
title: 创建一个 Swarm
weight: 10
notoc: true
---

完成 [教程设置](index.md) 步骤后，您就可以创建一个 Swarm 了。确保主机上的 Docker Engine 守护进程已启动。

1.  打开终端并 SSH 登录到您想要运行管理节点的机器。本教程使用一台名为 `manager1` 的机器。

2.  运行以下命令来创建一个新的 Swarm：

    ```console
    $ docker swarm init --advertise-addr <MANAGER-IP>
    ```

    在本教程中，以下命令在 `manager1` 机器上创建一个 Swarm：

    ```console
    $ docker swarm init --advertise-addr 192.168.99.100
    Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

    `--advertise-addr` 标志配置管理节点将其地址发布为 `192.168.99.100`。Swarm 中的其他节点必须能够通过该 IP 地址访问管理节点。

    输出包含了加入新节点到 Swarm 的命令。节点将根据 `--token` 标志的值以管理节点或工作节点的身份加入。

3.  运行 `docker info` 查看 Swarm 的当前状态：

    ```console
    $ docker info

    Containers: 2
    Running: 0
    Paused: 0
    Stopped: 2
      ...裁剪...
    Swarm: active
      NodeID: dxn1zf6l61qsb1josjja83ngz
      Is Manager: true
      Managers: 1
      Nodes: 1
      ...裁剪...
    ```

4.  运行 `docker node ls` 命令查看节点信息：

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader

    ```

    节点 ID 旁边的 `*` 表示您当前正连接到此节点。

    Docker Engine Swarm 模式会自动以机器主机名命名节点。本教程将在后续步骤中介绍其他列。

## 下一步

接下来，您将向集群再添加两个节点。

{{< button text="再添加两个节点" url="add-nodes.md" >}}
