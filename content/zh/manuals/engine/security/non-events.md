---
description: Review of security vulnerabilities Docker mitigated
keywords: Docker, Docker documentation,  security, security non-events
title: Docker 安全非事件
---

本页列出了 Docker 已缓解的安全漏洞，因此在 Docker 容器中运行的进程从未受到该漏洞的影响——即使在漏洞修复之前也是如此。这假设容器在运行时未添加额外的能力或未以 `--privileged` 方式运行。

下面的列表甚至远不完整。相反，它只是我们实际注意到的、吸引了安全审查并公开披露漏洞的少数 bug 的样本。很可能，未被报告的 bug 数量远远超过已报告的。幸运的是，由于 Docker 通过 apparmor、seccomp 和删除能力实现默认安全的方法，它很可能像缓解已知 bug 一样有效地缓解未知 bug。

已缓解的 bug：

* [CVE-2013-1956](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1956)，
[1957](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1957)，
[1958](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1958)，
[1959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1959)，
[1979](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1979)，
[CVE-2014-4014](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4014)，
[5206](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5206)，
[5207](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5207)，
[7970](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7970)，
[7975](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7975)，
[CVE-2015-2925](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-2925)，
[8543](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8543)，
[CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134)，
[3135](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3135) 等：
非特权用户命名空间的引入大大增加了非特权用户可用的攻击面，因为它使这些用户能够合法访问以前仅 root 可用的系统调用，如 `mount()`。所有这些 CVE 都是由于引入用户命名空间而导致的安全漏洞示例。Docker 可以使用用户命名空间来设置容器，但随后通过默认的 seccomp 配置文件禁止容器内的进程创建自己的嵌套命名空间，使这些漏洞无法被利用。
* [CVE-2014-0181](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0181)，
[CVE-2015-3339](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3339)：
这些是需要存在 setuid 二进制文件的 bug。Docker 通过 `NO_NEW_PRIVS` 进程标志和其他机制禁用容器内的 setuid 二进制文件。
* [CVE-2014-4699](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4699)：
`ptrace()` 中的一个 bug 可能允许权限提升。Docker 使用 apparmor、seccomp 和删除 `CAP_PTRACE` 来禁用容器内的 `ptrace()`。这里有三层保护！
* [CVE-2014-9529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9529)：
一系列精心构造的 `keyctl()` 调用可能导致内核 DoS / 内存损坏。Docker 使用 seccomp 禁用容器内的 `keyctl()`。
* [CVE-2015-3214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3214)，
[4036](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-4036)：
这些是常见虚拟化驱动程序中的 bug，可能允许客户操作系统用户在宿主机操作系统上执行代码。利用它们需要访问客户机中的虚拟化设备。Docker 在不使用 `--privileged` 运行时会隐藏对这些设备的直接访问。有趣的是，这些似乎是容器比 VM "更安全"的案例，这与认为 VM 比容器"更安全"的常识相反。
* [CVE-2016-0728](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-0728)：
由精心构造的 `keyctl()` 调用导致的使用后释放可能导致权限提升。Docker 使用默认的 seccomp 配置文件禁用容器内的 `keyctl()`。
* [CVE-2016-2383](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2383)：
eBPF 中的一个 bug——用于表达诸如 seccomp 过滤器之类内容的特殊内核内 DSL——允许任意读取内核内存。`bpf()` 系统调用在 Docker 容器内使用（讽刺的是）seccomp 被阻止。
* [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134)，
[4997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4997)，
[4998](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4998)：
使用 `IPT_SO_SET_REPLACE`、`ARPT_SO_SET_REPLACE` 和 `ARPT_SO_SET_REPLACE` 的 setsockopt 中的一个 bug 导致内存损坏/本地权限提升。这些参数被 `CAP_NET_ADMIN` 阻止，Docker 默认不允许此能力。


未缓解的 bug：

* [CVE-2015-3290](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3290)，
[5157](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5157)：
内核的不可屏蔽中断处理中的 bug 允许权限提升。可以在 Docker 容器中利用，因为 `modify_ldt()` 系统调用目前未使用 seccomp 阻止。
* [CVE-2016-5195](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5195)：
在 Linux 内核的内存子系统处理私有只读内存映射的写时复制（COW）中断方式中发现了一个竞争条件，这允许非特权本地用户获得对只读内存的写访问权限。也称为"dirty COW"。
*部分缓解：*在某些操作系统上，通过 seccomp 过滤 `ptrace` 以及 `/proc/self/mem` 为只读的事实，可以缓解此漏洞。
