---
title: 使用 Docker Compose 设置 Laravel 的前提条件
description: 在使用 Docker Compose 设置 Laravel 之前，确保你具备所需的工具和知识。
weight: 10
---

在开始使用 Docker Compose 设置 Laravel 之前，请确保你满足以下前提条件：

## Docker 和 Docker Compose

你需要在系统上安装 Docker 和 Docker Compose。Docker 允许你容器化应用程序，Docker Compose 帮助你管理多容器应用程序。

- Docker：确保 Docker 已安装并在你的机器上运行。请参阅 [Docker 安装指南](/get-docker/)来安装 Docker。
- Docker Compose：Docker Compose 包含在 Docker Desktop 中，但如果需要，你也可以按照 [Docker Compose 安装指南](/compose/install/)进行安装。

## 对 Docker 和容器的基本理解

对 Docker 和容器工作原理的基本理解将会有所帮助。如果你是 Docker 新手，请考虑查阅 [Docker 概述](/get-started/overview/)以熟悉容器化概念。

## Laravel 基础知识

本指南假设你对 Laravel 和 PHP 有基本的了解。熟悉 Laravel 的命令行工具（如 [Artisan](https://laravel.com/docs/12.x/artisan)）及其项目结构对于遵循说明非常重要。

- Laravel CLI：你应该能够熟练使用 Laravel 的命令行工具（`artisan`）。
- Laravel 项目结构：熟悉 Laravel 的文件夹结构（`app`、`config`、`routes`、`tests` 等）。
