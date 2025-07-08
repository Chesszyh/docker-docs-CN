---
title: "接口: NavigationIntents"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/NavigationIntents/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/NavigationIntents/
---

**`自`**

0.2.0

## 容器方法

### viewContainers

▸ **viewContainers**(): `Promise`<`void`\>

导航到 Docker Desktop 中的**容器**选项卡。

```typescript
ddClient.desktopUI.navigate.viewContainers()
```

#### 返回值

`Promise`<`void`\>

___

### viewContainer

▸ **viewContainer**(`id`): `Promise`<`void`\>

导航到 Docker Desktop 中的**容器**选项卡。

```typescript
await ddClient.desktopUI.navigate.viewContainer(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，则 Promise 失败。

___

### viewContainerLogs

▸ **viewContainerLogs**(`id`): `Promise`<`void`\>

导航到 Docker Desktop 中的**容器日志**选项卡。

```typescript
await ddClient.desktopUI.navigate.viewContainerLogs(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，则 Promise 失败。

___

### viewContainerInspect

▸ **viewContainerInspect**(`id`): `Promise`<`void`\>

导航到 Docker Desktop 中的**检查容器**视图。

```typescript
await ddClient.desktopUI.navigate.viewContainerInspect(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，则 Promise 失败。

___

### viewContainerTerminal

▸ **viewContainerTerminal**(`id`): `Promise`<`void`\>

导航到 Docker Desktop 中的容器终端窗口。

```typescript
await ddClient.desktopUI.navigate.viewContainerTerminal(id)
```

**`自`**

0.3.4

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，则 Promise 失败。

___

### viewContainerStats

▸ **viewContainerStats**(`id`): `Promise`<`void`\>

导航到容器统计信息以查看 CPU、内存、磁盘读/写和网络 I/O 使用情况。

```typescript
await ddClient.desktopUI.navigate.viewContainerStats(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，则 Promise 失败。

___

## 镜像方法

### viewImages

▸ **viewImages**(): `Promise`<`void`\>

导航到 Docker Desktop 中的**镜像**选项卡。

```typescript
await ddClient.desktopUI.navigate.viewImages()
```

#### 返回值

`Promise`<`void`\>

___

### viewImage

▸ **viewImage**(`id`, `tag`): `Promise`<`void`\>

导航到 Docker Desktop 中由 `id` 和 `tag` 引用的特定镜像。
在此导航路由中，您可以找到镜像层、命令、创建时间和大小。

```typescript
await ddClient.desktopUI.navigate.viewImage(id, tag)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的镜像 ID（包括 sha），例如 `sha256:34ab3ae068572f4e85c448b4035e6be5e19cc41f69606535cd4d768a63432673`。 |
| `tag` | `string` | 镜像的标签，例如 `latest`、`0.0.1` 等。 |

#### 返回值

`Promise`<`void`\>

如果镜像不存在，则 Promise 失败。

___

## 卷方法

### viewVolumes

▸ **viewVolumes**(): `Promise`<`void`\>

导航到 Docker Desktop 中的**卷**选项卡。

```typescript
ddClient.desktopUI.navigate.viewVolumes()
```

#### 返回值

`Promise`<`void`\>

___

### viewVolume

▸ **viewVolume**(`volume`): `Promise`<`void`\>

导航到 Docker Desktop 中的特定卷。

```typescript
await ddClient.desktopUI.navigate.viewVolume(volume)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `volume` | `string` | 卷的名称，例如 `my-volume`。 |

#### 返回值

`Promise`<`void`\>
