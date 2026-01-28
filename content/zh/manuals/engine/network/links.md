---
description: 学习如何连接 Docker 容器。
keywords: Examples, Usage, user guide, links, linking, docker, documentation, examples,
  names, name, container naming, port, map, network port, network
title: 旧版容器链接
aliases:
- /userguide/dockerlinks/
- /engine/userguide/networking/default_network/dockerlinks/
- /network/links/
---

> [!WARNING]
>
> `--link` 标志是 Docker 的遗留功能。它最终
>可能会被移除。除非你绝对需要继续使用它，我们建议你使用
>用户定义网络来促进两个容器之间的通信，而不是使用
>`--link`。用户定义网络不支持的一个功能是
>使用 `--link` 在容器之间共享环境变量。但是，
>你可以使用其他机制（如卷）以更可控的方式在容器之间共享环境变量。
>
> 请参阅[用户定义桥接网络和默认桥接网络之间的区别](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge)
> 了解一些 `--link` 的替代方案。

本节中的信息解释了在安装 Docker 时自动创建的
Docker 默认 `bridge` 网络中的旧版容器链接。

在 [Docker 网络功能](index.md)出现之前，你可以使用
Docker 链接功能允许容器相互发现并安全地
将一个容器的信息传输到另一个容器。随着
Docker 网络功能的引入，你仍然可以创建链接，但它们
在默认 `bridge` 网络和
[用户定义网络](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge)之间的行为不同。

本节简要讨论通过网络端口连接，然后详细介绍
默认 `bridge` 网络中的容器链接。

## 使用网络端口映射连接

假设你使用以下命令运行一个简单的 Python Flask 应用程序：

```console
$ docker run -d -P training/webapp python app.py
```

> [!NOTE]
>
> 容器有一个内部网络和一个 IP 地址。
> Docker 可以有多种网络配置。你可以在[这里](index.md)看到更多
> 关于 Docker 网络的信息。

当创建该容器时，使用了 `-P` 标志自动将
其内部的任何网络端口映射到 Docker 主机上*临时端口
范围*内的随机高端口。接下来，当运行 `docker ps` 时，你看到
容器中的端口 5000 绑定到主机上的端口 49155。

```console
$ docker ps nostalgic_morse

CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```

你还看到了如何使用
`-p` 标志将容器的端口绑定到特定端口。这里主机的端口 80 映射到
容器的端口 5000：

```console
$ docker run -d -p 80:5000 training/webapp python app.py
```

你也看到了为什么这不是一个好主意，因为它限制你
在该特定端口上只能运行一个容器。

相反，你可以指定一个主机端口范围来绑定容器端口，
这与默认的*临时端口范围*不同：

```console
$ docker run -d -p 8000-9000:5000 training/webapp python app.py
```

这将把容器中的端口 5000 绑定到主机上
8000 到 9000 之间随机可用的端口。

还有一些其他方法可以配置 `-p` 标志。默认情况下，
`-p` 标志将指定的端口绑定到主机上的所有接口。但你也可以指定绑定到特定
接口，例如只绑定到 `localhost`。

```console
$ docker run -d -p 127.0.0.1:80:5000 training/webapp python app.py
```

这将把容器内的端口 5000 绑定到主机上
`localhost` 或 `127.0.0.1` 接口的端口 80。

或者，要将容器的端口 5000 绑定到动态端口但只绑定到
`localhost`，你可以使用：

```console
$ docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```

你还可以通过添加尾部的 `/udp` 或 `/sctp` 来绑定 UDP 和 SCTP（通常用于 SIGTRAN、Diameter 和 S1AP/X2AP 等电信协议）端口。例如：

```console
$ docker run -d -p 127.0.0.1:80:5000/udp training/webapp python app.py
```

你还学习了有用的 `docker port` 快捷命令，它显示
当前的端口绑定。这对于显示特定端口
配置也很有用。例如，如果你已将容器端口绑定到
主机上的 `localhost`，那么 `docker port` 输出会反映这一点。

```console
$ docker port nostalgic_morse 5000

127.0.0.1:49155
```

> [!NOTE]
>
> `-p` 标志可以多次使用来配置多个端口。

## 使用链接系统连接

> [!NOTE]
>
> 本节涵盖默认 `bridge` 网络中的旧版链接功能。
> 有关用户定义网络中链接的更多信息，请参阅[用户定义桥接网络和默认桥接网络之间的区别](drivers/bridge.md#differences-between-user-defined-bridges-and-the-default-bridge)。

网络端口映射不是 Docker 容器相互连接的唯一方式。Docker 还有一个链接系统，允许你将多个
容器链接在一起，并将连接信息从一个发送到另一个。当
容器被链接时，关于源容器的信息可以发送到
接收容器。这允许接收方看到描述
源容器方面的选定数据。

### 命名的重要性

为了建立链接，Docker 依赖于你的容器的名称。
你已经看到每个创建的容器都有一个自动
创建的名称；确实你已经在本指南中熟悉了我们的老朋友
`nostalgic_morse`。你也可以自己命名容器。命名提供了两个有用的功能：

1. 以使你更容易记住的方式命名执行特定功能的容器会很有用，例如将
   包含 Web 应用程序的容器命名为 `web`。

2. 它为 Docker 提供了一个参考点，允许它引用其他
   容器，例如，你可以指定将容器 `web` 链接到容器 `db`。

你可以使用 `--name` 标志命名容器，例如：

```console
$ docker run -d -P --name web training/webapp python app.py
```

这将启动一个新容器并使用 `--name` 标志
将容器命名为 `web`。你可以使用
`docker ps` 命令查看容器的名称。

```console
$ docker ps -l

CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```

你也可以使用 `docker inspect` 返回容器的名称。


> [!NOTE]
>
> 容器名称必须是唯一的。这意味着你只能将
> 一个容器命名为 `web`。如果你想重用容器名称，你必须删除
> 旧容器（使用 `docker container rm`）才能创建一个
> 同名的新容器。作为替代，你可以在 `docker run` 命令中使用 `--rm`
> 标志。这会在容器
> 停止后立即删除它。

## 跨链接通信

链接允许容器相互发现并安全地将一个容器的信息
传输到另一个容器。当你设置链接时，你在
源容器和接收容器之间创建了一个管道。接收方
然后可以访问关于源的选定数据。要创建链接，你使用 `--link`
标志。首先，创建一个新容器，这次是一个包含数据库的容器。

```console
$ docker run -d --name db training/postgres
```

这从 `training/postgres`
镜像创建了一个名为 `db` 的新容器，其中包含一个 PostgreSQL 数据库。

现在，你需要删除之前创建的 `web` 容器，以便用
一个链接的容器替换它：

```console
$ docker container rm -f web
```

现在，创建一个新的 `web` 容器并将其链接到你的 `db` 容器。

```console
$ docker run -d -P --name web --link db:db training/webapp python app.py
```

这将新的 `web` 容器与你之前创建的 `db` 容器
链接起来。`--link` 标志采用以下形式：

    --link <name or id>:alias

其中 `name` 是我们要链接的容器的名称，`alias` 是
链接名称的别名。该别名稍后会用到。
`--link` 标志也采用以下形式：

    --link <name or id>

在这种情况下，别名与名称匹配。你可以将前面的
示例写成：

```console
$ docker run -d -P --name web --link db training/webapp python app.py
```

接下来，使用 `docker inspect` 检查你的链接容器：


```console
$ docker inspect -f "{{ .HostConfig.Links }}" web

[/db:/web/db]
```


你可以看到 `web` 容器现在链接到 `db` 容器
`web/db`。这允许它访问关于 `db` 容器的信息。

那么链接容器实际上做了什么？你已经了解到链接允许
源容器向接收容器提供关于自己的信息。在
我们的示例中，接收方 `web` 可以访问关于源 `db` 的信息。为此，
Docker 在容器之间创建一个安全隧道，不需要
在容器上对外暴露任何端口；当我们启动
`db` 容器时，我们没有使用 `-P` 或 `-p` 标志。这是
链接的一大好处：我们不需要将源容器（这里是 PostgreSQL 数据库）暴露给
网络。

Docker 以两种方式向接收容器暴露源容器的连接信息：

* 环境变量，
* 更新 `/etc/hosts` 文件。

### 环境变量

当你链接容器时，Docker 会创建多个环境变量。Docker
根据 `--link` 参数在目标容器中自动创建环境变量。它还暴露来自 Docker 的源容器的所有环境变量。这些包括来自以下来源的变量：

* 源容器 Dockerfile 中的 `ENV` 命令
* 启动源容器时 `docker run`
命令中的 `-e`、`--env` 和 `--env-file` 选项

这些环境变量使得从目标容器内以编程方式
发现与源容器相关的信息成为可能。

> [!WARNING]
>
> 重要的是要理解，容器内所有来自 Docker 的
> 环境变量都会对链接到它的任何容器
> 可用。如果其中存储了敏感
> 数据，这可能会产生严重的安全影响。

Docker 为 `--link` 参数中列出的每个目标容器设置一个 `<alias>_NAME` 环境变量。例如，如果一个名为
`web` 的新容器通过 `--link db:webdb` 链接到一个名为 `db` 的数据库容器，
那么 Docker 会在 `web` 容器中创建一个 `WEBDB_NAME=/web/webdb` 变量。

Docker 还为源容器暴露的每个端口定义一组环境变量。每个变量都有一个格式为 `<name>_PORT_<port>_<protocol>` 的唯一前缀

此前缀中的组成部分是：

* 在 `--link` 参数中指定的别名 `<name>`（例如，`webdb`）
* 暴露的 `<port>` 端口号
* TCP 或 UDP 的 `<protocol>`

Docker 使用此前缀格式定义三个不同的环境变量：

* `prefix_ADDR` 变量包含 URL 中的 IP 地址，例如
`WEBDB_PORT_5432_TCP_ADDR=172.17.0.82`。
* `prefix_PORT` 变量只包含 URL 中的端口号，例如
`WEBDB_PORT_5432_TCP_PORT=5432`。
* `prefix_PROTO` 变量只包含 URL 中的协议，例如
`WEBDB_PORT_5432_TCP_PROTO=tcp`。

如果容器暴露多个端口，则为每个端口定义一组环境变量。这意味着，例如，如果一个容器暴露 4 个端口，
Docker 会创建 12 个环境变量，每个端口 3 个。

此外，Docker 会创建一个名为 `<alias>_PORT` 的环境变量。
这个变量包含源容器第一个暴露端口的 URL。
'第一个'端口定义为具有最低编号的暴露端口。
例如，考虑 `WEBDB_PORT=tcp://172.17.0.82:5432` 变量。如果
该端口同时用于 tcp 和 udp，则指定 tcp 的那个。

最后，Docker 还将源容器中每个来自 Docker 的环境变量
作为目标中的环境变量暴露。对于每个
变量，Docker 在目标容器中创建一个 `<alias>_ENV_<name>` 变量。变量的值设置为 Docker 启动源容器时
使用的值。

回到我们的数据库示例，你可以运行 `env`
命令列出指定容器的环境变量。

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

你可以看到 Docker 创建了一系列关于源 `db` 容器的有用信息的环境变量。每个变量都以
`DB_` 为前缀，这是从你上面指定的 `alias` 填充的。如果 `alias`
是 `db1`，变量将以 `DB1_` 为前缀。你可以使用这些
环境变量配置你的应用程序以连接到
`db` 容器上的数据库。连接是安全和私密的；只有
链接的 `web` 容器可以与 `db` 容器通信。

### 关于 Docker 环境变量的重要说明

与 [`/etc/hosts` 文件](#更新-etchosts-文件)中的主机条目不同，
如果源容器重新启动，存储在环境变量中的 IP 地址不会自动更新。我们建议使用
`/etc/hosts` 中的主机条目来解析链接容器的 IP 地址。

这些环境变量只为容器中的第一个进程设置。某些守护进程（如 `sshd`）在为连接生成 shell
时会清除它们。

### 更新 `/etc/hosts` 文件

除了环境变量之外，Docker 还会在 `/etc/hosts` 文件中为
源容器添加主机条目。这是 `web`
容器的一个条目：

```console
$ docker run -t -i --rm --link db:webdb training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.5  webdb 6e5cdeb2d300 db
```

你可以看到两个相关的主机条目。第一个是 `web`
容器的条目，它使用容器 ID 作为主机名。第二个条目使用
链接别名引用 `db` 容器的 IP 地址。除了
你提供的别名之外，如果链接容器的名称与提供给 `--link` 参数的别名
不同，则链接容器的名称以及链接容器的主机名
也会添加到 `/etc/hosts` 中用于链接容器的 IP 地址。你可以通过
这些条目中的任何一个 ping 该主机：

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
> 在示例中，你必须安装 `ping`，因为它最初
> 没有包含在容器中。

在这里，你使用 `ping` 命令使用其主机条目 ping `db` 容器，
该条目解析为 `172.17.0.5`。你可以使用此主机条目配置应用程序
以使用你的 `db` 容器。

> [!NOTE]
>
> 你可以将多个接收容器链接到单个源。例如，
> 你可以将多个（不同名称的）web 容器连接到你的
>`db` 容器。

如果你重新启动源容器，链接容器上的 `/etc/hosts` 文件
会自动更新为源容器的新 IP 地址，
允许链接通信继续。

```console
$ docker restart db
db

$ docker run -t -i --rm --link db:db training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.9  db
```
