---
title: 仪表板
description: Docker 扩展 API
keywords: Docker, extensions, sdk, API
aliases:
 - /desktop/extensions-sdk/dev/api/dashboard/
---

## 用户通知

Toast（弹出通知）为用户提供简短的通知。它们是临时显示的，不应中断用户体验。它们也不需要用户输入即可消失。

### success

▸ **success**(`msg`): `void`

用于显示成功类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.success("message");
```

### warning

▸ **warning**(`msg`): `void`

用于显示警告类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.warning("message");
```

### error

▸ **error**(`msg`): `void`

用于显示错误类型的 toast 消息。

```typescript
ddClient.desktopUI.toast.error("message");
```

有关方法参数和可用返回类型的更多详细信息，请参阅 [Toast API 参考](/reference/api/extensions-sdk/Toast.md)。

> 已弃用的用户通知
>
> 这些方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
window.ddClient.toastSuccess("message");
window.ddClient.toastWarning("message");
window.ddClient.toastError("message");
```

## 打开文件选择对话框

此函数打开一个文件选择器对话框，要求用户选择文件或文件夹。

▸ **showOpenDialog**(`dialogProperties`): `Promise`<[`OpenDialogResult`](/reference/api/extensions-sdk/OpenDialogResult.md)\>:

`dialogProperties` 参数是传递给 Electron 以自定义对话框行为的标志列表。例如，您可以传递 `multiSelections` 以允许用户选择多个文件。有关完整列表，请参阅 [Electron 文档](https://www.electronjs.org/docs/latest/api/dialog)。

```typescript
const result = await ddClient.desktopUI.dialog.showOpenDialog({
  properties: ["openDirectory"],
});
if (!result.canceled) {
  console.log(result.paths);
}
```

## 打开 URL

此函数使用系统默认浏览器打开外部 URL。

▸ **openExternal**(`url`): `void`

```typescript
ddClient.host.openExternal("https://docker.com");
```

> URL 必须使用 `http` 或 `https` 协议。

有关方法参数和可用返回类型的更多详细信息，请参阅 [Desktop host API 参考](/reference/api/extensions-sdk/Host.md)。

> 已弃用的用户通知
>
> 此方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
window.ddClient.openExternal("https://docker.com");
```

## 导航到仪表板路由

从您的扩展中，您还可以[导航](dashboard-routes-navigation.md)到 Docker Desktop 仪表板的其他部分。
