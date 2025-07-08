### 使用便捷脚本安装

Docker 在 [https://get.docker.com/](https://get.docker.com/) 提供了一个便捷脚本，用于以非交互方式将 Docker 安装到开发环境中。不建议在生产环境中使用该便捷脚本，但它对于创建适合您需求的配置脚本很有用。另请参阅[使用存储库安装](#install-using-the-repository)步骤，以了解使用软件包存储库进行安装的步骤。该脚本的源代码是开源的，您可以在 [GitHub 上的 `docker-install` 存储库](https://github.com/docker/docker-install)中找到它。

<!-- prettier-ignore -->
在本地运行从互联网下载的脚本之前，请务必仔细检查。在安装之前，请熟悉便捷脚本的潜在风险和限制：

- 该脚本需要 `root` 或 `sudo` 权限才能运行。
- 该脚本会尝试检测您的 Linux ���行版和版本，并为您配置软件包管理系统。
- 该脚本不允许您自定义大多数安装参数。
- 该脚本会安装依赖项和建议项，而不会要求确认。这可能会安装大量软件包，具体取决于您主机的当前配置。
- 默认情况下，该脚本会安装 Docker、containerd 和 runc 的最新稳定版本。使用此脚本配置计算机时，这可能会导致 Docker 的主要版本意外升级。在部署到生产系统之前，请务必在测试环境中测试升级。
- 该脚本并非旨在升级现有的 Docker 安装。使用该脚本更新现有安装时，依赖项可能不会更新到预期版本，从而导致版本过时。

> [!TIP]
>
> 在运行之前预览脚本步骤。您可以使用 `--dry-run` 选项运行脚本，以了解在调用脚本时将运行哪些步骤：
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

此示例从 [https://get.docker.com/](https://get.docker.com/) 下载脚本并运行它以在 Linux 上安装 Docker 的最新稳定版本：

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

您现在已经成功���装并启动了 Docker 引擎。`docker` 服务会在基于 Debian 的发行版上自动启动。在基于 `RPM` 的发行版（例如 CentOS、Fedora、RHEL 或 SLES）上，您需要使用相应的 `systemctl` 或 `service` 命令手动启动它。如消息所示，非 root 用户默认情况下无法运行 Docker 命令。

> **以非特权用户身份使用 Docker，还是以无根模式安装？**
>
> 安装脚本需要 `root` 或 `sudo` 权限才能安装和使用 Docker。如果您想授予非 root 用户访问 Docker 的权限，请参阅 [Linux 的安装后步骤](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您也可以在没有 `root` 权限的情况下安装 Docker，或者将其配置为以无根模式运行。有关以无根模式运行 Docker 的说明，请参阅[以非 root 用户身份运行 Docker 守护程序（无根模式）](/engine/security/rootless/)。

#### 安装预发布版本

Docker 还在 [https://test.docker.com/](https://test.docker.com/) 提供了一个便捷脚本，用于在 Linux 上安装 Docker 的预发布版本。此脚本与 `get.docker.com` 上的脚本相同，但它会配置您的软件包管理器以使用 Docker 软件包存储库的测试通道。测试通道包括 Docker 的稳定版和预发布版（测试版、候选发布版）。使用此脚本可以抢先体验新版本，并在将其发布为稳定版之前在测试环境中对其进行评估。

要从测试通道在 Linux 上安装最新版本的 Docker，请运行：

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### 使用便捷脚本后升级 Docker

如果您使用便捷脚本安装了 Docker，则应直接使用软件包管理器升级 Docker。重新运行便捷脚本没有任何优势。如果它尝试重新安装主机上已存在的存储库，则重新运行它可能会导致问题。
