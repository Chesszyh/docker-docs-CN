---
title: "接口: ExtensionVM"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
---

**`起始版本`**

0.2.0

## 属性

### cli

• `Readonly` **cli**: [`ExtensionCli`](ExtensionCli.md)

在后端容器中执行命令。

示例：在后端容器内执行 `ls -l` 命令：

```typescript
await ddClient.extension.vm.cli.exec(
  "ls",
  ["-l"]
);
```

以流的形式输出在后端容器中执行的命令的输出。

当扩展使用包含多个容器的 `compose.yaml` 文件定义时，命令会在第一个定义的容器上执行。
更改容器的定义顺序可以在其他容器上执行命令。

示例：在后端容器内生成 `ls -l` 命令：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
           stream: {
             onOutput(data): void {
                 // 由于我们可以同时收到 `stdout` 和 `stderr`，我们将它们包装在 JSON 对象中
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```

**`参数`**

要执行的命令。

**`参数`**

要执行的命令的参数。

**`参数`**

用于监听命令输出数据和错误的回调函数。

___

### service

• `Optional` `Readonly` **service**: [`HttpService`](HttpService.md)
