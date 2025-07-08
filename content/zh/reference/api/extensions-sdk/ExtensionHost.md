---
title: "接口: ExtensionHost"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionHost/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionHost/
---

**`自`**

0.2.0

## 属性

### cli

• `只读` **cli**: [`ExtensionCli`](ExtensionCli.md)

在主机中执行命令。

例如，在主机中执行附带的二进制 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

---

流式传输在后端容器或主机中执行的命令的输出。

如果 `kubectl` 二进制文件作为扩展的一部分提供，您可以在主机中生成 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
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
