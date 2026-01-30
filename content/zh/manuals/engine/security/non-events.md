---
description: Docker 缓解的安全性漏洞回顾
keywords: Docker, Docker documentation, security, security non-events, 安全漏洞, 漏洞缓解
title: Docker 安全性非事件
---

本页列出了 Docker 已缓解的安全性漏洞，即在 Docker 容器中运行的进程从未受到这些漏洞的影响 —— 甚至在漏洞修复之前也是如此。这假设容器在运行时没有添加额外的 capabilities (能力)，也没有使用 `--privileged` 参数。

下面的列表还远远不够完整。相反，它只是我们注意到的少数引起了安全审查并公开披露的漏洞样本。很有可能，尚未报告的漏洞数量远远超过已报告的漏洞。幸运的是，由于 Docker 采取的默认安全方法 (通过 apparmor、seccomp 和丢弃能力)，它可能对未知漏洞的缓解效果与对已知漏洞的缓解效果一样好。

已缓解的漏洞：

* [CVE-2013-1956](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1956)、[1957](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1957)、[1958](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1958)、[1959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1959)、[1979](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1979)、[CVE-2014-4014](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4014)、[5206](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5206)、[5207](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5207)、[7970](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7970)、[7975](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7975)、[CVE-2015-2925](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-2925)、[8543](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8543)、[CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134)、[3135](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3135) 等：
  非特权用户命名空间的引入导致非特权用户可用的攻击面大幅增加，因为这让此类用户能够合法访问以前仅限 root 的系统调用 (如 `mount()`)。所有这些 CVE 都是由于引入用户命名空间而导致的安全性漏洞示例。Docker 可以使用用户命名空间来设置容器，但随后通过默认的 seccomp 配置文件禁止容器内的进程创建其自己的嵌套命名空间，从而使这些漏洞无法被利用。
* [CVE-2014-0181](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0181)、[CVE-2015-3339](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3339)：
  这些是需要存在 setuid 二进制文件的漏洞。Docker 通过 `NO_NEW_PRIVS` 进程标志和其他机制禁用了容器内的 setuid 二进制文件。
* [CVE-2014-4699](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4699)：
  `ptrace()` 中的一个错误可能允许特权提升。Docker 使用 apparmor、seccomp 并通过丢弃 `CAP_PTRACE` 禁用了容器内的 `ptrace()`。三重保护层！
* [CVE-2014-9529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9529)：
  一系列精心构造的 `keyctl()` 调用可能导致内核 DoS / 内存损坏。Docker 使用 seccomp 禁用了容器内的 `keyctl()`。
* [CVE-2015-3214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3214)、[4036](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-4036)：
  这些是常见虚拟化驱动程序中的错误，可能允许客户机操作系统用户在宿主机操作系统上执行代码。利用它们需要访问客户机中的虚拟化设备。在不带 `--privileged` 运行的情况下，Docker 隐藏了对这些设备的直接访问。有趣的是，这些似乎是容器比虚拟机“更安全”的情况，违背了虚拟机比容器“更安全”的普遍看法。
* [CVE-2016-0728](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-0728)：
  由精心构造的 `keyctl()` 调用引起的 Use-after-free 错误可能导致特权提升。Docker 使用默认的 seccomp 配置文件禁用了容器内的 `keyctl()`。
* [CVE-2016-2383](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2383)：
  eBPF (用于表达 seccomp 过滤器等内容的内核特有 DSL) 中的一个错误允许对内核内存进行任意读取。在 Docker 容器内部，`bpf()` 系统调用被 (具有讽刺意味地) 使用 seccomp 阻止了。
* [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134)、[4997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4997)、[4998](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4998)：
  在使用 `IPT_SO_SET_REPLACE`、`ARPT_SO_SET_REPLACE` 和 `ARPT_SO_SET_REPLACE` 调用 setsockopt 时存在的一个错误，会导致内存损坏 / 本地特权提升。这些参数被 `CAP_NET_ADMIN` 阻止，而 Docker 默认不允许该能力。


未缓解的漏洞：

* [CVE-2015-3290](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3290)、[5157](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5157)：
  内核不可屏蔽中断处理中的错误允许特权提升。这在 Docker 容器中是可以被利用的，因为目前尚未通过 seccomp 阻止 `modify_ldt()` 系统调用。
* [CVE-2016-5195](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5195)：
  Linux 内核内存子系统处理私有只读内存映射的写时复制 (COW) 破坏的方式存在竞态条件，这允许非特权本地用户获得对只读内存的写访问权限。也称为 "dirty COW" (脏牛漏洞)。
  *部分缓解：* 在某些操作系统上，通过对 `ptrace` 的 seccomp 过滤以及 `/proc/self/mem` 设为只读这一事实，此漏洞得到了缓解。
