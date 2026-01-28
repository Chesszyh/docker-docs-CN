---
description: 如何使用 Docker Compose 的 include 顶级元素
keywords: compose, docker, include, compose file
title: Include
aliases:
- /compose/multiple-compose-files/include/
---

{{< summary-bar feature_name="Compose include" >}}

{{% include "compose/include.md" %}}

[`include` 顶级元素](/reference/compose-file/include.md)有助于将负责代码的工程团队直接反映在配置文件的组织中。它还解决了 [`extends`](extends.md) 和 [merge](merge.md) 存在的相对路径问题。

`include` 部分中列出的每个路径都作为单独的 Compose 应用程序模型加载，具有自己的项目目录，用于解析相对路径。

一旦包含的 Compose 应用程序加载完成，所有资源都会被复制到当前的 Compose 应用程序模型中。

> [!NOTE]
>
> `include` 递归应用，因此声明了自己 `include` 部分的被包含 Compose 文件也会导致那些文件被包含。

## 示例

```yaml
include:
  - my-compose-include.yaml  #声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB #直接使用 serviceB，就像它在这个 Compose 文件中声明一样
```

`my-compose-include.yaml` 管理 `serviceB`，其中详细说明了一些副本、用于检查数据的 Web UI、隔离的网络、用于数据持久化的卷等。依赖 `serviceB` 的应用程序不需要了解基础设施细节，并将 Compose 文件作为可以依赖的构建块使用。

这意味着管理 `serviceB` 的团队可以重构自己的数据库组件以引入额外的服务，而不会影响任何依赖团队。这也意味着依赖团队不需要在每个运行的 Compose 命令上包含额外的标志。

```yaml
include:
  - oci://docker.io/username/my-compose-app:latest # 使用存储为 OCI 工件的 Compose 文件
services:
  serviceA:
    build: .
    depends_on:
      - serviceB
```
`include` 允许你从远程来源引用 Compose 文件，例如 OCI 工件或 Git 仓库。
这里 `serviceB` 定义在存储在 Docker Hub 上的 Compose 文件中。

## 对包含的 Compose 文件使用覆盖

如果来自 `include` 的任何资源与被包含 Compose 文件的资源冲突，Compose 会报告错误。此规则防止
与被包含 compose 文件作者定义的资源发生意外冲突。但是，在某些情况下你可能想要自定义
包含的模型。这可以通过向 include 指令添加覆盖文件来实现：

```yaml
include:
  - path :
      - third-party/compose.yaml
      - override.yaml  # 第三方模型的本地覆盖
```

此方法的主要限制是你需要为每个 include 维护一个专用的覆盖文件。对于具有多个
include 的复杂项目，这将导致许多 Compose 文件。

另一个选项是使用 `compose.override.yaml` 文件。虽然当使用 `include` 的文件声明相同
资源时冲突会被拒绝，但全局 Compose 覆盖文件可以覆盖生成的合并模型，如以下示例所示：

主 `compose.yaml` 文件：
```yaml
include:
  - team-1/compose.yaml # 声明 service-1
  - team-2/compose.yaml # 声明 service-2
```

覆盖 `compose.override.yaml` 文件：
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

结合起来，这允许你受益于第三方可重用组件，并根据你的需要调整 Compose 模型。

## 参考信息

[`include` 顶级元素](/reference/compose-file/include.md)
