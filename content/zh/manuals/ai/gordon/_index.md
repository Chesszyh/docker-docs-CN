---
title: 询问 Gordon
description: 了解如何使用 Docker 的 AI 助手简化您的工作流程。
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

{{< summary-bar feature_name="询问 Gordon" >}}

询问 Gordon 是您嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，并帮助您充分利用 Docker 生态系统。

## 主要功能

询问 Gordon 在 Docker 工具中提供 AI 驱动的帮助。它可以：

- 改进 Dockerfile
- 运行和排除容器故障
- 与您的镜像和代码交互
- 查找漏洞或配置问题

它了解您的本地环境，包括源代码、Dockerfile 和镜像，以提供个性化和可操作的指导。

询问 Gordon 会记住对话，让您更轻松地切换话题。

询问 Gordon 默认不启用，并且尚未投入生产。您也可能会遇到“Docker AI”一词，作为对这项技术的更广泛引用。

> [!NOTE] 
>
> 询问 Gordon 由大型语言模型 (LLM) 提供支持。与所有基于 LLM 的工具一样，其响应有时可能不准确。请务必验证所提供的信息。

### Gordon 访问哪些数据？

当您使用询问 Gordon 时，它访问的数据取决于您的查询上下文：

- 本地文件：如果您使用 `docker ai` 命令，询问 Gordon 可以访问执行命令的当前工作目录中的文件和目录。在 Docker Desktop 中，如果您在**询问 Gordon** 视图中询问特定文件或目录，系统会提示您选择相关上下文。
- 本地镜像：Gordon 与 Docker Desktop 集成，可以查看本地镜像存储中的所有镜像。这包括您构建或从注册表拉取的镜像。

为了提供准确的响应，询问 Gordon 可能会将相关文件、目录或镜像元数据与您的查询一起发送到 Gordon 后端。此数据传输通过网络进行，但绝不会永久存储或与第三方共享。它仅用于处理您的请求并形成响应。有关 Docker AI 隐私条款和条件的更多信息，请查看 [Gordon 的补充条款](https://www.docker.com/legal/docker-ai-supplemental-terms/)。

所有传输的数据在传输过程中都经过加密。

### 您的数据如何收集和使用

Docker 从您与询问 Gordon 的交互中收集匿名数据，以增强服务。这包括以下内容：

- 您的查询：您向 Gordon 提出的问题。
- 响应：Gordon 提供的答案。
- 反馈：点赞和点踩评级。

为确保隐私和安全：

- 数据是匿名的，无法追溯到您或您的帐户。
- Docker 不会使用此数据来训练 AI 模型或与第三方共享。

通过使用询问 Gordon，您可以帮助提高 Docker AI 的可靠性和准确性，使其对所有用户更有效。

如果您对数据收集或使用有疑虑，您可以随时[禁用](#disable-ask-gordon)该功能。

## 启用询问 Gordon

1. 登录您的 Docker 帐户。
2. 导航到设置中的**Beta 功能**选项卡。
3. 勾选**启用 Docker AI** 复选框。

   将显示 Docker AI 服务条款协议。您必须同意条款才能启用该功能。查看条款并选择**接受并启用**以继续。

4. 选择**应用**。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于**开发中功能**页面上的**实验性功能**选项卡下。

## 使用询问 Gordon

Docker AI 功能的主要界面是通过 Docker Desktop 中的**询问 Gordon** 视图，或者如果您喜欢使用 CLI：`docker ai` CLI 命令。

启用 Docker AI 功能后，您还会在 Docker Desktop 用户界面的其他各个地方找到**询问 Gordon** 的引用。
每当您在用户界面中遇到带有**闪光** (✨) 图标的按钮时，您都可以使用该按钮从询问 Gordon 获取上下文支持。

## 示例工作流程

询问 Gordon 是一个通用 AI 助手，旨在帮助您完成所有与 Docker 相关的任务和工作流程。如果您需要一些灵感，这里有一些您可以尝试的方法：

- [排除崩溃容器的故障](#troubleshoot-a-crashed-container)
- [获取运行容器的帮助](#get-help-with-running-a-container)
- [改进 Dockerfile](#improve-a-dockerfile)

有关更多示例，请尝试直接询问 Gordon。例如：

```console
$ docker ai "你能做什么？"
```

### 排除崩溃容器的故障

如果您尝试使用无效配置或命令启动容器，您可以使用询问 Gordon 来排除错误。例如，尝试在未指定数据库密码的情况下启动 Postgres 容器：

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

在 Docker Desktop 的**容器**视图中，选择容器名称旁边的 ✨ 图标，或检查容器并打开**询问 Gordon** 选项卡。

### 获取运行容器的帮助

如果您想运行特定镜像但不确定如何操作，Gordon 可能会帮助您进行设置：

1. 从 Docker Hub 拉取镜像（例如，`postgres`）。
2. 在 Docker Desktop 的**镜像**视图中打开并选择镜像。
3. 选择**运行**按钮。

在**运行新容器**对话框中，您应该会看到有关**询问 Gordon** 的消息。

![Docker Desktop 中的询问 Gordon 提示](../../images/gordon-run-ctr.png)

提示中的链接文本是启动与询问 Gordon 对话的建议提示。

### 改进 Dockerfile

Gordon 可以分析您的 Dockerfile 并提出改进建议。要让 Gordon 使用 `docker ai` 命令评估您的 Dockerfile：

1. 导航到您的项目目录：

   ```console
   $ cd path/to/my/project
   ```

2. 使用 `docker ai` 命令评估您的 Dockerfile：

   ```console
   $ docker ai rate my Dockerfile
   ```

Gordon 将分析您的 Dockerfile 并识别在多个方面进行改进的机会：

- 构建缓存优化
- 安全性
- 镜像大小效率
- 最佳实践合规性
- 可维护性
- 可重现性
- 可移植性
- 资源效率

## 禁用询问 Gordon

### 对于个人用户

如果您已启用询问 Gordon 并想再次禁用它：

1. 打开 Docker Desktop 中的**设置**视图。
2. 导航到**Beta 功能**。
3. 取消勾选**启用 Docker AI** 复选框。
4. 选择**应用**。

### 对于组织

如果您想为整个 Docker 组织禁用询问 Gordon，请使用
[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md)，
将以下属性添加到您的 `admin-settings.json` 文件中：

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

我们重视您对询问 Gordon 的意见，并鼓励您分享您的经验。
您的反馈有助于我们改进和完善询问 Gordon，使其对所有用户更有效。如果您
遇到问题、有建议，或者只是想分享您喜欢的内容，
可以通过以下方式联系我们：

- 点赞和点踩按钮

  使用响应中的点赞或点踩按钮评价询问 Gordon 的响应。

- 反馈调查

  您可以通过 Docker Desktop 中**询问 Gordon** 视图中的“提供反馈”链接，或通过 CLI 运行 `docker ai feedback` 命令来访问询问 Gordon 调查。