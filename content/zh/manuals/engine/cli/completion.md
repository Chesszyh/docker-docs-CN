---
title: 命令补全 (Completion)
weight: 10
description: 设置您的 shell 以获取 Docker 命令和标志的自动补全
keywords: cli, shell, fish, bash, zsh, completion, options, 命令补全
---

您可以使用 `docker completion` 命令为 Docker CLI 生成 shell 补全脚本。当您在终端输入命令、标志和 Docker 对象 (如容器和卷的名称) 时，按下 `<Tab>` 键即可获得单词补全。

您可以为以下 shell 生成补全脚本：

- [Bash](#bash)
- [Zsh](#zsh)
- [fish](#fish)

## Bash

要使用 Bash 获取 Docker CLI 补全，首先需要安装 `bash-completion` 软件包，该包包含许多用于 shell 补全的 Bash 函数。

```bash
# 使用 APT 安装：
sudo apt install bash-completion

# 使用 Homebrew 安装 (Bash 4 或更高版本)：
brew install bash-completion@2
# 旧版本 Bash 的 Homebrew 安装：
brew install bash-completion

# 使用 pacman：
sudo pacman -S bash-completion
```

安装 `bash-completion` 后，在 shell 配置文件 (本例中为 `.bashrc`) 中引用该脚本：

```bash
# 在 Linux 上：
cat <<EOT >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
EOT

# 在 macOS 上 / 使用 Homebrew：
cat <<EOT >> ~/.bash_profile
[[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
EOT
```

并重新加载您的 shell 配置：

```console
$ source ~/.bashrc
```

现在您可以使用 `docker completion` 命令生成 Bash 补全脚本：

```console
$ mkdir -p ~/.local/share/bash-completion/completions
$ docker completion bash > ~/.local/share/bash-completion/completions/docker
```

## Zsh

只要可以通过 `FPATH` 找到补全脚本，Zsh [补全系统](http://zsh.sourceforge.net/Doc/Release/Completion-System.html) 就会处理好一切。

如果您使用 Oh My Zsh，可以通过将补全脚本存储在 `~/.oh-my-zsh/completions` 目录中来安装补全，而无需修改 `~/.zshrc`。

```console
$ mkdir -p ~/.oh-my-zsh/completions
$ docker completion zsh > ~/.oh-my-zsh/completions/_docker
```

如果您没有使用 Oh My Zsh，请将补全脚本存储在您选择的目录中，并将该目录添加到 `.zshrc` 中的 `FPATH` 中。

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

fish shell 原生支持 [补全系统](https://fishshell.com/docs/current/#tab-completion)。要激活 Docker 命令的补全，请将补全脚本复制或软链接到您的 fish shell `completions/` 目录：

```console
$ mkdir -p ~/.config/fish/completions
$ docker completion fish > ~/.config/fish/completions/docker.fish
```
