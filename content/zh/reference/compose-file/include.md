---
title: Include
description: 了解 include
keywords: compose, compose specification, include, compose file reference
aliases:
 - /compose/compose-file/14-include/
weight: 110
---

{{< summary-bar feature_name="Composefile include" >}}

Compose 应用程序可以声明对另一个 Compose 应用程序的依赖。这在以下情况下很有用：
- 你想重用其他 Compose 文件。
- 你需要将应用程序模型的部分分解到单独的 Compose 文件中，以便可以单独管理或与他人共享。
- 团队需要保持 Compose 文件相对简单，因为它只需为较大部署中的自己子域声明有限数量的资源。

`include` 顶级部分用于定义对另一个 Compose 应用程序或子域的依赖。
`include` 部分中列出的每个路径都作为单独的 Compose 应用程序模型加载，具有自己的项目目录，以解析相对路径。

一旦包含的 Compose 应用程序被加载，所有资源定义都会被复制到当前 Compose 应用程序模型中。如果资源名称冲突，Compose 会显示警告且不会尝试合并它们。为了强制执行此操作，`include` 在选定用于定义 Compose 应用程序模型的 Compose 文件被解析和合并后进行评估，以便检测 Compose 文件之间的冲突。

`include` 递归应用，因此声明了自己的 `include` 部分的被包含 Compose 文件会触发这些其他文件也被包含。

从包含的 Compose 文件中引入的任何卷、网络或其他资源都可以被当前 Compose 应用程序用于跨服务引用。例如：

```yaml
include:
  - my-compose-include.yaml  #声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB #直接使用 serviceB，就像它在此 Compose 文件中声明的一样
```

Compose 还支持在 `include` 中使用插值变量。建议你[指定必需变量](interpolation.md)。例如：

```text
include:
  -${INCLUDE_PATH:?FOO}/compose.yaml
```

## 短语法

短语法仅定义其他 Compose 文件的路径。文件以父文件夹作为项目目录加载，并加载可选的 `.env` 文件以通过插值定义任何变量的默认值。本地项目的环境可以覆盖这些值。

```yaml
include:
  - ../commons/compose.yaml
  - ../another_domain/compose.yaml

services:
  webapp:
    depends_on:
      - included-service # 由 another_domain 定义
```

在前面的示例中，`../commons/compose.yaml` 和 `../another_domain/compose.yaml` 都作为单独的 Compose 项目加载。被 `include` 引用的 Compose 文件中的相对路径相对于它们自己的 Compose 文件路径解析，而不是基于本地项目的目录。变量使用同一文件夹中可选的 `.env` 文件中设置的值进行插值，并被本地项目的环境覆盖。

## 长语法

长语法提供对子项目解析的更多控制：

```yaml
include:
   - path: ../commons/compose.yaml
     project_directory: ..
     env_file: ../another/.env
```

### `path`

`path` 是必需的，定义要解析并包含到本地 Compose 模型中的 Compose 文件的位置。

`path` 可以设置为：

- 字符串：当使用单个 Compose 文件时。
- 字符串列表：当需要将多个 Compose 文件[合并](merge.md)在一起以定义本地应用程序的 Compose 模型时。

```yaml
include:
   - path:
       - ../commons/compose.yaml
       - ./commons-override.yaml
```

### `project_directory`

`project_directory` 定义解析 Compose 文件中设置的相对路径的基本路径。默认为被包含 Compose 文件的目录。

### `env_file`

`env_file` 定义在解析 Compose 文件时用于定义插值变量默认值的环境文件。默认为被解析 Compose 文件的 `project_directory` 中的 `.env` 文件。

当需要合并多个环境文件以定义项目环境时，`env_file` 可以设置为字符串或字符串列表。

```yaml
include:
   - path: ../another/compose.yaml
     env_file:
       - ../another/.env
       - ../another/dev.env
```

本地项目的环境优先于 Compose 文件设置的值，以便本地项目可以覆盖值进行自定义。

## 其他资源

有关使用 `include` 的更多信息，请参阅[使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)
