---
description: 了解如何配置 Docker Compose 以使用 NVIDIA GPU 运行基于 CUDA 的容器
keywords: documentation, docs, docker, compose, GPU access, NVIDIA, samples
title: 使用 GPU 访问运行 Docker Compose 服务
linkTitle: 启用 GPU 支持
weight: 90
aliases:
- /compose/gpu-support/
---

如果 Docker 主机包含 GPU 设备并且 Docker 守护进程已相应设置，Compose 服务可以定义 GPU 设备预留。为此，如果您尚未安装，请确保安装[先决条件](/manuals/engine/containers/resource_constraints.md#gpu)。

以下部分的示例专门关注使用 Docker Compose 为服务容器提供 GPU 设备访问。您可以使用 `docker-compose` 或 `docker compose` 命令。有关更多信息，请参阅[迁移到 Compose V2](/manuals/compose/releases/migrate.md)。

## 为服务容器启用 GPU 访问

GPU 在 `compose.yaml` 文件中使用 Compose Deploy 规范中的 [device](/reference/compose-file/deploy.md#devices) 属性引用，位于需要它们的服务中。

这为 GPU 预留提供了更精细的控制，因为可以为以下设备属性设置自定义值：

- `capabilities`。此值指定为字符串列表。例如，`capabilities: [gpu]`。您必须在 Compose 文件中设置此字段。否则，在服务部署时会返回错误。
- `count`。指定为整数或值 `all`，表示应预留的 GPU 设备数量（前提是主机拥有该数量的 GPU）。如果 `count` 设置为 `all` 或未指定，则默认使用主机上所有可用的 GPU。
- `device_ids`。此值指定为字符串列表，表示主机的 GPU 设备 ID。您可以在主机上的 `nvidia-smi` 输出中找到设备 ID。如果未设置 `device_ids`，则默认使用主机上所有可用的 GPU。
- `driver`。指定为字符串，例如 `driver: 'nvidia'`
- `options`。表示驱动程序特定选项的键值对。


> [!IMPORTANT]
>
> 您必须设置 `capabilities` 字段。否则，在服务部署时会返回错误。

> [!NOTE]
>
> `count` 和 `device_ids` 是互斥的。您一次只能定义一个字段。

有关这些属性的更多信息，请参阅 [Compose Deploy 规范](/reference/compose-file/deploy.md#devices)。

### 运行访问 1 个 GPU 设备的服务的 Compose 文件示例

```yaml
services:
  test:
    image: nvidia/cuda:12.9.0-base-ubuntu22.04
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

使用 Docker Compose 运行：

```console
$ docker compose up
Creating network "gpu_default" with the default driver
Creating gpu_test_1 ... done
Attaching to gpu_test_1
test_1  | +-----------------------------------------------------------------------------+
test_1  | | NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.1     |
test_1  | |-------------------------------+----------------------+----------------------+
test_1  | | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
test_1  | | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
test_1  | |                               |                      |               MIG M. |
test_1  | |===============================+======================+======================|
test_1  | |   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
test_1  | | N/A   23C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
test_1  | |                               |                      |                  N/A |
test_1  | +-------------------------------+----------------------+----------------------+
test_1  |
test_1  | +-----------------------------------------------------------------------------+
test_1  | | Processes:                                                                  |
test_1  | |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
test_1  | |        ID   ID                                                   Usage      |
test_1  | |=============================================================================|
test_1  | |  No running processes found                                                 |
test_1  | +-----------------------------------------------------------------------------+
gpu_test_1 exited with code 0

```

在托管多个 GPU 的机器上，可以设置 `device_ids` 字段来定位特定的 GPU 设备，并且可以使用 `count` 来限制分配给服务容器的 GPU 设备数量。

您可以在每个服务定义中使用 `count` 或 `device_ids`。如果您尝试组合两者、指定无效的设备 ID 或使用高于系统中 GPU 数量的 count 值，将返回错误。

```console
$ nvidia-smi
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            On   | 00000000:00:1B.0 Off |                    0 |
| N/A   72C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  Tesla T4            On   | 00000000:00:1C.0 Off |                    0 |
| N/A   67C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   2  Tesla T4            On   | 00000000:00:1D.0 Off |                    0 |
| N/A   74C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   3  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
| N/A   62C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```

## 访问特定设备

要仅允许访问 GPU-0 和 GPU-3 设备：

```yaml
services:
  test:
    image: tensorflow/tensorflow:latest-gpu
    command: python -c "import tensorflow as tf;tf.test.gpu_device_name()"
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            device_ids: ['0', '3']
            capabilities: [gpu]

```
