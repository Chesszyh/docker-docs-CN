---
description: 在 Swarm 上排空 (drain) 节点
keywords: tutorial, cluster management, swarm, service, drain, get started, 教程, 节点排空
title: 在 Swarm 上排空一个节点
weight: 80
notoc: true
---

在教程的早期步骤中，所有节点都以 `Active` (活动) 可用性运行。Swarm 管理节点可以将任务分配给任何 `Active` 节点，因此到目前为止，所有节点都可以接收任务。

有时，例如计划维护期间，您需要将节点设置为 `Drain` (排空) 可用性。`Drain` 可用性防止节点接收来自 Swarm 管理节点的新任务。这也意味着管理节点会停止在该节点上运行的任务，并在具有 `Active` 可用性的节点上启动副本任务。

> [!IMPORTANT]: 
>
> 将节点设置为 `Drain` 不会移除该节点上的独立容器，例如使用 `docker run`、`docker compose up` 或 Docker Engine API 创建的容器。节点的各种状态 (包括 `Drain`) 仅影响节点调度 Swarm 服务工作负载的能力。

1.  如果您还没有这样做，请打开终端并 SSH 登录到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  验证您的所有节点是否都处于活动可用状态。

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    1bcef6utixb0l0ca7gxuivsj0    worker2   Ready   Active
    38ciaotwjuritcdtn9npbnkuz    worker1   Ready   Active
    e216jshn25ckzbvmwlnh5jr3g *  manager1  Ready   Active        Leader
    ```

3.  如果您还没有运行来自 [滚动更新](rolling-update.md) 教程的 `redis` 服务，请现在启动它：

    ```console
    $ docker service create --replicas 3 --name redis --update-delay 10s redis:7.4.0

    c5uo6kdmzpon37mgj9mwglcfw
    ```

4.  运行 `docker service ps redis` 查看 Swarm 管理节点如何将任务分配给不同的节点：

    ```console
    $ docker service ps redis

    NAME                               IMAGE        NODE     DESIRED STATE  CURRENT STATE
    redis.1.7q92v0nr1hcgts2amcjyqg3pq  redis:7.4.0  manager1 Running        Running 26 seconds
    redis.2.7h2l8h3q3wqy5f66hlv9ddmi6  redis:7.4.0  worker1  Running        Running 26 seconds
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd  redis:7.4.0  worker2  Running        Running 26 seconds
    ```

    在这种情况下，Swarm 管理节点向每个节点分配了一个任务。在您的环境中，您可能会看到任务在节点之间的分布有所不同。

5.  运行 `docker node update --availability drain <NODE-ID>` 来排空分配了任务的节点：

    ```console
    $ docker node update --availability drain worker1

    worker1
    ```

6.  检查该节点以核实其可用性：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Drain
    ...裁剪...
    ```

    排空的节点在 `Availability` 下显示为 `Drain`。

7.  运行 `docker service ps redis` 查看 Swarm 管理节点如何更新 `redis` 服务的任务分配：

    ```console
    $ docker service ps redis

    NAME                                    IMAGE        NODE      DESIRED STATE  CURRENT STATE           ERROR
    redis.1.7q92v0nr1hcgts2amcjyqg3pq       redis:7.4.0  manager1  Running        Running 4 minutes
    redis.2.b4hovzed7id8irg1to42egue8       redis:7.4.0  worker2   Running        Running About a minute
     \_ redis.2.7h2l8h3q3wqy5f66hlv9ddmi6   redis:7.4.0  worker1   Shutdown       Shutdown 2 minutes ago
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd       redis:7.4.0  worker2   Running        Running 4 minutes
    ```

    Swarm 管理节点通过在具有 `Drain` 可用性的节点上结束任务，并在具有 `Active` 可用性的节点上创建新任务，来维持期望状态。

8.  运行 `docker node update --availability active <NODE-ID>` 将排空的节点恢复到活动状态：

    ```console
    $ docker node update --availability active worker1

    worker1
    ```

9.  检查该节点以查看更新后的状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Active
    ...裁剪...
    ```

    当您将节点重新设置为 `Active` 可用性后，它可以重新接收新任务：

    * 在向上扩展的服务更新期间
    * 在滚动更新期间
    * 当您将另一个节点设置为 `Drain` 可用性时
    * 当某个任务在另一个活动节点上失败时

## 下一步

接下来，您将学习如何使用 Swarm 模式的路由网格 (routing mesh)

{{< button text="使用 Swarm 模式路由网格" url="../ingress.md" >}}
