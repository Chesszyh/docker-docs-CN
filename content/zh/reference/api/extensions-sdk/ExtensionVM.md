---
title: "接口: ExtensionVM"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
---

**`自`**

0.2.0

## 属性

### cli

• `只读` **cli**: [`ExtensionCli`](ExtensionCli.md)

在后端容器中执行命令。

示例：在后端容器中执行命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec(
  "ls",
  ["-l"]
);
```

流式传输在后端容器中执行的命令的输出。

当扩展定义了自己的 `compose.yaml` 文件，其中包含多个容器时，命令将在定义的第一个容器上执行。
更改容器的定义顺序以在另一个容器上执行命令。

示例：在后端容器中生成命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
           stream: {
             onOutput(data): void {
                 // 由于我们可以同时接收 `stdout` 和 `stderr`，因此我们将它们包装在 JSON 对象中
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

用于侦听命令输出数据和错误的 callback 函数。

___

### service

• `可选` `只读` **service**: [`HttpService`](HttpService.md)
