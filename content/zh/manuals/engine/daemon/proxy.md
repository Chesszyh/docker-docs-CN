---
description: 了解如何配置 Docker 守护进程使用 HTTP 代理
keywords: dockerd, daemon, configuration, proxy, networking, http_proxy, https_proxy, no_proxy, systemd, environment variables, 代理, 配置, 守护进程, 环境变量
title: 守护进程代理配置
weight: 30
aliases:
  - /articles/host_integration/
  - /articles/systemd/
  - /engine/admin/systemd/
  - /engine/articles/systemd/
  - /config/daemon/systemd/
  - /config/daemon/proxy/
---

<a name="httphttps-proxy"><!-- 包含用于指向旧章节的深层链接 --></a>

如果您的组织使用代理服务器连接互联网，您可能需要配置 Docker 守护进程使用该代理服务器。守护进程使用代理服务器访问存储在 Docker Hub 和其他注册表上的镜像，并连接 Docker Swarm 中的其他节点。

本页介绍了如何为 Docker 守护进程配置代理。有关为 Docker CLI 配置代理设置的说明，请参阅 [配置 Docker CLI 使用代理服务器](/manuals/engine/cli/proxy.md)。

> [!IMPORTANT]
> Docker Desktop 会忽略 `daemon.json` 中指定的代理配置。如果您使用的是 Docker Desktop，可以通过 [Docker Desktop 设置](/manuals/desktop/settings-and-maintenance/settings.md#proxies) 配置代理。

有两种方式可以配置这些设置：

- 通过配置文件或 CLI 标志 [配置守护进程](#daemon-configuration)
- 在系统上设置 [环境变量](#environment-variables)

直接配置守护进程的优先级高于环境变量。

## 守护进程配置 (Daemon configuration)

您可以在 `daemon.json` 文件中配置守护进程的代理行为，或者在 `dockerd` 命令中使用 `--http-proxy` 或 `--https-proxy` CLI 标志。推荐使用 `daemon.json` 进行配置。

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }
}
```

更改配置文件后，重启守护进程使代理配置生效：

```console
$ sudo systemctl restart docker
```

## 环境变量 (Environment variables)

Docker 守护进程在其启动环境中检查以下环境变量以配置 HTTP 或 HTTPS 代理行为：

- `HTTP_PROXY`
- `http_proxy`
- `HTTPS_PROXY`
- `https_proxy`
- `NO_PROXY`
- `no_proxy`

### systemd 单元文件

如果您将 Docker 守护进程作为 systemd 服务运行，可以创建一个 systemd 配置文件 (drop-in file) 为 `docker` 服务设置变量。

> **无根模式 (Rootless mode) 说明**
>
> 在 [无根模式](/manuals/engine/security/rootless.md) 下运行 Docker 时，systemd 配置文件的位置会有所不同。在无根模式下，Docker 作为用户模式的 systemd 服务启动，使用存储在每个用户主目录下的文件：`~/.config/systemd/user/docker.service.d/`。此外，执行 `systemctl` 时不能带 `sudo`，且必须带 `--user` 标志。如果您正在运行无根模式 Docker，请选择“无根模式”选项卡。

{{< tabs >}}
{{< tab name="常规安装" >}}

1. 为 `docker` 服务创建一个 systemd drop-in 目录：

   ```console
   $ sudo mkdir -p /etc/systemd/system/docker.service.d
   ```

2. 创建一个名为 `/etc/systemd/system/docker.service.d/http-proxy.conf` 的文件，添加 `HTTP_PROXY` 环境变量：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   ```

   如果您位于 HTTPS 代理服务器后面，请设置 `HTTPS_PROXY` 环境变量：

   ```systemd
   [Service]
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   ```

   可以设置多个环境变量；要同时设置非 HTTPS 和 HTTPS 代理：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   ```

   > [!NOTE]
   >
   > 代理值中的特殊字符 (如 `#?!()[]{}`) 必须使用 `%%` 进行双重转义。例如：
   >
   > ```systemd
   > [Service]
   > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
   > ```

3. 如果您有需要直接连接而不通过代理的内部 Docker 注册表，可以通过 `NO_PROXY` 环境变量指定它们。

   `NO_PROXY` 变量指定一个包含逗号分隔值的字符串，用于指定应排除在代理之外的主机。您可以指定以下选项来排除主机：

   - IP 地址前缀 (`1.2.3.4`)
   - 域名或特殊的 DNS 标签 (`*`)
   - 域名匹配该名称及其所有子域。以 "." 开头的域名仅匹配子域。例如，给定域名 `foo.example.com` 和 `example.com`：
     - `example.com` 匹配 `example.com` 和 `foo.example.com`
     - `.example.com` 仅匹配 `foo.example.com`
   - 单个星号 (`*`) 表示不进行代理
   - IP 地址前缀 (`1.2.3.4:80`) 和域名 (`foo.example.com:80`) 接受字面端口号

   示例：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
   ```

4. 刷新更改并重启 Docker

   ```console
   $ sudo systemctl daemon-reload
   $ sudo systemctl restart docker
   ```

5. 验证配置是否已加载并符合您所做的更改，例如：

   ```console
   $ sudo systemctl show --property=Environment docker

   Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
   ```

{{< /tab >}}
{{< tab name="无根模式" >}}

1. 为 `docker` 服务创建一个 systemd drop-in 目录：

   ```console
   $ mkdir -p ~/.config/systemd/user/docker.service.d
   ```

2. 创建一个名为 `~/.config/systemd/user/docker.service.d/http-proxy.conf` 的文件，添加 `HTTP_PROXY` 环境变量：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   ```

   如果您位于 HTTPS 代理服务器后面，请设置 `HTTPS_PROXY` 环境变量：

   ```systemd
   [Service]
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   ```

   可以设置多个环境变量；要同时设置非 HTTPS 和 HTTPS 代理：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   ```

   > [!NOTE]
   >
   > 代理值中的特殊字符 (如 `#?!()[]{}`) 必须使用 `%%` 进行双重转义。例如：
   >
   > ```systemd
   > [Service]
   > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
   > ```

3. 如果您有需要直接连接而不通过代理的内部 Docker 注册表，可以通过 `NO_PROXY` 环境变量指定它们。

   `NO_PROXY` 变量指定一个包含逗号分隔值的字符串，用于指定应排除在代理之外的主机。您可以指定以下选项来排除主机：

   - IP 地址前缀 (`1.2.3.4`)
   - 域名或特殊的 DNS 标签 (`*`)
   - 域名匹配该名称及其所有子域。以 "." 开头的域名仅匹配子域。例如，给定域名 `foo.example.com` 和 `example.com`：
     - `example.com` 匹配 `example.com` 和 `foo.example.com`
     - `.example.com` 仅匹配 `foo.example.com`
   - 单个星号 (`*`) 表示不进行代理
   - IP 地址前缀 (`1.2.3.4:80`) 和域名 (`foo.example.com:80`) 接受字面端口号

   示例：

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=https://proxy.example.com:3129"
   Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
   ```

4. 刷新更改并重启 Docker

   ```console
   $ systemctl --user daemon-reload
   $ systemctl --user restart docker
   ```

5. 验证配置是否已加载并符合您所做的更改，例如：

   ```console
   $ systemctl --user show --property=Environment docker

   Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
   ```

{{< /tab >}}
{{< /tabs >}}
