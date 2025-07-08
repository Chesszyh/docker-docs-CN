---
title: "接口: HttpService"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/HttpService/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/HttpService/
---

**`自`**

0.2.0

## 方法

### get

▸ **get**(`url`): `Promise`<`unknown`\>

向后端服务执行 HTTP GET 请求。

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

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
ddClient.extension.vm.service
 .post("/some/service", { ... })
 .then((value: any) => console.log(value));
```

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
ddClient.extension.vm.service
 .put("/some/service", { ... })
 .then((value: any) => console.log(value));
```

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
ddClient.extension.vm.service
 .patch("/some/service", { ... })
 .then((value: any) => console.log(value));
```

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
ddClient.extension.vm.service
 .delete("/some/service")
 .then((value: any) => console.log(value));
```

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
ddClient.extension.vm.service
 .head("/some/service")
 .then((value: any) => console.log(value));
```

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
ddClient.extension.vm.service
 .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
 .then((value: any) => console.log(value));
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `config` | [`RequestConfig`](RequestConfig.md) | 后端服务的 URL。 |

#### 返回值

`Promise`<`unknown`\>
