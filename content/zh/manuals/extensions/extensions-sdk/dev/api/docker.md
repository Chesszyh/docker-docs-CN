---
title: Docker
description: Docker 扩展 API
keywords: Docker, extensions, sdk, API
aliases:
 - /desktop/extensions-sdk/dev/api/docker/
---

## Docker 对象

▸ **listContainers**(`options?`): `Promise`<`unknown`\>

获取容器列表：

```typescript
const containers = await ddClient.docker.listContainers();
```

▸ **listImages**(`options?`): `Promise`<`unknown`\>

获取本地容器镜像列表：

```typescript
const images = await ddClient.docker.listImages();
```

有关这些方法的详细信息，请参阅 [Docker API 参考](/reference/api/extensions-sdk/Docker.md)。

> 已弃用的 Docker 对象访问
>
> 以下方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
const containers = await window.ddClient.listContainers();

const images = await window.ddClient.listImages();
```

## Docker 命令

扩展也可以直接执行 `docker` 命令行。

▸ **exec**(`cmd`, `args`): `Promise`<[`ExecResult`](/reference/api/extensions-sdk/ExecResult.md)\>

```typescript
const result = await ddClient.docker.cli.exec("info", [
  "--format",
  '"{{ json . }}"',
]);
```

结果包含执行命令的标准输出和标准错误：

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

在此示例中，命令输出是 JSON。
为方便起见，命令结果对象还具有易于解析的方法：

- `result.lines(): string[]` 分割输出行。
- `result.parseJsonObject(): any` 解析格式良好的 json 输出。
- `result.parseJsonLines(): any[]` 将每个输出行解析为 json 对象。

▸ **exec**(`cmd`, `args`, `options`): `void`

上述命令流式输出执行 Docker 命令的结果。
如果您需要将输出作为流获取，或者命令的输出太长，这将很有用。

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    onOutput(data) {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error) {
      console.error(error);
    },
    onClose(exitCode) {
      console.log("onClose with exit code " + exitCode);
    },
    splitOutputLines: true,
  },
});
```

当您关闭 Docker Desktop 中的仪表板或退出扩展 UI 时，扩展创建的子进程会自动被终止（`SIGTERM`）。
如果需要，您还可以使用 `exec(streamOptions)` 调用的结果来终止（`SIGTERM`）该进程。

```typescript
const logListener = await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    // ...
  },
});

// when done listening to logs or before starting a new one, kill the process
logListener.close();
```

此 `exec(streamOptions)` API 也可用于监听 docker 事件：

```typescript
await ddClient.docker.cli.exec(
  "events",
  ["--format", "{{ json . }}", "--filter", "container=my-container"],
  {
    stream: {
      onOutput(data) {
        if (data.stdout) {
          const event = JSON.parse(data.stdout);
          console.log(event);
        } else {
          console.log(data.stderr);
        }
      },
      onClose(exitCode) {
        console.log("onClose with exit code " + exitCode);
      },
      splitOutputLines: true,
    },
  }
);
```

> [!NOTE]
>
>您不能在单个 `exec()` 调用中使用命令链（如 `docker kill $(docker ps -q)` 或在命令之间使用管道）。
>
> 您需要为每个命令调用 `exec()`，并在需要时解析结果以将参数传递给下一个命令。

有关这些方法的详细信息，请参阅 [Exec API 参考](/reference/api/extensions-sdk/Exec.md)。

> 已弃用的 Docker 命令执行
>
> 此方法已被弃用，将在未来版本中移除。请使用下面指定的方法。

```typescript
const output = await window.ddClient.execDockerCmd(
  "info",
  "--format",
  '"{{ json . }}"'
);

window.ddClient.spawnDockerCmd("logs", ["-f", "..."], (data, error) => {
  console.log(data.stdout);
});
```
