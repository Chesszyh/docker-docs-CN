---
description: Apply rolling updates to a service on the swarm
keywords: tutorial, cluster management, swarm, service, rolling-update
title: 对服务应用滚动更新
weight: 70
notoc: true
---

在本教程的前一步中，你[扩展](scale-service.md)了服务的实例数量。在本教程的这一部分，你将部署一个基于 Redis 7.4.0 容器标签的服务。然后使用滚动更新将服务升级到使用 Redis 7.4.1 容器镜像。

1.  如果你还没有，打开终端并 ssh 到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  将你的 Redis 标签部署到 swarm，并配置 10 秒的更新延迟。注意以下示例显示的是较旧的 Redis 标签：

    ```console
    $ docker service create \
      --replicas 3 \
      --name redis \
      --update-delay 10s \
      redis:7.4.0

    0u6a4s31ybk7yw2wyvtikmu50
    ```

    你在服务部署时配置滚动更新策略。

    `--update-delay` 标志配置服务任务或任务集之间的更新时间延迟。你可以将时间 `T` 描述为秒数 `Ts`、分钟数 `Tm` 或小时数 `Th` 的组合。因此 `10m30s` 表示 10 分 30 秒的延迟。

    默认情况下，调度器一次更新 1 个任务。你可以传递 `--update-parallelism` 标志来配置调度器同时更新的最大服务任务数。

    默认情况下，当对单个任务的更新返回 `RUNNING` 状态时，调度器会调度另一个任务进行更新，直到所有任务都更新完毕。如果在更新过程中任何时候某个任务返回 `FAILED`，调度器会暂停更新。你可以使用 `docker service create` 或 `docker service update` 的 `--update-failure-action` 标志来控制行为。

3.  检查 `redis` 服务：

    ```console
    $ docker service inspect --pretty redis

    ID:             0u6a4s31ybk7yw2wyvtikmu50
    Name:           redis
    Service Mode:   Replicated
     Replicas:      3
    Placement:
     Strategy:	    Spread
    UpdateConfig:
     Parallelism:   1
     Delay:         10s
    ContainerSpec:
     Image:         redis:7.4.0
    Resources:
    Endpoint Mode:  vip
    ```

4.  现在你可以更新 `redis` 的容器镜像。swarm 管理节点根据 `UpdateConfig` 策略将更新应用到节点：

    ```console
    $ docker service update --image redis:7.4.1 redis
    redis
    ```

    调度器默认按如下方式应用滚动更新：

    * 停止第一个任务。
    * 为已停止的任务调度更新。
    * 启动更新后任务的容器。
    * 如果任务的更新返回 `RUNNING`，等待指定的延迟期后再启动下一个任务。
    * 如果在更新过程中任何时候任务返回 `FAILED`，暂停更新。

5.  运行 `docker service inspect --pretty redis` 查看期望状态中的新镜像：

    ```console
    $ docker service inspect --pretty redis

    ID:             0u6a4s31ybk7yw2wyvtikmu50
    Name:           redis
    Service Mode:   Replicated
     Replicas:      3
    Placement:
     Strategy:	    Spread
    UpdateConfig:
     Parallelism:   1
     Delay:         10s
    ContainerSpec:
     Image:         redis:7.4.1
    Resources:
    Endpoint Mode:  vip
    ```

    `service inspect` 的输出会显示你的更新是否因失败而暂停：

    ```console
    $ docker service inspect --pretty redis

    ID:             0u6a4s31ybk7yw2wyvtikmu50
    Name:           redis
    ...snip...
    Update status:
     State:      paused
     Started:    11 seconds ago
     Message:    update paused due to failure or early termination of task 9p7ith557h8ndf0ui9s0q951b
    ...snip...
    ```

    要重新启动暂停的更新，请运行 `docker service update <SERVICE-ID>`。例如：

    ```console
    $ docker service update redis
    ```

    为避免重复某些更新失败，你可能需要通过向 `docker service update` 传递标志来重新配置服务。

6.  运行 `docker service ps <SERVICE-ID>` 观察滚动更新：

    ```console
    $ docker service ps redis

    NAME                                   IMAGE        NODE       DESIRED STATE  CURRENT STATE            ERROR
    redis.1.dos1zffgeofhagnve8w864fco      redis:7.4.1  worker1    Running        Running 37 seconds
     \_ redis.1.88rdo6pa52ki8oqx6dogf04fh  redis:7.4.0  worker2    Shutdown       Shutdown 56 seconds ago
    redis.2.9l3i4j85517skba5o7tn5m8g0      redis:7.4.1  worker2    Running        Running About a minute
     \_ redis.2.66k185wilg8ele7ntu8f6nj6i  redis:7.4.0  worker1    Shutdown       Shutdown 2 minutes ago
    redis.3.egiuiqpzrdbxks3wxgn8qib1g      redis:7.4.1  worker1    Running        Running 48 seconds
     \_ redis.3.ctzktfddb2tepkr45qcmqln04  redis:7.4.0  mmanager1  Shutdown       Shutdown 2 minutes ago
    ```

    在 Swarm 更新所有任务之前，你可以看到一些正在运行 `redis:7.4.0`，而另一些正在运行 `redis:7.4.1`。上面的输出显示了滚动更新完成后的状态。

## 下一步

接下来，你将学习如何排空 swarm 中的节点。

{{< button text="排空节点" url="drain-node.md" >}}
