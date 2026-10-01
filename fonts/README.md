# 字体与分发许可

模板直接加载本目录内的官方原始字体文件，无需安装到操作系统。

| 用途 | 字体与版本 | 随附字形 | 原始许可 |
| --- | --- | --- | --- |
| 中文正文、标题 | Source Han Sans CN 2.005，发布标签 2.005R | Regular、Bold | `source-han-sans/LICENSE.txt` |
| 西文正文、标题、图表 | Source Sans 3 3.052，发布标签 3.052R | Regular、Bold、Italic、Bold Italic | `source-sans/LICENSE.md` |
| 代码 | JetBrains Mono 2.304，发布标签 v2.304 | Regular、Bold、Italic、Bold Italic | `jetbrains-mono/OFL.txt` |

三种字体均采用 SIL Open Font License 1.1。该许可允许使用、嵌入 PDF、复制和随模板一起分发。随字体分发时需要保留版权声明和许可证；字体继续适用 OFL，不能将字体文件本身单独出售。使用字体生成的报告、论文和幻灯片无需采用 OFL。

本目录的 10 个字体文件保持官方原始内容。Adobe 的两套字体声明了 Reserved Font Name `Source`；若以后修改字体文件，需要遵守 OFL 对保留名称的要求。普通文本排版、缩放、加粗字重选择及 PDF 嵌入不改变本目录的原始字体文件。

`manifest.json` 记录每个字体及许可证的官方原始地址、发布标签、不可变 Git commit、文件大小和 SHA-256；字体还记录内部版本与 `OS/2.fsType`。校验以原始许可为依据，`fsType` 仅作为技术元数据补充。

中文使用大陆简体中文区域字体 Source Han Sans CN。中文的 italic 配置使用直立字形；英文保留真实 italic 字体。数学字符由 TeX Live 的标准数学字体提供，并随 PDF 嵌入。

分享完整模板时保留整个 `fonts/` 目录。单独分享生成的 PDF 时，文档中已经嵌入其实际使用的字形。
