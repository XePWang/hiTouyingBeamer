# hiTouyingBeamer

用于论文阅读、研究进展和答辩展示的中文 Beamer 模板。蓝白配色、浅灰画布、双语封面和章节导航采用 `cuDilithium-方班汇报` 的设计语言。示例包含公式、代码、流程图、科学绘图、三线表、指标、讨论和附录。

## 使用

使用 TeX Live 中的 XeLaTeX 与 latexmk，在本目录执行：

```powershell
.\build.ps1
```

生成 `example.pdf`。完整示例为 22 页；从 `starter.tex` 开始撰写自己的报告：

```powershell
.\build.ps1 -Document starter
```

其他系统可在本目录执行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error example.tex`。

字体从 `fonts/` 直接加载。保留 `fontset=none` 和文件夹结构，即可在具备相应 TeX 包的环境中编译。正文建议使用 16:9 画幅、11 pt 文档选项；导航适合 3–5 个名称简洁的章节，可通过 `\section[短标题]{完整标题}` 控制导航文字。封面与重点页为 `plain` 页面，其余页面展示物理页码。

## 文件入口

| 文件或目录 | 用途 |
| --- | --- |
| `example.tex`、`example.pdf` | 完整模板示例及直接阅读的 PDF |
| `starter.tex` | 含目录的七页简洁文档起点 |
| `hit-agenda.sty` | 支持 2–6 项的自适应目录，标题和编号为矢量文字 |
| `agenda-gallery.tex`、`agenda-gallery.pdf` | 2–6 项中文目录及三项英文目录，共六页 |
| `examples/` | 按章节组织的可复制 frame |
| `beamerthemehit.sty` | 配色、页眉、页脚、标题、表格和代码样式 |
| `beamercmdhit.sty` | 封面、重点页、结束页、注记、结论和指标命令 |
| `hit-fonts.sty`、`fonts/` | 字体加载、原始字体、许可及校验清单 |
| `assets/` | 校名标识、矢量图及 Mermaid 源文件 |
| `build.ps1` | XeLaTeX 构建入口 |
| `build-plots.py`、`build-diagrams.ps1` | 插图生成入口 |
| `check-template.py` | 字体完整性、PDF 与编译日志检查 |
| `check-agenda.py`、`tests/agenda-*.tex` | 自动目录、章节跳转、两行标题和无效输入检查 |
| `CHANGELOG.md` | 版本与修改记录 |

## 版式索引

| 页码 | 示例 |
| --- | --- |
| 1–2 | 中英双语封面、章节目录 |
| 3–6 | 研究问题、公式与符号、方法对照、流程图 |
| 7–10 | 整页重点、CUDA 代码与解释、访存地址表、双栏机制说明 |
| 11–14 | Scaling curve、Roofline、计算结果表、实验设计 |
| 15–18 | 成本分析、适用范围、三点结论、结束页 |
| 19–22 | 字体、注记高度、长标题与组件、最小文档说明 |

示例中的 Amdahl 曲线、Roofline 和数值表是解析模型，图内和正文写明了变量与假设。填入实验结果时，应同步填写设备、输入、软件版本和计时边界。

## 文档命令

| 命令 | 作用 |
| --- | --- |
| `\title[短标题]{中文标题}` | 中文封面与默认页脚；可用 `\\` 控制封面换行 |
| `\englishtitle{英文标题}` | 中文标题下方的英文标题 |
| `\titlecontext{作者、刊物或活动信息}` | 封面的补充信息 |
| `\hitlogo{文件路径}` | 封面和页眉标识 |
| `\hitfooter{文字}` | 页脚左侧内容 |
| `\TitleSlide`、`\OutlineSlide[选项]` | 封面、自动读取主章节的目录 |
| `\AgendaSlide[选项]{条目}`、`\AgendaItem[跳转目标]{标题}` | 手动指定目录及可选的 PDF 跳转目标 |
| `\FocusSlide[英文栏目]{核心句}` | 蓝底重点页 |
| `\EndSlide{结束语}` | 结束页 |
| `\hitappendix` | 进入附录并显示 APPENDIX 导航 |
| `\subhead{小标题}` | 蓝色内容小标题 |
| `\notebox{条件}` | 2 pt 左色块，与整段文字上下边界对齐 |
| `\insight{结论}` | 浅蓝背景结论区 |
| `\captiontext{说明}` | 图注、条件与单位 |
| `\metric{宽度}{数值}{含义}` | 大数字与说明 |
| `\fig{文件名}` | 读取 `assets/figures/文件名.pdf` |

代码页使用 `\begin{frame}[fragile]`，代码放入 `lstlisting` 环境。正文中的重要条件使用图注或注记；完整来源放入文档、讲稿或附录。

## 自适应目录

目录使用左侧标题色块和右侧编号条目，按 2–6 项自动计算垂直间距。它是纯矢量版式，文字可以选择和搜索。默认显示中文“目录”和英文“CONTENTS”；标题与副标题可独立设置。章节名称最多两行，超长标题会给出明确错误，建议用简短名称。

自动目录放在封面后，读取正文 `\section`，不显示子章节和附录章节；保留章节跳转。首次编译需要再运行一次，`latexmk` 会自动完成。

```latex
\TitleSlide
\OutlineSlide
% 英文版本：\OutlineSlide[title=Outline,subtitle=CONTENTS]
\section{研究问题}
```

手动目录用于主题路线或短标题，条目个数须为 2–6。可以直接复制以下英文例子：

```latex
\AgendaSlide[title=Outline,subtitle={WORKING WITH AI AGENTS}]{
  \AgendaItem{Getting Started}
  \AgendaItem{A Project Demo}
  \AgendaItem{Review and Control}
}
```

如需跳转，使用 `\AgendaItem[项目标签]{标题}`，并在对应页面放置 `\hypertarget{项目标签}{}`。自动目录直接跳转到章节首页。查看不同条目数量的版式：

```powershell
.\build.ps1 -Document agenda-gallery
python check-agenda.py
```

设计参考用户提供的答辩 PPT 目录页，采用左侧色块、编号与圆角横条的构图；代码在本模板中重新绘制，使用模板的配色和字体。参考 PPT 的个人信息、其他页面和原文件不随模板分发。当前完整示例仍为 22 页，起始文件增加目录后为 7 页。

## 插图与检查

现有矢量图可直接用于编译。重新生成解析模型图需要 Python、Matplotlib 和 NumPy：

```powershell
python build-plots.py
```

流程图使用 Mermaid CLI 12.0.0、Node.js 与 Chrome；脚本在 `.work/` 中管理所需本地依赖。可以通过参数指定 Chrome 和现有 Mermaid CLI 的位置：

```powershell
.\build-diagrams.ps1 -ChromePath 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

生成 PDF 后，安装 `pypdf`、`fonttools`，并确保 Poppler 的 `pdffonts` 可用，执行：

```powershell
python check-template.py
```

检查结果写入 `.work/template-check.json`。PDF 的视觉排版还应结合逐页阅读检查。

## 许可与来源

主题和示例使用 LPPL-1.3c 或更新版本，见 `LICENSE`。本目录的包标识为 `hiTouyingBeamer Academic`，是独立的派生作品，维护状态为 `author-maintained`。上游作者为 SchrodingerBlume，原始作品可从 `git@github.com:hithesis/hiTouyingBeamer.git` 的提交 `a1b947ed63671135884f4417d2c91cb9e9555b59` 获取。派生版本的维护和分发由当前项目负责。

字体分别适用 SIL Open Font License 1.1，详见 `fonts/README.md` 和各字体目录内的原始许可证。生成的文档不因使用字体而必须采用 OFL。校名、校徽等视觉标识的权利属于相应权利人；素材来源与使用范围见 `assets/README.md`。
