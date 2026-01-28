---
description: 增强容器隔离 - 优势、使用原因、与 Docker rootless 的区别、适用人群
keywords: containers, rootless, security, sysbox, runtime
title: 什么是增强容器隔离？
linkTitle: 增强容器隔离
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/
weight: 20
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

增强容器隔离（Enhanced Container Isolation，ECI）提供了额外的安全层，以防止在容器中运行的恶意工作负载危害 Docker Desktop 或主机。

它使用各种先进技术来强化容器隔离，同时不影响开发人员的生产力。

增强容器隔离确保更强的容器隔离，并锁定管理员创建的任何安全配置，例如通过[镜像仓库访问管理策略](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)或[设置管理](../settings-management/_index.md)创建的配置。

> [!NOTE]
>
> ECI 是对 Docker 使用的其他容器安全技术的补充。例如，减少的 Linux Capabilities、seccomp 和 AppArmor。

## 适用人群

- 适用于希望防止容器攻击并减少开发人员环境中漏洞的组织和开发人员。
- 适用于希望确保更强容器隔离且易于在开发人员机器上直观实施的组织。

## 启用增强容器隔离后会发生什么？

启用增强容器隔离后，将启用以下功能和安全技术：

- 所有用户容器自动在 Linux 用户命名空间中运行，确保更强的隔离。每个容器在专用的 Linux 用户命名空间中运行。
- 容器中的 root 用户映射到 Docker Desktop Linux 虚拟机内的非特权用户。
- 容器更难被突破。例如，敏感的系统调用会被审查，`/proc` 和 `/sys` 的部分内容会在容器内被模拟。
- 用户可以继续像往常一样使用容器，包括绑定挂载主机目录、卷等。
- 开发人员运行容器的方式没有变化，不需要特殊的容器镜像。
- 特权容器（例如，`--privileged` 标志）可以工作，但它们仅在容器的 Linux 用户命名空间内具有特权，而不是在 Docker Desktop 虚拟机中。因此它们不能用于突破 Docker Desktop 虚拟机。
- Docker-in-Docker 甚至 Kubernetes-in-Docker 都可以工作，但在 Docker Desktop Linux 虚拟机内以非特权方式运行。

此外，还施加了以下限制：

- 容器不能再与 Docker Desktop 虚拟机共享命名空间（例如，`--network=host`、`--pid=host` 是不允许的）。
- 容器不能再修改 Docker Desktop 虚拟机内的配置文件（例如，将任何虚拟机目录挂载到容器中是不允许的）。
- 容器不能再访问 Docker Engine。例如，将 Docker Engine 的 socket 挂载到容器中是受限的，这可以防止恶意容器获得对 Docker Engine 的控制。管理员可以为[可信容器镜像](config.md)放宽此限制。
- 禁止所有用户对 Docker Desktop 虚拟机进行控制台访问。

这些功能和限制确保容器在运行时得到更好的保护，同时对开发人员体验和生产力的影响最小。开发人员可以继续像往常一样使用 Docker Desktop，但他们启动的容器隔离性更强。

有关增强容器隔离工作原理的更多信息，请参阅[工作原理](how-eci-works.md)。

> [!IMPORTANT]
>
> ECI 对 Docker 构建和 [Docker Desktop 中的 Kubernetes](/manuals/desktop/features/kubernetes.md) 的保护因 Docker Desktop 版本而异。较新版本比旧版本包含更多保护。此外，ECI 尚不保护扩展容器。有关已知限制和解决方法的更多信息，请参阅[常见问题](faq.md)。

## 如何启用增强容器隔离？

### 作为开发人员

要作为开发人员启用增强容器隔离：
1. 确保您的组织拥有 Docker Business 订阅。
2. 在 Docker Desktop 中登录您的组织。这将确保 ECI 功能在 Docker Desktop 的设置菜单中可用。
3. 停止并删除所有现有容器。
4. 在 Docker Desktop 中导航到 **Settings** > **General**。
5. 在 **Use Enhanced Container Isolation** 旁边，选中复选框。
6. 选择 **Apply and restart** 以保存设置。

> [!IMPORTANT]
>
> 增强容器隔离不保护在启用 ECI 之前创建的容器。有关已知限制和解决方法的更多信息，请参阅[常见问题](faq.md)。

### 作为管理员

#### 先决条件

您首先需要[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)，以确保所有 Docker Desktop 开发人员都使用您的组织进行身份验证。由于设置管理需要 Docker Business 订阅，强制登录可确保只有经过身份验证的用户才能访问，并且该功能在所有用户中始终生效，即使在没有强制登录的情况下它仍可能工作。

#### 设置

[创建并配置 `admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)并指定：

```json
{
  "configurationFileVersion": 2,
  "enhancedContainerIsolation": {
    "value": true,
    "locked": true
  }
}
```

设置 `"value": true` 确保默认启用 ECI。通过设置 `"locked": true`，开发人员无法禁用 ECI。如果您想让开发人员能够禁用该功能，请设置 `"locked": false`。

此外，您还可以[为容器配置 Docker socket 挂载权限](config.md)。

要使其生效：

- 在新安装中，开发人员需要启动 Docker Desktop 并向其组织进行身份验证。
- 在现有安装中，开发人员需要通过 Docker 菜单退出 Docker Desktop，然后重新启动 Docker Desktop。如果他们已经登录，则无需再次登录即可使更改生效。

> [!IMPORTANT]
>
> 从 Docker 菜单选择 **Restart** 是不够的，因为它只重启 Docker Desktop 的部分组件。

## 当管理员强制执行此设置时，用户会看到什么？

> [!TIP]
>
> 您现在也可以在 [Docker Admin Console](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md) 中配置这些设置。

启用增强容器隔离后，用户会看到：
- **Settings** > **General** 中的 **Use Enhanced Container Isolation** 已开启。
- 容器在 Linux 用户命名空间内运行。

要检查，请运行：

```console
$ docker run --rm alpine cat /proc/self/uid_map
```

显示以下输出：

```text
         0     100000      65536
```

这表明容器的 root 用户（0）映射到 Docker Desktop 虚拟机中的非特权用户（100000），并且映射范围扩展了 64K 个用户 ID。如果容器进程逃离容器，它会发现自己在虚拟机级别没有特权。用户 ID 映射随每个新容器而变化，因为每个容器获得一个独占的主机用户 ID 范围以进行隔离。用户 ID 映射由 Docker Desktop 自动管理。有关更多详情，请参阅[增强容器隔离的工作原理](how-eci-works.md)。

相比之下，没有 ECI 时，容器不使用 Linux 用户命名空间，显示如下：

```text
         0          0 4294967295
```

这意味着容器中的 root 用户（0）实际上是 Docker Desktop 虚拟机中的 root 用户（0），这降低了容器隔离性。

由于增强容器隔离[使用嵌入在 Docker Desktop Linux 虚拟机中的 Sysbox 容器运行时](how-eci-works.md)，另一种确定容器是否使用增强容器隔离运行的方法是使用 `docker inspect`：

```console
$ docker inspect --format='{{.HostConfig.Runtime}}' my_container
```

输出：

```text
sysbox-runc
```

没有增强容器隔离时，`docker inspect` 输出 `runc`，这是标准的 OCI 运行时。

## 更多资源

- [视频：增强容器隔离](https://www.youtube.com/watch?v=oA1WQZWnTAk)
