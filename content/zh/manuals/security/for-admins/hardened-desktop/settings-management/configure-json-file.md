---
description: 如何为 Docker Desktop 配置设置管理
keywords: admin, 管理, 控制, rootless, 增强型容器隔离
title: 使用 JSON 文件配置设置管理
linkTitle: 使用 JSON 文件
weight: 10
alias:
 - /desktop/hardened-desktop/settings-management/configure/
 - /security/for-admins/hardened-desktop/settings-management/configure/
---

{{< summary-bar feature_name="强化版 Docker Desktop" >}}

本页介绍了如何使用 `admin-settings.json` 文件来配置并强制执行 Docker Desktop 设置。使用此方法可以在您的组织中标准化 Docker Desktop 环境。

## 前提条件

- [强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)以确保所有用户都使用您的组织身份进行身份验证。
- 需要 Docker Business 订阅。

只有在身份验证和 Docker Business 许可检查都成功的情况下，Docker Desktop 才会应用来自 `admin-settings.json` 文件的设置。

> [!IMPORTANT]
> 
> 如果用户未登录或不属于 Docker Business 组织，设置文件将被忽略。

## 限制

- `admin-settings.json` 文件在物理隔离（air-gapped）或离线环境中无法工作。
- 该文件与限制 Docker Hub 身份验证的环境不兼容。

## 第一步：创建设置文件

您可以：

- 使用 `--admin-settings` 安装程序标志自动生成文件。请参阅：
    - [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 安装指南
    - [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 安装指南
- 或手动创建文件并将其放置在以下位置：
    - Mac：`/Library/Application\ Support/com.docker.docker/admin-settings.json`
    - Windows：`C:\ProgramData\DockerDesktop\admin-settings.json`
    - Linux：`/usr/share/docker-desktop/admin-settings.json`

> [!IMPORTANT]
> 
> 请将文件放置在受保护的目录中以防止被修改。请使用像 [Jamf](https://www.jamf.com/lp/en-gb/apple-mobile-device-management-mdm-jamf-shared/?attr=google_ads-brand-search-shared&gclid=CjwKCAjw1ICZBhAzEiwAFfvFhEXjayUAi8FHHv1JJitFPb47C_q_RCySTmF86twF1qJc_6GST-YDmhoCuJsQAvD_BwE) 这样的 MDM 工具来进行大规模分发。

## 第二步：定义设置

> [!TIP]
> 
> 有关可用设置的完整列表、支持的平台以及它们适用的配置方法，请参阅[设置参考](settings-reference.md)。

`admin-settings.json` 文件使用结构化的键来定义可以配置的内容以及这些值是否被强制执行。

每个设置都支持 `locked` 字段。当 `locked` 设置为 `true` 时，用户无法在 Docker Desktop、CLI 或配置文件中更改该值。当 `locked` 设置为 `false` 时，该值仅作为默认建议，用户仍然可以更新它。

如果用户已经在 `settings-store.json`、`settings.json` 或 `daemon.json` 中自定义了该值，则在现有安装中会忽略 `locked` 设置为 `false` 的设置。

> [!NOTE]
> 
> 某些设置是特定于平台的，或者需要最低的 Docker Desktop 版本。详情请参阅[设置参考](/manuals/security/for-admins/hardened-desktop/settings-management/settings-reference.md)。

### 设置文件示例

以下是一个 `admin-settings.json` 文件示例。有关 `admin-settings.json` 文件可配置设置的完整列表，请参阅 [`admin-settings.json` 配置](#admin-settingsjson-配置)。

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

## 第三步：重新启动并应用设置

重新启动 Docker Desktop 且用户登录后，设置将生效。

- 新安装：启动 Docker Desktop 并登录。
- 现有安装：完全退出 Docker Desktop 并重新启动。

> [!IMPORTANT]
> 
> 仅从菜单中重新启动 Docker Desktop 是不够的。必须将其完全退出并重新打开。

## `admin-settings.json` 配置

### 常规 (General)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`configurationFileVersion`|   |指定配置文件格式的版本。|   |
|`analyticsEnabled`|  |如果 `value` 设置为 false，Docker Desktop 不会向 Docker 发送使用统计信息。|  |
|`disableUpdate`|  |如果 `value` 设置为 true，则禁用检查和通知 Docker Desktop 更新。|  |
|`extensionsEnabled`|  |如果 `value` 设置为 false，则禁用 Docker 扩展。|  |
| `blockDockerLoad` | | 如果 `value` 设置为 `true`，用户将无法运行 [`docker load`](/reference/cli/docker/image/load/)，如果尝试运行将收到错误提示。|  |
| `displayedOnboarding` |  | 如果 `value` 设置为 `true`，则不会向新用户显示新手引导调查。将 `value` 设置为 `false` 没有效果。| Docker Desktop 4.30 及更高版本 |
| `desktopTerminalEnabled` |  | 如果 `value` 设置为 `false`，开发人员将无法使用 Docker 终端与宿主机交互并直接从 Docker Desktop 执行命令。|  |
|`exposeDockerAPIOnTCP2375`| 仅限 Windows | 在指定端口上公开 Docker API。如果 `value` 设置为 true，Docker API 将在端口 2375 上公开。注意：这是未经身份验证的，仅应在受适当防火墙规则保护的情况下启用。|  |

### 文件共享和模拟 (File sharing and emulation)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
| `filesharingAllowedDirectories` |  | 指定您的开发人员可以将文件共享添加到的路径。还接受 `$HOME`、`$TMP` 或 `$TEMP` 作为 `path` 变量。添加路径后，其子目录也将被允许。如果 `sharedByDefault` 设置为 `true`，则在恢复出厂设置或 Docker Desktop 首次启动时将添加该路径。|  |
| `useVirtualizationFrameworkVirtioFS`| 仅限 macOS | 如果 `value` 设置为 `true`，则将 VirtioFS 设置为文件共享机制。注意：如果 `useVirtualizationFrameworkVirtioFS` 和 `useGrpcfuse` 的 `value` 都设置为 `true`，则 VirtioFS 优先。同样，如果两者都设置为 `false`，则将 osxfs 设置为文件共享机制。|  |
| `useGrpcfuse` | 仅限 macOS | 如果 `value` 设置为 `true`，则将 gRPC Fuse 设置为文件共享机制。|  |
| `useVirtualizationFrameworkRosetta`| 仅限 macOS | 如果 `value` 设置为 `true`，Docker Desktop 将开启 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制模拟。注意：这也会自动启用 `Use Virtualization framework`。| Docker Desktop 4.29 及更高版本 |

### Docker Scout

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`scout`| | 将 `useBackgroundIndexing` 设置为 `false` 会禁用对加载到镜像存储的镜像进行自动索引。将 `sbomIndexing` 设置为 `false` 会阻止用户通过在 Docker Desktop 中检查镜像或使用 `docker scout` CLI 命令来索引镜像。|  |

### 代理 (Proxy)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`proxy`|   |如果 `mode` 设置为 `system` 而不是 `manual`，Docker Desktop 将从系统获取代理值，并忽略为 `http`、`https` 和 `exclude` 设置的任何值。将 `mode` 更改为 `manual` 以手动配置代理服务器。如果代理端口是自定义的，请在 `http` 或 `https` 属性中指定，例如 `"https": "http://myotherproxy.com:4321"`。`exclude` 属性指定要绕过代理的主机和域名的逗号分隔列表。|  |
|&nbsp; &nbsp; &nbsp; &nbsp;`windowsDockerdPort`| 仅限 Windows | 在此端口上本地公开 Docker Desktop 的内部代理，供 Windows Docker 守护进程连接。如果设置为 0，则选择一个随机空闲端口。如果值大于 0，则使用该确切值作为端口。默认值为 -1，表示禁用此选项。|  |
|&nbsp; &nbsp; &nbsp; &nbsp;`enableKerberosNtlm`|  |设置为 `true` 时，启用 Kerberos 和 NTLM 身份验证。默认为 `false`。有关更多信息，请参阅设置文档。| Docker Desktop 4.32 及更高版本 |

### 容器代理 (Container proxy)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`containersProxy` | | 创建物理隔离容器。有关更多信息，请参阅[物理隔离容器](../air-gapped-containers.md)。| Docker Desktop 4.29 及更高版本 |

### Linux VM

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
| `linuxVM` |   |与 Linux VM 选项相关的参数和设置 - 为了方便起见在此分组。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`wslEngineEnabled`  | 仅限 Windows | 如果 `value` 设置为 true，Docker Desktop 将使用基于 WSL 2 的引擎。这会覆盖在安装时使用 `--backend=<backend name>` 标志设置的任何内容。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  |如果 `value` 设置为 true，它将覆盖 Docker Engine 配置文件中的选项。请参阅 [Docker Engine 参考](/reference/cli/dockerd/#daemon-configuration-file)。请注意，为了增加安全性，当启用增强型容器隔离时，可能会覆盖一些配置属性。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`vpnkitCIDR` |  |覆盖用于 `*.docker.internal` 的 vpnkit DHCP/DNS 的网络范围。|  |

### Windows 容器 (Windows containers)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
| `windowsContainers` |  | 与 `windowsContainers` 选项相关的参数和设置 - 为了方便起见在此分组。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  | 覆盖 Windows 守护进程配置文件中的选项。请参阅 [Docker Engine 参考](/reference/cli/dockerd/#daemon-configuration-file)。|  |

> [!NOTE]
> 
> 此设置无法通过 Docker 管理控制台进行配置。

### Kubernetes

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`kubernetes`|  | 如果 `enabled` 设置为 true，则在 Docker Desktop 启动时启动 Kubernetes 单节点集群。如果 `showSystemContainers` 设置为 true，则在 Docker Desktop 控制面板和运行 `docker ps` 时显示 Kubernetes 容器。`imagesRepository` 设置允许您指定 Docker Desktop 从哪个存储库拉取控制平面 Kubernetes 镜像。|  |

> [!NOTE]
> 
> 当使用 `imagesRepository` 设置和增强型容器隔离 (ECI) 时，请将以下镜像添加到 [ECI Docker 套接字挂载镜像列表](#增强型容器隔离)：
> 
> * [imagesRepository]/desktop-cloud-provider-kind:*
> * [imagesRepository]/desktop-containerd-registry-mirror:*
> 
> 这些容器会挂载 Docker 套接字，因此您必须将这些镜像添加到 ECI 镜像列表中。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

### 网络 (Networking)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
| `defaultNetworkingMode` | 仅限 Windows 和 Mac | 为新的 Docker 网络定义默认 IP 协议：`dual-stack`（IPv4 + IPv6，默认）、`ipv4only` 或 `ipv6only`。| Docker Desktop 4.43 及更高版本 |
| `dnsInhibition` | 仅限 Windows 和 Mac | 控制返回给容器的 DNS 记录过滤。选项：`auto`（推荐）、`ipv4`、`ipv6`、`none`| Docker Desktop 4.43 及更高版本 |

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### Beta 功能 (Beta features)

> [!IMPORTANT]
> 
> 对于 Docker Desktop 4.41 及更早版本，其中一些设置位于 **Features in development**（开发中功能）页面的 **Experimental features**（实验性功能）选项卡下。

| 参数                                            | 操作系统 | 说明                                                                                                                                                                                                                                               | 版本                                 |
|:-----------------------------------------------------|----|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `allowBetaFeatures`                                  |    | 如果 `value` 设置为 `true`，则启用 Beta 功能。|                                         |
| `enableDockerAI`                                     |    | 如果 `allowBetaFeatures` 为 true，则将 `enableDockerAI` 设置为 `true` 会默认启用 [Docker AI (Ask Gordon)](/manuals/ai/gordon/_index.md)。您可以独立于 `allowBetaFeatures` 设置来控制此设置。|                                         |
| `enableInference`                                    |    | 如果 `allowBetaFeatures` 为 true，则将 `enableInference` 设置为 `true` 会默认启用 [Docker Model Runner](/manuals/ai/model-runner/_index.md)。您可以独立于 `allowBetaFeatures` 设置来控制此设置。|                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceTCP`     |    | 启用宿主机侧 TCP 支持。此设置要求先启用 Docker Model Runner 设置。|                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceTCPPort` |    | 指定公开的 TCP 端口。此设置要求先启用 Docker Model Runner 设置。|                                         |
| &nbsp; &nbsp; &nbsp; &nbsp; `enableInferenceCORS`    |    | 指定允许的 CORS 源。空字符串表示拒绝所有，`*` 表示接受所有，或使用逗号分隔的值列表。此设置要求先启用 Docker Model Runner 设置。|                                         |
| `enableDockerMCPToolkit`                             |    | 如果 `allowBetaFeatures` 为 true，则将 `enableDockerMCPToolkit` 设置为 `true` 会默认启用 [MCP 工具包功能](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)。您可以独立于 `allowBetaFeatures` 设置来控制此设置。|                                         |
| `allowExperimentalFeatures`                          |    | 如果 `value` 设置为 `true`，则启用实验性功能。| Docker Desktop 4.41 及更早版本 |

### 增强型容器隔离 (Enhanced Container Isolation)

|参数|操作系统|说明|版本| 
|:-------------------------------|---|:-------------------------------|---|
|`enhancedContainerIsolation`|  | 如果 `value` 设置为 true，Docker Desktop 会通过 Linux 用户命名空间以无特权方式运行所有容器，防止它们修改 Docker Desktop VM 内部的敏感配置，并使用其他先进技术来隔离它们。有关更多信息，请参阅[增强型容器隔离](../enhanced-container-isolation/_index.md)。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerSocketMount` |  | 默认情况下，增强型容器隔离会阻止将 Docker Engine 套接字绑定挂载到容器中（例如 `docker run -v /var/run/docker.sock:/var/run/docker.sock ...`）。这允许您以受控方式放宽此限制。有关更多信息，请参阅 [ECI 配置](../enhanced-container-isolation/config.md)。|  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `imageList` |  | 指示允许将 Docker Engine 套接字绑定挂载到其中的容器镜像。|  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `commandList` |  | 限制容器可以通过绑定挂载的 Docker Engine 套接字发出的命令。|  |
