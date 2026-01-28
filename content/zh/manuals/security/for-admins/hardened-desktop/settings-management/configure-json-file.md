---
description: 如何为 Docker Desktop 配置设置管理
keywords: admin, controls, rootless, enhanced container isolation
title: 使用 JSON 文件配置设置管理
linkTitle: 使用 JSON 文件
weight: 10
aliases:
 - /desktop/hardened-desktop/settings-management/configure/
 - /security/for-admins/hardened-desktop/settings-management/configure/
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

本页说明如何使用 `admin-settings.json` 文件来配置和
强制执行 Docker Desktop 设置。使用此方法在组织中标准化 Docker
Desktop 环境。

## 前提条件

- [强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)以
确保所有用户使用您的组织进行身份验证。
- 需要 Docker Business 订阅。

只有在身份验证和 Docker Business 许可证检查都成功时，Docker Desktop 才会应用 `admin-settings.json` 文件中的设置。

> [!IMPORTANT]
>
> 如果用户未登录或不属于 Docker Business 组织，
设置文件将被忽略。

## 限制

- `admin-settings.json` 文件在气隙（air-gapped）或离线
环境中不起作用。
- 该文件与限制
Docker Hub 身份验证的环境不兼容。

## 第一步：创建设置文件

您可以：

- 使用 `--admin-settings` 安装程序标志自动生成文件。请参阅：
    - [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 安装指南
    - [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 安装指南
- 或手动创建并放置在以下位置：
    - Mac：`/Library/Application\ Support/com.docker.docker/admin-settings.json`
    - Windows：`C:\ProgramData\DockerDesktop\admin-settings.json`
    - Linux：`/usr/share/docker-desktop/admin-settings.json`

> [!IMPORTANT]
>
> 将文件放置在受保护的目录中以防止被修改。使用
[Jamf](https://www.jamf.com/lp/en-gb/apple-mobile-device-management-mdm-jamf-shared/?attr=google_ads-brand-search-shared&gclid=CjwKCAjw1ICZBhAzEiwAFfvFhEXjayUAi8FHHv1JJitFPb47C_q_RCySTmF86twF1qJc_6GST-YDmhoCuJsQAvD_BwE) 等 MDM 工具进行大规模分发。

## 第二步：定义设置

> [!TIP]
>
> 有关可用设置的完整列表、支持的平台以及它们适用的配置方法，请参阅[设置参考](settings-reference.md)。

`admin-settings.json` 文件使用结构化键来定义可以
配置的内容以及值是否被强制执行。

每个设置都支持 `locked` 字段。当 `locked` 设置为 `true` 时，用户
无法在 Docker Desktop、CLI 或配置文件中更改该值。当
`locked` 设置为 `false` 时，该值作为默认建议，用户
仍可以更新它。

如果用户已在 `settings-store.json`、`settings.json` 或 `daemon.json` 中自定义了该值，则 `locked` 设置为 `false` 的设置在现有安装中会被忽略。

> [!NOTE]
>
> 某些设置是平台特定的或需要最低 Docker Desktop
版本。详情请参阅[设置参考](/manuals/security/for-admins/hardened-desktop/settings-management/settings-reference.md)。

### 示例设置文件

以下文件是 `admin-settings.json` 文件的示例。有关
`admin-settings.json` 文件可配置设置的完整列表，请参阅 [`admin-settings.json` 配置](#admin-settingsjson-配置)。

```json {collapse=true}
{
  "configurationFileVersion": 2,
  "exposeDockerAPIOnTCP2375": {
    "locked": true,
    "value": false
  },
  "proxy": {
    "locked": true,
    "mode": "system",
    "http": "",
    "https": "",
    "exclude": [],
    "windowsDockerdPort": 65000,
    "enableKerberosNtlm": false
  },
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac":"",
    "transparentPorts": ""
  },
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*"
        ]
      },
      "commandList": {
        "type": "deny",
        "commands": ["push"]
      }
    }
  },
  "linuxVM": {
    "wslEngineEnabled": {
      "locked": false,
      "value": false
    },
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    },
    "vpnkitCIDR": {
      "locked": false,
      "value":"192.168.65.0/24"
    }
  },
  "kubernetes": {
     "locked": false,
     "enabled": false,
     "showSystemContainers": false,
     "imagesRepository": ""
  },
  "windowsContainers": {
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    }
  },
  "disableUpdate": {
    "locked": false,
    "value": false
  },
  "analyticsEnabled": {
    "locked": false,
    "value": true
  },
  "extensionsEnabled": {
    "locked": true,
    "value": false
  },
  "scout": {
    "locked": false,
    "sbomIndexing": true,
    "useBackgroundIndexing": true
  },
  "allowBetaFeatures": {
    "locked": false,
    "value": false
  },
  "blockDockerLoad": {
    "locked": false,
    "value": true
  },
  "filesharingAllowedDirectories": [
    {
      "path": "$HOME",
      "sharedByDefault": true
    },
    {
      "path":"$TMP",
      "sharedByDefault": false
    }
  ],
  "useVirtualizationFrameworkVirtioFS": {
    "locked": true,
    "value": true
  },
  "useVirtualizationFrameworkRosetta": {
    "locked": true,
    "value": true
  },
  "useGrpcfuse": {
    "locked": true,
    "value": true
  },
  "displayedOnboarding": {
    "locked": true,
    "value": true
  },
  "desktopTerminalEnabled": {
    "locked": false,
    "value": false
  }
}
```

## 第三步：重启并应用设置

设置在 Docker Desktop 重启且用户登录后生效。

- 新安装：启动 Docker Desktop 并登录。
- 现有安装：完全退出 Docker Desktop 并重新启动。

> [!IMPORTANT]
>
> 从菜单重启 Docker Desktop 是不够的。必须完全
退出并重新打开。

## `admin-settings.json` 配置

### 常规

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`configurationFileVersion`|   |指定配置文件格式的版本。|   |
|`analyticsEnabled`|  |如果 `value` 设置为 false，Docker Desktop 不会向 Docker 发送使用统计信息。 |  |
|`disableUpdate`|  |如果 `value` 设置为 true，将禁用 Docker Desktop 更新检查和通知。|  |
|`extensionsEnabled`|  |如果 `value` 设置为 false，将禁用 Docker 扩展。 |  |
| `blockDockerLoad` | | 如果 `value` 设置为 `true`，用户将无法运行 [`docker load`](/reference/cli/docker/image/load/)，尝试时会收到错误。|  |
| `displayedOnboarding` |  | 如果 `value` 设置为 `true`，将不会向新用户显示引导调查。将 `value` 设置为 `false` 无效。 |  Docker Desktop 4.30 及更高版本 |
| `desktopTerminalEnabled` |  | 如果 `value` 设置为 `false`，开发人员无法使用 Docker 终端与主机交互并直接从 Docker Desktop 执行命令。 |  |
|`exposeDockerAPIOnTCP2375`| 仅限 Windows| 在指定端口上公开 Docker API。如果 `value` 设置为 true，Docker API 将在端口 2375 上公开。注意：这是未经身份验证的，仅应在有适当防火墙规则保护时启用。|  |

### 文件共享和模拟

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `filesharingAllowedDirectories` |  | 指定开发人员可以添加文件共享的路径。也接受 `$HOME`、`$TMP` 或 `$TEMP` 作为 `path` 变量。添加路径时，其子目录也被允许。如果 `sharedByDefault` 设置为 `true`，该路径将在恢复出厂设置或 Docker Desktop 首次启动时添加。 |  |
| `useVirtualizationFrameworkVirtioFS`|  仅限 macOS | 如果 `value` 设置为 `true`，VirtioFS 将被设置为文件共享机制。注意：如果 `useVirtualizationFrameworkVirtioFS` 和 `useGrpcfuse` 的 `value` 都设置为 `true`，VirtioFS 优先。同样，如果两者的 `value` 都设置为 `false`，osxfs 将被设置为文件共享机制。 |  |
| `useGrpcfuse` | 仅限 macOS | 如果 `value` 设置为 `true`，gRPC Fuse 将被设置为文件共享机制。 |  |
| `useVirtualizationFrameworkRosetta`|  仅限 macOS | 如果 `value` 设置为 `true`，Docker Desktop 将开启 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制模拟。注意：这也会自动启用 `Use Virtualization framework`。 | Docker Desktop 4.29 及更高版本。 |

### Docker Scout

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`scout`| | 将 `useBackgroundIndexing` 设置为 `false` 会禁用自动索引加载到镜像存储的镜像。将 `sbomIndexing` 设置为 `false` 会阻止用户通过在 Docker Desktop 中检查镜像或使用 `docker scout` CLI 命令来索引镜像。 |  |

### 代理

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`proxy`|   |如果 `mode` 设置为 `system` 而不是 `manual`，Docker Desktop 从系统获取代理值并忽略为 `http`、`https` 和 `exclude` 设置的值。将 `mode` 更改为 `manual` 以手动配置代理服务器。如果代理端口是自定义的，请在 `http` 或 `https` 属性中指定，例如 `"https": "http://myotherproxy.com:4321"`。`exclude` 属性指定一个逗号分隔的主机和域列表，以绕过代理。 |  |
|&nbsp; &nbsp; &nbsp; &nbsp;`windowsDockerdPort`| 仅限 Windows | 在此端口上本地公开 Docker Desktop 的内部代理，供 Windows Docker 守护进程连接。如果设置为 0，将选择一个随机可用端口。如果值大于 0，使用该确切值作为端口。默认值为 -1，表示禁用该选项。 |  |
|&nbsp; &nbsp; &nbsp; &nbsp;`enableKerberosNtlm`|  |设置为 `true` 时，启用 Kerberos 和 NTLM 身份验证。默认为 `false`。有关更多信息，请参阅设置文档。 | Docker Desktop 4.32 及更高版本。 |

### 容器代理

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`containersProxy` | | 创建气隙容器。有关更多信息，请参阅[气隙容器](../air-gapped-containers.md)。| Docker Desktop 4.29 及更高版本。 |

### Linux VM

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `linuxVM` |   |与 Linux VM 选项相关的参数和设置 - 为方便起见在此处分组。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`wslEngineEnabled`  | 仅限 Windows | 如果 `value` 设置为 true，Docker Desktop 使用基于 WSL 2 的引擎。这会覆盖安装时使用 `--backend=<backend name>` 标志设置的任何内容。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  |如果 `value` 设置为 true，它会覆盖 Docker Engine 配置文件中的选项。请参阅 [Docker Engine 参考](/reference/cli/dockerd/#daemon-configuration-file)。请注意，为了增加安全性，启用增强容器隔离时，某些配置属性可能会被覆盖。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`vpnkitCIDR` |  |覆盖用于 vpnkit DHCP/DNS 的 `*.docker.internal` 网络范围  |  |

### Windows 容器

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `windowsContainers` |  | 与 `windowsContainers` 选项相关的参数和设置 - 为方便起见在此处分组。  |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  | 覆盖 Linux 守护进程配置文件中的选项。请参阅 [Docker Engine 参考](/reference/cli/dockerd/#daemon-configuration-file)。|  |

> [!NOTE]
>
> 此设置无法通过 Docker Admin Console 配置。

### Kubernetes

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`kubernetes`|  | 如果 `enabled` 设置为 true，Docker Desktop 启动时会启动一个 Kubernetes 单节点集群。如果 `showSystemContainers` 设置为 true，Kubernetes 容器会显示在 Docker Desktop Dashboard 中以及运行 `docker ps` 时。[imagesRepository](../../../../desktop/features/kubernetes.md#configuring-a-custom-image-registry-for-kubernetes-control-plane-images) 设置允许您指定 Docker Desktop 从哪个仓库拉取控制平面 Kubernetes 镜像。 |  |

> [!NOTE]
>
> 使用 `imagesRepository` 设置和增强容器隔离（ECI）时，请将以下镜像添加到 [ECI Docker socket 挂载镜像列表](#增强容器隔离)：
>
> * [imagesRepository]/desktop-cloud-provider-kind:*
> * [imagesRepository]/desktop-containerd-registry-mirror:*
>
> 这些容器会挂载 Docker socket，因此您必须将镜像添加到 ECI 镜像列表。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

### 网络

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `defaultNetworkingMode` | 仅限 Windows 和 Mac | 定义新 Docker 网络的默认 IP 协议：`dual-stack`（IPv4 + IPv6，默认）、`ipv4only` 或 `ipv6only`。 | Docker Desktop 4.43 及更高版本。 |
| `dnsInhibition` | 仅限 Windows 和 Mac | 控制返回给容器的 DNS 记录过滤。选项：`auto`（推荐）、`ipv4`、`ipv6`、`none`| Docker Desktop 4.43 及更高版本。 |

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### Beta 功能

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，其中一些设置位于 **Features in development** 页面的 **Experimental features** 选项卡下。

| 参数                                            | 操作系统 | 描述                                                                                                                                                                                                                                               | 版本                                 |
|:-----------------------------------------------------|----|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `allowBetaFeatures`                                  |    | 如果 `value` 设置为 `true`，启用 beta 功能。                                                                                                                                                                                                   |                                         |
| `enableDockerAI`                                     |    | 如果 `allowBetaFeatures` 为 true，将 `enableDockerAI` 设置为 `true` 会默认启用 [Docker AI (Ask Gordon)](/manuals/ai/gordon/_index.md)。您可以独立于 `allowBetaFeatures` 设置控制此设置。                            |                                         |
| `enableInference`                                    |    | 如果 `allowBetaFeatures` 为 true，将 `enableInference` 设置为 `true` 会默认启用 [Docker Model Runner](/manuals/ai/model-runner/_index.md)。您可以独立于 `allowBetaFeatures` 设置控制此设置。                        |                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceTCP`     |    | 启用主机端 TCP 支持。此设置需要先启用 Docker Model Runner 设置。                                                                                                                      |                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceTCPPort` |    | 指定公开的 TCP 端口。此设置需要先启用 Docker Model Runner 设置。                                                                                                                    |                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceCORS`    |    | 指定允许的 CORS 源。空字符串拒绝所有，`*` 接受所有，或逗号分隔的值列表。此设置需要先启用 Docker Model Runner 设置。                                                                                                                                                    |                                         |
| `enableDockerMCPToolkit`                             |    | 如果 `allowBetaFeatures` 为 true，将 `enableDockerMCPToolkit` 设置为 `true` 会默认启用 [MCP toolkit 功能](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)。您可以独立于 `allowBetaFeatures` 设置控制此设置。 |                                         |
| `allowExperimentalFeatures`                          |    | 如果 `value` 设置为 `true`，启用实验性功能。                                                                                                                                           | Docker Desktop 4.41 及更早版本 |

### 增强容器隔离

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`enhancedContainerIsolation`|  | 如果 `value` 设置为 true，Docker Desktop 通过 Linux 用户命名空间以非特权方式运行所有容器，防止它们修改 Docker Desktop VM 内的敏感配置，并使用其他高级技术隔离它们。有关更多信息，请参阅[增强容器隔离](../enhanced-container-isolation/_index.md)。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerSocketMount` |  | 默认情况下，增强容器隔离会阻止将 Docker Engine socket 绑定挂载到容器中（例如，`docker run -v /var/run/docker.sock:/var/run/docker.sock ...`）。这允许您以受控方式放宽此限制。有关更多信息，请参阅 [ECI 配置](../enhanced-container-isolation/config.md)。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `imageList` |  | 指示允许绑定挂载 Docker Engine socket 的容器镜像。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `commandList` |  | 限制容器可以通过绑定挂载的 Docker Engine socket 发出的命令。 |  |
