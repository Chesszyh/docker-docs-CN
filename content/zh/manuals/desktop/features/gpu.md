---
title: Docker Desktop for Windows 中的 GPU 支持
linkTitle: GPU 支持
weight: 40
description: 了解如何在 Docker Desktop 中使用 GPU
keywords: gpu, gpu support, nvidia, wsl2, docker desktop, windows
toc_max: 3
aliases:
- /desktop/gpu/
---

> [!NOTE]
>
> 目前 Docker Desktop 中的 GPU 支持仅适用于具有 WSL2 后端的 Windows 系统。

Docker Desktop for Windows 支持在 NVIDIA GPU 上使用 NVIDIA GPU 半虚拟化 (GPU-PV)，允许容器访问 GPU 资源，用于 AI、机器学习或视频处理等计算密集型工作负载。

## 前提条件

要启用 WSL 2 GPU 半虚拟化，您需要：

- 一台带有 NVIDIA GPU 的 Windows 机器
- 最新的 Windows 10 或 Windows 11 安装
- 来自 NVIDIA 的 [最新驱动程序](https://developer.nvidia.com/cuda/wsl)，支持 WSL 2 GPU 半虚拟化
- 最新版本的 WSL 2 Linux 内核。在命令行使用 `wsl --update`
- 确保在 Docker Desktop 中 [开启了 WSL 2 后端](wsl/_index.md#开启-docker-desktop-wsl-2)

## 验证 GPU 支持

要确认 Docker 内部的 GPU 访问是否正常工作，请运行以下命令：

```console
$ docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

这将在 GPU 上运行 n-body 模拟基准测试。输出将类似于：

```console
Run "nbody -benchmark [-numbodies=<numBodies>]" to measure performance.
        -fullscreen       (run n-body simulation in fullscreen mode)
        -fp64             (use double precision floating point values for simulation)
        -hostmem          (stores simulation data in host memory)
        -benchmark        (run benchmark to measure performance)
        -numbodies=<N>    (number of bodies (>= 1) to run in simulation)
        -device=<d>       (where d=0,1,2.... for the CUDA device to use)
        -numdevices=<i>   (where i=(number of CUDA devices > 0) to use for simulation)
        -compare          (compares simulation results running once on the default GPU and once on the CPU)
        -cpu              (run n-body simulation on the CPU)
        -tipsy=<file.bin> (load a tipsy model file for simulation)

> NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.

> Windowed mode
> Simulation data stored in video memory
> Single precision floating point simulation
> 1 Devices used for simulation
MapSMtoCores for SM 7.5 is undefined.  Default to use 64 Cores/SM
GPU Device 0: "GeForce RTX 2060 with Max-Q Design" with compute capability 7.5

> Compute 7.5 CUDA device: [GeForce RTX 2060 with Max-Q Design]
30720 bodies, total time for 10 iterations: 69.280 ms
= 136.219 billion interactions per second
= 2724.379 single-precision GFLOP/s at 20 flops per interaction
```

## 运行一个真实的模型：基于 Ollama 的 Llama2

使用 [官方 Ollama 镜像](https://hub.docker.com/r/ollama/ollama) 在 GPU 加速下运行 Llama2 LLM：

```console
$ docker run --gpus=all -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

然后启动模型：

```console
$ docker exec -it ollama ollama run llama2
```
