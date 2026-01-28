---
title: "接口: NavigationIntents"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/NavigationIntents/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/NavigationIntents/
---

**`起始版本`**

0.2.0

## 容器方法

### viewContainers

▸ **viewContainers**(): `Promise`<`void`\>

在 Docker Desktop 中导航到**容器**标签页。

```typescript
ddClient.desktopUI.navigate.viewContainers()
```

#### 返回值

`Promise`<`void`\>

___

### viewContainer

▸ **viewContainer**(`id`): `Promise`<`void`\>

在 Docker Desktop 中导航到**容器**标签页。

```typescript
await ddClient.desktopUI.navigate.viewContainer(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 id，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 id。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，promise 将失败。

___

### viewContainerLogs

▸ **viewContainerLogs**(`id`): `Promise`<`void`\>

在 Docker Desktop 中导航到**容器日志**标签页。

```typescript
await ddClient.desktopUI.navigate.viewContainerLogs(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 id，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 id。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，promise 将失败。

___

### viewContainerInspect

▸ **viewContainerInspect**(`id`): `Promise`<`void`\>

在 Docker Desktop 中导航到**检查容器**视图。

```typescript
await ddClient.desktopUI.navigate.viewContainerInspect(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 id，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 id。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，promise 将失败。

___

### viewContainerTerminal

▸ **viewContainerTerminal**(`id`): `Promise`<`void`\>

在 Docker Desktop 中导航到容器终端窗口。

```typescript
await ddClient.desktopUI.navigate.viewContainerTerminal(id)
```

**`起始版本`**

0.3.4

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 id，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 id。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，promise 将失败。

___

### viewContainerStats

▸ **viewContainerStats**(`id`): `Promise`<`void`\>

导航到容器统计信息，查看 CPU、内存、磁盘读写和网络 I/O 使用情况。

```typescript
await ddClient.desktopUI.navigate.viewContainerStats(id)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 id，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。您可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 id。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，promise 将失败。

___

## 镜像方法

### viewImages

▸ **viewImages**(): `Promise`<`void`\>

在 Docker Desktop 中导航到**镜像**标签页。

```typescript
await ddClient.desktopUI.navigate.viewImages()
```

#### 返回值

`Promise`<`void`\>

___

### viewImage

▸ **viewImage**(`id`, `tag`): `Promise`<`void`\>

在 Docker Desktop 中导航到由 `id` 和 `tag` 引用的特定镜像。
在此导航路由中，您可以查看镜像层、命令、创建时间和大小。

```typescript
await ddClient.desktopUI.navigate.viewImage(id, tag)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的镜像 id（包含 sha），例如 `sha256:34ab3ae068572f4e85c448b4035e6be5e19cc41f69606535cd4d768a63432673`。 |
| `tag` | `string` | 镜像的标签，例如 `latest`、`0.0.1` 等。 |

#### 返回值

`Promise`<`void`\>

如果镜像不存在，promise 将失败。

___

## 卷方法

### viewVolumes

▸ **viewVolumes**(): `Promise`<`void`\>

在 Docker Desktop 中导航到**卷**标签页。

```typescript
ddClient.desktopUI.navigate.viewVolumes()
```

#### 返回值

`Promise`<`void`\>

___

### viewVolume

▸ **viewVolume**(`volume`): `Promise`<`void`\>

在 Docker Desktop 中导航到特定卷。

```typescript
await ddClient.desktopUI.navigate.viewVolume(volume)
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `volume` | `string` | 卷的名称，例如 `my-volume`。 |

#### 返回值

`Promise`<`void`\>
