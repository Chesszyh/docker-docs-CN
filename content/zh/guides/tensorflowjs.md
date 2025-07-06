---
description: 了解如何��� TensorFlow.js Web 应用程序中部署预训练模型以执行人脸检测。
keywords: tensorflow.js, 机器学习, ml, mediapipe, blazeface, 人脸检测
title: 使用 TensorFlow.js 进行人脸检测
summary: |
  本指南介绍了如何在 Docker 容器中运行 TensorFlow.js。
tags: [ai]
languages: [js]
aliases:
  - /guides/use-case/tensorflowjs/
params:
  time: 20 分钟
---

本指南介绍了 TensorFlow.js 与 Docker 的无缝集成，以执行人脸检测。在本指南中，你将探索如何：

- 使用 Docker 运行容器化的 TensorFlow.js 应用程序。
- 在 Web 应用程序中使用 TensorFlow.js 实现人脸检测。
- 为 TensorFlow.js Web 应用程序构建 Dockerfile。
- 使用 Docker Compose 进行实时应用程序开发和更新。
- 在 Docker Hub 上共享你的 Docker 镜像，以方便部署和扩大影响范围。

> **致谢**
>
> Docker 感谢 [Harsh Manvar](https://github.com/harsh4870) 对本指南的贡献。

## 先决条件

- 你已经安装了最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [Git 客户端](https://git-scm.com/downloads)。本指南中的示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 什么是 TensorFlow.js？

[TensorFlow.js](https://www.tensorflow.org/js) 是一个用于机器学习的开源 JavaScript 库，可让你在浏览器或 Node.js 中训练和部署机器学习模型。它支持从头开始创建新模型或使用预训练模型，从而在 Web 环境中直接促进广泛的机器学习应用。TensorFlow.js 提供高效的计算，使复杂的机器学习任务对 Web 开发人员来说触手可及，而无需深厚的机器学习专业知识。

## 为什么将 TensorFlow.js 和 Docker 一起使用？

- 环境一致性和简化的部署：Docker 将 TensorFlow.js 应用程序及其依赖项打包到容器中，确保在所有环境中一致运行并简化部署。
- 高效的开发和轻松的扩展：Docker 通过热重载等功能提高了开发效率，并使用 Kubernetes 等编排工具轻松扩展 TensorFlow.js 应用程序。
- 隔离和增强的安全性：Docker 将 TensorFlow.js 应用程序隔离在安全的环境中，在以有限的权限运行应用程序的同时，最大限度地减少冲突和安全漏洞。

## 获取并运行示例应用程序

在终端中，使用以下命令克隆示例应用程序。

```console
$ git clone https://github.com/harsh4870/TensorJS-Face-Detection
```

克隆应用程序后，你会注意到该应用程���有一个 `Dockerfile`。这个 Dockerfile 让你只需使用 Docker 即可在本地构建和运行该应用程序。

在将应用程序作为容器运行之前，你必须将其构建为镜像。在 `TensorJS-Face-Detection` 目录中运行以下命令，以构建一个名为 `face-detection-tensorjs` 的镜像。

```console
$ docker build -t face-detection-tensorjs .
```

该命令将应用程序构建为镜像。根据你的网络连接情况，首次运行该命令时，下载必要的组件可能需要几分钟时间。

要将镜像作为容器运行，请在终端中运行以下命令。

```console
$ docker run -p 80:80 face-detection-tensorjs
```

该命令运行容器并将容器中的 80 端口映射到你系统上的 80 端口。

应用程序运行后，打开 Web 浏览器并在 [http://localhost:80](http://localhost:80) 访问该应用程序。你可能需要授予应用程序访问你的网络摄像头的权限。

在 Web 应用程序中，你可以将后端更改为使用以下之一：

- WASM
- WebGL
- CPU

要停止应用程序，请在终端中按 `ctrl`+`c`。

## 关于应用程序

该示例应用程序使用 [MediaPipe](https://developers.google.com/mediapipe/) 执行实时人脸检测，这是一个用于构建多模式机器学习管道的综合框架。它专门使用 BlazeFace 模型，这是���个用于检测图像中人脸的轻量级模型。

在 TensorFlow.js 或类似的基于 Web 的机器学习框架的背景下，WASM、WebGL 和 CPU 后端可用于执行操作。这些后端中的每一个都利用了现代浏览器中可用的不同资源和技术，并且各有其优缺点。以下各节简要介绍了不同的后端。

### WASM

WebAssembly (WASM) 是一种低级的、类似汇编的语言，具有紧凑的二进制格式，可在 Web 浏览器中以接近本机的速度运行。它允许用 C/C++ 等语言编写的代码编译成可在浏览器中执行的二进制文件。

当需要高性能，并且不支持 WebGL 后端，或者你希望在所有设备上获得一致的性能而不依赖于 GPU 时，这是一个不错的选择。

### WebGL

WebGL 是一种浏览器 API，允许 GPU 加速使用物理和图像处理以及效果，作为网页画布的一部分。

WebGL 非常适合可并行化并且可以从 GPU 加速中显着受益的操作，例如深度学习模型中常见的矩阵乘法和卷积。

### CPU

CPU 后端使用纯 JavaScript 执行，利用设备的中央处理器 (CPU)。该后端是通用性最强的，当 WebGL 和 WASM 后端都不可用或不适用时，可作为后备方案。

## 探索应用程序的代码

在以下各节中探索每个文件的用途及其内容。

### index.html 文件

`index.html` 文件用作 Web 应用程序的前端，该应用程序利用 TensorFlow.js 从网络摄像头视频源进行实时人脸检测。它集成了多种技术和库，以直接在浏览器中促进机器学习。它使用了几个 TensorFlow.js 库，包括：

- tfjs-core 和 tfjs-converter 用于核心 TensorFlow.js 功能和模型转换。
- tfjs-backend-webgl、tfjs-backend-cpu 和 tf-backend-wasm 脚本用于 TensorFlow.js 可用于处理的不同计算后端选项。这些后端允许应用程序通过利用用户的硬件功能来高效地执行机器学习任务。
- BlazeFace 库，一个用于人脸检测的 TensorFlow 模型。

它还使用了以下附加库：

- dat.GUI 用于创建图形界面，以实时与应用程序的设置进行交互，例如在 TensorFlow.js 后端之间切换。
- Stats.min.js 用于显示性能指标（如 FPS），以监控应用程序在运行期间的效率。

{{< accordion title="index.html" >}}

```html
<style>
  body {
    margin: 25px;
  }

  .true {
    color: green;
  }

  .false {
    color: red;
  }

  #main {
    position: relative;
    margin: 50px 0;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
  }

  #description {
    margin-top: 20px;
    width: 600px;
  }

  #description-title {
    font-weight: bold;
    font-size: 18px;
  }
</style>

<body>
  <div id="main">
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      width: auto;
      height: auto;
      "
    ></video>
    <canvas id="output"></canvas>
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      visibility: hidden;
      width: auto;
      height: auto;
      "
    ></video>
  </div>
</body>
<script src="https://unpkg.com/@tensorflow/tfjs-core@2.1.0/dist/tf-core.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-converter@2.1.0/dist/tf-converter.js"></script>

<script src="https://unpkg.com/@tensorflow/tfjs-backend-webgl@2.1.0/dist/tf-backend-webgl.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-backend-cpu@2.1.0/dist/tf-backend-cpu.js"></script>
<script src="./tf-backend-wasm.js"></script>

<script src="https://unpkg.com/@tensorflow-models/blazeface@0.0.5/dist/blazeface.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.6/dat.gui.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r16/Stats.min.js"></script>
<script src="./index.js"></script>
```

{{< /accordion >}}

### index.js 文件

`index.js` 文件执行面部检测逻辑。它演示了 Web 开发和机器学习集成中的几个高级概念。以下是其一些关键组件和功能的分解：

- Stats.js：该脚本首先创建一个 Stats 实例，以实时监控和显示应用程序的帧率 (FPS)。这对于性能分析很有用，尤其是在测试不同 TensorFlow.js 后端对应用程序速度的影响时。
- TensorFlow.js：该应用程序允许用户通过 dat.GUI 提供的图形界面在不同的计算后端（wasm、webgl 和 cpu）之间切换 TensorFlow.js。更改后端可能会影响性能和兼容性，具体取决于设备和浏览器。addFlagLabels 函数动态检查并显示是否支持 SIMD（单指令，多数据）和多线程，这与 wasm 后端中的性能优化相关。
- setupCamera 函数：使用 MediaDevices Web API 初始化用户的网络摄像头。它将视频流配置为不包含音频并使用前置摄像头（facingMode: 'user'）。一旦视频元数据加载完毕，它就会解析一个带有视频元素的 promise，然后该元素将用于人脸检测。
- BlazeFace：此应用程序的核心是 renderPrediction 函数，它使用 BlazeFace 模型（一种用于检测图像中人脸的轻量级模型）执行实时人脸检测。该函数在每个动画帧上调用 model.estimateFaces 以从视频源中检测人脸。对于每个检测到的人脸，它会在视频上覆盖的画布上绘制一个围绕人脸的红色矩形和用于面部标志的蓝点。

{{< accordion title="index.js" >}}

```javascript
const stats = new Stats();
stats.showPanel(0);
document.body.prepend(stats.domElement);

let model, ctx, videoWidth, videoHeight, video, canvas;

const state = {
  backend: "wasm",
};

const gui = new dat.GUI();
gui
  .add(state, "backend", ["wasm", "webgl", "cpu"])
  .onChange(async (backend) => {
    await tf.setBackend(backend);
    addFlagLables();
  });

async function addFlagLables() {
  if (!document.querySelector("#simd_supported")) {
    const simdSupportLabel = document.createElement("div");
    simdSupportLabel.id = "simd_supported";
    simdSupportLabel.style = "font-weight: bold";
    const simdSupported = await tf.env().getAsync("WASM_HAS_SIMD_SUPPORT");
    simdSupportLabel.innerHTML = `SIMD supported: <span class=${simdSupported}>${simdSupported}<span>`;
    document.querySelector("#description").appendChild(simdSupportLabel);
  }

  if (!document.querySelector("#threads_supported")) {
    const threadSupportLabel = document.createElement("div");
    threadSupportLabel.id = "threads_supported";
    threadSupportLabel.style = "font-weight: bold";
    const threadsSupported = await tf
      .env()
      .getAsync("WASM_HAS_MULTITHREAD_SUPPORT");
    threadSupportLabel.innerHTML = `Threads supported: <span class=${threadsSupported}>${threadsSupported}</span>`;
    document.querySelector("#description").appendChild(threadSupportLabel);
  }
}

async function setupCamera() {
  video = document.getElementById("video");

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: { facingMode: "user" },
  });
  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}

const renderPrediction = async () => {
  stats.begin();

  const returnTensors = false;
  const flipHorizontal = true;
  const annotateBoxes = true;
  const predictions = await model.estimateFaces(
    video,
    returnTensors,
    flipHorizontal,
    annotateBoxes,
  );

  if (predictions.length > 0) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < predictions.length; i++) {
      if (returnTensors) {
        predictions[i].topLeft = predictions[i].topLeft.arraySync();
        predictions[i].bottomRight = predictions[i].bottomRight.arraySync();
        if (annotateBoxes) {
          predictions[i].landmarks = predictions[i].landmarks.arraySync();
        }
      }

      const start = predictions[i].topLeft;
      const end = predictions[i].bottomRight;
      const size = [end[0] - start[0], end[1] - start[1]];
      ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
      ctx.fillRect(start[0], start[1], size[0], size[1]);

      if (annotateBoxes) {
        const landmarks = predictions[i].landmarks;

        ctx.fillStyle = "blue";
        for (let j = 0; j < landmarks.length; j++) {
          const x = landmarks[j][0];
          const y = landmarks[j][1];
          ctx.fillRect(x, y, 5, 5);
        }
      }
    }
  }

  stats.end();

  requestAnimationFrame(renderPrediction);
};

const setupPage = async () => {
  await tf.setBackend(state.backend);
  addFlagLables();
  await setupCamera();
  video.play();

  videoWidth = video.videoWidth;
  videoHeight = video.videoHeight;
  video.width = videoWidth;
  video.height = videoHeight;

  canvas = document.getElementById("output");
  canvas.width = videoWidth;
  canvas.height = videoHeight;
  ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(255, 0, 0, 0.5)";

  model = await blazeface.load();

  renderPrediction();
};

setupPage();
```

{{< /accordion >}}

### tf-backend-wasm.js 文件

`tf-backend-wasm.js` 文件是 [TensorFlow.js 库](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm) 的一部分。它包含 TensorFlow.js WASM 后端的初始化逻辑、一些用于与 WASM 二进制文件交互的实用程序，以及用于为 WASM 二进制文件设置自定义路径的函数。

### tfjs-backend-wasm-simd.wasm 文件

`tfjs-backend-wasm-simd.wasm` 文件是 [TensorFlow.js 库](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm) 的一部分。它是一个 WASM 二进制文件，用于 WebAssembly 后端，专门优化以利用 SIMD（单指令，多数据）指令。

## 探索 Dockerfile

在基于 Docker 的项目中，Dockerfile 是构建应用程序环境的基础资产。

Dockerfile 是一个文本文件，它指示 Docker 如何创建应用程序环境的镜像。镜像包含运行应用程序时所需的一切，例如文件、包和工具。

以下是此项目的 Dockerfile。

```dockerfile
FROM nginx:stable-alpine3.17-slim
WORKDIR /usr/share/nginx/html
COPY . .
```

此 Dockerfile 定义了一个使用 Nginx 从 Alpine Linux 基础镜像提供静态内容的镜像。

## 使用 Compose 进行开发

Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。使用 Compose，你可以使用 YAML 文件来配置应用程序的服务、网络和卷。在这种情况下，该应用程序不是多容器应用程序，但 Docker Compose 具有其他有用的开发功能，例如 [Compose Watch](/manuals/compose/how-tos/file-watch.md)。

示例应用程序还没有 Compose 文件。要创建 Compose 文件，请在 `TensorJS-Face-Detection` 目录中创建一个名为 `compose.yaml` 的文本文件，然后添加以下内容。

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 80:80
    develop:
      watch:
        - action: sync
          path: .
          target: /usr/share/nginx/html
```

此 Compose 文件定义了一个使用同一目录中的 Dockerfile 构建的服务。它将主机上的 80 端口映射到容器中的 80 端口。它还有一个带有 `watch` 属性的 `develop` 子部分，该属性定义了一系列规则，这些规则根据本地文件更改控制自动服务更新。有关 Compose 指令的更多详细信息，请参�� [Compose 文件参考](/reference/compose-file/_index.md)。

将更改保存到 `compose.yaml` 文件，然后运行以下命令以运行该应用程序。

```console
$ docker compose watch
```

应用程序运行后，打开 Web 浏览器并在 [http://localhost:80](http://localhost:80) 访问该应用程序。你可能需要授予应用程序访问你的网络摄像头的权限。

现在，你可以对源代码进行更改，并看到更改自动反映在容器中，而无需重新构建和重新运行容器。

打开 `index.js` 文件，并将第 83 行的标志点更新为绿色而不是蓝色。

```diff
-        ctx.fillStyle = "blue";
+        ctx.fillStyle = "green";
```

将更改保存到 `index.js` 文件，然后刷新浏览器页面。标志点现在应该显示为绿色。

要停止应用程序，请在终端中按 `ctrl`+`c`。

## 共享你的镜像

在 Docker Hub 上发布你的 Docker 镜像可以简化其他人的部署过程，从而实现与不同项目的无缝集成。它还促进了你的容器化解决方案的采用，从而扩大了它们在开发人员生态系统中的影响。要共享你的镜像：

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) 或登录 [Docker Hub](https://hub.docker.com)。

2. 重新构建你���镜像以包含对你的应用程序的更改。这一次，在镜像名称前加上你的 Docker ID。Docker 使用该名称来确定要将其推送到哪个存储库。打开一个终端，并在 `TensorJS-Face-Detection` 目录中运行以下命令。将 `YOUR-USER-NAME` 替换为你的 Docker ID。

   ```console
   $ docker build -t YOUR-USER-NAME/face-detection-tensorjs .
   ```

3. 运行以下 `docker push` 命令将镜像推送到 Docker Hub。将 `YOUR-USER-NAME` 替换为你的 Docker ID。

   ```console
   $ docker push YOUR-USER-NAME/face-detection-tensorjs
   ```

4. 验证你已将镜像推送到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看你的存储库的 **Last pushed** 时间。

其他用户现在可以使用 `docker run` 命令下载并运行你的镜像。他们需要将 `YOUR-USER-NAME` 替换为你的 Docker ID。

```console
$ docker run -p 80:80 YOUR-USER-NAME/face-detection-tensorjs
```

## 总结

本指南演示了如何利用 TensorFlow.js 和 Docker 在 Web 应用程序中进行人脸检测。它强调了运行容器化的 TensorFlow.js 应用程序的简便性，以及使用 Docker Compose 进行实时代码更改的开发。此外，它还介绍了如何在 Docker Hub 上共享你的 Docker 镜像可以简化��他人的部署，从而增强应用程序在开发人员社区中的影响力。

相关信息：

- [TensorFlow.js 网站](https://www.tensorflow.org/js)
- [MediaPipe 网站](https://developers.google.com/mediapipe/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Docker CLI 参考](/reference/cli/docker/)
- [Docker 博客：使用 TensorFlow.js 加速机器学习](https://www.docker.com/blog/accelerating-machine-learning-with-tensorflow-js-using-pretrained-models-and-docker/)
