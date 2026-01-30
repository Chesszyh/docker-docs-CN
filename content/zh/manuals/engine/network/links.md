---
description: 了解如何将 Docker 容器连接在一起。
keywords: Examples, Usage, user guide, links, linking, docker, documentation, examples, names, name, container naming, port, map, network port, network, 链接, 容器命名, 端口映射
title: 传统的容器链接 (Legacy container links)
aliases:
- /userguide/dockerlinks/
- /engine/userguide/networking/default_network/dockerlinks/
- /network/links/
---

> [!WARNING]
>
> `--link` 标志是 Docker 的一个传统功能。它最终可能会被移除。除非您确实需要继续使用它，否则我们建议您使用用户定义网络来实现两个容器之间的通信，而不是使用 `--link`。用户定义网络不支持的一个功能是跨容器共享环境变量 (这是 `--link` 可以做到的)。但是，您可以使用其他机制 (例如卷) 以更受控的方式跨容器共享环境变量。
>
> 参见 [用户定义 bridge 网络与默认 bridge 网络的区别](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge)，以了解 `--link` 的一些替代方案。

本节中的信息解释了 Docker 默认 `bridge` 网络中的传统容器链接，该网络在您安装 Docker 时自动创建。

在 [Docker 网络功能](index.md) 推出之前，您可以使用 Docker link 功能让容器相互发现并安全地将一个容器的信息传输到另一个容器。随着 Docker 网络功能的引入，您仍然可以创建 link，但它们在默认 `bridge` 网络和 [用户定义网络](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge) 之间的行为有所不同。

本节简要讨论通过网络端口连接，然后详细介绍默认 `bridge` 网络中的容器链接。

## 使用网络端口映射连接

假设您使用此命令运行一个简单的 Python Flask 应用程序：

```console
$ docker run -d -P training/webapp python app.py
```

> [!NOTE]
>
> 容器有一个内部网络和一个 IP 地址。Docker 可以有各种网络配置。您可以在 [这里](index.md) 查看有关 Docker 网络的更多信息。

创建该容器时，使用了 `-P` 标志，以自动将其内部的任何网络端口映射到 Docker 主机上 *临时端口范围* 内的一个随机高端口。接下来，当运行 `docker ps` 时，您会看到容器中的 5000 端口被绑定到主机上的 49155 端口。

```console
$ docker ps nostalgic_morse

CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```

您还看到了如何使用 `-p` 标志将容器的端口绑定到特定端口。这里主机的 80 端口被映射到容器的 5000 端口：

```console
$ docker run -d -p 80:5000 training/webapp python app.py
```

您也看到了为什么这不是一个好主意，因为它限制了在该特定端口上只能运行一个容器。

相反，您可以指定一个主机端口范围来绑定容器端口，该范围不同于默认的 *临时端口范围*：

```console
$ docker run -d -p 8000-9000:5000 training/webapp python app.py
```

这将把容器中的 5000 端口绑定到主机上 8000 到 9000 之间的随机可用端口。

您还可以通过其他几种方式配置 `-p` 标志。默认情况下，`-p` 标志将指定的端口绑定到主机上的所有接口。但您也可以指定绑定到特定接口，例如仅绑定到 `localhost`。

```console
$ docker run -d -p 127.0.0.1:80:5000 training/webapp python app.py
```

这将把容器内的 5000 端口绑定到主机上的 `localhost` 或 `127.0.0.1` 接口的 80 端口。

或者，要将容器的 5000 端口绑定到一个动态端口，但仅在 `localhost` 上，您可以使用：

```console
$ docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```

您还可以通过添加后缀 `/udp` 或 `/sctp` 来绑定 UDP 和 SCTP 端口 (SCTP 通常由 SIGTRAN、Diameter 和 S1AP/X2AP 等电信协议使用)。例如：

```console
$ docker run -d -p 127.0.0.1:80:5000/udp training/webapp python app.py
```

您还学习了非常有用的 `docker port` 快捷方式，它向我们展示了当前的端口绑定。这对于显示特定端口配置也很有用。例如，如果您已将容器端口绑定到主机上的 `localhost`，那么 `docker port` 输出会反映这一点。

```console
$ docker port nostalgic_morse 5000

127.0.0.1:49155
```

> [!NOTE]
>
> `-p` 标志可以多次使用以配置多个端口。

## 使用链接系统连接

> [!NOTE]
>
> 本节介绍默认 `bridge` 网络中的传统 link 功能。有关用户定义网络中 link 的更多信息，请参阅 [用户定义 bridge 网络与默认 bridge 网络的区别](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge)。

网络端口映射不是 Docker 容器相互连接的唯一方式。Docker 还有一个链接 (linking) 系统，允许您将多个容器链接在一起并将连接信息从一个容器发送到另一个容器。当容器被链接时，有关源容器的信息可以发送到接收容器。这允许接收方查看描述源容器各个方面的选定数据。

### 命名的重要性

为了建立链接，Docker 依赖于容器的名称。您已经看到，您创建的每个容器都有一个自动生成的名称；事实上，在本指南中您已经熟悉了我们的老朋友 `nostalgic_morse`。您也可以自己命名容器。这种命名提供了两个有用的功能：

1. 为具有特定功能的容器命名，使您更容易记住它们，例如将包含 Web 应用程序的容器命名为 `web`。

2. 它为 Docker 提供了一个参考点，使其能够引用其他容器，例如，您可以指定将容器 `web` 链接到容器 `db`。

您可以使用 `--name` 标志为容器命名，例如：

```console
$ docker run -d -P --name web training/webapp python app.py
```

这将启动一个新容器，并使用 `--name` 标志将容器命名为 `web`。您可以使用 `docker ps` 命令查看容器的名称。

```console
$ docker ps -l

CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```

您还可以使用 `docker inspect` 返回容器的名称。

> [!NOTE]
>
> 容器名称必须是唯一的。这意味着您只能将一个容器命名为 `web`。如果您想重用一个容器名称，必须在创建具有相同名称的新容器之前删除旧容器 (使用 `docker container rm`)。作为替代方案，您可以在 `docker run` 命令中使用 `--rm` 标志。这将在容器停止后立即将其删除。

## 跨链接的通信

链接允许容器相互发现并安全地将有关一个容器的信息传输到另一个容器。设置链接时，您在源容器和接收容器之间创建了一个管道。接收方随后可以访问有关源的选定数据。要创建链接，请使用 `--link` 标志。首先，创建一个新容器，这次是一个包含数据库的容器。

```console
$ docker run -d --name db training/postgres
```

这将从 `training/postgres` 镜像创建一个名为 `db` 的新容器，该镜像包含一个 PostgreSQL 数据库。

现在，您需要删除之前创建的 `web` 容器，以便将其替换为链接的容器：

```console
$ docker container rm -f web
```

现在，创建一个新的 `web` 容器并将其与您的 `db` 容器链接。

```console
$ docker run -d -P --name web --link db:db training/webapp python app.py
```

这将把新的 `web` 容器与您之前创建的 `db` 容器链接起来。`--link` 标志的形式如下：

    --link <name or id>:alias

其中 `name` 是我们要链接到的容器名称，`alias` 是链接名称的别名。该别名很快就会被用到。`--link` 标志也可以采用以下形式：

    --link <name or id>

在这种情况下，别名与名称匹配。您可以将前面的示例写为：

```console
$ docker run -d -P --name web --link db training/webapp python app.py
```

接下来，使用 `docker inspect` 检查您的链接容器：

```console
$ docker inspect -f "{{ .HostConfig.Links }}" web

[/db:/web/db]
```

您可以看到 `web` 容器现在已链接到 `db` 容器 `web/db`。这使其能够访问有关 `db` 容器的信息。

那么链接容器到底做了什么呢？您已经了解到，链接允许源容器向接收容器提供有关自身的信息。在我们的示例中，接收方 `web` 可以访问有关源 `db` 的信息。为此，Docker 在容器之间创建了一个安全隧道，无需在容器上向外暴露任何端口；当我们启动 `db` 容器时，我们没有使用 `-P` 或 `-p` 标志。这是链接的一个巨大优势：我们不需要将源容器 (此处为 PostgreSQL 数据库) 暴露在网络中。

Docker 以两种方式将源容器的连接信息暴露给接收容器：

* 环境变量
* 更新 `/etc/hosts` 文件

### 环境变量

当您链接容器时，Docker 会创建多个环境变量。Docker 根据 `--link` 参数在目标容器中自动创建环境变量。它还会从源容器中暴露所有源自 Docker 的环境变量。这些包括来自以下位置的变量：

* 源容器 Dockerfile 中的 `ENV` 命令
* 启动源容器时 `docker run` 命令中的 `-e`、`--env` 和 `--env-file` 选项

这些环境变量使得从目标容器内部以编程方式发现与源容器相关的信息成为可能。

> [!WARNING]
>
> 必须理解，容器内源自 Docker 的所有环境变量都可供链接到它的任何容器使用。如果在其中存储了敏感数据，可能会产生严重的安全影响。

Docker 为 `--link` 参数中列出的每个目标容器设置一个 `<alias>_NAME` 环境变量。例如，如果一个名为 `web` 的新容器通过 `--link db:webdb` 链接到一个名为 `db` 的数据库容器，那么 Docker 会在 `web` 容器中创建一个 `WEBDB_NAME=/web/webdb` 变量。

Docker 还为源容器暴露的每个端口定义了一组环境变量。每个变量都有一个唯一的前缀，格式为 `<name>_PORT_<port>_<protocol>`。

此协议中的组件是：

* 在 `--link` 参数中指定的别名 `<name>` (例如 `webdb`)
* 暴露的 `<port>` 编号
* 协议 `<protocol>`，为 TCP 或 UDP

Docker 使用此格式前缀来定义三个不同的环境变量：

* `prefix_ADDR` 变量包含 URL 中的 IP 地址，例如 `WEBDB_PORT_5432_TCP_ADDR=172.17.0.82`。
* `prefix_PORT` 变量仅包含 URL 中的端口号，例如 `WEBDB_PORT_5432_TCP_PORT=5432`。
* `prefix_PROTO` 变量仅包含 URL 中的协议，例如 `WEBDB_PORT_5432_TCP_PROTO=tcp`。

如果容器暴露多个端口，则为每个端口定义一组环境变量。这意味着，例如，如果一个容器暴露 4 个端口，Docker 将创建 12 个环境变量，每个端口 3 个。

此外，Docker 还会创建一个名为 `<alias>_PORT` 的环境变量。该变量包含源容器第一个暴露端口的 URL。“第一个”端口被定义为编号最小的暴露端口。例如，考虑 `WEBDB_PORT=tcp://172.17.0.82:5432` 变量。如果该端口同时用于 tcp 和 udp，则指定 tcp 的那个。

最后，Docker 还将源容器中源自 Docker 的每个环境变量在目标容器中暴露为环境变量。对于每个变量，Docker 在目标容器中创建一个 `<alias>_ENV_<name>` 变量。变量的值被设置为 Docker 启动源容器时使用的值。

回到我们的数据库示例，您可以运行 `env` 命令来列出指定容器的环境变量。

```console
$ docker run --rm --name web2 --link db:db training/webapp env

<...>
DB_NAME=/web2/db
DB_PORT=tcp://172.17.0.5:5432
DB_PORT_5432_TCP=tcp://172.17.0.5:5432
DB_PORT_5432_TCP_PROTO=tcp
DB_PORT_5432_TCP_PORT=5432
DB_PORT_5432_TCP_ADDR=172.17.0.5
<...>
```

您可以看到 Docker 创建了一系列包含有关源 `db` 容器有用信息的环境变量。每个变量都以前缀 `DB_` 开头，该前缀是从您上面指定的 `alias` 填充的。如果别名是 `db1`，变量将以 `DB1_` 开头。您可以使用这些环境变量配置您的应用程序，使其连接到 `db` 容器上的数据库。连接是安全且私密的；只有链接的 `web` 容器可以与 `db` 容器通信。

### 关于 Docker 环境变量的重要说明

与 [`/etc/hosts` 文件](#updating-the-etchosts-file) 中的主机条目不同，如果源容器重新启动，存储在环境变量中的 IP 地址不会自动更新。我们建议使用 `/etc/hosts` 中的主机条目来解析链接容器的 IP 地址。

这些环境变量仅为容器中的第一个进程设置。某些守护进程 (如 `sshd`) 在为连接生成 shell 时会清除它们。

### 更新 `/etc/hosts` 文件

除了环境变量之外，Docker 还会将源容器的主机条目添加到 `/etc/hosts` 文件中。这是 `web` 容器的一个条目：

```console
$ docker run -t -i --rm --link db:webdb training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.5  webdb 6e5cdeb2d300 db
```

您可以看到两个相关的主机条目。第一个是 `web` 容器的条目，它使用容器 ID 作为主机名。第二个条目使用链接别名来引用 `db` 容器的 IP 地址。除了您提供的别名之外，如果链接容器的名称与提供给 `--link` 参数的别名不同，链接容器的名称以及链接容器的主机名也会添加到 `/etc/hosts` 中以对应链接容器的 IP 地址。您可以通过以下任何条目 ping 该主机：

```console
root@aed84ee21bde:/opt/webapp# apt-get install -yqq inetutils-ping
root@aed84ee21bde:/opt/webapp# ping webdb

PING webdb (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
```

> [!NOTE]
>
> 在示例中，您必须安装 `ping`，因为容器最初不包含它。

在这里，您使用 `ping` 命令通过其主机条目 ping `db` 容器，该条目解析为 `172.17.0.5`。您可以使用此主机条目配置应用程序以利用您的 `db` 容器。

> [!NOTE]
>
> 您可以将多个接收容器链接到单个源。例如，您可以将多个 (名称不同的) Web 容器连接到您的 `db` 容器。

如果您重新启动源容器，链接容器上的 `/etc/hosts` 文件将自动更新为源容器的新 IP 地址，从而允许链接通信继续。

```console
$ docker restart db
db

$ docker run -t -i --rm --link db:db training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.9  db
```
