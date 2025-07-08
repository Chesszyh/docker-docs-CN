---
title: "接口: Toast"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Toast/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Toast/
---

Toast 向用户提供简短通知。
它们暂时出现，不应中断用户体验。
它们也不需要用户输入即可消失。

**`自`**

0.2.0

## 方法

### success

▸ **success**(`msg`): `void`

显示成功类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.success("message");
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在 toast 中显示的消息。 |

#### 返回值

`void`

___

### warning

▸ **warning**(`msg`): `void`

显示警告类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.warning("message");
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在警告中显示的消息。 |

#### 返回值

`void`

___

### error

▸ **error**(`msg`): `void`

显示错误类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.error("message");
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在 toast 中显示的消息。 |

#### 返回值

`void`
