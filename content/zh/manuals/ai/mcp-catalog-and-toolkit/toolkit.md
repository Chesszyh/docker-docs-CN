---
title: MCP Toolkit
description: 使用 MCP Toolkit 设置 MCP 服务器和 MCP 客户端。
keywords: Docker MCP Toolkit, MCP server, MCP client, AI agents
aliases:
  - /desktop/features/gordon/mcp/gordon-mcp-server/
  - /ai/gordon/mcp/gordon-mcp-server/
---

Docker MCP Toolkit 能够无缝设置、管理和执行容器化的 MCP 服务器及其与 AI 代理的连接。它通过提供安全的默认设置、一键设置以及对不断增长的基于 LLM 的客户端生态系统的支持，消除了工具使用的阻力。它是从 MCP 工具发现到本地执行的最快路径。

## 主要功能

- 跨 LLM 兼容性：即时支持 Claude Desktop、Cursor、Continue.dev 和 [Gordon](/manuals/ai/gordon/_index.md)。
- 集成工具发现：直接在 Docker Desktop 中浏览和启动 Docker MCP Catalog 中的 MCP 服务器。
- 零手动设置：无需依赖管理、运行时配置或服务器设置。
- 既作为 MCP 服务器聚合器，也作为客户端访问已安装 MCP 服务器的网关。

## MCP toolkit 的工作原理

MCP 引入了两个核心概念：MCP 客户端和 MCP 服务器。

- MCP 客户端通常嵌入在基于 LLM 的应用程序中，例如 Claude Desktop 应用。它们请求资源或操作。
- MCP 服务器由客户端启动以执行请求的任务，使用任何必要的工具、语言或进程。

Docker 标准化了应用程序的开发、打包和分发，包括 MCP 服务器。通过将 MCP 服务器打包为容器，Docker 消除了与隔离和环境差异相关的问题。用户可以直接运行容器，无需管理依赖项或配置运行时。

根据 MCP 服务器的不同，它提供的工具可能在与服务器相同的容器内运行，也可能在专用容器中运行：


{{< tabs group="" >}}
{{< tab name="单个容器">}}

![MCP toolkit 可视化](/assets/images/mcp_servers.png)

{{< /tab >}}
{{< tab name="独立容器">}}

![MCP toolkit 可视化](/assets/images/mcp_servers_2.png)

{{< /tab >}}
{{</tabs >}}

## 安全性

Docker MCP Toolkit 结合被动和主动措施来减少攻击面并确保安全的运行时行为。

### 被动安全

- 镜像签名和证明：[catalog](catalog.md) 中 `mcp/` 下的所有 MCP 服务器镜像都由 Docker 构建并经过数字签名，以验证其来源和完整性。每个镜像都包含软件物料清单（SBOM）以实现完全透明。

### 主动安全

通过资源和访问限制在运行时强制执行安全性：

- CPU 分配：MCP 工具在自己的容器中运行。它们被限制为 1 个 CPU，限制了计算资源潜在滥用的影响。

- 内存分配：MCP 工具的容器限制为 2 GB。

- 文件系统访问：默认情况下，MCP 服务器无权访问主机文件系统。用户明确选择将被授予文件挂载的服务器。

- 工具请求拦截：包含敏感信息（如密钥）的工具请求和响应会被阻止。

## 启用 Docker MCP Toolkit

1. 打开 Docker Desktop 设置并选择 **Beta features**。
2. 选择 **Enable Docker MCP Toolkit**。
3. 选择 **Apply**。

>[!NOTE]
>
> 此功能最初是作为 MCP Toolkit _扩展_提供的。此扩展现已弃用，应予以卸载。

## 安装 MCP 服务器

要安装 MCP 服务器：

1. 在 Docker Desktop 中，选择 **MCP Toolkit** 并选择 **Catalog** 选项卡。
   当你选择服务器时，可以看到以下信息：

   - 工具名称和描述
   - 合作伙伴/发布者
   - 服务器提供的可调用工具列表。

2. 找到你选择的 MCP 服务器并选择 **Plus** 图标。
3. 可选：某些服务器需要额外配置。要配置它们，请选择 **Config** 选项卡并按照 MCP 服务器提供商仓库中提供的说明操作。

> [!TIP]
> 默认情况下，Gordon [客户端](#安装-mcp-客户端)已启用，这意味着 Gordon 可以自动与你的 MCP 服务器交互。

要了解有关 MCP 服务器目录的更多信息，请参阅 [Catalog](catalog.md)。

### 示例：使用 **GitHub Official** MCP 服务器

假设你想让 Ask Gordon 与你的 GitHub 账户交互：

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog** 选项卡，找到 **GitHub Official** 服务器并添加它。
2. 在服务器的 **Config** 选项卡中，[通过 OAuth 连接](#通过-oauth-认证)。
3. 在 **Clients** 选项卡中，确保 Gordon 已连接。
4. 从 **Ask Gordon** 菜单中，你现在可以根据 GitHub Official 服务器提供的工具发送与 GitHub 账户相关的请求。要测试它，问 Gordon：

   ```text
   What's my GitHub handle?
   ```

   确保在 Gordon 的回答中选择 **Always allow** 以允许 Gordon 与 GitHub 交互。

## 安装 MCP 客户端

当你安装了 MCP 服务器后，可以向 MCP Toolkit 添加客户端。这些客户端可以与已安装的 MCP 服务器交互，使 MCP Toolkit 成为一个网关。

要安装客户端：

1. 在 Docker Desktop 中，选择 **MCP Toolkit** 并选择 **Clients** 选项卡。
2. 找到你选择的客户端并选择 **Connect**。

你的客户端现在可以与 MCP Toolkit 交互了。

### 示例：使用 Claude Desktop 作为客户端

假设你已安装 Claude Desktop，并且想要使用 GitHub MCP 服务器和 Puppeteer MCP 服务器，你不必在 Claude Desktop 中安装这些服务器。你可以简单地在 MCP Toolkit 中安装这 2 个 MCP 服务器，并将 Claude Desktop 添加为客户端：

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog** 选项卡，找到 **Puppeteer** 服务器并添加它。
2. 对 **GitHub Official** 服务器重复此操作。
3. 从 **Clients** 选项卡中，选择 **Claude Desktop** 旁边的 **Connect**。如果 Claude Desktop 正在运行，请重启它，它现在可以访问 MCP Toolkit 中的所有服务器。
4. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示进行测试：

   ```text
   Take a screenshot of docs.docker.com and then invert the colors
   ```
5. 从 **Clients** 选项卡中，选择 **Claude Desktop** 旁边的 **Connect**。如果 Claude Desktop 正在运行，请重启它，它现在可以访问 MCP Toolkit 中的所有服务器。
6. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示进行测试：

   ```text
   Take a screenshot of docs.docker.com and then invert the colors
   ```

### 示例：使用 Visual Studio Code 作为客户端

你可以在 VS Code 中与所有已安装的 MCP 服务器交互：

1. 要启用 MCP Toolkit：


   {{< tabs group="" >}}
   {{< tab name="全局启用">}}

   1. 在 VS Code 的用户 `settings.json` 中插入以下内容：

      ```json
      "mcp": {
       "servers": {
         "MCP_DOCKER": {
           "command": "docker",
           "args": [
             "mcp",
             "gateway",
             "run"
           ],
           "type": "stdio"
         }
       }
      }
      ```

   {{< /tab >}}
   {{< tab name="为特定项目启用">}}

   1. 在终端中，导航到项目文件夹。
   1. 运行：

      ```bash
      docker mcp client connect vscode
      ```

      > [!NOTE]
      > 此命令在当前目录中创建一个 `.vscode/mcp.json` 文件。我们建议将其添加到 `.gitignore` 文件中。

  {{< /tab >}}
  {{</tabs >}}

1. 在 Visual Studio Code 中，打开一个新的聊天并选择 **Agent** 模式：

   ![Copilot 模式切换](./images/copilot-mode.png)

1. 你还可以查看可用的 MCP 工具：

   ![在 VSCode 中显示工具](./images/tools.png)

有关 Agent 模式的更多信息，请参阅 [Visual Studio Code 文档](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)。

## 通过 OAuth 认证

你可以通过 OAuth 集成将 MCP Toolkit 连接到你的开发工作流程。目前，MCP Toolkit 仅支持 GitHub OAuth。

1. 在 https://github.com/ 上，确保你已登录。
1. 在 Docker Desktop 中，选择 **MCP Toolkit** 并选择 **OAuth** 选项卡。
1. 在 GitHub 条目中，选择 **Authorize**。你的浏览器会打开 GitHub 授权页面。
1. 在 GitHub 授权页面中，选择 **Authorize Docker**。授权成功后，你会自动重定向到 Docker Desktop。
1. 安装 **GitHub Official** MCP 服务器，请参阅[安装 MCP 服务器](#安装-mcp-服务器)。

MCP Toolkit 现在可以访问你的 GitHub 账户了。要撤销访问权限，请在 **OAuth** 选项卡中选择 **Revoke**。
请参阅[使用 **GitHub Official** MCP 服务器](#示例使用-github-official-mcp-服务器)中的示例。
