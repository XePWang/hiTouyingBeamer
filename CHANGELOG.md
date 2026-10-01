# CHANGELOG

## 2026-10-01 · 双主题重构 2.2

- 拆分为两种主题：`beamerthemehit.sty` 恢复为上游经典主题样式（原有选项与默认值全部保留），
  新增 `beamerthemehitacademic.sty` 承载 Academic 风格，通过 `\usetheme{hit}` 与
  `\usetheme{hitacademic}` 切换。
- `beamercmdhit.sty` 改为唯一公共命令层：公共命令只定义一次，主题通过版式槽位与解析钩子
  提供实现；未加载这两种主题时退回标准 Beamer 或通用实现，配 Madrid 等内建主题仍可编译。
- `hit-agenda.sty` 只保留章节收集、条目管理、跳转、输入校验与版式判定，绘制交给主题，
  不再重复定义 `\OutlineSlide`。
- 自动目录分版式：2–6 项使用左侧标题色块与右侧编号圆角横条的版块版式，超出范围改用
  主题一致的普通列表，章节不被截断；手动目录仍为 2–6 项且条目标题最多两行。
- 封面、重点页与结束页统一在 `\begin{frame}` 之前设置背景，修复 `plain` 帧丢失背景的问题。
- 经典主题在文档写 `fontset=none` 时改用随模板分发的字体，中文不再缺字；文档自带中文
  字体时保持原样。
- Academic 封面加入标准 `\subtitle` 的显示位置，副标题内容不再丢失。
- `\insight` 改用 `\colorbox` 包固定宽度的 `\parbox`，`\metric` 恢复固定字号与颜色，
  主题字体声明去掉累加基线间距的写法，Academic 示例的版式与页数回到重构前状态。
- 新增 `examples/legacy-classic.tex`（经典主题与旧公开接口）、`examples/theme-switch.tex`
  与三个主题切换入口；新增 `tests/` 下的接口矩阵、经典目录、4:3 画幅与覆盖层检查。
- `build.ps1` 支持七个文档入口，编译产物统一写在工作目录；`check-template.py` 检查
  七个分发 PDF 的页数、画幅与字体嵌入，并读取编译日志告警；`check-agenda.py` 重写为
  在工作目录内独立编译，覆盖列表版式、首次构建与经典目录。

### 验证结果

- `example.pdf` 22 页、`starter.pdf` 7 页、`agenda-gallery.pdf` 6 页，三者在
  XeLaTeX 下无错误、无缺字、无溢出、无字体告警。
- `legacy-classic.pdf` 28 页，与上游 `template.pdf` 页数一致，两种封面与上游基准逐像素一致。
- `hit`、`hitacademic`、Madrid 三种主题 × 命令层前后两种加载顺序共六个变体全部编译通过；
  同一份正文的三个主题变体全部编译通过。
- `check-agenda.py` 覆盖自动目录 2–6 项版块版式、1 项与超过 6 项的列表版式、首次无缓存
  构建提示、章节跳转目标、附录排除、两行标题、经典目录子章节，以及数量越界、标题超长、
  条目错位三类无效输入。

## 2026-10-01 · hiTouyingBeamer Academic 2.1 自适应目录

- 新增 `hit-agenda.sty`，使用 TikZ 重绘左侧标题色块、右侧编号与圆角条目；支持 2–6 项自动间距、中英文标题和最多两行的条目标题。
- `\OutlineSlide` 读取正文主章节并保留跳转；新增 `\AgendaSlide` 和 `\AgendaItem`，支持手动路线目录及可选跳转目标。
- 起始文件加入目录；完整示例仍为 22 页，起始文件为 7 页。新增六页目录示例和构建入口。
- 新增真实编译检查，覆盖 2–6 项自动目录、目标页面、子章节与附录排除、两行英文标题，以及数量越界、标题超长、条目放置错误的诊断。
- 设计构图参考典型学术答辩与汇报版式，使用当前模板字体与配色重新实现，保持清晰结构。

## 2026-09-27 · hiTouyingBeamer Academic 2.0

- 将学术汇报通用的蓝白主题、顶部导航、双语封面、表格、代码与注记整理为通用模板。
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
