---
description: 如何使用 Docker Compose 的顶级元素 include
keywords: compose, docker, 包含, compose 文件
title: 包含 (Include)
aliases:
- /compose/multiple-compose-files/include/
---

{{< summary-bar feature_name="Compose 包含功能" >}}

{{% include "compose/include.md" %}}

[`include` 顶级元素](/reference/compose-file/include.md) 有助于在配置文件组织中直接反映负责代码的工程团队。它还解决了 [`extends`](extends.md) 和 [合并 (merge)](merge.md) 存在的相对路径问题。 

`include` 部分中列出的每个路径都会作为一个独立的 Compose 应用程序模型加载，并拥有自己的项目目录，以便解析相对路径。

一旦包含的 Compose 应用程序加载完毕，所有资源都会被复制到当前的 Compose 应用程序模型中。

> [!NOTE]
>
> `include` 是递归应用的，因此如果被包含的 Compose 文件声明了它自己的 `include` 部分，也会导致那些文件被包含进来。

## 示例

```yaml
include:
  - my-compose-include.yaml  # 声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB # 直接使用 serviceB，就像它是在此 Compose 文件中声明的一样
```

`my-compose-include.yaml` 管理着 `serviceB`，其中包括副本数、用于检查数据的 Web UI、隔离的网络、用于数据持久化的卷等详细信息。依赖于 `serviceB` 的应用程序不需要知道这些基础设施细节，而是将该 Compose 文件作为一个可以信赖的构建块来使用。 

这意味着管理 `serviceB` 的团队可以重构自己的数据库组件以引入额外的服务，而不会影响任何依赖团队。这也意味着依赖团队在运行每个 Compose 命令时不需要包含额外的标志。

```yaml
include:
  - oci://docker.io/username/my-compose-app:latest # 使用存储为 OCI 构件的 Compose 文件
services:
  serviceA:
    build: .
    depends_on:
      - serviceB 
```
`include` 允许您引用来自远程源（如 OCI 构件或 Git 仓库）的 Compose 文件。在这里，`serviceB` 定义在存储于 Docker Hub 的 Compose 文件中。

## 对包含的 Compose 文件使用覆盖 (Overrides)

如果来自 `include` 的任何资源与被包含的 Compose 文件中的资源冲突，Compose 会报错。此规则旨在防止与被包含 Compose 文件作者定义的资源发生意外冲突。然而，在某些情况下，您可能希望自定义被包含的模型。这可以通过向 include 指令添加覆盖文件来实现：

```yaml
include:
  - path : 
      - third-party/compose.yaml
      - override.yaml  # 针对第三方模型的本地覆盖
```

这种方法的主要局限在于您需要为每个包含维护一个专门的覆盖文件。对于具有多个包含的复杂项目，这将导致产生许多 Compose 文件。

另一个选项是使用 `compose.override.yaml` 文件。虽然在使用 `include` 的文件中声明相同资源会导致冲突被拒绝，但全局 Compose 覆盖文件可以覆盖生成的合并模型，如以下示例所示：

主 `compose.yaml` 文件：
```yaml
include:
  - team-1/compose.yaml # 声明 service-1
  - team-2/compose.yaml # 声明 service-2
```

覆盖文件 `compose.override.yaml`：
```yaml
services:
  service-1:
    # 覆盖包含的 service-1 以启用调试器端口
    ports:
      - 2345:2345

  service-2:
    # 覆盖包含的 service-2 以使用包含测试数据的本地数据文件夹
    volumes:
      - ./data:/data
```

结合在一起，这使您可以从第三方可重用组件中受益，并根据需要调整 Compose 模型。

## 参考信息

[`include` 顶级元素](/reference/compose-file/include.md)
