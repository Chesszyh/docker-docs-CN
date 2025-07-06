---
title: 在开发和测试中使用 WireMock 模拟 API 服务
description: &desc 在开发和测试中使用 WireMock 模拟 API 服务
keywords: WireMock, 容器支持的开发
linktitle: 使用 WireMock 模拟 API 服务
summary: *desc
tags: [app-dev, distributed-systems]
languages: [js]
params:
  time: 20 分钟
---

## 简介

在本地开发和测试期间，经常会遇到你的应用程序依赖于远程 API 的情况。网络问题、速率限制，甚至 API 提供商的停机都可能阻碍你的进度。这会严重影响你的工作效率，并使测试更具挑战性。这就是 WireMock 发挥作用的地方。

WireMock 是一个开源工具，可帮助开发人员创建模拟服务器，以模拟真实 API 的行为，从而为开发和测试提供一个受控的环境。

想象一下，你同时拥有一个 API 和一个前端应用程序，并且你想测试前端如何与 API 交互。使用 WireMock，你可以设置一个模拟服务器来模拟 API 的响应，从而让你可以在不依赖实际 API 的情况下测试前端行为。当 API 仍在开发中或当你想在不影响实际 API 的情况下测试不同场景时，这尤其有用。WireMock 支持 HTTP 和 HTTPS 协议，并可以模拟各种响应场景，包括延迟、错误和不同的 HTTP 状态代码。

在本指南中，你将学习如何：

- 使用 Docker 启动 WireMock 容器。
- 在本地开发中使用模拟数据，而无需依赖外部 API
- 在生产环境中使用实时 API 从 AccuWeather 获取实时天气数据。

## 将 WireMock 与 Docker 结合使用

官方的 [Docker image for WireMock](https://hub.docker.com/r/wiremock/wiremock) 提供了一种方便的方式来部署和管理 WireMock 实例。WireMock 可用于各种 CPU 架构，包括 amd64、armv7 和 armv8，确保与不同设备和平台的兼容性。你可以在 [WireMock 文档网站](https://wiremock.org/docs/standalone/docker/)上了解有关 WireMock 独立版的更多信息。

### 先决条件

要学习本操作指南，需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 启动 WireMock

通过以下步骤快速演示 WireMock：

 1. 在本地克隆 [GitHub 存储库](https://github.com/dockersamples/wiremock-node-docker)。

    ```console
    $ git clone https://github.com/dockersamples/wiremock-node-docker
    ```

 2. 导航到 `wiremock-endpoint` 目录

    ```console
    $ cd wiremock-node-docker/
    ```

    WireMock 充当你的后端将与之通信以检索数据的模拟 API。模拟 API 响应��在 mappings 目录中为你创建。

 3. 通过在克隆的项目目录的根目录下运行以下命令来启动 Compose 堆栈

    ```console
    $ docker compose up -d
    ```

    稍后，应用程序将启动并运行。

    ![显示在 Docker Desktop 上运行的 WireMock 容器的图表](./images/wiremock-using-docker.webp)


    你可以通过选择 `wiremock-node-docker` 容器来检查日志：

    ![显示在 Docker Desktop 上运行的 WireMock 容器日志的图表](./images/wiremock-logs-docker-desktop.webp)

 4. 测试模拟 API。

    ```console
    $ curl http://localhost:8080/api/v1/getWeather\?city\=Bengaluru
    ```
 
    它将返回以下带有模拟数据的预设响应：

    ```plaintext
    {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}
    ```

    使用 WireMock，你可以使用��射文件定义预设响应。
    对于此请求，模拟数据在位于 `wiremock-endpoint/mappings/getWeather/getWeatherBengaluru.json` 的 JSON 文件中定义。
    
    有关存根预设响应的更多信息，请参阅 [WireMock 文档](https://wiremock.org/docs/stubbing/)。


## 在开发中使用 WireMock

现在你已经尝试了 WireMock，让我们在开发和测试中使用它。在此示例中，你将使用一个具有 Node.js 后端的示例应用程序。此应用程序堆栈具有以下配置：

  - 本地开发环境：Node.js 后端和 WireMock 正在运行的上下文。
  - Node.js 后端：表示处理 HTTP 请求的后端应用程序。
  - 外部 AccuWeather API：从中获取实时天气数据的真实 API。
  - WireMock：在测试期间模拟 API 响应的模拟服务器。它作为 Docker 容器运行。

  ![显示开发中 WireMock 架构的图表](./images/wiremock-arch.webp)

  - 在开发中，Node.js 后端向 WireMock 发送请求，而不是实际的 AccuWeather API。
  - 在生产中，它直接连接到实时 AccuWeather API 以获取真实数据。

## 在本地开发中使用模拟数据

让我们设置一个 Node 应用程序，以将请求发送到 WireMock 容器，而不是实际的 AccuWeather API。

### 先决条件

- 安装 [Node.js 和 npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- 确保 WireMock 容器已启动并正在运行（请参阅[启动 Wiremock](#launching-wiremock)


按照以下步骤设置非容器化的 Node 应用程序：

1. 导航到 `accuweather-api` 目录

   确保你位于 `package.json` 文件所在的目录中。

2. 设置环境变量。

   打开位于 `accuweather-api/` 目录下的 `.env` 文件。删除旧条目，并确保它只包含以下单行。
 
   ```plaintext
   API_ENDPOINT_BASE=http://localhost:8080
   ```

   这将告诉你的 Node.js 应用程序使用 WireMock 服务器进行 API 调用。

3. 检查应用程序入口点

   - 应用程序的主文件是 `index.js`，位于 `accuweather-api/src/api` 目录中。
   - 此文件启动 `getWeather.js` 模块，这对于你的 Node.js 应用程序至关重要。它使用 `dotenv` 包从 `.env` 文件加载环境变量。
   - 根据 `API_ENDPOINT_BASE` 的值，应用程序将请求路由到 WireMock 服务器 (`http://localhost:8080`) 或 AccuWeather API。在此设置中，它使用 WireMock 服务器。
   - 该代码确保仅当应用程序不使用 WireMock 时才需要 `ACCUWEATHER_API_KEY`，从而提高效率并避免错误。


    ```javascript
    require("dotenv").config();

    const express = require("express");
    const axios = require("axios");

    const router = express.Router();
    const API_ENDPOINT_BASE = process.env.API_ENDPOINT_BASE;
    const API_KEY = process.env.ACCUWEATHER_API_KEY;

    console.log('API_ENDPOINT_BASE:', API_ENDPOINT_BASE);  // Log after it's defined
    console.log('ACCUWEATHER_API_KEY is set:', !!API_KEY); // Log boolean instead of actual key

    if (!API_ENDPOINT_BASE) {
      throw new Error("API_ENDPOINT_BASE is not defined in environment variables");
    }

    // Only check for API key if not using WireMock
    if (API_ENDPOINT_BASE !== 'http://localhost:8080' && !API_KEY) {
      throw new Error("ACCUWEATHER_API_KEY is not defined in environment variables");
    }
    // Function to fetch the location key for the city
    async function fetchLocationKey(townName) {
      const { data: locationData } = await
    axios.get(`${API_ENDPOINT_BASE}/locations/v1/cities/search`, {
        params: { q: townName, details: false, apikey: API_KEY },
      });
      return locationData[0]?.Key;
    }
    ```  

4. 启动 Node 服务器

   在启动 Node 服务器之前，请确保你已通过运行 `npm install` 安装了 package.json 文件中列出的节点包。

   ```console
   npm install 
   npm run start
   ```
 
   你应该会看到以下输出：

    ```plaintext
    > express-api-starter@1.2.0 start
    > node src/index.js

    API_ENDPOINT_BASE: http://localhost:8080
    ..
    Listening: http://localhost:5001
    ```

   输出表明你的 Node 应用程序已成功启动。
   保持此终端窗口打开。

5. 测试模拟 API

   打开一个新的终端窗口并运行以下命令以测试模拟 API：

   ```console
   $ curl "http://localhost:5001/api/v1/getWeather?city=Bengaluru"
   ```

   你应该会看到以下输出：

   ```plaintext
   {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}%
   ```

   这表明你的 Node.js 应用程序现在已成功将请求路由到 WireMock 容器并接收模拟响应

   你可能已经注意到，你正在尝试使用 `http://localhost:5001` 作为 URL，而不是端口 `8080`。这是因为你的 Node.js 应用程序正在端口 `5001` 上运行，并且它正在将请求路由��正在侦听端口 `8080` 的 WireMock 容器。

   > [!TIP]
   > 在继续下一步之前，请确保你已停止节点应用程序服务。

## 在生产环境中使用实时 API 从 AccuWeather 获取实时天气数据

   为了使用实时天气数据增强你的 Node.js 应用程序，你可以无缝集成 AccuWeather API。本指南的这一部分将引导你完成设置非容器化 Node.js 应用程序并直接从 AccuWeather API 获取天气信息的步骤。

1. 创建一个 AccuWeather API 密钥

   在 [https://developer.accuweather.com/](https://developer.accuweather.com/) 注册一个免费的 AccuWeather 开发者帐户。在你的帐户中，通过在顶部导航菜单上选择 `MY APPS` 来创建一个新应用程序，以获取你的唯一 API 密钥。

   ![显示 AccuWeather 仪表板的图表](images/wiremock-accuweatherapi.webp)

    [AccuWeather API](https://developer.accuweather.com/) 是一个提供实时天气数据和预报的 Web API。开发人员可以使用此 API 将天气信息集成到他们的应用程序、网站或其他项目中。

2. 将目录更改为 `accuweather-api`

   ```console
   $ cd accuweather-api
   ```

3. 使用 `.env` 文件设置你的 AccuWeather API 密钥：

   > [!TIP]
   >  为防止冲突，请确保在修改 `.env` 文件之前删除任何名�� `API_ENDPOINT_BASE` 或 `ACCUWEATHER_API_KEY` 的现有环境变量。

   在你的终端上运行以下命令：

   ```console
   unset API_ENDPOINT_BASE
   unset ACCUWEATHER_API_KEY
   ```

   现在是时候在 `.env` 文件中设置环境变量了：

   ```plaintext
   ACCUWEATHER_API_KEY=XXXXXX
   API_ENDPOINT_BASE=http://dataservice.accuweather.com
   ``` 

   确保使用正确的值填充 `ACCUWEATHER_API_KEY`。

4. 安装依赖项

   运行以下命令以安装所需的包：

   ```console
   $ npm install
   ```

   这将安装 `package.json` 文件中列出的所有包。这些包对于项目正常运行至关重要。

   如果遇到任何与已弃用包相关的警告，对于此演示，你现在可以忽略它们。

5. 假设你的系统上没有预先存在的 Node 服务器正在运行，请继续并通过运行以下命令来启动 Node 服务器：

   ```console
   $ npm run start
   ```
  
   你应该会看到以下输出：

   ```plaintext
   > express-api-starter@1.2.0 start
   > node src/index.js

   API_ENDPOINT_BASE: http://dataservice.accuweather.com
   ACCUWEATHER_API_KEY is set: true 
   Listening: http://localhost:5001
   ``` 
   
   保持此终端窗口打开。

6. 运行 curl 命令以向服务器 URL 发送 GET 请求。

   在新终端窗口中，输入以下命令：

   ```console
   $ curl "http://localhost:5000/api/v1/getWeather?city=Bengaluru"
   ``` 

   通过运行该命令，你实际上是在告诉你的本地服务器为你提供名为 `Bengaluru` 的城市的天气数据。该请求专门针对 `/api/v1/getWeather` 端点，并且你正在提供查询参数 `city=Bengaluru`。一旦你执行该命令，服务器就会处理此请求，获取数据并将其作为响应返回，`curl` 将在你的终端中显示该响应。

   从外部 AccuWeather API 获取数据时，你正在与反映最新天气状况的实时数据进行交互。


## 回顾

本指南引导你完成了使用 Docker 设置 WireMock 的过程。你已经学习了如何创建存根来模拟 API 端点，从而让你可以在不依赖外部服务的情况下开发和测试你的应用程序。通过使用 WireMock，你可以创建可靠且一致的测试环境，重现边缘情况，并加快你的开发工作流程。
