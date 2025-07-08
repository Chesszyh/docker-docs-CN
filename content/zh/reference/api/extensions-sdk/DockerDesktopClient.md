---
title: "接口: DockerDesktopClient"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/DockerDesktopClient/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/DockerDesktopClient/
---

Docker Desktop API 客户端的 v0 和 v1 接口的合并，出于向后兼容性原因提供。除非您正在使用旧版扩展，否则请改用 v1 类型。

## 属性

### backend

• `只读` **backend**: `undefined` \| [`BackendV0`](BackendV0.md)

`window.ddClient.backend` 对象可用于与扩展元数据 vm 部分中定义的后端通信。
客户端已连接到后端。

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [extension](DockerDesktopClient.md#extension)。

#### 继承自

DockerDesktopClientV0.backend

___

### extension

• `只读` **extension**: [`Extension`](Extension.md)

`ddClient.extension` 对象可用于与扩展元数据 vm 部分中定义的后端通信。
客户端已连接到后端。

#### 继承自

DockerDesktopClientV1.extension

___

### desktopUI

• `只读` **desktopUI**: [`DesktopUI`](DesktopUI.md)

#### 继承自

DockerDesktopClientV1.desktopUI

___

### host

• `只读` **host**: [`Host`](Host.md)

#### 继承自

DockerDesktopClientV1.host

___

### docker

• `只读` **docker**: [`Docker`](Docker.md)

#### 继承自

DockerDesktopClientV1.docker

## 容器方法

### listContainers

▸ **listContainers**(`options`): `Promise`<`unknown`\>

获取正在运行的容器列表（与 `docker ps` 相同）。

默认情况下，这不会列出已停止的容器。
您可以使用选项 `{"all": true}` 列出所有正在运行和已停止的容器。

```typescript
const containers = await window.ddClient.listContainers();
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [listContainers](Docker.md#listcontainers)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options` | `never` | （可选）。一个 JSON 对象，例如 `{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }`。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#operation/ContainerList)。 |

#### 返回值

`Promise`<`unknown`\>

#### 继承自

DockerDesktopClientV0.listContainers

___

## 镜像方法

### listImages

▸ **listImages**(`options`): `Promise`<`unknown`\>

获取镜像列表

```typescript
const images = await window.ddClient.listImages();
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [listImages](Docker.md#listimages)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options` | `never` | （可选）。一个 JSON 对象，例如 `{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true }`。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#tag/Image)。 |

#### 返回值

`Promise`<`unknown`\>

#### 继承自

DockerDesktopClientV0.listImages

___

## 导航方法

### navigateToContainers

▸ **navigateToContainers**(): `void`

导航到 Docker Desktop 中的容器窗口。
```typescript
window.ddClient.navigateToContainers();
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [viewContainers](NavigationIntents.md#viewcontainers)。

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToContainers

___

### navigateToContainer

▸ **navigateToContainer**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器窗口。
```typescript
await window.ddClient.navigateToContainer(id);
```

> [!WARNING]
>
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 失败。

#### 继承自

DockerDesktopClientV0.navigateToContainer

___

### navigateToContainerLogs

▸ **navigateToContainerLogs**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器日志窗口。
```typescript
await window.ddClient.navigateToContainerLogs(id);
```

> [!WARNING]
>
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerLogs

___

### navigateToContainerInspect

▸ **navigateToContainerInspect**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器检查窗口。
```typescript
await window.ddClient.navigateToContainerInspect(id);
```

> [!WARNING]
>
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerInspect

___

### navigateToContainerStats

▸ **navigateToContainerStats**(`id`): `Promise`<`any`\>

导航到容器统计信息以查看 CPU、内存、磁盘读/写和网络 I/O 使用情况。

```typescript
await window.ddClient.navigateToContainerStats(id);
```

> [!WARNING]
>
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerStats

___

### navigateToImages

▸ **navigateToImages**(): `void`

导航到 Docker Desktop 中的镜像窗口。
```typescript
await window.ddClient.navigateToImages(id);
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [viewImages](NavigationIntents.md#viewimages)。

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToImages

___

### navigateToImage

▸ **navigateToImage**(`id`, `tag`): `Promise`<`any`\>

导航到 Docker Desktop 中由 `id` 和 `tag` 引用的特定镜像。
在此导航路由中，您可以找到镜像层、命令、创建时间和大小。

```typescript
await window.ddClient.navigateToImage(id, tag);
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [viewImage](NavigationIntents.md#viewimage)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的镜像 ID（包括 sha），例如 `sha256:34ab3ae068572f4e85c448b4035e6be5e19cc41f69606535cd4d768a63432673`。 |
| `tag` | `string` | 镜像的标签，例如 `latest`、`0.0.1` 等。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 失败。

#### 继承自

DockerDesktopClientV0.navigateToImage

___

### navigateToVolumes

▸ **navigateToVolumes**(): `void`

导航到 Docker Desktop 中的卷窗口。

```typescript
await window.ddClient.navigateToVolumes();
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [viewVolumes](NavigationIntents.md#viewvolumes)。

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToVolumes

___

### navigateToVolume

▸ **navigateToVolume**(`volume`): `void`

导航到 Docker Desktop 中的特定卷。

```typescript
window.ddClient.navigateToVolume(volume);
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [viewVolume](NavigationIntents.md#viewvolume)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `volume` | `string` | 卷的名称，例如 `my-volume`。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToVolume

___

## 其他方法

### execHostCmd

▸ **execHostCmd**(`cmd`): `Promise`<[`ExecResultV0`](ExecResultV0.md)\>

您可以在扩展元数据的主机部分中运行定义的二进制文件。

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
 console.log(cmdResult);
});
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [exec](ExtensionCli.md#exec)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |

#### 返回值

`Promise`<[`ExecResultV0`](ExecResultV0.md)\>

#### 继承自

DockerDesktopClientV0.execHostCmd

___

### spawnHostCmd

▸ **spawnHostCmd**(`cmd`, `args`, `callback`): `void`

在您的主机上调用扩展二进制文件并获取输出流。

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // 一旦命令退出，我们就会得到状态码
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [exec](ExtensionCli.md#exec)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |
| `args` | `string`[] | 要执行的命令的参数。 |
| `callback` | (`data`: `any`, `error`: `any`) => `void` | 用于侦听命令输出数据和错误的 callback 函数。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.spawnHostCmd

___

### execDockerCmd

▸ **execDockerCmd**(`cmd`, `...args`): `Promise`<[`ExecResultV0`](ExecResultV0.md)\>

您也可以直接执行 Docker 二进制文件。

```typescript
const output = await window.ddClient.execDockerCmd("info");
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [exec](DockerCommand.md#exec)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |
| `...args` | `string`[] | 要执行的命令的参数。 |

#### 返回值

`Promise`<[`ExecResultV0`](ExecResultV0.md)\>

结果将包含执行命令的标准输出和标准错误：
```json
{
  "stderr": "...",
  "stdout": "..."
}
```
为方便起见，命令结果对象还具有根据输出格式轻松解析它的方法：

- `output.lines(): string[]` 分割输出行。
- `output.parseJsonObject(): any` 解析格式良好的 JSON 输出。
- `output.parseJsonLines(): any[]` 将每行输出解析为 JSON 对象。

如果命令输出过长，或者您需要以流形式获取输出，则可以使用
 * spawnDockerCmd 函数：

```typescript
window.ddClient.spawnDockerCmd("logs", ["-f", "..."], (data, error) => {
  console.log(data.stdout);
});
```

#### 继承自

DockerDesktopClientV0.execDockerCmd

___

### spawnDockerCmd

▸ **spawnDockerCmd**(`cmd`, `args`, `callback`): `void`

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [exec](DockerCommand.md#exec)。

#### 参数

| 名称 | 类型 |
| :------ | :------ |
| `cmd` | `string` |
| `args` | `string`[] |
| `callback` | (`data`: `any`, `error`: `any`) => `void` |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.spawnDockerCmd

___

### openExternal

▸ **openExternal**(`url`): `void`

使用系统默认浏览器打开外部 URL。

```typescript
window.ddClient.openExternal("https://docker.com");
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [openExternal](Host.md#openexternal)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 浏览器打开的 URL（必须包含协议 `http` 或 `https`）。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.openExternal

___

## Toast 方法

### toastSuccess

▸ **toastSuccess**(`msg`): `void`

显示成功类型的 toast 消息。

```typescript
window.ddClient.toastSuccess("message");
```

>**警告`**
>
> 它将在未来的版本中移除。请改用 [success](Toast.md#success)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在 toast 中显示的消息。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.toastSuccess

___

### toastWarning

▸ **toastWarning**(`msg`): `void`

显示警告类型的 toast 消息。

```typescript
window.ddClient.toastWarning("message");
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [warning](Toast.md#warning)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在 toast 中显示的消息。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.toastWarning

___

### toastError

▸ **toastError**(`msg`): `void`

显示错误类型的 toast 消息。

```typescript
window.ddClient.toastError("message");
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [error](Toast.md#error)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在 toast 中显示的消息。 |

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.toastError
