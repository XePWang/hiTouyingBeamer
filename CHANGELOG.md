# CHANGELOG

## 2026-10-01 · hiTouyingBeamer Academic 2.1 自适应目录

- 新增 `hit-agenda.sty`，使用 TikZ 重绘左侧标题色块、右侧编号与圆角条目；支持 2–6 项自动间距、中英文标题和最多两行的条目标题。
- `\OutlineSlide` 读取正文主章节并保留跳转；新增 `\AgendaSlide` 和 `\AgendaItem`，支持手动路线目录及可选跳转目标。
- 起始文件加入目录；完整示例仍为 22 页，起始文件为 7 页。新增六页目录示例和构建入口。
- 新增真实编译检查，覆盖 2–6 项自动目录、目标页面、子章节与附录排除、两行英文标题，以及数量越界、标题超长、条目放置错误的诊断。
- 设计构图参考用户提供的答辩 PPT 第 2 页，使用当前模板字体与配色重新实现，不分发参考 PPT。

## 2026-09-27 · hiTouyingBeamer Academic 2.0

- 将 `cuDilithium-方班汇报` 的蓝白主题、顶部导航、双语封面、表格、代码与注记整理为通用模板。
- 主题包与命令包保留 `beamerthemehit.sty`、`beamercmdhit.sty` 文件名，以包版本和日志标识派生作品。
- 使用 `example.tex` 和 `example.pdf` 作为完整示例入口，替换 `template.tex`、`template.pdf`；提供独立的 `starter.tex`。
- 新增四个主题章节与四页附录，共 22 页示例；纳入 Mermaid 流程图、Amdahl 和 Roofline 解析模型图及绘图源码。
- 随模板提供 Source Han Sans CN、Source Sans 3、JetBrains Mono 的官方原始字体、原始许可及 SHA-256 清单。
- 注记色块按照文本盒的高度和深度计算，宽度为 2 pt，右侧间距为 1.5 mm。
- 新增构建入口、字体与 PDF 检查、资源说明和当前版式文档；编译缓存统一放入 Git 忽略范围。

## 上游基线

仓库：`git@github.com:hithesis/hiTouyingBeamer.git`。
提交：`a1b947ed63671135884f4417d2c91cb9e9555b59`。
上游作者与维护者：SchrodingerBlume。
上游包版本：v1.2026b（2026-09-02）。许可：LPPL-1.3c 或更新版本。

原始版本及其修改记录可由该提交完整获取。本目录的派生版本由当前项目维护，维护状态为 `author-maintained`。
