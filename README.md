# hiTouyingBeamer

用于论文阅读、研究进展和答辩展示的中文 Beamer 模板，提供两种视觉风格：

- `\usetheme{hit}`：上游经典主题，保留原有视觉效果、公开命令与默认行为。
- `\usetheme{hitacademic}`：Academic 风格，蓝色标题栏、浅灰画布、顶部章节导航、双语封面与内容组件。

两种主题共用同一套命令层 `beamercmdhit.sty`，同一份正文只改主题行即可分别编译。
命令层也可以配合 Madrid 等内建主题使用。

## 使用

使用 TeX Live 中的 XeLaTeX 与 latexmk，在本目录执行：

```powershell
.\build.ps1                          # 编译 example.tex，得到 22 页完整示例
.\build.ps1 -Document starter        # 从 7 页的简洁文档开始写
.\build.ps1 -Document agenda-gallery # 2–6 项自适应目录的六页展示
.\build.ps1 -Document legacy-classic # 经典主题与旧公开接口的 28 页示例
.\build.ps1 -Document theme-switch-hitacademic # 主题切换示例
```

`-Document` 可取 `example`、`starter`、`agenda-gallery`、`legacy-classic`、
`theme-switch-hit`、`theme-switch-hitacademic`、`theme-switch-madrid`。
编译产物统一写在工作目录，分发的 PDF 复制到仓库根目录。

其他系统可在本目录执行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error example.tex`。

正文建议使用 16:9 画幅与 11 pt 文档选项，经典主题同样支持 4:3。
导航适合 3–5 个名称简洁的章节，可用 `\section[短标题]{完整标题}` 控制导航文字。

## 主题选择

```latex
\documentclass[aspectratio=169,11pt,fontset=none]{ctexbeamer}
\usetheme{hitacademic}   % 或 \usetheme{hit}
\usepackage{beamercmdhit} % 写在 \usetheme 前后都可以
```

| 项目 | `hit` 经典主题 | `hitacademic` |
| --- | --- | --- |
| 画布 | 白色 | 浅灰 `#F7F9FB` |
| 标题栏 | 主色文字加下横线 | 主色底白色文字 |
| 页眉 | 章节圆点导航条 | 校名标识加章节导航 |
| 封面 | 白色封面、蓝色照片封面 | 校名标识、蓝色标题栏、双语标题 |
| 章节过渡页 | 大标题、校训图、分栏目录 | 无自动过渡页 |
| 目录 | 编号加大号章节名，显示子章节 | 左侧标题色块、右侧编号圆角横条 |
| 字体 | 文档自定，中文可用系统字体 | 随模板分发的字号与字体 |
| 页码 | 封面与目录用小写罗马数字 | 物理页码 |
| 附录 | 隐藏页脚文字 | 页眉显示 `APPENDIX` |

### 经典主题选项

```latex
\usetheme[serif]{hit}          % 用衬线字体；不写则用非衬线
\usetheme[sans]{hit}           % 用非衬线字体，用于关掉前面写过的 serif
\usetheme[top]{hit}            % 正文顶部对齐；不写则垂直居中
\usetheme[navsymbols]{hit}     % 显示右下角翻页按钮；不写则隐藏
\usetheme[nosectionpage]{hit}  % 不自动插入章节过渡页
\usetheme[sectionpage]{hit}    % 自动插入章节过渡页；默认打开
```

## 公共接口

两种主题共用下列命令，只定义一次：

| 命令 | 作用 |
| --- | --- |
| `\TitleSlide` | 封面 |
| `\BlueTitleSlide` | 蓝色照片封面；`hitacademic` 下与 `\TitleSlide` 相同 |
| `\OutlineSlide[选项]` | 自动读取正文主章节的目录；经典主题沿用无参数调用 |
| `\AgendaSlide[选项]{条目}`、`\AgendaItem[跳转目标]{标题}` | 手动指定目录 |
| `\FocusSlide[栏目]{核心句}` | 整页强调页；`hit` 下只用单参数形式 |
| `\EndSlide{结束语}` | 结束页 |
| `\hitfooter{文字}` | 页脚左侧文字；`hit` 下默认取 `\institute`，`hitacademic` 下默认取 `\title` 的短标题 |
| `\renewcommand{\hitvipath}{...}` | 经典主题的视觉形象资产目录，默认 `vi/` |
| `\renewcommand{\hitoutlinetitle}{...}` | 目录页标题，默认“目录” |
| `\appendix` | 标准附录入口，两种主题都支持 |

Academic 扩展接口：

| 命令 | 作用 |
| --- | --- |
| `\englishtitle{英文标题}` | 封面上的英文标题 |
| `\titlecontext{补充信息}` | 封面上的作者、刊物或活动信息 |
| `\hitlogo{文件路径}` | 封面与页眉标识，默认 `assets/hit-logo.png` |
| `\hitappendix` | 与 `\appendix` 等价，保留为兼容入口 |
| `\subhead{小标题}` | 内容小标题，用主题的结构色 |
| `\insight{结论}` | 浅色背景结论区 |
| `\notebox{条件}` | 2 pt 左侧竖线，与整段文字上下边界对齐 |
| `\captiontext{说明}` | 图注、条件与单位 |
| `\metric{宽度}{数值}{含义}` | 大数字与说明 |
| `\fig{文件名}` | 读取 `assets/figures/文件名.pdf` |
| `\smalltext`、`\bodytext`、`\minitext` | 字号辅助命令 |
| `denseitems` 环境 | 条目间距收紧的 `itemize` |

标准 `\subtitle` 在两种主题下都会显示：`hit` 排在标题下方，`hitacademic` 排在主标题与英文标题之间。
`\subtitle` 与 `\englishtitle` 相互独立，两者的内容都不会丢失。

代码页使用 `\begin{frame}[fragile]`，代码放入 `lstlisting` 环境。

## 自适应目录

自动目录读取正文 `\section`，不显示子章节与附录章节，保留章节跳转。

- 章节数为 2–6 项时，`hitacademic` 使用左侧标题色块与右侧编号圆角横条的版式。
- 章节数不在 2–6 项范围时改用主题一致的普通列表，章节不会被截断，必要时整体缩放。
- 经典主题的 `\OutlineSlide` 沿用原有版式，显示子章节，不受 2–6 项限制。

```latex
\TitleSlide
\OutlineSlide
% 英文版本：\OutlineSlide[title=Outline,subtitle=CONTENTS]
\section{研究问题}
```

手动目录条目个数须为 2–6，标题最多两行，非法输入会给出明确错误：

```latex
\AgendaSlide[title=Outline,subtitle={WORKING WITH AI AGENTS}]{
  \AgendaItem{Getting Started}
  \AgendaItem{A Project Demo}
  \AgendaItem{Review and Control}
}
```

需要跳转时用 `\AgendaItem[项目标签]{标题}`，并在目标页放 `\hypertarget{项目标签}{}`。
自动目录直接跳转到章节页。

首次编译时 `.toc` 还不存在，目录页会提示重新运行一次；`latexmk` 会自动完成多遍编译。

## 字体与素材

字体从 `fonts/` 加载，随模板分发 Source Han Sans CN、Source Sans 3 与 JetBrains Mono
的官方原始字体、原始许可和 SHA-256 清单。`hitacademic` 主题始终使用这份字体。

经典主题在文档写 `fontset=none` 时也改用这份字体；文档已自带中文字体时保持原样。

素材配置入口：

| 项目 | 默认值 | 修改方式 |
| --- | --- | --- |
| 经典主题视觉形象目录 | `vi/` | `\renewcommand{\hitvipath}{<路径>/}` |
| Academic 封面标识 | `assets/hit-logo.png` | `\hitlogo{<文件路径>}` |
| Academic 插图目录 | `assets/figures/` | `\renewcommand{\hit@figpath}{<路径>/}` |

## 文件入口

| 文件或目录 | 用途 |
| --- | --- |
| `beamerthemehit.sty` | 经典主题样式与原有选项 |
| `beamerthemehitacademic.sty` | Academic 主题样式 |
| `beamercmdhit.sty` | 公共命令、参数、内容语义与主题实现接口 |
| `hit-agenda.sty` | 目录模块：章节收集、条目管理、跳转与输入校验 |
| `hit-fonts.sty`、`fonts/` | 字体加载、原始字体、许可及校验清单 |
| `example.tex`、`example.pdf` | Academic 完整示例与直接阅读的 PDF |
| `starter.tex` | 含目录的七页简洁文档起点 |
| `agenda-gallery.tex`、`agenda-gallery.pdf` | 2–6 项中文目录及三项英文目录，共六页 |
| `examples/legacy-classic.tex`、`legacy-classic.pdf` | 经典主题与旧公开接口的完整示例 |
| `examples/theme-switch.tex`、`theme-switch-*.pdf` | 同一份正文换主题的对照示例 |
| `examples/` | 按章节组织的可复制 frame |
| `assets/` | 校名标识、矢量图及 Mermaid 源文件 |
| `build.ps1` | XeLaTeX 构建入口 |
| `build-plots.py`、`build-diagrams.ps1` | 插图生成入口 |
| `check-template.py` | 字体完整性、分发 PDF 的页数画幅与编译日志检查 |
| `check-agenda.py`、`tests/` | 目录、接口矩阵、主题切换、画幅与覆盖层检查 |
| `CHANGELOG.md` | 版本与修改记录 |

## 版式索引（example.pdf）

| 页码 | 示例 |
| --- | --- |
| 1–2 | 中英双语封面、章节目录 |
| 3–6 | 研究问题、公式与符号、方法对照、流程图 |
| 7–10 | 整页重点、CUDA 代码与解释、访存地址表、双栏机制说明 |
| 11–14 | Scaling curve、Roofline、计算结果表、实验设计 |
| 15–18 | 成本分析、适用范围、三点结论、结束页 |
| 19–22 | 字体、注记高度、长标题与组件、最小文档说明 |

示例中的 Amdahl 曲线、Roofline 和数值表是解析模型，图内和正文写明了变量与假设。
填入实验结果时，应同步填写设备、输入、软件版本和计时边界。

## 插图与检查

现有矢量图可直接用于编译。重新生成解析模型图需要 Python、Matplotlib 和 NumPy：

```powershell
python build-plots.py
```

流程图使用 Mermaid CLI 12.0.0、Node.js 与 Chrome；脚本在 `.work/` 中管理所需本地依赖。

```powershell
.\build-diagrams.ps1 -ChromePath 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

生成 PDF 后，安装 `pypdf`、`fonttools`，并确保 Poppler 的 `pdffonts` 可用，执行：

```powershell
python check-template.py   # 字体完整性、页数画幅、编译日志告警
python check-agenda.py     # 目录版式、跳转、附录排除与无效输入诊断
```

检查结果写入 `.work/template-check.json` 与 `.work/agenda-check/validation.json`。
PDF 的视觉排版还应结合逐页阅读检查。

## 许可与来源

主题和示例使用 LPPL-1.3c 或更新版本，见 `LICENSE`。两种主题都是基于
hithesis/hiTouyingBeamer 的派生作品，上游作者为 SchrodingerBlume，原始作品可从
`git@github.com:hithesis/hiTouyingBeamer.git` 的提交
`a1b947ed63671135884f4417d2c91cb9e9555b59` 获取。派生版本的维护和分发由当前项目负责。

字体分别适用 SIL Open Font License 1.1，详见 `fonts/README.md` 和各字体目录内的原始许可证。
生成的文档不因使用字体而必须采用 OFL。校名、校徽等视觉标识的权利属于相应权利人；
素材来源与使用范围见 `assets/README.md`。
