---
title: 安装 Docker Scout
linkTitle: 安装
weight: 10
description: Docker Scout CLI 插件的安装说明
keywords: scout, cli, install, download
---

Docker Scout CLI 插件预装在 Docker Desktop 中。

如果您运行的是不带 Docker Desktop 的 Docker Engine，
Docker Scout 不会预装，
但您可以将其作为独立二进制文件安装。

## 安装脚本

要安装最新版本的插件，请运行以下命令：

```console
$ curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
$ sh install-scout.sh
```

> [!NOTE]
>
> 在本地运行从互联网下载的脚本之前，请务必先检查它们。
> 在安装之前，请熟悉该便捷脚本的潜在风险和限制。

## 手动安装

{{< tabs >}}
{{< tab name="Linux" >}}

1. 从[发布页面](https://github.com/docker/scout-cli/releases)下载最新版本。
2. 在 `$HOME/.docker` 下创建一个名为 `scout` 的子目录。

   ```console
   $ mkdir -p $HOME/.docker/scout
   ```

3. 解压存档并将 `docker-scout` 二进制文件移动到 `$HOME/.docker/scout` 目录。
4. 使二进制文件可执行：`chmod +x $HOME/.docker/scout/docker-scout`。
5. 将 `scout` 子目录作为插件目录添加到您的 `.docker/config.json` 中：

   ```json
   {
     "cliPluginsExtraDirs": [
       "/home/<USER>/.docker/scout"
     ]
   }
   ```

   将 `<USER>` 替换为您在系统上的用户名。

   > [!NOTE]
   > `cliPluginsExtraDirs` 的路径必须是绝对路径。

{{< /tab >}}
{{< tab name="macOS" >}}

1. 从[发布页面](https://github.com/docker/scout-cli/releases)下载最新版本。
2. 在 `$HOME/.docker` 下创建一个名为 `scout` 的子目录。

   ```console
   $ mkdir -p $HOME/.docker/scout
   ```

3. 解压存档并将 `docker-scout` 二进制文件移动到 `$HOME/.docker/scout` 目录。
4. 使二进制文件可执行：

   ```console
   $ chmod +x $HOME/.docker/scout/docker-scout
   ```

5. 在 macOS 上授权该二进制文件可执行：

   ```console
   xattr -d com.apple.quarantine $HOME/.docker/scout/docker-scout
   ```

6. 将 `scout` 子目录作为插件目录添加到您的 `.docker/config.json` 中：

   ```json
   {
     "cliPluginsExtraDirs": [
       "/Users/<USER>/.docker/scout"
     ]
   }
   ```

   将 `<USER>` 替换为您在系统上的用户名。

   > [!NOTE]
   > `cliPluginsExtraDirs` 的路径必须是绝对路径。

{{< /tab >}}
{{< tab name="Windows" >}}

1. 从[发布页面](https://github.com/docker/scout-cli/releases)下载最新版本。
2. 在 `%USERPROFILE%/.docker` 下创建一个名为 `scout` 的子目录。

   ```console
   % mkdir %USERPROFILE%\.docker\scout
   ```

3. 解压存档并将 `docker-scout.exe` 二进制文件移动到 `%USERPROFILE%\.docker\scout` 目录。
4. 将 `scout` 子目录作为插件目录添加到您的 `.docker\config.json` 中：

   ```json
   {
     "cliPluginsExtraDirs": [
       "C:\Users\<USER>\.docker\scout"
     ]
   }
   ```

   将 `<USER>` 替换为您在系统上的用户名。

   > [!NOTE]
   > `cliPluginsExtraDirs` 的路径必须是绝对路径。

{{< /tab >}}
{{< /tabs >}}

## 容器镜像

Docker Scout CLI 插件也可以作为[容器镜像](https://hub.docker.com/r/docker/scout-cli)使用。
使用 `docker/scout-cli` 在不在主机上安装 CLI 插件的情况下运行 `docker scout` 命令。

```console
$ docker run -it \
  -e DOCKER_SCOUT_HUB_USER=<your Docker Hub user name> \
  -e DOCKER_SCOUT_HUB_PASSWORD=<your Docker Hub PAT>  \
  docker/scout-cli <command>
```

## GitHub Action

Docker Scout CLI 插件也可以作为 [GitHub action](https://github.com/docker/scout-action) 使用。
您可以在 GitHub 工作流中使用它，在每次推送时自动分析镜像并评估策略合规性。

Docker Scout 还与更多 CI/CD 工具集成，例如 Jenkins、GitLab 和 Azure DevOps。
了解更多关于 Docker Scout 可用[集成](./integrations/_index.md)的信息。
