---
title: Ask Gordon
description: 学习如何使用 Docker 的 AI 驱动助手来简化你的工作流程。
weight: 10
params:
  sidebar:
    badge:
      color: blue
      text: Beta
    group: AI
aliases:
 - /desktop/features/gordon/
---

{{< summary-bar feature_name="Ask Gordon" >}}

Ask Gordon 是你的个人 AI 助手，嵌入在 Docker Desktop 和 Docker CLI 中。它旨在简化你的工作流程，帮助你充分利用 Docker 生态系统。

## 主要功能

Ask Gordon 在 Docker 工具中提供 AI 驱动的帮助。它可以：

- 改进 Dockerfile
- 运行和排查容器问题
- 与你的镜像和代码交互
- 发现漏洞或配置问题

它理解你的本地环境，包括源代码、Dockerfile 和镜像，以提供个性化和可操作的指导。

Ask Gordon 会记住对话内容，使你可以更轻松地切换话题。

Ask Gordon 默认未启用，且尚未达到生产就绪状态。你可能还会看到 "Docker AI" 这个术语，它是对该技术的更广泛称呼。

> [!NOTE]
>
> Ask Gordon 由大型语言模型（LLM）驱动。与所有基于 LLM 的工具一样，其响应有时可能不准确。请始终验证所提供的信息。

### Gordon 访问哪些数据？

当你使用 Ask Gordon 时，它访问的数据取决于你查询的上下文：

- 本地文件：如果你使用 `docker ai` 命令，Ask Gordon 可以访问执行命令所在当前工作目录中的文件和目录。在 Docker Desktop 中，如果你在 **Ask Gordon** 视图中询问特定文件或目录的问题，系统会提示你选择相关上下文。
- 本地镜像：Gordon 与 Docker Desktop 集成，可以查看本地镜像存储中的所有镜像。这包括你构建的镜像或从注册表拉取的镜像。

为了提供准确的响应，Ask Gordon 可能会将相关文件、目录或镜像元数据与你的查询一起发送到 Gordon 后端。此数据传输通过网络进行，但永远不会被持久存储或与第三方共享。它仅用于处理你的请求并形成响应。有关 Docker AI 的隐私条款和条件的更多信息，请查阅 [Gordon 补充条款](https://www.docker.com/legal/docker-ai-supplemental-terms/)。

所有传输的数据在传输过程中都经过加密。

### 你的数据如何被收集和使用

Docker 从你与 Ask Gordon 的交互中收集匿名数据以增强服务。这包括以下内容：

- 你的查询：你向 Gordon 提出的问题。
- 响应：Gordon 提供的回答。
- 反馈：点赞和点踩评级。

为确保隐私和安全：

- 数据是匿名的，无法追溯到你或你的账户。
- Docker 不会使用这些数据来训练 AI 模型或与第三方共享。

通过使用 Ask Gordon，你可以帮助提高 Docker AI 的可靠性和准确性，使其对所有用户更加有效。

如果你对数据收集或使用有疑虑，可以随时[禁用](#禁用-ask-gordon)该功能。

## 启用 Ask Gordon

1. 登录到你的 Docker 账户。
2. 导航到设置中的 **Beta features** 选项卡。
3. 勾选 **Enable Docker AI** 复选框。

   系统将显示 Docker AI 服务条款协议。你必须同意条款才能启用该功能。查阅条款并选择 **Accept and enable** 继续。

4. 选择 **Apply**。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于 **Features in development** 页面的 **Experimental features** 选项卡下。

## 使用 Ask Gordon

Docker AI 功能的主要界面是 Docker Desktop 中的 **Ask Gordon** 视图，或者如果你更喜欢使用 CLI：`docker ai` CLI 命令。

启用 Docker AI 功能后，你还会在 Docker Desktop 用户界面的其他各个位置看到 **Ask Gordon** 的引用。当你在用户界面中遇到带有 **Sparkles**（✨）图标的按钮时，可以使用该按钮获取 Ask Gordon 的上下文支持。

## 示例工作流程

Ask Gordon 是一个通用 AI 助手，旨在帮助你完成所有与 Docker 相关的任务和工作流程。如果你需要一些灵感，这里有一些可以尝试的事情：

- [排查崩溃的容器](#排查崩溃的容器)
- [获取运行容器的帮助](#获取运行容器的帮助)
- [改进 Dockerfile](#改进-dockerfile)

想要更多示例，可以直接问 Gordon。例如：

```console
$ docker ai "What can you do?"
```

### 排查崩溃的容器

如果你尝试使用无效配置或命令启动容器，可以使用 Ask Gordon 来排查错误。例如，尝试在不指定数据库密码的情况下启动 Postgres 容器：

```console
$ docker run postgres
Error: Database is uninitialized and superuser password is not specified.
       You must specify POSTGRES_PASSWORD to a non-empty value for the
       superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".

       You may also use "POSTGRES_HOST_AUTH_METHOD=trust" to allow all
       connections without a password. This is *not* recommended.

       See PostgreSQL documentation about "trust":
       https://www.postgresql.org/docs/current/auth-trust.html
```

在 Docker Desktop 的 **Containers** 视图中，选择容器名称旁边的 ✨ 图标，或检查容器并打开 **Ask Gordon** 选项卡。

### 获取运行容器的帮助

如果你想运行特定镜像但不确定如何操作，Gordon 可能能够帮助你进行设置：

1. 从 Docker Hub 拉取镜像（例如 `postgres`）。
2. 在 Docker Desktop 中打开 **Images** 视图并选择该镜像。
3. 选择 **Run** 按钮。

在 **Run a new container** 对话框中，你应该会看到关于 **Ask Gordon** 的消息。

![Docker Desktop 中的 Ask Gordon 提示](../../images/gordon-run-ctr.png)

提示中的链接文本是一个建议的提示词，用于开始与 Ask Gordon 的对话。

### 改进 Dockerfile

Gordon 可以分析你的 Dockerfile 并提出改进建议。要让 Gordon 使用 `docker ai` 命令评估你的 Dockerfile：

1. 导航到你的项目目录：

   ```console
   $ cd path/to/my/project
   ```

2. 使用 `docker ai` 命令来评估你的 Dockerfile：

   ```console
   $ docker ai rate my Dockerfile
   ```

Gordon 将分析你的 Dockerfile 并识别多个维度的改进机会：

- 构建缓存优化
- 安全性
- 镜像大小效率
- 最佳实践合规性
- 可维护性
- 可重现性
- 可移植性
- 资源效率

## 禁用 Ask Gordon

### 对于个人用户

如果你已启用 Ask Gordon 并想要再次禁用它：

1. 在 Docker Desktop 中打开 **Settings** 视图。
2. 导航到 **Beta features**。
3. 取消勾选 **Enable Docker AI** 复选框。
4. 选择 **Apply**。

### 对于组织

如果你想为整个 Docker 组织禁用 Ask Gordon，使用[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)，将以下属性添加到你的 `admin-settings.json` 文件：

```json
{
  "enableDockerAI": {
    "value": false,
    "locked": true
  }
}
```

或者，你可以通过将 `allowBetaFeatures` 设置为 false 来禁用所有 Beta 功能：

```json
{
  "allowBetaFeatures": {
    "value": false,
    "locked": true
  }
}
```

## 反馈

<!-- vale Docker.We = NO -->

我们重视你对 Ask Gordon 的反馈，并鼓励你分享你的体验。你的反馈帮助我们为所有用户改进和完善 Ask Gordon。如果你遇到问题、有建议或只是想分享你喜欢的内容，以下是联系方式：

- 点赞和点踩按钮

  使用响应中的点赞或点踩按钮对 Ask Gordon 的响应进行评级。

- 反馈调查

  你可以通过 Docker Desktop 中 **Ask Gordon** 视图的 _Give feedback_ 链接访问 Ask Gordon 调查，或从 CLI 运行 `docker ai feedback` 命令。


