# 更现代的哈尔滨工业大学 Beamer 幻灯片主题 hiTouyingBeamer（读作「嗨！投影 Beamer」）

**预览**：[现代主题（默认，16:9）](examples/template.pdf)　·　[极简主题（`minimalist` 选项，16:9）](examples/template-minimalist.pdf)　·　[经典主题（`classic` 选项，4:3）](examples/template-classic.pdf)

本主题的灵感来自于上海交通大学 Touying 幻灯片主题
（[touying-simpl-sjtu](https://github.com/sjtug/touying-sjtu)）。

## 文件结构

| 文件 / 目录 | 说明 |
| --- | --- |
| `beamerthemehit.sty` | 主题入口（`\usetheme{hit}`）：解析选项，分派到 `styles/` 下的主题实现 |
| `beamercmdhit.sty` | 文档命令（`\TitleSlide` 等）与配套包（`\upcite`/`\cmd`/`\env`、unicode-math、physics、listings 等），各套主题共用，主题会自动加载 |
| `styles/` | 主题样式实现目录：`beamerthemehitouying.sty`（现代）、`beamerthemehitclassic.sty`（经典）、`beamerthemehitminimalist.sty`（极简） |
| `examples/` | 各主题编译预览成品 PDF（`template.pdf`、`template-classic.pdf`、`template-minimalist.pdf`） |
| `template.tex` | 模板兼完整示例（动画、TikZ、双栏、跨页、块与公式、表格、代码清单、GB/T 7714 参考文献等），各主题共用正文，从这里开始写 |
| `vi/` | 哈尔滨工业大学视觉形象素材（均获取自网络，经 AI 处理，如有侵权请联系 hiThesis 团队） |

样式与命令是分开的。`beamercmdhit.sty` 里的专用命令在加载 hit 主题时会处理为定制版式，
而未加载时自动改用标准 Beamer 写法，例如 `\titlepage`、`\tableofcontents`。
所以只要文档里保留 `\usepackage{beamercmdhit}`，把 `\usetheme{hit}` 换成任意
内建主题（如 `Madrid`）仍可直接编译。

## 使用

```latex
\documentclass[aspectratio=169]{ctexbeamer}
\usetheme{hit}

\title{标题}
\subtitle{副标题}
\author{作者}
\institute{哈尔滨工业大学}
\date{\today}

\begin{document}
\TitleSlide      % 白色标题页（或 \BlueTitleSlide 蓝色标题页）
\OutlineSlide    % 目录页

\section{...}    % 每个 \section 自动生成章节过渡页
\subsection{...}
\begin{frame}{帧标题}
  ...
\end{frame}

\appendix        % 附录：隐藏页脚并冻结页码总数
\EndSlide{感谢使用\par\medskip Thanks for Using!}
\end{document}
```

应使用 XeLaTeX 编译：

```console
latexmk -xelatex template.tex
```

`template.tex` 中的参考文献使用 `biblatex-gb7714-2015`，需要 `biber`
（`latexmk` 会自动调用）。章节过渡页与导航条需要编译两遍才能稳定。
打开 `minted` 选项时命令改成 `latexmk -xelatex -shell-escape template.tex`。

## 专用命令

| 命令 | 说明 |
| --- | --- |
| `\TitleSlide` / `\BlueTitleSlide` | 白色 / 蓝色标题页 |
| `\OutlineSlide` | 目录页（标题文字可 `\renewcommand{\hitoutlinetitle}{...}`） |
| `\FocusSlide{...}` | 蓝底白字强调页 |
| `\EndSlide{...}` | 结束页 |
| `\hitfooter{...}` | 页脚左侧文字（默认继承 `\institute`） |
| `\themetitle` / `\themeauthor` | 当前主题的标题 / 作者，各主题预置（现代主题 `SchrodingerBlume`、经典主题 `syvshc`、极简主题 `XePWang`）；模板用 `\title{\themetitle}`、`\author{\themeauthor}` |
| `\renewcommand{\hitvipath}{...}` | `vi/` 视觉形象资产目录路径（默认 `vi/`） |

封面与目录属于前置页，用小写罗马数字计数（`i`、`ii`、`iii`），正文页码从 1 重新起算
（现代主题）；极简主题右下角显示当前物理页码（`\insertpagenumber`）；经典主题按 beamer 原样连续编号。`\hitfooter` 在现代与极简主题生效，
经典主题的页脚固定为旧 HITBeamer 的两行样式。

## 主题选项

```latex
\usetheme[classic]{hit}        % 经典主题（旧 HITBeamer 观感）；不写则用现代主题
\usetheme[touying]{hit}        % 现代主题（默认），写与不写一样
\usetheme[minimalist]{hit}     % 极简主题（带顶部章节导航与浅灰画布）
\usetheme[minted]{hit}         % 代码用 minted 排版（编译加 -shell-escape）
\usetheme[serif]{hit}          % 用衬线字体（经典主题的默认）
\usetheme[sans]{hit}           % 用非衬线字体（现代与极简主题的默认）
\usetheme[top]{hit}            % 正文顶端对齐（默认垂直居中）
\usetheme[navsymbols]{hit}     % 显示右下角翻页按钮（默认隐藏）
\usetheme[nosectionpage]{hit}  % 不自动生成章节过渡页（经典与现代主题跳过 \section 后的目录帧）
\usetheme[sectionpage]{hit}    % 显式生成章节过渡页（极简主题默认不插过渡页，加此项开启）
```

## 极简主题（minimalist 选项）

`\usetheme[minimalist]{hit}` 切换到极简学术主题（原 Academic 风格）：
- **展示作者覆写**：加载时默认展示作者覆写为 `XePWang`（`\themeauthor`），独立于共享命令层与其他主题默认作者。
- **顶部章节导航**：页眉左侧展示校徽，右侧等宽连续铺满 2–6 章节导航，当前章以整格蓝色（`#0070C0`）高亮，附录页自动切换为 APPENDIX 标识。基于实际字体尺寸测量与两行上限自动适配：优先使用默认字号（单行或自然换为两行），单元格空间不足时自动逐级缩小字号（7.5pt $\to$ 5.0pt）以容纳在两行内，高亮切换前后字号与断行保持稳定；若极端长标题仍无法在两行内容纳，将输出明确的编译诊断警告。章节标题过长时推荐使用标准 `\section[短标题]{完整长标题}`。
- **浅灰背景画布**：正文使用高雅浅灰背景（`#F7F9FB`）与蓝色标题栏（`#0070C0`），适合学术答辩与技术报告。
- **专属目录页排版**：`\OutlineSlide` 提供极简专属 Outline 胶囊排版（左侧白字大号 Outline 结合外沿浅蓝轮廓与圆角蓝底形状，右侧 2–6 章节等宽胶囊、数字序号与跳转超链接）；胶囊内标题同样自动限制在两行内，确保完整容纳于胶囊内；并支持通过 `\renewcommand{\hitoutlinetitle}{...}` 自定义目录标题。
- **全通栏三段式封面**：`\TitleSlide` 采用整页比例三段式布局（顶部居中校徽约 32%、中间主色蓝带约 42% 左右贯通并居中主副标题、底部居中作者与单位信息约 26%），构图比例严格自适应不同画幅（16:9 与 4:3）。
- **三段式致谢页**：`\EndSlide{...}` 统一提供顶部校徽、中部通栏蓝底白色致谢、底部作者/单位信息的典雅版式。
- **共用正文**：与现代主题、经典主题共用完全一致的 LaTeX 正文与命令，无需按主题分支编写内容。
- **选项兼容**：支持 `top`（顶端对齐）、`navsymbols`（导航按钮）、`serif`（衬线字体）、`sectionpage`（显式开启章节过渡页）等通用选项。

## 经典主题（classic 选项）

`\usetheme[classic]{hit}` 切换到移植自 HITBeamer 的经典主题：顶部 smoothbars
导航条（章节名加小节方块）、整条深蓝帧标题、两行页脚、circle 列表、编号圆球目录，
每个 `\section` 与 `\subsection` 后自动插一页目录。主色统一为校色 `#166183`
（旧版是 `#00668E`）。`\TitleSlide`、`\OutlineSlide`、`\FocusSlide`、`\EndSlide`
在经典主题下都有一套经典版式；`\BlueTitleSlide`（照片蓝色封面）是共用命令，
各套主题下一样。

原 hit-extra 的配套包与命令（ctex、unicode-math、physics、listings、multicol、
booktabs 等，以及 `\upcite`、`\cmd`、`\env`）在共用命令层 `beamercmdhit.sty` 里，
各套主题都可用。从 v2.2026a 起数学字体由 unicode-math 排（Latin Modern Math）。
minted 是主题选项，每个主题均可使用：`\usetheme[classic,minted]{hit}`，编译加
`-shell-escape`。

对于旧的基于未经自行修改的 HITBeamer 的文档只需将文档类改成新写法即可，正文一般不用修改：

```latex
% 旧：\documentclass{beamer} + \usepackage{hit-style} + \usepackage[minted,fira,siyuan]{hit-extra}
\documentclass[aspectratio=169]{ctexbeamer}
\usetheme[classic,minted]{hit}   % minted 按需；HITbeamer的 fira、siyuan 选项不再提供
```

旧文档里的 `\bibliographystyle{hithesis}\bibliography{...}` 依赖 `hithesis.bst`，
本仓库不附带，可以换成 `template.tex` 里的 biblatex-gb7714-2015 方案，
或自行保证 bst 可用。

## 把主题装进 TeX 目录树（可选）

若不想把 `.sty` 和 `vi/` 复制到每个项目，可把它们一起放入
`TEXMFHOME`（如 `~/texmf/tex/latex/hitouyingbeamer/`），并在文档中
`\renewcommand{\hitvipath}{<vi 的绝对路径>/}`。

## 发布前

跑一次 `./build-previews.sh`：它在临时目录里编译所有子主题，并把各自的预览 PDF
拷入 `examples/`（现代 16:9 `template.pdf`、经典 4:3 `template-classic.pdf`、
极简 16:9 `template-minimalist.pdf`），连同改动一起提交。主题是自动发现的：脚本扫描
`styles/beamerthemehit*.sty` 里文件头的 `%% Preview:` 标记（主题选项、画幅、输出文件名），
以后新增主题只要在皮肤文件里加上这行标记，不用改脚本。

贡献与提交规则（命令必须所有主题通用、输出变化需人工审核等）见
[CONTRIBUTING.md](CONTRIBUTING.md)；本地自测跑 `./tests/ci.sh`。

## License

本项目采用 LaTeX Project Public License 1.3c（LPPL-1.3c）发布，详见 [LICENSE](LICENSE)。
维护状态为 `maintained`，当前维护者 @SchrodingerBlume。
