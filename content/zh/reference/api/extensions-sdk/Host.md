---
title: "接口: Host"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Host/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Host/
---

**`起始版本`**

0.2.0

## 方法

### openExternal

▸ **openExternal**(`url`): `void`

使用系统默认浏览器打开外部 URL。

**`起始版本`**

0.2.0

```typescript
ddClient.host.openExternal("https://docker.com");
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 浏览器将打开的 URL（必须使用 `http` 或 `https` 协议）。 |

#### 返回值

`void`

## 属性

### platform

• **platform**: `string`

返回标识操作系统平台的字符串。请参阅 https://nodejs.org/api/os.html#osplatform

**`起始版本`**

0.2.2

___

### arch

• **arch**: `string`

返回操作系统 CPU 架构。请参阅 https://nodejs.org/api/os.html#osarch

**`起始版本`**

0.2.2

___

### hostname

• **hostname**: `string`

返回操作系统的主机名。请参阅 https://nodejs.org/api/os.html#oshostname

**`起始版本`**

0.2.2
