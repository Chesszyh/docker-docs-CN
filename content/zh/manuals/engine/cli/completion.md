---
title: Completion
weight: 10
description: Set up your shell to get autocomplete for Docker commands and flags
keywords: cli, shell, fish, bash, zsh, completion, options
aliases:
  - /config/completion/
---

您可以使用 `docker completion` 命令为 Docker CLI 生成 shell 补全脚本。当您在终端中输入时按下 `<Tab>` 键，补全脚本可以为命令、标志和 Docker 对象（如容器和卷名称）提供单词补全。

您可以为以下 shell 生成补全脚本：

- [Bash](#bash)
- [Zsh](#zsh)
- [fish](#fish)

## Bash

要在 Bash 中获得 Docker CLI 补全功能，您首先需要安装 `bash-completion` 包，该包包含许多用于 shell 补全的 Bash 函数。

```bash
# Install using APT:
sudo apt install bash-completion

# Install using Homebrew (Bash version 4 or later):
brew install bash-completion@2
# Homebrew install for older versions of Bash:
brew install bash-completion

# With pacman:
sudo pacman -S bash-completion
```

安装 `bash-completion` 后，在您的 shell 配置文件（在本例中为 `.bashrc`）中 source 该脚本：

```bash
# On Linux:
cat <<EOT >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
EOT

# On macOS / with Homebrew:
cat <<EOT >> ~/.bash_profile
[[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
EOT
```

然后重新加载您的 shell 配置：

```console
$ source ~/.bashrc
```

现在您可以使用 `docker completion` 命令生成 Bash 补全脚本：

```console
$ mkdir -p ~/.local/share/bash-completion/completions
$ docker completion bash > ~/.local/share/bash-completion/completions/docker
```

## Zsh

只要可以使用 `FPATH` 来 source 补全脚本，Zsh [补全系统](http://zsh.sourceforge.net/Doc/Release/Completion-System.html)就会处理这些事情。

如果您使用 Oh My Zsh，您可以通过将补全脚本存储在 `~/.oh-my-zsh/completions` 目录中来安装补全功能，而无需修改 `~/.zshrc`。

```console
$ mkdir -p ~/.oh-my-zsh/completions
$ docker completion zsh > ~/.oh-my-zsh/completions/_docker
```

如果您没有使用 Oh My Zsh，请将补全脚本存储在您选择的目录中，并在 `.zshrc` 中将该目录添加到 `FPATH`。

```console
$ mkdir -p ~/.docker/completions
$ docker completion zsh > ~/.docker/completions/_docker
```

```console
$ cat <<"EOT" >> ~/.zshrc
FPATH="$HOME/.docker/completions:$FPATH"
autoload -Uz compinit
compinit
EOT
```

## Fish

fish shell 原生支持[补全系统](https://fishshell.com/docs/current/#tab-completion)。
要激活 Docker 命令的补全功能，请将补全脚本复制或符号链接到您的 fish shell `completions/` 目录：

```console
$ mkdir -p ~/.config/fish/completions
$ docker completion fish > ~/.config/fish/completions/docker.fish
```
