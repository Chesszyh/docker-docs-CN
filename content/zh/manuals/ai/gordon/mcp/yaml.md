---
title: YAML 配置
description: 学习如何在 Gordon 中使用 MCP 服务器
keywords: ai, mcp, gordon
aliases:
 - /desktop/features/gordon/mcp/yaml/
---

Docker 与 Anthropic 合作构建了 MCP 服务器[参考实现](https://github.com/modelcontextprotocol/servers/)的容器镜像，这些镜像可在 Docker Hub 的 [mcp 命名空间](https://hub.docker.com/u/mcp)下获取。

当你在终端中运行 `docker ai` 命令提问时，Gordon 会在你的工作目录中查找 `gordon-mcp.yml` 文件（如果存在），以获取在该上下文中应使用的 MCP 服务器列表。`gordon-mcp.yml` 文件是一个 Docker Compose 文件，它将 MCP 服务器配置为 Compose 服务以供 Gordon 访问。

以下最小示例展示了如何使用 [mcp-time 服务器](https://hub.docker.com/r/mcp/time)为 Gordon 提供时间功能。有关更多信息，你可以查看[源代码和文档](https://github.com/modelcontextprotocol/servers/tree/main/src/time)。

在你的工作目录中创建 `gordon-mcp.yml` 文件并添加 time 服务器：

```yaml
services:
  time:
    image: mcp/time
```

有了这个文件，你现在可以让 Gordon 告诉你另一个时区的时间：

  ```bash
  $ docker ai 'what time is it now in kiribati?'

      • Calling get_current_time

    The current time in Kiribati (Tarawa) is 9:38 PM on January 7, 2025.

  ```

如你所见，Gordon 找到了 MCP time 服务器并在需要时调用了它的工具。

## 高级用法

一些 MCP 服务器需要访问你的文件系统或系统环境变量。Docker Compose 可以帮助解决这个问题。由于 `gordon-mcp.yml` 是一个 Compose 文件，你可以使用常规的 Docker Compose 语法添加绑定挂载，使你的文件系统资源对容器可用：

```yaml
services:
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

`gordon-mcp.yml` 文件为 Gordon 添加了文件系统访问功能，由于所有内容都在容器内运行，Gordon 只能访问你指定的目录。

Gordon 可以处理任意数量的 MCP 服务器。例如，如果你使用 `mcp/fetch` 服务器让 Gordon 访问互联网：

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

你现在可以询问这样的问题：

```bash
$ docker ai can you fetch rumpl.dev and write the summary to a file test.txt

    • Calling fetch ✔️
    • Calling write_file ✔️

  The summary of the website rumpl.dev has been successfully written to the file test.txt in the allowed directory. Let me know if you need further assistance!


$ cat test.txt
The website rumpl.dev features a variety of blog posts and articles authored by the site owner. Here's a summary of the content:

1. **Wasmio 2023 (March 25, 2023)**: A recap of the WasmIO 2023 conference held in Barcelona. The author shares their experience as a speaker and praises the organizers for a successful event.

2. **Writing a Window Manager in Rust - Part 2 (January 3, 2023)**: The second part of a series on creating a window manager in Rust. This installment focuses on enhancing the functionality to manage windows effectively.

3. **2022 in Review (December 29, 2022)**: A personal and professional recap of the year 2022. The author reflects on the highs and lows of the year, emphasizing professional achievements.

4. **Writing a Window Manager in Rust - Part 1 (December 28, 2022)**: The first part of the series on building a window manager in Rust. The author discusses setting up a Linux machine and the challenges of working with X11 and Rust.

5. **Add docker/docker to your dependencies (May 10, 2020)**: A guide for Go developers on how to use the Docker client library in their projects. The post includes a code snippet demonstrating the integration.

6. **First (October 11, 2019)**: The inaugural post on the blog, featuring a simple "Hello World" program in Go.
```

## 下一步

现在你已经学会了如何在 Gordon 中使用 MCP 服务器，以下是一些入门方式：

- 实验：尝试将一个或多个经过测试的 MCP 服务器集成到你的 `gordon-mcp.yml` 文件中，探索它们的功能。
- 探索生态系统：查看 [GitHub 上的参考实现](https://github.com/modelcontextprotocol/servers/)或浏览 [Docker Hub MCP 命名空间](https://hub.docker.com/u/mcp)以获取可能满足你需求的其他服务器。
- 构建你自己的：如果现有服务器都不能满足你的需求，或者你想更详细地了解它们的工作原理，可以考虑开发自定义 MCP 服务器。使用 [MCP 规范](https://www.anthropic.com/news/model-context-protocol)作为指南。
- 分享你的反馈：如果你发现与 Gordon 配合良好的新服务器或遇到现有服务器的问题，[分享你的发现以帮助改进生态系统](https://docker.qualtrics.com/jfe/form/SV_9tT3kdgXfAa6cWa)。

通过 MCP 支持，Gordon 提供了强大的可扩展性和灵活性来满足你的特定用例，无论你是添加时间感知、文件管理还是互联网访问。
