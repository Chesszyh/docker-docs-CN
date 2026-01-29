---
title: MCP 工具包
description: 使用 MCP 工具包设置 MCP 服务器和 MCP 客户端。
keywords: Docker MCP 工具包, MCP 服务器, MCP 客户端, AI 代理
aliases:
  - /desktop/features/gordon/mcp/gordon-mcp-server/
  - /ai/gordon/mcp/gordon-mcp-server/
---

Docker MCP 工具包能够无缝地设置、管理和执行容器化的 MCP 服务器，并将其连接到 AI 代理。它通过提供安全默认值、一键设置以及对不断增长的基于 LLM 的客户端生态系统的支持，消除了工具使用中的障碍。它是从发现 MCP 工具到本地执行的最快路径。

## 主要功能

- 跨 LLM 兼容性：立即可与 Claude Desktop、Cursor、Continue.dev 和 [Gordon](/manuals/ai/gordon/_index.md) 配合使用。
- 集成工具发现：直接在 Docker Desktop 中浏览并启动 Docker MCP 目录中的 MCP 服务器。
- 零手动设置：无需管理依赖项、运行时配置或服务器设置。
- 同时充当 MCP 服务器聚合器和客户端访问已安装 MCP 服务器的网关。

## MCP 工具包的工作原理

MCP 引入了两个核心概念：MCP 客户端和 MCP 服务器。 

- MCP 客户端通常嵌入在基于 LLM 的应用程序中，例如 Claude Desktop App。它们请求资源或操作。
- MCP 服务器由客户端启动以执行请求的任务，并使用任何必要的工具、语言或进程。

Docker 标准化了应用程序（包括 MCP 服务器）的开发、打包和分发。通过将 MCP 服务器打包为容器，Docker 消除了与隔离和环境差异相关的问题。用户可以直接运行容器，而无需管理依赖项或配置运行时。

根据 MCP 服务器的不同，它提供的工具可能与服务器在同一个容器中运行，也可能在专用容器中运行：


{{< tabs group="" >}}
{{< tab name="单容器">}}

![MCP 工具包可视化](/assets/images/mcp_servers.png)

{{< /tab >}}
{{< tab name="独立容器">}}

![MCP 工具包可视化](/assets/images/mcp_servers_2.png)

{{< /tab >}}
{{</tabs >}}

## 安全

Docker MCP 工具包结合了被动和主动措施，以减少攻击面并确保安全的运行时行为。

### 被动安全

- 镜像签名和证明：[目录](catalog.md) 中 `mcp/` 下的所有 MCP 服务器镜像均由 Docker 构建并经过数字签名，以验证其来源和完整性。每个镜像都包含软件物料清单 (SBOM)，以实现完全透明。

### 主动安全

运行时的安全性通过资源和访问限制来强制执行：

- CPU 分配：MCP 工具在它们自己的容器中运行。它们被限制在 1 个 CPU，从而限制了潜在滥用计算资源的影响。

- 内存分配：用于 MCP 工具的容器限制为 2 GB。

- 文件系统访问：默认情况下，MCP 服务器无法访问宿主文件系统。用户显式选择将被授予文件挂载权限的服务器。

- 拦截工具请求：包含机密信息（如密钥）的工具进出请求将被拦截。

## 启用 Docker MCP 工具包

1. 打开 Docker Desktop 设置并选择 **Beta features**（Beta 功能）。
2. 选择 **Enable Docker MCP Toolkit**（启用 Docker MCP 工具包）。
3. 选择 **Apply**（应用）。

>[!NOTE]
>
> 此功能最初作为 MCP Toolkit _扩展程序_。该扩展程序现已弃用，应予以卸载。

## 安装 MCP 服务器

安装 MCP 服务器的步骤：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Catalog**（目录）选项卡。选择服务器时，您可以看到以下信息：

   - 工具名称和描述 
   - 合作伙伴/发布者
   - 服务器提供的可调用工具列表。

2. 找到您选择的 MCP 服务器，然后选择 **Plus**（加号）图标。
3. 可选：某些服务器需要额外配置。要配置它们，请选择 **Config**（配置）选项卡，并遵循 MCP 服务器提供商仓库中提供的说明。

> [!TIP]
> 默认情况下，Gordon [客户端](#安装-mcp-客户端) 已启用，这意味着 Gordon 可以自动与您的 MCP 服务器交互。

要了解更多关于 MCP 服务器目录的信息，请参阅 [目录 (Catalog)](catalog.md)。

### 示例：使用 **GitHub Official** MCP 服务器

假设您想让 Ask Gordon 能够与您的 GitHub 账户交互：

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog**（目录）选项卡，找到 **GitHub Official** 服务器并添加它。
2. 在服务器的 **Config**（配置）选项卡中，[通过 OAuth 连接](#通过-oauth-进行身份验证)。
3. 在 **Clients**（客户端）选项卡中，确保 Gordon 已连接。
4. 从 **Ask Gordon** 菜单中，您现在可以根据 GitHub Official 服务器提供的工具发送与您的 GitHub 账户相关的请求。要进行测试，请询问 Gordon：

   ```text
   我的 GitHub 用户名是什么？
   ```

   请务必通过在 Gordon 的回答中选择 **Always allow**（始终允许）来允许 Gordon 与 GitHub 交互。

## 安装 MCP 客户端

安装 MCP 服务器后，您可以向 MCP 工具包添加客户端。这些客户端可以与已安装的 MCP 服务器交互，从而将 MCP 工具包变成一个网关。

安装客户端的步骤：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Clients**（客户端）选项卡。
2. 找到您选择的客户端，然后选择 **Connect**（连接）。

您的客户端现在可以与 MCP 工具包交互了。

### 示例：使用 Claude Desktop 作为客户端

假设您安装了 Claude Desktop，并且想要使用 GitHub MCP 服务器和 Puppeteer MCP 服务器，您不必在 Claude Desktop 中安装这些服务器。您只需在 MCP 工具包中安装这两个 MCP 服务器，并将 Claude Desktop 添加为客户端即可：

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog**（目录）选项卡，找到 **Puppeteer** 服务器并添加它。
2. 对 **GitHub Official** 服务器重复上述步骤。
3. 从 **Clients**（客户端）选项卡中，选择 **Claude Desktop** 旁边的 **Connect**（连接）。如果 Claude Desktop 正在运行，请将其重启，现在它就可以访问 MCP 工具包中的所有服务器了。
4. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示词进行测试：

   ```text
   对 docs.docker.com 进行截图并反转颜色
   ```
5. 从 **Clients**（客户端）选项卡中，选择 **Claude Desktop** 旁边的 **Connect**（连接）。如果 Claude Desktop 正在运行，请将其重启，现在它就可以访问 MCP 工具包中的所有服务器了。
6. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示词进行测试：

   ```text
   对 docs.docker.com 进行截图并反转颜色
   ```

### 示例：使用 Visual Studio Code 作为客户端

您可以在 VS Code 中与所有已安装的 MCP 服务器交互：

1. 启用 MCP 工具包：


   {{< tabs group="" >}}
   {{< tab name="全局启用">}}

   1. 在您的 VS Code 用户 `settings.json` 中插入以下内容：
   
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

   1. 在终端中，导航至您的项目文件夹。
   1. 运行：
    
      ```bash
      docker mcp client connect vscode
      ```
   
      > [!NOTE]
      > 此命令会在当前目录中创建一个 `.vscode/mcp.json` 文件。我们建议您将其添加到 `.gitignore` 文件中。

  {{< /tab >}}
  {{</tabs >}}

1. 在 Visual Studio Code 中，打开一个新的 Chat 并选择 **Agent**（代理）模式：
   
   ![Copilot 模式切换](./images/copilot-mode.png)

1. 您还可以查看可用的 MCP 工具：

   ![在 VSCode 中显示工具](./images/tools.png)

有关代理模式的更多信息，请参阅 [Visual Studio Code 文档](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)。

## 通过 OAuth 进行身份验证

您可以通过 OAuth 集成将 MCP 工具包连接到您的开发工作流。目前，MCP 工具包仅支持 GitHub OAuth。

1. 在 https://github.com/ 上，确保您已登录。
2. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **OAuth** 选项卡。 
3. 在 GitHub 条目中，选择 **Authorize**（授权）。您的浏览器将打开 GitHub 授权页面。
4. 在 GitHub 授权页面，选择 **Authorize Docker**。授权成功后，您将自动重定向回 Docker Desktop。
5. 安装 **GitHub Official** MCP 服务器，请参阅 [安装 MCP 服务器](#安装-mcp-服务器)。

MCP 工具包现在可以访问您的 GitHub 账户了。要撤销访问权限，请在 **OAuth** 选项卡中选择 **Revoke**（撤销）。
示例请参阅 [使用 GitHub Official MCP 服务器](#示例使用-github-official-mcp-服务器)。
