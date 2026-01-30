---
description: 自动锁定 Swarm 管理节点以保护加密密钥
keywords: swarm, manager, lock, unlock, autolock, encryption, 管理节点, 锁定, 解锁, 自动锁定, 加密
title: 锁定您的 Swarm 以保护其加密密钥
---

Swarm 管理节点使用的 Raft 日志在磁盘上默认是加密的。这种静态加密保护了您的服务配置和数据，防止攻击者通过获取加密的 Raft 日志来进行破坏。引入此功能的原因之一是为了支持 [Docker 机密 (Secrets)](secrets.md) 功能。

当 Docker 重启时，用于加密 Swarm 节点间通信的 TLS 密钥以及用于加解密磁盘上 Raft 日志的密钥都会加载到每个管理节点的内存中。Docker 有能力保护双向 TLS 加密密钥以及用于加解密静态 Raft 日志的密钥，方法是允许您接管这些密钥的所有权，并要求手动解锁管理节点。此功能称为“自动锁定 (autolock)”。

当 Docker 重启时，您必须首先使用 Docker 在锁定 Swarm 时生成的密钥加密密钥 (key encryption key) 来 [解锁 Swarm](#unlock-a-swarm)。您可以随时轮换此密钥加密密钥。

> [!NOTE]
> 
> 当新节点加入 Swarm 时，您不需要解锁 Swarm，因为该密钥会通过双向 TLS 传播给它。

## 初始化一个启用了自动锁定的 Swarm

初始化一个新 Swarm 时，您可以使用 `--autolock` 标志，以在 Docker 重启时启用 Swarm 管理节点的自动锁定功能。

```console
$ docker swarm init --autolock

Swarm initialized: current node (k1q27tfyx9rncpixhk69sa61v) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-0j52ln6hxjpxk2wgk917abcnxywj3xed0y8vi1e5m9t3uttrtu-7bnxvvlz2mrcpfonjuztmtts9 \
    172.31.46.109:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-WuYH/IX284+lRcXuoVf38viIDK3HJEKY13MIHX+tTt8
```

将该密钥存储在安全的地方，例如密码管理器中。

当 Docker 重启时，您需要 [解锁 Swarm](#unlock-a-swarm)。被锁定的 Swarm 在您尝试启动或重启服务时会导致类似于以下的错误：

```console
$ sudo service docker restart

$ docker service ls

Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used. Use "docker swarm unlock" to unlock it.
```

## 在现有 Swarm 上启用或禁用自动锁定

要在现有 Swarm 上启用自动锁定，请将 `autolock` 标志设置为 `true`。

```console
$ docker swarm update --autolock=true

Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-+MrE8NgAyKj5r3NcR4FiQMdgu+7W72urH0EZeSmP/0Y

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

要禁用自动锁定，请将 `--autolock` 设置为 `false`。此时，用于读写 Raft 日志的密钥和双向 TLS 密钥将以未加密形式存储在磁盘上。这涉及到在磁盘上存储未加密密钥的风险与重启 Swarm 时无需解锁每个管理节点的便利性之间的权衡。

```console
$ docker swarm update --autolock=false
```

在禁用自动锁定后，请保留解锁密钥一段时间，以防某个管理节点在仍配置为使用旧密钥锁定的情况下宕机。

## 解锁 Swarm

要解锁处于锁定状态的 Swarm，请使用 `docker swarm unlock`。

```console
$ docker swarm unlock

Please enter unlock key:
```

输入您在锁定 Swarm 或轮换密钥时生成并显示在命令输出中的加密密钥，Swarm 即可解锁。

## 查看运行中 Swarm 的当前解锁密钥

考虑这样一种情况：您的 Swarm 运行正常，但某个管理节点变得不可用。您排查了问题并将物理节点重新上线，但您需要提供解锁密钥来解锁该管理节点，以便读取加密的凭据和 Raft 日志。

如果自该节点离开 Swarm 以来密钥尚未被轮换，且 Swarm 中还有法定人数的功能正常的管理节点，您可以使用不带参数的 `docker swarm unlock-key` 来查看当前的解锁密钥。

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

如果 Swarm 节点不可用后密钥已被轮换，且您没有记录先前的密钥，您可能需要强制该管理节点离开 Swarm 并作为新管理节点重新加入 Swarm。

## 轮换解锁密钥

您应该定期轮换被锁定 Swarm 的解锁密钥。

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

> [!WARNING]
> 
> 轮换解锁密钥时，请将旧密钥记录保留几分钟，以便如果管理节点在获得新密钥之前宕机，仍可使用旧密钥进行解锁。
