---
description: Drain nodes on the swarm
keywords: tutorial, cluster management, swarm, service, drain, get started
title: 排空 swarm 上的节点
weight: 80
notoc: true
---

在本教程的早期步骤中，所有节点都以 `Active` 可用性运行。swarm 管理节点可以将任务分配给任何 `Active` 节点，因此到目前为止所有节点都可以接收任务。

有时，例如在计划维护期间，你需要将节点设置为 `Drain` 可用性。`Drain` 可用性阻止节点从 swarm 管理节点接收新任务。这也意味着管理节点会停止该节点上运行的任务，并在具有 `Active` 可用性的节点上启动副本任务。

> [!IMPORTANT]:
>
> 将节点设置为 `Drain` 不会从该节点删除独立容器，例如使用 `docker run`、`docker compose up` 或 Docker Engine API 创建的容器。节点的状态（包括 `Drain`）仅影响节点调度 swarm 服务工作负载的能力。

1.  如果你还没有，打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  验证所有节点都处于活动可用状态。

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    1bcef6utixb0l0ca7gxuivsj0    worker2   Ready   Active
    38ciaotwjuritcdtn9npbnkuz    worker1   Ready   Active
    e216jshn25ckzbvmwlnh5jr3g *  manager1  Ready   Active        Leader
    ```

3.  如果你还没有运行[滚动更新](rolling-update.md)教程中的 `redis` 服务，现在启动它：

    ```console
    $ docker service create --replicas 3 --name redis --update-delay 10s redis:7.4.0

    c5uo6kdmzpon37mgj9mwglcfw
    ```

4.  运行 `docker service ps redis` 查看 swarm 管理节点如何将任务分配给不同节点：

    ```console
    $ docker service ps redis

    NAME                               IMAGE        NODE     DESIRED STATE  CURRENT STATE
    redis.1.7q92v0nr1hcgts2amcjyqg3pq  redis:7.4.0  manager1 Running        Running 26 seconds
    redis.2.7h2l8h3q3wqy5f66hlv9ddmi6  redis:7.4.0  worker1  Running        Running 26 seconds
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd  redis:7.4.0  worker2  Running        Running 26 seconds
    ```

    在这种情况下，swarm 管理节点将每个节点分配了一个任务。你的环境中任务在节点之间的分布可能不同。

5.  运行 `docker node update --availability drain <NODE-ID>` 来排空一个已分配任务的节点：

    ```console
    $ docker node update --availability drain worker1

    worker1
    ```

6.  检查节点以查看其可用性：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Drain
    ...snip...
    ```

    被排空的节点在 `Availability` 中显示 `Drain`。

7.  运行 `docker service ps redis` 查看 swarm 管理节点如何更新 `redis` 服务的任务分配：

    ```console
    $ docker service ps redis

    NAME                                    IMAGE        NODE      DESIRED STATE  CURRENT STATE           ERROR
    redis.1.7q92v0nr1hcgts2amcjyqg3pq       redis:7.4.0  manager1  Running        Running 4 minutes
    redis.2.b4hovzed7id8irg1to42egue8       redis:7.4.0  worker2   Running        Running About a minute
     \_ redis.2.7h2l8h3q3wqy5f66hlv9ddmi6   redis:7.4.0  worker1   Shutdown       Shutdown 2 minutes ago
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd       redis:7.4.0  worker2   Running        Running 4 minutes
    ```

    swarm 管理节点通过结束 `Drain` 可用性节点上的任务并在 `Active` 可用性节点上创建新任务来维护期望状态。

8.  运行 `docker node update --availability active <NODE-ID>` 将被排空的节点恢复为活动状态：

    ```console
    $ docker node update --availability active worker1

    worker1
    ```

9.  检查节点查看更新后的状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Active
    ...snip...
    ```

    当你将节点恢复为 `Active` 可用性时，它可以接收新任务：

    * 在服务更新期间进行扩展
    * 在滚动更新期间
    * 当你将另一个节点设置为 `Drain` 可用性时
    * 当任务在另一个活动节点上失败时

## 下一步

接下来，你将学习如何使用 Swarm 模式路由网格。

{{< button text="使用 Swarm 模式路由网格" url="../ingress.md" >}}
