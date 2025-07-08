---
title: "接口: BackendV0"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/BackendV0/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/BackendV0/
---

## 容器方法

### execInContainer

▸ **execInContainer**(`container`, `cmd`): `Promise`<[`ExecResultV0`](ExecResultV0.md)\>

在容器内执行命令。

```typescript
const output = await window.ddClient.backend.execInContainer(container, cmd);

console.log(output);
```

> [!WARNING]
>
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `container` | `string` | - |
| `cmd` | `string` | 要执行的命令。 |

#### 返回值

`Promise`<[`ExecResultV0`](ExecResultV0.md)\>

___

## HTTP 方法

### get

▸ **get**(`url`): `Promise`<`unknown`\>

向后端服务执行 HTTP GET 请求。

```typescript
window.ddClient.backend
 .get("/some/service")
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [get](HttpService.md#get)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |

#### 返回值

`Promise`<`unknown`\>

___

### post

▸ **post**(`url`, `data`): `Promise`<`unknown`\>

向后端服务执行 HTTP POST 请求。

```typescript
window.ddClient.backend
 .post("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [post](HttpService.md#post)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |
| `data` | `any` | 请求体。 |

#### 返回值

`Promise`<`unknown`\>

___

### put

▸ **put**(`url`, `data`): `Promise`<`unknown`\>

向后端服务执行 HTTP PUT 请求。

```typescript
window.ddClient.backend
 .put("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [put](HttpService.md#put)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |
| `data` | `any` | 请求体。 |

#### 返回值

`Promise`<`unknown`\>

___

### patch

▸ **patch**(`url`, `data`): `Promise`<`unknown`\>

向后端服务执行 HTTP PATCH 请求。

```typescript
window.ddClient.backend
 .patch("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [patch](HttpService.md#patch)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |
| `data` | `any` | 请求体。 |

#### 返回值

`Promise`<`unknown`\>

___

### delete

▸ **delete**(`url`): `Promise`<`unknown`\>

向后端服务执行 HTTP DELETE 请求。

```typescript
window.ddClient.backend
 .delete("/some/service")
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [delete](HttpService.md#delete)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |

#### 返回值

`Promise`<`unknown`\>

___

### head

▸ **head**(`url`): `Promise`<`unknown`\>

向后端服务执行 HTTP HEAD 请求。

```typescript
window.ddClient.backend
 .head("/some/service")
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [head](HttpService.md#head)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 后端服务的 URL。 |

#### 返回值

`Promise`<`unknown`\>

___

### request

▸ **request**(`config`): `Promise`<`unknown`\>

向后端服务执行 HTTP 请求。

```typescript
window.ddClient.backend
 .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
 .then((value: any) => console.log(value));
```

> [!WARNING]
>
> 它将在未来的版本中移除。请改用 [request](HttpService.md#request)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `config` | [`RequestConfigV0`](RequestConfigV0.md) | 后端服务的 URL。 |

#### 返回值

`Promise`<`unknown`\>

___

## VM 方法

### execInVMExtension

▸ **execInVMExtension**(`cmd`): `Promise`<[`ExecResultV0`](ExecResultV0.md)\>

在后端容器内执行命令。
如果您的扩展附带了应在后端容器内运行的其他二进制文件，则可以使用 `execInVMExtension` 函数。

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);

console.log(output);
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

___

### spawnInVMExtension

▸ **spawnInVMExtension**(`cmd`, `args`, `callback`): `void`

从后端容器中执行的命令返回流。

```typescript
window.ddClient.spawnInVMExtension(
  `cmd`,
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
> 它将在未来的版本中移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |
| `args` | `string`[] | 要执行的命令的参数。 |
| `callback` | (`data`: `any`, `error`: `any`) => `void` | 用于侦听命令输出数据和错误的 callback 函数。 |

#### 返回值

`void`
