---
title: 合并
description: 了解合并规则
keywords: compose, compose 规范, 合并, compose 文件参考
aliases: 
 - /compose/compose-file/13-merge/
weight: 100
---

{{% include "compose/merge.md" %}}

这些规则概述如下。

## 映射

YAML `mapping` 通过添加缺失条目和合并冲突条目进行合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    key1: value1
    key2: value2
```

```yaml
services:
  foo:
    key2: VALUE
    key3: value3
```

结果是等效于以下 YAML 树的 Compose 应用程序模型：

```yaml
services:
  foo:
    key1: value1
    key2: VALUE
    key3: value3
```

## 序列

YAML `sequence` 通过将覆盖 Compose 文件中的值附加到前一个文件来合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
```

```yaml
services:
  foo:
    DNS: 
      - 8.8.8.8
```

结果是等效于以下 YAML 树的 Compose 应用程序模型：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
      - 8.8.8.8
```

## 例外

### Shell 命令

合并使用服务属性 [command](services.md#command)、[entrypoint](services.md#entrypoint) 和 [healthcheck: `test`](services.md#healthcheck) 的 Compose 文件时，值将被最新的 Compose 文件覆盖，而不是附加。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    command: ["echo", "foo"]
```

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

结果是等效于以下 YAML 树的 Compose 应用程序模型：

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

### 唯一资源

适用于 [ports](services.md#ports)、[volumes](services.md#volumes)、[secrets](services.md#secrets) 和 [configs](services.md#configs) 服务属性。
虽然这些类型在 Compose 文件中建模为序列，但它们具有特殊的唯一性要求：

| 属性   | 唯一键               |
|-------------|--------------------------|
| volumes     |  target                  |
| secrets     |  target                  |
| configs     |  target                  |
| ports       |  {ip, target, published, protocol}   |

合并 Compose 文件时，Compose 会附加不违反唯一性约束的新条目，并合并共享唯一键的条目。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    volumes:
      - foo:/work
```

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

结果是等效于以下 YAML 树的 Compose 应用程序模型：

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

### 重置值

除了前面描述的机制之外，覆盖 Compose 文件还可以用于从应用程序模型中删除元素。
为此，自定义 [YAML 标签](https://yaml.org/spec/1.2.2/#24-tags) `!reset` 可以设置为
覆盖被覆盖的 Compose 文件设置的值。必须提供属性的有效值，
但该值将被忽略，目标属性将设置为类型的默认值或 `null`。

为了可读性，建议将属性值明确设置为 null (`null`) 或空
数组 `[]`（使用 `!reset null` 或 `!reset []`），以便清楚地表明结果属性将被
清除。

一个基础 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80" 
    environment:
      FOO: BAR           
```

和一个 `compose.override.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports: !reset []
    environment:
      FOO: !reset null
```

结果是：

```yaml
services:
  app:
    image: myapp
```

### 替换值

{{< summary-bar feature_name="Compose 替换文件" >}}

虽然 `!reset` 可用于使用覆盖文件从 Compose 文件中删除声明，但 `!override` 允许您
完全替换属性，绕过标准合并规则。一个典型的例子是完全替换资源定义，以依赖不同的模型但使用相同的名称。

一个基础 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80"
```

要删除原始端口，但公开新端口，使用以下覆盖文件：

```yaml
services:
  app:
    ports: !override
      - "8443:443" 
```

结果是：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8443:443" 
```

如果未使用 `!override`，则根据[上面概述的合并规则](#sequence)，`8080:80` 和 `8443:443` 都将被公开。

## 附加资源

有关如何使用合并创建复合 Compose 文件的更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)
