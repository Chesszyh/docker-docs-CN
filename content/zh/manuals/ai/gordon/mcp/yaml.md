---
title: YAML 配置
description: 了解如何将 MCP 服务器与 Gordon 结合使用
keywords: ai, mcp, gordon
aliases: 
 - /desktop/features/gordon/mcp/yaml/
---

Docker 已与 Anthropic 合作，为 [mcp 命名空间](https://hub.docker.com/u/mcp) 下 Docker Hub 上可用的 MCP 服务器的 [参考实现](https://github.com/modelcontextprotocol/servers/) 构建容器镜像。

当您在终端中运行 `docker ai` 命令提问时，Gordon 会在您的工作目录中查找 `gordon-mcp.yml` 文件（如果存在），以获取在该上下文中应使用的 MCP 服务器列表。`gordon-mcp.yml` 文件是一个 Docker Compose 文件，它将 MCP 服务器配置为 Gordon 可以访问的 Compose 服务。

以下最小示例展示了如何使用 [mcp-time 服务器](https://hub.docker.com/r/mcp/time) 为 Gordon 提供时间功能。有关更多信息，您可以查看 [源代码和文档](https://github.com/modelcontextprotocol/servers/tree/main/src/time)。

在您的工作目录中创建 `gordon-mcp.yml` 文件并添加时间服务器：

```yaml
services:
  time:
    image: mcp/time
```

有了这个文件，您现在可以要求 Gordon 告诉您另一个时区的时间：

  ```bash
  $ docker ai '基里巴斯现在几点？'
  
      • 调用 get_current_time
  
    基里巴斯（塔拉瓦）现在是 2025 年 1 月 7 日晚上 9:38。
  
  ```

如您所见，Gordon 找到了 MCP 时间服务器并在需要时调用了它的工具。

## 高级用法

一些 MCP 服务器需要访问您的文件系统或系统环境变量。Docker Compose 可以帮助解决这个问题。由于 `gordon-mcp.yml` 是一个 Compose 文件，您可以使用常规的 Docker Compose 语法添加绑定挂载，这使得您的文件系统资源可用于容器：

```yaml
services:
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

`gordon-mcp.yml` 文件为 Gordon 添加了文件系统访问功能，并且由于所有内容都在容器内运行，Gordon 只能访问您指定的目录。

Gordon 可以处理任意数量的 MCP 服务器。例如，如果您使用 `mcp/fetch` 服务器为 Gordon 提供互联网访问：

```yaml
services:
  fetch:
    image: mcp/fetch
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

您现在可以提出以下问题：

```bash
$ docker ai 你能获取 rumpl.dev 并将摘要写入文件 test.txt 吗？

    • 调用 fetch ✔️
    • 调用 write_file ✔️
  
  rumpl.dev 网站的摘要已成功写入允许目录中的 test.txt 文件。如果您需要进一步帮助，请告诉我！


$ cat test.txt 
rumpl.dev 网站包含网站所有者撰写的各种博客文章和文章。以下是内容的摘要：

1. **Wasmio 2023（2023 年 3 月 25 日）**：WasmIO 2023 巴塞罗那会议回顾。作者分享了作为演讲者的经验，并赞扬组织者成功举办了此次活动。

2. **用 Rust 编写窗口管理器 - 第 2 部分（2023 年 1 月 3 日）**：关于用 Rust 创建窗口管理器系列的第二部分。本期重点介绍增强功能以有效管理窗口。

3. **2022 年回顾（2022 年 12 月 29 日）**：2022 年的个人和专业回顾。作者回顾了这一年的高潮和低谷，强调了专业成就。

4. **用 Rust 编写窗口管理器 - 第 1 部分（2022 年 12 月 28 日）**：关于用 Rust 构建窗口管理器系列的第一部分。作者讨论了设置 Linux 机器以及使用 X11 和 Rust 的挑战。

5. **将 docker/docker 添加到您的依赖项（2020 年 5 月 10 日）**：Go 开发人员如何在项目中使用 Docker 客户端库的指南。该帖子包含一个演示集成的代码片段。

6. **首次（2019 年 10 月 11 日）**：博客的首次发布，其中包含一个简单的 Go 语言“Hello World”程序。
```

## 接下来是什么？

现在您已经了解了如何将 MCP 服务器与 Gordon 结合使用，以下是一些入门方法：

- 实验：尝试将一个或多个经过测试的 MCP 服务器集成到您的 `gordon-mcp.yml` 文件中，并探索它们的功能。
- 探索生态系统：查看 [GitHub 上的参考实现](https://github.com/modelcontextprotocol/servers/) 或浏览 [Docker Hub MCP 命名空间](https://hub.docker.com/u/mcp) 以获取可能适合您需求的更多服务器。
- 构建您自己的：如果现有服务器都不能满足您的需求，或者您对更详细地探索它们的工作原理感到好奇，请考虑开发自定义 MCP 服务器。使用 [MCP 规范](https://www.anthropic.com/news/model-context-protocol) 作为指南。
- 分享您的反馈：如果您发现与 Gordon 配合良好的新服务器或遇到现有服务器的问题，请[分享您的发现以帮助改进生态系统](https://docker.qualtrics.com/jfe/form/SV_9tT3kdgXfAa6cWa)。

借助 MCP 支持，Gordon 提供了强大的可扩展性和灵活性，可以满足您的特定用例，无论您是添加时间感知、文件管理还是互联网访问。