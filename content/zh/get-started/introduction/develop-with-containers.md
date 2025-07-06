---
title: 使用容器进行开发
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 此概念页面将教您如何使用容器进行开发
summary: |
  了解如何运行您的第一个容器，获得
  Docker 强大功能的动手经验。我们将介绍如何在容器化环境中对
  后端和前端代码进行实时更改，确保
  无缝集成和测试。
weight: 2
aliases:
 - /guides/getting-started/develop-with-containers/
---

{{< youtube-embed D0SDBrS3t9I >}}

## 说明

现在您已经安装了 Docker Desktop，您可以进行一些应用程序开发了。具体来说，您将执行以下操作：

1. 克隆并启动一个开发项目
2. 对后端和前端进行更改
3. 立即看到更改

## 动手试试

在这个动手指南中，您将学习如何使用容器进行开发。


## 启动项目

1. 首先，将[项目克隆或下载为 ZIP 文件](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到您的本地计算机。

    ```console
    $ git clone https://github.com/docker/getting-started-todo-app
    ```

    克隆项目后，导航到克隆创建的新目录：

    ```console
    $ cd getting-started-todo-app
    ```

2. 拥有项目后，使用 Docker Compose 启动开发环境。


    要使用 CLI 启动项目，请运行以下命令：

   ```console
   $ docker compose watch
   ```

   您将看到一个输出，显示正在拉取容器镜像、启动容器等。如果您此时不完全理解，请不要担心。但是，稍等片刻，一切都应该稳定下来并完成。


3. 在浏览器中打开 [http://localhost](http://localhost) 以查看正在运行的应用程序。应用程序可能需要几分钟才能运行。该应用程序是一个简单的待办事项应用程序，因此您可以随时添加一两个项目、将某些项目标记为已完成，甚至删除一个项目。

    ![首次启动后入门待办事项应用程序的屏幕截图](images/develop-getting-started-app-first-launch.webp)


### 环境中有什么？

现在环境已经启动并正在运行，它实际上包含什么？从高层次上讲，有几个容器（或进程），每个容器都为应用程序提供特定的需求：

- React 前端 - 一个正在运行 React 开发服务器的 Node 容器，使用 [Vite](https://vitejs.dev/)。
- Node 后端 - 后端提供一个 API，该 API 提供检索、创建和删除待办事项的功能。
- MySQL 数据库 - 一个用于存储项目列表的数据库。
- phpMyAdmin - 一个基于 Web 的界面，用于��可在 [http://db.localhost](http://db.localhost) 访问的数据库进行交互。
- Traefik 代理 - [Traefik](https://traefik.io/traefik/) 是一个应用程序代理，可根据路由规则将请求路由到正确的服务。它将所有对 `localhost/api/*` 的请求发送到后端，将对 `localhost/*` 的请求发送到前端，然后将对 `db.localhost` 的请求发送到 phpMyAdmin。这提供了使用端口 80（而不是每个服务使用不同的端口）访问所有应用程序的能力。

有了这个环境，作为开发人员，您无需安装或配置任何服务、填充数据库模式、配置数据库凭据或任何其他东西。您只需要 Docker Desktop。其余的都可以正常工作。


## 对应用程序进行更改

有了这个正在运行的环境，您就可以对应用程序进行一些更改，并了解 Docker 如何帮助提供快速的反馈循环。

### 更改问候语

页面顶部的问候语由 `/api/greeting` 处的 API 调用填充。目前，它总是返回“Hello world!”。您现在将修改它以返回三个随机消息之一（您可以选择）。

1. 在文本编辑器中打开 `backend/src/routes/getGreeting.js` 文件。此文件提供 API 端点的处理程序。

2. 将顶部的变量修改为问候语数组。随时使用以下修改或根据自己的喜好进行自定义。此��，更新端点以从此列表中发送随机问候语。

    ```js {linenos=table,hl_lines=["1-5",9],linenostart=1}
    const GREETINGS = [
        "Whalecome!",
        "All hands on deck!",
        "Charting the course ahead!",
    ];

    module.exports = async (req, res) => {
        res.send({
            greeting: GREETINGS[ Math.floor( Math.random() * GREETINGS.length )],
        });
    };
    ```

3. 如果您还没有这样做，请保存文件。如果您刷新浏览器，您应该会看到一个新的问候语。如果您继续刷新，您应该会看到所有消息都出现。

    ![带有新问候语的待办事项应用程序的屏幕截图](images/develop-app-with-greetings.webp)


### 更改占位符文本

当您查看应用程序时，您会看到占位符文本只是“New Item”。您现在将使其更具描述性和趣味性。您还将对应用程序的样式进行一些更改。

1. 打开 `client/src/components/AddNewItemForm.jsx` 文件。这提供了用于向待办事项列表添加新项目的组件。

2. 将 `Form.Control` 元素的 `placeholder` 属性修改为您想要显示的任何内容。

    ```js {linenos=table,hl_lines=[5],linenostart=33}
    <Form.Control
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        type="text"
        placeholder="What do you need to do?"
        aria-label="New item"
    />
    ```

3. 保存文件并返回浏览器。您应该会看到更改已热重载到您的浏览器中。如果您不喜欢它，可以随时调整它，直到它看起来恰到好处。

![在添加项目文本字段中具有更新占位符的待办事项应用程序的屏幕截图"](images/develop-app-with-updated-placeholder.webp)


### 更改背景颜色

在您认为应用程序最终确定之前，您需要使颜色更好。

1. 打开 `client/src/index.scss` 文件。

2. 将 `background-color` 属性调整为您喜欢的任何颜色。提供的代码段是一种柔和的蓝色，以配合 Docker 的航海主题。

    如果您使用的是 IDE，则可以使用集成的颜色选择器选择颜色。否则，可以随时使用在线[颜色选择器](https://www.w3schools.com/colors/colors_picker.asp)。

    ```css {linenos=table,hl_lines=2,linenostart=3}
    body {
        background-color: #99bbff;
        margin-top: 50px;
        font-family: 'Lato';
    }
    ```

    每次保存都应该让您立即在浏览器中看到更改。继续调整它，直到它成为您的完美设置。


    ![具有新占位符和背景颜色的待办事项应用程序的屏幕截图"](images/develop-app-with-updated-client.webp)

这样���您就完成了。恭喜您更新了您的网站。


## 回顾

在继续之前，花点时间回顾一下这里发生的事情。在几分钟内，您就能够：

- 以零安装工作量启动一个完整的开发项目。容器化环境提供了开发环境，确保您拥有所需的一切。您不必直接在您的机器上安装 Node、MySQL 或任何其他依赖项。您只需要 Docker Desktop 和一个代码编辑器。

- 进行更改并立即看到它们。这之所以成为可能，是因为 1) 每个容器中运行的进程都在监视和响应文件更改，以及 2) 文件与容器化环境共享。

Docker Desktop 实现了所有这些以及更多功能。一旦您开始使用容器进行思考，您就可以创建几乎任何环境并轻松地与您的团队共享。

## 后续步骤

现在应用程序已经更新，您已准备好了解如何将其打包为容器镜像并将其推送到仓库，特别是 Docker Hub。

{{< button text="构建并推送您的第一个镜像" url="build-and-push-first-image" >}}

