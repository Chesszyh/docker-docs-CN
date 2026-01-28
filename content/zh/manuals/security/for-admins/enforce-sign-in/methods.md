---
description: 了解强制开发者登录 Docker Desktop 的不同方法
keywords: authentication, registry.json, configure, enforce sign-in, docker desktop, security, .plist. registry key, mac, windows
title: 强制 Docker Desktop 登录的方法
tags: [admin]
linkTitle: 方法
---

{{< summary-bar feature_name="Enforce sign-in" >}}

本页概述了强制 Docker Desktop 登录的不同方法。

## 注册表键方法（仅限 Windows）

> [!NOTE]
>
> 注册表键方法适用于 Docker Desktop 4.32 及更高版本。

要在 Windows 上强制 Docker Desktop 登录，您可以配置一个注册表键来指定组织的允许用户。以下步骤指导您创建和部署注册表键以强制执行此策略：

1. 创建注册表键。您的新键应如下所示：

   ```console
   $ HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop
   ```
2. 创建一个多字符串值 `allowedOrgs`。
   > [!IMPORTANT]
   >
   > 从 Docker Desktop 4.36 及更高版本开始，您可以添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。
3. 使用您组织的名称（全部小写）作为字符串数据。如果添加多个组织，请确保每个组织单独一行。不要使用空格或逗号等其他分隔符。
4. 重新启动 Docker Desktop。
5. 当 Docker Desktop 重新启动时，验证是否出现 **Sign in required!** 提示。

在某些情况下，可能需要重新启动系统才能使强制生效。

> [!NOTE]
>
> 如果注册表键和 `registry.json` 文件同时存在，注册表键优先。

### 通过组策略部署示例

以下示例概述了如何使用组策略部署注册表键以强制 Docker Desktop 登录。根据您组织的基础设施、安全策略和管理工具，有多种方法可以部署此配置。

1. 创建注册表脚本。编写一个脚本来创建 `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop` 键，添加 `allowedOrgs` 多字符串，然后将值设置为您组织的名称。
2. 在组策略中，创建或编辑一个应用于您要定位的计算机或用户的组策略对象（GPO）。
3. 在 GPO 中，导航到 **Computer Configuration** 并选择 **Preferences**。
4. 选择 **Windows Settings**，然后选择 **Registry**。
5. 要添加注册表项，右键单击 **Registry** 节点，选择 **New**，然后选择 **Registry Item**。
6. 配置新注册表项以匹配您创建的注册表脚本，将操作指定为 **Update**。确保输入正确的路径、值名称（`allowedOrgs`）和值数据（您的组织名称）。
7. 将 GPO 链接到包含您要应用此设置的计算机的组织单位（OU）。
8. 首先在一小组计算机上测试 GPO，以确保其按预期运行。您可以在测试计算机上使用 `gpupdate /force` 命令手动刷新其组策略设置，并检查注册表以确认更改。
9. 验证后，您可以继续进行更广泛的部署。监控部署以确保设置在组织的计算机上正确应用。

## 配置描述文件方法（仅限 Mac）

{{< summary-bar feature_name="Config profiles" >}}

配置描述文件是 macOS 的一项功能，可让您向管理的 Mac 分发配置信息。这是在 macOS 上强制登录的最安全方法，因为已安装的配置描述文件受 Apple 系统完整性保护（SIP）保护，因此用户无法篡改。

1. 将以下 XML 文件保存为扩展名为 `.mobileconfig` 的文件，例如 `docker.mobileconfig`：

   ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>PayloadContent</key>
        <array>
          <dict>
            <key>PayloadType</key>
            <string>com.docker.config</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>PayloadIdentifier</key>
            <string>com.docker.config</string>
            <key>PayloadUUID</key>
            <string>eed295b0-a650-40b0-9dda-90efb12be3c7</string>
            <key>PayloadDisplayName</key>
            <string>Docker Desktop Configuration</string>
            <key>PayloadDescription</key>
            <string>Configuration profile to manage Docker Desktop settings.</string>
            <key>PayloadOrganization</key>
            <string>Your Company Name</string>
            <key>allowedOrgs</key>
            <string>first_org;second_org</string>
          </dict>
        </array>
        <key>PayloadType</key>
        <string>Configuration</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
        <key>PayloadIdentifier</key>
        <string>com.yourcompany.docker.config</string>
        <key>PayloadUUID</key>
        <string>0deedb64-7dc9-46e5-b6bf-69d64a9561ce</string>
        <key>PayloadDisplayName</key>
        <string>Docker Desktop Config Profile</string>
        <key>PayloadDescription</key>
        <string>Config profile to enforce Docker Desktop settings for allowed organizations.</string>
        <key>PayloadOrganization</key>
        <string>Your Company Name</string>
      </dict>
    </plist>
   ```

2. 将占位符 `com.yourcompany.docker.config` 和 `Your Company Name` 更改为您公司的名称。

3. 添加您的组织名称。允许的组织名称存储在 `allowedOrgs` 属性中。它可以包含单个组织的名称或以分号分隔的组织名称列表：

   ```xml
            <key>allowedOrgs</key>
            <string>first_org;second_org</string>
   ```

4. 使用 MDM 解决方案将修改后的 `.mobileconfig` 文件分发到您的 macOS 客户端。

5. 验证配置描述文件已添加到 macOS 客户端的 **Device (Managed)** 描述文件列表中（**System Settings** > **General** > **Device Management**）。

## plist 方法（仅限 Mac）

> [!NOTE]
>
> `plist` 方法适用于 Docker Desktop 4.32 及更高版本。

要在 macOS 上强制 Docker Desktop 登录，您可以使用定义所需设置的 `plist` 文件。以下步骤指导您完成创建和部署必要的 `plist` 文件以强制执行此策略的过程：

1. 创建文件 `/Library/Application Support/com.docker.docker/desktop.plist`。
2. 在文本编辑器中打开 `desktop.plist` 并添加以下内容，其中 `myorg` 替换为您组织的名称（全部小写）：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
     <dict>
	     <key>allowedOrgs</key>
	     <array>
             <string>myorg1</string>
             <string>myorg2</string>
         </array>
     </dict>
   </plist>
   ```
   > [!IMPORTANT]
   >
   > 从 Docker Desktop 4.36 及更高版本开始，您可以添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

3. 修改文件权限以确保任何非管理员用户都无法编辑该文件。
4. 重新启动 Docker Desktop。
5. 当 Docker Desktop 重新启动时，验证是否出现 **Sign in required!** 提示。

> [!NOTE]
>
> 如果 `plist` 和 `registry.json` 文件同时存在，`plist` 文件优先。

### 部署示例

以下示例概述了如何创建和分发 `plist` 文件以强制 Docker Desktop 登录。根据您组织的基础设施、安全策略和管理工具，有多种方法可以部署此配置。

{{< tabs >}}
{{< tab name="MDM" >}}

1. 按照之前概述的步骤创建 `desktop.plist` 文件。
2. 使用 Jamf 或 Fleet 等 MDM 工具将 `desktop.plist` 文件分发到目标 macOS 设备的 `/Library/Application Support/com.docker.docker/`。
3. 通过 MDM 工具，将文件权限设置为仅允许管理员编辑。

{{< /tab >}}
{{< tab name="Shell script" >}}

1. 创建一个 Bash 脚本，可以检查正确目录中是否存在 `.plist` 文件，根据需要创建或修改它，并设置适当的权限。
   在脚本中包含命令以：
    - 导航到 `/Library/Application Support/com.docker.docker/` 目录，如果不存在则创建它。
    - 使用 `defaults` 命令将所需的键和值写入 `desktop.plist` 文件。例如：
       ```console
       $ defaults write /Library/Application\ Support/com.docker.docker/desktop.plist allowedOrgs -string "myorg"
       ```
    - 使用 `chmod` 更改 `plist` 文件的权限以限制编辑，可能还需要使用 `chown` 将所有者设置为 root 或其他管理员账户，确保未经授权的用户无法轻易修改它。
2. 在将脚本部署到整个组织之前，在本地 macOS 计算机上测试它以确保其按预期运行。注意目录路径、权限和 `plist` 设置的成功应用。
3. 确保您有能力在 macOS 设备上远程执行脚本。这可能涉及设置 SSH 访问或使用支持 macOS 的远程支持工具。
4. 使用适合您组织基础设施的远程脚本执行方法。选项包括：
    - SSH：如果目标计算机上启用了 SSH，您可以使用它远程执行脚本。此方法需要了解设备的 IP 地址和适当的凭据。
    - 远程支持工具：对于使用远程支持工具的组织，您可以将脚本添加到任务中并在所有选定的计算机上执行。
5. 确保脚本在所有目标设备上按预期运行。您可能需要检查日志文件或在脚本本身中实现日志记录以报告其成功或失败。

{{< /tab >}}
{{< /tabs >}}

## registry.json 方法（全平台）

以下说明解释了如何创建 `registry.json` 文件并将其部署到单个设备。有多种方法可以部署 `registry.json` 文件。您可以按照 `.plist` 文件部分中概述的示例部署进行操作。您选择的方法取决于您组织的基础设施、安全策略和最终用户的管理权限。

### 选项 1：创建 registry.json 文件以强制登录

1. 确保用户是 Docker 中您组织的成员。有关更多详细信息，请参阅[管理成员](/admin/organization/members/)。
2. 创建 `registry.json` 文件。

    根据用户的操作系统，在以下位置创建名为 `registry.json` 的文件，并确保用户无法编辑该文件。

    | 平台 | 位置 |
    | --- | --- |
    | Windows | `/ProgramData/DockerDesktop/registry.json` |
    | Mac | `/Library/Application Support/com.docker.docker/registry.json` |
    | Linux | `/usr/share/docker-desktop/registry/registry.json` |

3. 在 `registry.json` 文件中指定您的组织。

    在文本编辑器中打开 `registry.json` 文件并添加以下内容，其中 `myorg` 替换为您组织的名称。文件内容区分大小写，您必须使用小写字母表示组织名称。


    ```json
    {
    "allowedOrgs": ["myorg1", "myorg2"]
    }
    ```
   > [!IMPORTANT]
   >
   > 从 Docker Desktop 4.36 及更高版本开始，您可以添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

4. 验证登录是否被强制执行。

    要激活 `registry.json` 文件，请在用户的计算机上重新启动 Docker Desktop。当 Docker Desktop 启动时，验证是否出现 **Sign in required!** 提示。

    在某些情况下，可能需要重新启动系统才能使强制生效。

    > [!TIP]
    >
    > 如果您的用户在您强制登录后启动 Docker Desktop 时遇到问题，他们可能需要更新到最新版本。

### 选项 2：在安装 Docker Desktop 时创建 registry.json 文件

要在安装 Docker Desktop 时创建 `registry.json` 文件，请根据用户的操作系统使用以下说明。

{{< tabs >}}
{{< tab name="Windows" >}}

要在安装 Docker Desktop 时自动创建 `registry.json` 文件，请下载 `Docker Desktop Installer.exe` 并从包含 `Docker Desktop Installer.exe` 的目录运行以下命令之一。将 `myorg` 替换为您组织的名称。您必须使用小写字母表示组织名称。

如果使用 PowerShell：

```powershell
PS> Start-Process '.\Docker Desktop Installer.exe' -Wait 'install --allowed-org=myorg'
```

如果使用 Windows 命令提示符：

```console
C:\Users\Admin> "Docker Desktop Installer.exe" install --allowed-org=myorg
```
> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 及更高版本开始，您可以向单个 `registry.json` 文件添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

{{< /tab >}}
{{< tab name="Mac" >}}

要在安装 Docker Desktop 时自动创建 `registry.json` 文件，请下载 `Docker.dmg` 并从包含 `Docker.dmg` 的目录在终端中运行以下命令。将 `myorg` 替换为您组织的名称。您必须使用小写字母表示组织名称。

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install --allowed-org=myorg
$ sudo hdiutil detach /Volumes/Docker
```

{{< /tab >}}
{{< /tabs >}}

### 选项 3：使用命令行创建 registry.json 文件

要使用命令行创建 `registry.json`，请根据用户的操作系统使用以下说明。

{{< tabs >}}
{{< tab name="Windows" >}}

要使用 CLI 创建 `registry.json` 文件，请以管理员身份运行以下 PowerShell 命令，并将 `myorg` 替换为您组织的名称。文件内容区分大小写，您必须使用小写字母表示组织名称。

```powershell
PS>  Set-Content /ProgramData/DockerDesktop/registry.json '{"allowedOrgs":["myorg"]}'
```

这将在 `C:\ProgramData\DockerDesktop\registry.json` 创建 `registry.json` 文件，并包含用户所属的组织信息。确保用户无法编辑此文件，只有管理员可以：

```console
PS C:\ProgramData\DockerDesktop> Get-Acl .\registry.json


    Directory: C:\ProgramData\DockerDesktop


Path          Owner                  Access
----          -----                  ------
registry.json BUILTIN\Administrators NT AUTHORITY\SYSTEM Allow  FullControl...
```

> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 及更高版本开始，您可以向单个 `registry.json` 文件添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

{{< /tab >}}
{{< tab name="Mac" >}}

要使用 CLI 创建 `registry.json` 文件，请在终端中运行以下命令，并将 `myorg` 替换为您组织的名称。文件内容区分大小写，您必须使用小写字母表示组织名称。

```console
$ sudo mkdir -p "/Library/Application Support/com.docker.docker"
$ echo '{"allowedOrgs":["myorg"]}' | sudo tee "/Library/Application Support/com.docker.docker/registry.json"
```

这将在 `/Library/Application Support/com.docker.docker/registry.json` 创建（或更新，如果文件已存在）`registry.json` 文件，并包含用户所属的组织信息。确保文件具有预期的内容，并且用户无法编辑此文件，只有管理员可以。

验证文件内容是否包含正确的信息：

```console
$ sudo cat "/Library/Application Support/com.docker.docker/registry.json"
{"allowedOrgs":["myorg"]}
```

验证文件是否具有预期的权限（`-rw-r--r--`）和所有权（`root` 和 `admin`）：

```console
$ sudo ls -l "/Library/Application Support/com.docker.docker/registry.json"
-rw-r--r--  1 root  admin  26 Jul 27 22:01 /Library/Application Support/com.docker.docker/registry.json
```

> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 及更高版本开始，您可以向单个 `registry.json` 文件添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

{{< /tab >}}
{{< tab name="Linux" >}}

要使用 CLI 创建 `registry.json` 文件，请在终端中运行以下命令，并将 `myorg` 替换为您组织的名称。文件内容区分大小写，您必须使用小写字母表示组织名称。

```console
$ sudo mkdir -p /usr/share/docker-desktop/registry
$ echo '{"allowedOrgs":["myorg"]}' | sudo tee /usr/share/docker-desktop/registry/registry.json
```

这将在 `/usr/share/docker-desktop/registry/registry.json` 创建（或更新，如果文件已存在）`registry.json` 文件，并包含用户所属的组织信息。确保文件具有预期的内容，并且用户无法编辑此文件，只有 root 可以。

验证文件内容是否包含正确的信息：

```console
$ sudo cat /usr/share/docker-desktop/registry/registry.json
{"allowedOrgs":["myorg"]}
```

验证文件是否具有预期的权限（`-rw-r--r--`）和所有权（`root`）：

```console
$ sudo ls -l /usr/share/docker-desktop/registry/registry.json
-rw-r--r--  1 root  root  26 Jul 27 22:01 /usr/share/docker-desktop/registry/registry.json
```

> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 及更高版本开始，您可以向单个 `registry.json` 文件添加多个组织。在 Docker Desktop 4.35 及更早版本中，如果添加多个组织，登录强制会静默失败。

{{< /tab >}}
{{< /tabs >}}

## 更多资源

- [视频：使用 registry.json 强制登录](https://www.youtube.com/watch?v=CIOQ6wDnJnM)
