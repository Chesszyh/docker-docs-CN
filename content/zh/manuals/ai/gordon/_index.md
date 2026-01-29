---
title: Ask Gordon
description: 了解如何使用 Docker 的 AI 驱动助手简化您的工作流程。
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

Ask Gordon 是嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，并帮助您充分利用 Docker 生态系统。

## 主要功能

Ask Gordon 在 Docker 工具中提供 AI 驱动的协助。它可以：

- 改进 Dockerfile
- 运行容器并排除故障
- 与您的镜像和代码交互
- 发现漏洞或配置问题

它了解您的本地环境，包括源代码、Dockerfile 和镜像，以提供个性化且可操作的指导。

Ask Gordon 能够记住对话内容，让您可以更轻松地切换话题。

Ask Gordon 默认未启用，且尚未达到生产级标准。您可能还会遇到“Docker AI”一词，作为对该技术的更广泛引用。

> [!NOTE] 
>
> Ask Gordon 由大语言模型 (LLM) 驱动。与所有基于 LLM 的工具一样，它的回复有时可能不准确。请务必核实所提供的信息。

### Gordon 访问哪些数据？

当您使用 Ask Gordon 时，它访问的数据取决于您查询的上下文：

- 本地文件：如果您使用 `docker ai` 命令，Ask Gordon 可以访问执行该命令的当前工作目录中的文件和目录。在 Docker Desktop 中，如果您在 **Ask Gordon** 视图中询问有关特定文件或目录的问题，系统将提示您选择相关的上下文。
- 本地镜像：Gordon 与 Docker Desktop 集成，可以查看您本地镜像库中的所有镜像。这包括您构建的镜像或从镜像库拉取的镜像。

为了提供准确的回复，Ask Gordon 可能会将相关文件、目录或镜像元数据连同您的查询一起发送到 Gordon 后端。这种数据传输通过网络发生，但绝不会持久存储或与第三方共享。它专门用于处理您的请求并制定回复。有关 Docker AI 隐私条款和条件的更多信息，请查阅 [Gordon 补充条款](https://www.docker.com/legal/docker-ai-supplemental-terms/)。

所有传输的数据在传输过程中都是加密的。

### 您的数据如何被收集和使用

Docker 从您与 Ask Gordon 的互动中收集匿名数据以增强服务。这包括以下内容：

- 您的查询：您向 Gordon 提出的问题。
- 回复：Gordon 提供的回答。
- 反馈：点赞和点踩。

为确保隐私和安全：

- 数据是匿名的，无法追溯到您或您的账户。
- Docker 不会使用这些数据来训练 AI 模型或将其与第三方共享。

通过使用 Ask Gordon，您可以帮助提高 Docker AI 的可靠性和准确性，使其对所有用户都更加有效。

如果您对数据收集或使用有疑虑，可以随时 [禁用](#禁用-ask-gordon) 该功能。

## 启用 Ask Gordon

1. 登录您的 Docker 账户。
2. 导航至设置中的 **Beta features**（Beta 功能）选项卡。
3. 勾选 **Enable Docker AI**（启用 Docker AI）复选框。

   随后将显示 Docker AI 服务条款协议。您必须同意条款才能启用该功能。查看条款并选择 **Accept and enable**（接受并启用）以继续。

4. 选择 **Apply**（应用）。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于 **Features in development**（开发中的功能）页面上的 **Experimental features**（实验性功能）选项卡下。

## 使用 Ask Gordon

Docker AI 功能的主要界面是通过 Docker Desktop 中的 **Ask Gordon** 视图，或者如果您更喜欢使用 CLI：`docker ai` CLI 命令。

启用 Docker AI 功能后，您还可以在 Docker Desktop 用户界面的其他各种地方找到 **Ask Gordon** 的引用。每当您在用户界面中遇到带有 **闪烁** (✨) 图标的按钮时，都可以使用该按钮从 Ask Gordon 获取上下文支持。

## 示例工作流

Ask Gordon 是一个通用 AI 助手，旨在帮助您处理所有与 Docker 相关的任务和工作流。如果您需要一些灵感，可以尝试以下几种方式：

- [排除崩溃容器的故障](#排除崩溃容器的故障)
- [获取运行容器的帮助](#获取运行容器的帮助)
- [改进 Dockerfile](#改进-dockerfile)

有关更多示例，请尝试直接询问 Gordon。例如：

```console
$ docker ai "What can you do?"
```

### 排除崩溃容器的故障

如果您尝试使用无效的配置或命令启动容器，可以使用 Ask Gordon 来排除错误故障。例如，尝试在不指定数据库密码的情况下启动 Postgres 容器：

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

在 Docker Desktop 的 **Containers**（容器）视图中，选择容器名称旁边的 ✨ 图标，或检查容器并打开 **Ask Gordon** 选项卡。

### 获取运行容器的帮助

如果您想运行特定的镜像但不确定如何操作，Gordon 或许能帮您完成设置：

1. 从 Docker Hub 拉取镜像（例如 `postgres`）。
2. 在 Docker Desktop 中打开 **Images**（镜像）视图并选择该镜像。
3. 选择 **Run**（运行）按钮。

在 **Run a new container**（运行新容器）对话框中，您应该会看到一条关于 **Ask Gordon** 的消息。

![Ask Gordon hint in Docker Desktop](../../images/gordon-run-ctr.png)

提示中的链接文本是开始与 Ask Gordon 对话的建议提示语。

### 改进 Dockerfile

Gordon 可以分析您的 Dockerfile 并建议改进。要让 Gordon 使用 `docker ai` 命令评估您的 Dockerfile：

1. 导航至您的项目目录：

   ```console
   $ cd path/to/my/project
   ```

2. 使用 `docker ai` 命令为您的 Dockerfile 评分：

   ```console
   $ docker ai rate my Dockerfile
   ```

Gordon 将分析您的 Dockerfile，并在以下几个维度识别改进机会：

- 构建缓存优化
- 安全
- 镜像大小效率
- 最佳实践合规性
- 可维护性
- 可复现性
- 移植性
- 资源效率

## 禁用 Ask Gordon

### 针对个人用户

如果您启用了 Ask Gordon 并且想要再次禁用它：

1. 在 Docker Desktop 中打开 **Settings**（设置）视图。
2. 导航至 **Beta features**（Beta 功能）。
3. 取消勾选 **Enable Docker AI**（启用 Docker AI）复选框。
4. 选择 **Apply**（应用）。

### 针对组织

如果您想使用 [设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md) 为整个 Docker 组织禁用 Ask Gordon，请将以下属性添加到您的 `admin-settings.json` 文件中：

```json
{
  "enableDockerAI": {
    "value": false,
    "locked": true
  }
}
```

或者，您可以通过将 `allowBetaFeatures` 设置为 false 来禁用所有 Beta 功能：

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

我们非常重视您对 Ask Gordon 的意见，并鼓励您分享您的体验。您的反馈有助于我们为所有用户改进和完善 Ask Gordon。如果您遇到问题、有建议，或者只是想分享您喜欢的地方，可以通过以下方式与我们联系：

- 点赞和点踩按钮

  使用回复中的点赞或点踩按钮对 Ask Gordon 的回答进行评分。

- 反馈调查

  您可以通过点击 Docker Desktop 中 **Ask Gordon** 视图里的 _Give feedback_（提供反馈）链接，或者在 CLI 中运行 `docker ai feedback` 命令来访问 Ask Gordon 调查。
