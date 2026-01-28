---
title: 在容器中运行 Node.js 测试
linkTitle: 运行你的测试
weight: 30
keywords: node.js, node, test
description: 学习如何在容器中运行 Node.js 测试。
aliases:
  - /language/nodejs/run-tests/
  - /guides/language/nodejs/run-tests/
---

## 前提条件

完成本指南之前的所有章节，从[容器化 Node.js 应用程序](containerize.md)开始。

## 概述

测试是现代软件开发的重要组成部分。对于不同的开发团队，测试可能意味着很多不同的事情。有单元测试、集成测试和端到端测试。在本指南中，你将了解如何在开发和构建时在 Docker 中运行单元测试。

## 本地开发时运行测试

示例应用程序已经有用于运行测试的 Jest 包，测试位于 `spec` 目录中。在本地开发时，你可以使用 Compose 来运行测试。

运行以下命令，在容器内从 `package.json` 文件运行测试脚本。

```console
$ docker compose run server npm run test
```

要了解更多关于该命令的信息，请参阅 [docker compose run](/reference/cli/docker/compose/run/)。

你应该会看到类似以下的输出。

```console
> docker-nodejs@1.0.0 test
> jest

 PASS  spec/routes/deleteItem.spec.js
 PASS  spec/routes/getItems.spec.js
 PASS  spec/routes/addItem.spec.js
 PASS  spec/routes/updateItem.spec.js
 PASS  spec/persistence/sqlite.spec.js
  ● Console

    console.log
      Using sqlite database at /tmp/todo.db

      at Database.log (src/persistence/sqlite.js:18:25)

    console.log
      Using sqlite database at /tmp/todo.db

      at Database.log (src/persistence/sqlite.js:18:25)

    console.log
      Using sqlite database at /tmp/todo.db

      at Database.log (src/persistence/sqlite.js:18:25)

    console.log
      Using sqlite database at /tmp/todo.db

      at Database.log (src/persistence/sqlite.js:18:25)

    console.log
      Using sqlite database at /tmp/todo.db

      at Database.log (src/persistence/sqlite.js:18:25)


Test Suites: 5 passed, 5 total
Tests:       9 passed, 9 total
Snapshots:   0 total
Time:        2.008 s
Ran all test suites.
```

## 构建时运行测试

要在构建时运行测试，你需要更新 Dockerfile 以添加新的测试阶段。

以下是更新后的 Dockerfile。

```dockerfile {hl_lines="27-35"}
# syntax=docker/dockerfile:1

ARG NODE_VERSION=18.0.0

FROM node:${NODE_VERSION}-alpine as base
WORKDIR /usr/src/app
EXPOSE 3000

FROM base as dev
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev
USER node
COPY . .
CMD npm run dev

FROM base as prod
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev
USER node
COPY . .
CMD node src/index.js

FROM base as test
ENV NODE_ENV test
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev
USER node
COPY . .
RUN npm run test
```

在测试阶段中，使用 `RUN` 而不是 `CMD` 来运行测试。原因是 `CMD` 指令在容器运行时执行，而 `RUN` 指令在镜像构建时执行，如果测试失败，构建也会失败。

运行以下命令，使用测试阶段作为目标构建新镜像并查看测试结果。包含 `--progress=plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，以及 `--target test` 以指向测试阶段。

```console
$ docker build -t node-docker-image-test --progress=plain --no-cache --target test .
```

你应该会看到包含以下内容的输出。

```console
...

#11 [test 3/3] RUN npm run test
#11 1.058
#11 1.058 > docker-nodejs@1.0.0 test
#11 1.058 > jest
#11 1.058
#11 3.765 PASS spec/routes/getItems.spec.js
#11 3.767 PASS spec/routes/deleteItem.spec.js
#11 3.783 PASS spec/routes/updateItem.spec.js
#11 3.806 PASS spec/routes/addItem.spec.js
#11 4.179 PASS spec/persistence/sqlite.spec.js
#11 4.207
#11 4.208 Test Suites: 5 passed, 5 total
#11 4.208 Tests:       9 passed, 9 total
#11 4.208 Snapshots:   0 total
#11 4.208 Time:        2.168 s
#11 4.208 Ran all test suites.
#11 4.265 npm notice
#11 4.265 npm notice New major version of npm available! 8.6.0 -> 9.8.1
#11 4.265 npm notice Changelog: <https://github.com/npm/cli/releases/tag/v9.8.1>
#11 4.265 npm notice Run `npm install -g npm@9.8.1` to update!
#11 4.266 npm notice
#11 DONE 4.3s

...
```

## 总结

在本节中，你学习了如何在本地开发时使用 Compose 运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [docker compose run](/reference/cli/docker/compose/run/)

## 下一步

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 流水线。
