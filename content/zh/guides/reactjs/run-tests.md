---
title: 在容器中运行 React.js 测试
linkTitle: 运行你的测试
weight: 40
keywords: react.js, react, test, vitest
description: 了解如何在容器中运行你的 React.js 测试。

---

## 先决条件

完成本指南的所有前几节，从 [容器化 React.js 应用程序](containerize.md) 开始。

## 概述

测试是开发过程中的关键部分。在本节中，你将学习如何：

- 在 Docker 容器内使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离、可重现的环境中运行测试。

你将使用 [Vitest](https://vitest.dev) —— 一个专为 Vite 设计的极速测试运行器 —— 以及用于断言的 [Testing Library](https://testing-library.com/)。

---

## 在开发期间运行测试

`docker-reactjs-sample` 应用程序在以下位置包含一个示例测试文件：

```console
$ src/App.test.tsx
```

此文件使用 Vitest 和 React Testing Library 来验证 `App` 组件的行为。

### 第一步：安装 Vitest 和 React Testing Library

如果你尚未添加必要的测试工具，请通过运行以下命令安装它们：

```console
$ npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

然后，更新 `package.json` 文件的脚本部分以包含以下内容：

```json
"scripts": {
  "test": "vitest run"
}
```

---

### 第二步：配置 Vitest

使用以下配置更新项目根目录中的 `vitest.config.ts` 文件：

```ts {hl_lines="14-18",linenos=true}
/// <reference types="vitest" />

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/",
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
    globals: true,
  },
});
```

> [!NOTE]
> `vitest.config.ts` 中的 `test` 选项对于 Docker 内部的可靠测试至关重要：
> - `environment: "jsdom"` 模拟类似浏览器的环境以进行渲染和 DOM 交互。
> - `setupFiles: "./src/setupTests.ts"` 在每个测试文件之前加载全局配置或模拟（可选但推荐）。
> - `globals: true` 启用全局测试函数，如 `describe`、`it` 和 `expect`，而无需导入它们。
>
> 有关更多详细信息，请参阅官方 [Vitest 配置文档](https://vitest.dev/config/)。

### 第三步：更新 compose.yaml

在你的 `compose.yaml` 文件中添加一个名为 `react-test` 的新服务。此服务允许你在隔离的容器化环境中运行测试套件。

```yaml {hl_lines="22-26",linenos=true}
services:
  react-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - action: sync
          path: .
          target: /app

  react-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-reactjs-sample
    ports:
      - "8080:8080"

  react-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test"]

```

react-test 服务重用用于 [开发](develop.md) 的相同 `Dockerfile.dev`，并覆盖默认命令以使用 `npm run test` 运行测试。此设置确保了与你的本地开发配置匹配的一致测试环境。


完成前面的步骤后，你的项目目录应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 第四步：运行测试

要在容器内执行测试套件，请从项目根目录运行以下命令：

```console
$ docker compose run --rm react-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `react-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 在测试完成后自动移除容器 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令。

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，你学习了如何使用 Vitest 和 Docker Compose 在 Docker 容器内运行 React.js 应用程序的单元测试。

你完成了什么：
- 安装并配置了 Vitest 和 React Testing Library 用于测试 React 组件。
- 在 `compose.yaml` 中创建了 `react-test` 服务以隔离测试执行。
- 重用了开发 `Dockerfile.dev` 以确保开发和测试环境之间的一致性。
- 使用 `docker compose run --rm react-test` 在容器内运行测试。
- 确保了跨环境的可靠、可重复的测试，而不依赖于本地机器设置。

---

## 相关资源

探索官方参考和最佳实践以磨练你的 Docker 测试工作流程：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解配置 `compose.yaml` 中服务的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。
---

## 下一步

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 管道，以便在容器化环境中自动构建和测试 React.js 应用程序。这确保了你的代码在每次推送或拉取请求时都得到验证，从而保持开发工作流程的一致性和可靠性。
