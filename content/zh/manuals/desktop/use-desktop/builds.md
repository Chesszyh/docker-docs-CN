---
title: 探索 Docker Desktop 中的构建 (Builds) 视图
linkTitle: 构建 (Builds)
description: 了解如何使用 Docker Desktop 中的构建视图
keywords: Docker Dashboard, 管理, gui, 控制面板, 构建器, builders, 构建, builds
weight: 40
---

**构建 (Builds)** 视图提供了一个交互式界面，用于直接在 Docker Desktop 中检查构建历史、监控活动构建以及管理构建器。

默认情况下，**Build history** 选项卡显示已完成的构建列表，按日期排序（最新的排在最前面）。切换到 **Active builds** 选项卡可以查看正在进行的构建。

如果您通过 [Docker Build Cloud](../../build-cloud/_index.md) 连接到了云构建器，构建视图还会列出连接到同一云构建器的其他团队成员正在进行或已完成的云构建。

> [!NOTE]
>
> 当使用 `docker build` 命令构建 Windows 容器镜像时，使用的是旧版构建器，它不会填充 **Builds** 视图。要切换到使用 BuildKit，您可以：
> - 在构建命令中设置 `DOCKER_BUILDKIT=1`，例如 `DOCKER_BUILDKIT=1 docker build .`
> - 或者使用 `docker buildx build` 命令

## 显示构建列表

从 Docker 控制面板打开 **Builds** 视图，可以访问：

- **Build history**：已完成的构建，可访问日志、依赖项、追踪信息等。
- **Active builds**：当前正在进行的构建。

仅列出活跃且正在运行的构建器的构建。已移除或已停止的构建器的构建不会显示。

### 构建器设置 (Builder settings)

右上角显示了当前选中的构建器名称，**Builder settings** 按钮允许您在 Docker Desktop 设置中 [管理构建器](#管理构建器)。

### 导入构建 (Import builds)

{{< summary-bar feature_name="导入构建" >}}

**Import builds** 按钮允许您导入他人执行的构建记录，或 CI 环境中的构建记录。导入构建记录后，您可以直接在 Docker Desktop 中完全访问该构建的日志、追踪信息和其他数据。

`docker/build-push-action` 和 `docker/bake-action` GitHub Actions 的 [构建摘要 (build summary)](/manuals/build/ci/github-actions/build-summary.md) 包含一个下载构建记录的链接，以便使用 Docker Desktop 检查 CI 任务。

## 检查构建 (Inspect builds)

要检查某个构建，请在列表中选择您想要查看的构建。检查视图包含多个选项卡。

**Info** 选项卡显示有关构建的详细信息。

如果您正在检查多平台构建，该选项卡右上角的下拉菜单允许您将信息过滤到特定平台：

**Source details** 部分显示有关 [前端 (frontend)](/manuals/build/buildkit/frontend.md) 的信息，如果可用，还会显示用于构建的源代码存储库。

### 构建用时 (Build timing)

Info 选项卡的 **Build timing** 部分包含从多个角度分解构建执行情况的图表。

- **Real time**：完成构建所需的实际墙钟时间。
- **Accumulated time**：所有步骤的总 CPU 时间。
- **Cache usage**：构建操作被缓存的程度。
- **Parallel execution**：构建执行时间中有多少是用于并行运行步骤的。

图表颜色和图例说明了不同的构建操作。构建操作定义如下：

| 构建操作 | 说明 |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 本地文件传输 (Local file transfers) | 从客户端向构建器传输本地文件所花费的时间。 |
| 文件操作 (File operations) | 涉及在构建中创建和复制文件的任何操作。例如，Dockerfile 前端中的 `COPY`、`WORKDIR`、`ADD` 指令都会产生文件操作。 |
| 镜像拉取 (Image pulls) | 拉取镜像所花费的时间。 |
| 执行 (Executions) | 容器执行，例如 Dockerfile 前端中定义为 `RUN` 指令的命令。 |
| HTTP | 使用 `ADD` 下载的远程构件。 |
| Git | 与 **HTTP** 相同，但针对 Git URL。 |
| 结果导出 (Result exports) | 导出构建结果所花费的时间。 |
| SBOM | 生成 [SBOM 证明 (SBOM attestation)](/manuals/build/metadata/attestations/sbom.md) 所花费的时间。 |
| 空闲 (Idle) | 构建工作线程的空闲时间，这可能在您配置了 [最大并行限制 (max parallelism limit)](/manuals/build/buildkit/configure.md#max-parallelism) 时发生。 |

### 构建依赖 (Build dependencies)

**Dependencies** 部分显示了构建期间使用的镜像和远程资源。此处列出的资源包括：

- 构建期间使用的容器镜像
- 通过 `ADD` Dockerfile 指令包含的 Git 存储库
- 通过 `ADD` Dockerfile 指令包含的远程 HTTPS 资源

### 参数、机密和其他参数

Info 选项卡的 **Configuration** 部分显示传递给构建的参数：

- 构建参数 (Build arguments)，包括解析后的值
- 机密 (Secrets)，包括其 ID（但不包括其值）
- SSH 套接字
- 标签 (Labels)
- [额外上下文 (Additional contexts)](/reference/cli/docker/buildx/build/#build-context)

### 输出与构件 (Outputs and artifacts)

**Build results** 部分显示生成的构建构件摘要，包括镜像清单详情、证明 (attestations) 和构建追踪信息 (build traces)。

证明是附加到容器镜像的元数据记录。该元数据描述了镜像的一些信息，例如它是如何构建的或包含哪些软件包。有关证明的更多信息，请参阅 [构建证明](/manuals/build/metadata/attestations/_index.md)。

构建追踪信息捕获了有关 Buildx 和 BuildKit 中构建执行步骤的信息。追踪信息提供两种格式：OTLP 和 Jaeger。您可以从 Docker Desktop 下载构建追踪信息，方法是打开操作菜单并选择您想要下载的格式。

#### 使用 Jaeger 检查构建追踪信息

使用 Jaeger 客户端，您可以从 Docker Desktop 导入并检查构建追踪信息。以下步骤向您展示了如何从 Docker Desktop 导出追踪信息并在 [Jaeger](https://www.jaegertracing.io/) 中查看：

1. 启动 Jaeger UI：

   ```console
   $ docker run -d --name jaeger -p "16686:16686" jaegertracing/all-in-one
   ```

2. 打开 Docker Desktop 中的构建视图，并选择一个已完成的构建。

3. 导航到 **Build results** 部分，打开操作菜单并选择 **Download as Jaeger format**。

   <video controls>
     <source src="/assets/video/build-jaeger-export.mp4" type="video/mp4" />
   </video>

4. 在浏览器中访问 <http://localhost:16686> 以打开 Jaeger UI。

5. 选择 **Upload** 选项卡并打开您刚刚导出的 Jaeger 构建追踪文件。

现在您可以使用 Jaeger UI 分析构建追踪信息了：

![Jaeger UI 截图](../images/build-ui-jaeger-screenshot.png "Jaeger UI 中构建追踪信息的截图")

### Dockerfile 源码与错误

在检查成功完成的构建或正在进行的活动构建时，**Source** 选项卡会显示用于创建构建的 [前端](/manuals/build/buildkit/frontend.md)。

如果构建失败，则会显示 **Error** 选项卡而不是 **Source** 选项卡。错误消息会内联在 Dockerfile 源码中，指示失败发生的位置及原因。

### 构建日志 (Build logs)

**Logs** 选项卡显示构建日志。对于活动构建，日志会实时更新。

您可以在构建日志的 **列表视图 (List view)** 和 **纯文本视图 (Plain-text view)** 之间切换。

- **列表视图**以可折叠格式呈现所有构建步骤，并带有一个时间线，用于沿时间轴导航日志。

- **纯文本视图**以纯文本形式显示日志。

**Copy** 按钮允许您将日志的纯文本版本复制到剪贴板。

### 构建历史 (Build history)

**History** 选项卡显示有关已完成构建的统计数据。

时间序列图表展示了相关构建的持续时间、构建步骤和缓存使用情况的趋势，帮助您识别构建操作随时间变化的模式。例如，构建持续时间的大幅飙升或大量缓存未命中可能意味着 Dockerfile 存在优化空间。

您可以通过在图表中选择某个相关构建，或使用图表下方的 **Past builds** 列表来导航并检查该构建。

## 管理构建器 (Manage builders)

**Settings（设置）** 中的 **Builder** 选项卡允许您：

- 检查活动构建器的状态和配置
- 启动和停止构建器
- 删除构建历史
- 添加或移除构建器（或者在云构建器的情况下，进行连接和断开连接）

有关管理构建器的更多信息，请参阅 [修改设置](/manuals/desktop/settings-and-maintenance/settings.md#builders)。
