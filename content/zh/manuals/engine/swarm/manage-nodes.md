---
description: 管理 Swarm 中的现有节点
keywords: guide, swarm mode, node, 节点, 管理
title: 管理 Swarm 中的节点
---

作为 Swarm 管理生命周期的一部分，您可能需要：

* [列出 Swarm 中的节点](#list-nodes)
* [检查单个节点](#inspect-an-individual-node)
* [更新节点](#update-a-node)
* [离开 Swarm](#leave-the-swarm)

## 列出节点

要查看 Swarm 中的节点列表，请在管理节点上运行 `docker node ls`：

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
46aqrk4e473hjbt745z53cr3t    node-5    Ready   Active        Reachable
61pi3d91s0w3b90ijw3deeb2q    node-4    Ready   Active        Reachable
a5b2m3oghd48m8eu391pefq5u    node-3    Ready   Active
e7p8btxeu3ioshyuj6lxiv6g0    node-2    Ready   Active
ehkv3bcimagdese79dn78otj5 *  node-1    Ready   Active        Leader
```

`AVAILABILITY` (可用性) 列显示调度程序是否可以将任务分配给该节点：

* `Active` 意味着调度程序可以将任务分配给该节点。
* `Pause` 意味着调度程序不会向该节点分配新任务，但现有任务仍保持运行。
* `Drain` 意味着调度程序不会向该节点分配新任务。调度程序会关闭所有现有任务，并将其调度到另一个可用的节点上。

`MANAGER STATUS` 列显示节点在 Raft 共识中的参与情况：

* 无值表示该节点是工作节点，不参与 Swarm 管理。
* `Leader` 意味着该节点是主管理节点，负责为 Swarm 做出所有的管理和编排决策。
* `Reachable` 意味着该节点是参与 Raft 共识法定人数的管理节点。如果 Leader 节点不可用，该节点有资格被选举为新的 Leader。
* `Unavailable` 意味着该节点是无法与其他管理节点通信的管理节点。如果管理节点变得不可用，您应该向 Swarm 加入一个新的管理节点，或者将一个工作节点提升为管理节点。

有关 Swarm 管理的更多信息，请参考 [Swarm 管理指南](admin_guide.md)。

## 检查单个节点

您可以在管理节点上运行 `docker node inspect <NODE-ID>` 来查看单个节点的详细信息。输出默认为 JSON 格式，但您可以传递 `--pretty` 标志以人类可读的格式打印结果。例如：

```console
$ docker node inspect self --pretty

ID:                     ehkv3bcimagdese79dn78otj5
Hostname:               node-1
Joined at:              2016-06-16 22:52:44.9910662 +0000 utc
Status:
 State:                 Ready
 Availability:          Active
Manager Status:
 Address:               172.17.0.2:2377
 Raft Status:           Reachable
 Leader:                Yes
Platform:
 Operating System:      linux
 Architecture:          x86_64
Resources:
 CPUs:                  2
 Memory:                1.954 GiB
Plugins:
  Network:              overlay, host, bridge, overlay, null
  Volume:               local
Engine Version:         1.12.0-dev
```

## 更新节点

您可以修改节点属性以：

* [更改节点可用性](#change-node-availability)
* [添加或移除标签元数据](#add-or-remove-label-metadata)
* [更改节点角色](#promote-or-demote-a-node)

### 更改节点可用性

更改节点可用性允许您：

* Drain (排空) 一个管理节点，使其仅执行 Swarm 管理任务，而不参与任务分配。
* Drain 一个节点，以便您可以将其停机维护。
* Pause (暂停) 一个节点，使其无法接收新任务。
* 恢复不可用或已暂停节点的可用性状态。

例如，要将管理节点的可用性更改为 `Drain`：

```console
$ docker node update --availability drain node-1

node-1
```

参见 [列出节点](#list-nodes) 了解不同可用性选项的描述。

### 添加或移除标签元数据

节点标签 (node labels) 提供了一种灵活的节点组织方法。您也可以在服务约束中使用节点标签。在创建服务时应用约束，以限制调度程序分配该服务任务的节点。

在管理节点上运行 `docker node update --label-add` 向节点添加标签元数据。`--label-add` 标志支持 `<key>` 或 `<key>=<value>` 对。

每要添加一个节点标签，就传递一次 `--label-add` 标志：

```console
$ docker node update --label-add foo --label-add bar=baz node-1

node-1
```

您使用 `docker node update` 为节点设置的标签仅适用于 Swarm 内的节点实体。不要将它们与 [dockerd](/manuals/engine/manage-resources/labels.md) 的 Docker 守护进程标签混淆。

因此，节点标签可用于将关键任务限制在满足某些要求的节点上。例如，仅在应运行特殊工作负载的机器上进行调度，比如符合 [PCI-SS 合规性](https://www.pcisecuritystandards.org/) 的机器。

即使工作节点遭到破坏，也无法破坏这些特殊工作负载，因为它无法更改节点标签。

然而，Engine 标签仍然有用，因为某些不影响容器安全编排的功能可能更适合以去中心化的方式设置。例如，Engine 可以有一个标签来指示它具有某种类型的磁盘设备，这可能与安全没有直接关系。这些标签更容易被 Swarm 编排器“信任”。

参考 `docker service create` [CLI 参考](/reference/cli/docker/service/create.md) 了解更多关于服务约束的信息。

### 提升或降级节点

您可以将工作节点提升为管理节点角色。当管理节点变得不可用，或者您想停用一个管理节点进行维护时，这很有用。同样，您也可以将管理节点降级为工作节点角色。

> [!NOTE]
>
> 无论您提升或降级节点的原因为何，都必须始终维持 Swarm 中管理节点的法定人数。有关更多信息，请参考 [Swarm 管理指南](admin_guide.md)。

要提升一个或一组节点，请在管理节点上运行 `docker node promote`：

```console
$ docker node promote node-3 node-2

Node node-3 promoted to a manager in the swarm.
Node node-2 promoted to a manager in the swarm.
```

要降级一个或一组节点，请在管理节点上运行 `docker node demote`：

```console
$ docker node demote node-3 node-2

Manager node-3 demoted in the swarm.
Manager node-2 demoted in the swarm.
```

`docker node promote` 和 `docker node demote` 分别是 `docker node update --role manager` 和 `docker node update --role worker` 的便捷命令。

## 在 Swarm 节点上安装插件

如果您的 Swarm 服务依赖于一个或多个 [插件](/engine/extend/plugin_api/)，这些插件必须在服务可能部署到的每个节点上都可用。您可以手动在每个节点上安装插件，或者通过脚本安装。您还可以通过 Docker API 以类似于全局服务的方式部署插件，方法是指定 `PluginSpec` 而不是 `ContainerSpec`。

> [!NOTE]
>
> 目前无法使用 Docker CLI 或 Docker Compose 向 Swarm 部署插件。此外，无法从私有仓库安装插件。

[`PluginSpec`](/engine/extend/plugin_api/#json-specification) 由插件开发者定义。要将插件添加到所有 Docker 节点，请使用 [`service/create`](/reference/api/engine/v1.31/#operation/ServiceCreate) API，传递 `TaskTemplate` 中定义的 `PluginSpec` JSON。

## 离开 Swarm

在节点上运行 `docker swarm leave` 命令将其从 Swarm 中移除。

例如，要让工作节点离开 Swarm：

```console
$ docker swarm leave

Node left the swarm.
```

当节点离开 Swarm 时，Docker Engine 停止以 Swarm 模式运行。编排器不再向该节点调度任务。

如果该节点是管理节点，您会收到关于维持法定人数的警告。要忽略该警告，请传递 `--force` 标志。如果最后一个管理节点离开 Swarm，Swarm 将变得不可用，需要您采取灾难恢复措施。

有关维持法定人数和灾难恢复的信息，请参考 [Swarm 管理指南](admin_guide.md)。

节点离开 Swarm 后，您可以在管理节点上运行 `docker node rm` 将该节点从节点列表中移除。

例如：

```console
$ docker node rm node-2
```

## 了解更多

* [Swarm 管理指南](admin_guide.md)
* [Docker Engine 命令行参考](/reference/cli/docker/)
* [Swarm 模式教程](swarm-tutorial/_index.md)
