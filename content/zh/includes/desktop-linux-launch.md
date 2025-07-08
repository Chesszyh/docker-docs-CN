要启动 Docker Desktop for Linux：

1. 在您的 Gnome/KDE 桌面中导航到 Docker Desktop 应用程序。

2. 选择 **Docker Desktop** 启动 Docker。

   此时会显示 Docker 订阅服务协议。

3. 选择 **Accept** 继续。接受条款后，Docker Desktop 将启动。

   请注意，如果您不同意这些条款，Docker Desktop 将不会运行。您可以稍后通过打开 Docker Desktop 来选择接受这些条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读[常见问题解答](https://www.docker.com/pricing/faq)。

或者，打开一个终端并运行：

```console
$ systemctl --user start docker-desktop
```

Docker Desktop 启动时，它会创建一个专用的[上下文](/engine/context/working-with-contexts)，Docker CLI 可以将其用作目标，并将其设置为当前使用的上下文。这是为了避免与可能在 Linux 主机上运行并使用默认上下文的本地 Docker 引擎发生冲突。关闭时，Docker Desktop 会将当前上下文重置为前一个。

Docker Desktop 安装程序会更新主机上的 Docker Compose 和 Docker CLI 二进制文件。它会安装 Docker Compose V2，并允许用户从“设置”面板将其链接为 docker-compose。Docker Desktop 会在 `/usr/local/bin/com.docker.cli` 中安装包含云集成功能的新 Docker CLI 二进制文件，并在 `/usr/local/bin` 中创建指向经典 Docker CLI 的符号链接。

成功安装 Docker Desktop 后，您可以通过运行以下命令来检查这些二进制文件的版本：

```console
$ docker compose version
Docker Compose version v2.29.1

$ docker --version
Docker version 27.1.1, build 6312585

$ docker version
Client: 
 Version:           23.0.5
 API version:       1.42
 Go version:        go1.21.12
<...>
```

要使 Docker Desktop 在登录时启动，请从 Docker 菜单中选择 **Settings** > **General** > **Start Docker Desktop when you sign in to your computer**。

或者，打开一个终端并运行：

```console
$ systemctl --user enable docker-desktop
```

要停止 Docker Desktop，请选择 Docker 菜单图标以打开 Docker 菜单，然后选择 **Quit Docker Desktop**。

或者，打开一个终端并运行：

```console
$ systemctl --user stop docker-desktop
```
