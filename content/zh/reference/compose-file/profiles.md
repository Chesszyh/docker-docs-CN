---
title: 配置文件
description: 了解配置文件
keywords: compose, compose 规范, 配置文件, compose 文件参考
aliases: 
 - /compose/compose-file/15-profiles/
weight: 120
---

通过配置文件，您可以定义一组活动配置文件，以便您的 Compose 应用程序模型适应各种用途和环境。

[services](services.md) 顶级元素支持 `profiles` 属性来定义命名配置文件列表。
没有 `profiles` 属性的服务始终启用。

当列出的 `profiles` 都不匹配活动配置文件时，Compose 会忽略服务，除非服务被命令明确指定。在这种情况下，其配置文件将添加到活动配置文件集中。

> [!NOTE]
>
> 所有其他顶级元素不受 `profiles` 影响，并且始终处于活动状态。

对其他服务的引用（通过 `links`、`extends` 或共享资源语法 `service:xxx`）不会
自动启用否则会被活动配置文件忽略的组件。相反，Compose 会返回错误。

## 示例

```yaml
services:
  web:
    image: web_image

  test_lib:
    image: test_lib_image
    profiles:
      - test

  coverage_lib:
    image: coverage_lib_image
    depends_on:
      - test_lib
    profiles:
      - test

  debug_lib:
    image: debug_lib_image
    depends_on:
      - test_lib
    profiles:
      - debug
```

在上面的示例中：

- 如果 Compose 应用程序模型在没有启用配置文件的情况下进行解析，它只包含 `web` 服务。
- 如果启用了 `test` 配置文件，则模型包含服务 `test_lib` 和 `coverage_lib`，以及始终启用的服务 `web`。
- 如果启用了 `debug` 配置文件，则模型包含 `web` 和 `debug_lib` 服务，但不包含 `test_lib` 和 `coverage_lib`，
  因此模型在 `debug_lib` 的 `depends_on` 约束方面无效。
- 如果同时启用了 `debug` 和 `test` 配置文件，则模型包含所有服务；`web`、`test_lib`、`coverage_lib` 和 `debug_lib`。
- 如果 Compose 以 `test_lib` 作为要运行的显式服务执行，则 `test_lib` 和 `test` 配置文件
  即使未启用 `test` 配置文件也处于活动状态。
- 如果 Compose 以 `coverage_lib` 作为要运行的显式服务执行，则服务 `coverage_lib` 和
  `test` 配置文件处于活动状态，并且 `test_lib` 作为依赖项被拉入。
- 如果 Compose 以 `debug_lib` 作为要运行的显式服务执行，则模型再次
  在 `debug_lib` 的 `depends_on` 约束方面无效，因为 `debug_lib` 和 `test_lib` 没有共同的
  列出的配置文件。
- 如果 Compose 以 `debug_lib` 作为要运行的显式服务执行，并且启用了 `test` 配置文件，
  则 `debug` 配置文件会自动启用，并且服务 `test_lib` 作为依赖项被拉入，从而启动两个
  服务 `debug_lib` 和 `test_lib`。

请参阅如何在 [Docker Compose](/manuals/compose/how-tos/profiles.md) 中使用 `profiles`。
