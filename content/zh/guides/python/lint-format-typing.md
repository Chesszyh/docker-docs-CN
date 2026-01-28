---
title: Python 的代码检查、格式化和类型检查
linkTitle: 代码检查和类型检查
weight: 25
keywords: Python, linting, formatting, type checking, ruff, pyright
description: 学习如何为您的 Python 应用程序设置代码检查、格式化和类型检查。
aliases:
  - /language/python/lint-format-typing/
---

## 前提条件

完成[开发您的应用](develop.md)。

## 概述

在本节中，您将学习如何为 Python 应用程序设置代码质量工具。这包括：

- 使用 Ruff 进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 使用 pre-commit hooks 自动化检查

## 使用 Ruff 进行代码检查和格式化

Ruff 是一个用 Rust 编写的极其快速的 Python 代码检查器和格式化工具。它用一个统一的工具替代了多个工具，如 flake8、isort 和 black。

创建一个 `pyproject.toml` 文件：

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle 错误
    "W",  # pycodestyle 警告
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # 函数中未使用的参数
]
ignore = [
    "E501",  # 行太长，由 black 处理
    "B008",  # 不要在参数默认值中执行函数调用
    "W191",  # 缩进包含制表符
    "B904",  # 允许不使用 from e 抛出异常，用于 HTTPException
]
```

### 使用 Ruff

运行以下命令来检查和格式化您的代码：

```bash
# 检查错误
ruff check .

# 自动修复可修复的错误
ruff check --fix .

# 格式化代码
ruff format .
```

## 使用 Pyright 进行类型检查

Pyright 是一个快速的 Python 静态类型检查器，与现代 Python 特性配合良好。

在 `pyproject.toml` 中添加 `Pyright` 配置：

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

### 运行 Pyright

要检查代码中的类型错误：

```bash
pyright
```

## 设置 pre-commit hooks

Pre-commit hooks 在每次提交之前自动运行检查。以下 `.pre-commit-config.yaml` 代码片段设置了 Ruff：

```yaml
  https: https://github.com/charliermarsh/ruff-pre-commit
  rev: v0.2.2
  hooks:
    - id: ruff
      args: [--fix]
    - id: ruff-format
```

安装和使用：

```bash
pre-commit install
git commit -m "Test commit"  # 自动运行检查
```

## 总结

在本节中，您学习了如何：

- 配置和使用 Ruff 进行代码检查和格式化
- 设置 Pyright 进行静态类型检查
- 使用 pre-commit hooks 自动化检查

这些工具有助于维护代码质量，并在开发早期发现错误。

## 下一步

- [配置 GitHub Actions](configure-github-actions.md) 以自动运行这些检查
- 自定义代码检查规则以匹配您团队的风格偏好
- 探索高级类型检查功能
