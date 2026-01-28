---
title: 使用容器进行 Bun 开发
linkTitle: 开发你的应用
weight: 20
keywords: bun, local, development
description: 了解如何在本地开发你的 Bun 应用程序。
aliases:
- /language/bun/develop/
---

## 先决条件

完成 [容器化 Bun 应用程序](containerize.md)。

## 概览

在本节中，你将学习如何为容器化应用程序设置开发环境。这包括：

- 配置 Compose 以在你编辑并保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录更改为你想要工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

## 自动更新服务

使用 Compose Watch 在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开 `compose.yml` 文件，然后添加 Compose Watch 指令。以下示例展示了如何将 Compose Watch 添加到 `compose.yml` 文件中。

```yaml {hl_lines="9-12",linenos=true}
services:
  server:
    image: bun-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令以使用 Compose Watch 运行你的应用程序。

```console
$ docker compose watch
```

现在，如果你修改 `server.js`，你将实时看到更改，而无需重新构建镜像。

要进行测试，请在你喜欢的文本编辑器中打开 `server.js` 文件，并将消息从 `{"Status" : "OK"}` 更改为 `{"Status" : "Updated"}`。保存文件并刷新浏览器 `http://localhost:3000`。你应该看到更新后的消息。

在终端中按 `ctrl+c` 停止应用程序。

## 总结

在本节中，你还学习了如何使用 Compose Watch 在更新代码时自动重建并运行容器。

相关信息：
 - [Compose 文件参考](/reference/compose-file/)
 - [Compose 文件 watch](/manuals/compose/how-tos/file-watch.md)
 - [多阶段构建](/manuals/build/building/multi-stage.md)

## 后续步骤

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 管道。
