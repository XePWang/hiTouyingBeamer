# 写作与自定义

起点是根目录的 `starter.tex`。封面和主题写在起步文件，章节与页面写在 `slides/content.tex`，自己的图片放在 `slides/images/`。编译时以项目根目录为工作目录。

## 标题层级

| 写法 | 用途 | 是否进入目录 |
| --- | --- | --- |
| `\title[短标题]{完整标题}` | 整份演示文稿的标题；短标题供导航或页脚使用 | 否 |
| `\section{章节}` | 组织一组页面 | 是 |
| `\subsection{子章节}` | 可选的二级分组 | 开启子章节显示时进入 |
| `\begin{frame}{页面标题}` | 当前页的标题 | 否 |
| `\subhead{页内小标题}` | 页内内容分组 | 否 |

以下是完整的结构示例，可用于理解层级；日常继续编辑 `starter.tex` 和 `slides/content.tex`。

```latex
\documentclass[aspectratio=169,11pt,fontset=none]{ctexbeamer}
\usetheme[minimalist]{hit}
\hitnosectionpages
\hitoutlinesubs
\title[简短标题]{完整汇报标题}
\author{汇报人}
\date{汇报日期}
\begin{document}
  \TitleSlide
  \OutlineSlide[title={汇报提纲}]
  \section{研究方法}
  \subsection{方法定义}
  \begin{frame}{输入与输出}
    \subhead{输入条件}
    填写输入类型和适用范围。
    \subhead{输出内容}
    填写方法产生的结果。
  \end{frame}
  \EndSlide{感谢聆听}
\end{document}
```

设置写在 `\usetheme` 后、`\begin{document}` 前：

- `\hitoutlinesubs` 显示目录子章节，并自动使用适合层级内容的列表；`\hitnooutlinesubs` 只显示章节。
- `\hitsectionpages` 在章节开始处插入过渡页，`\hitnosectionpages` 关闭。
- `\OutlineSlide[title={汇报提纲}]` 设置本次目录的标题。旧文档的全局标题变量仍可用 `\renewcommand{\hitoutlinetitle}{汇报提纲}` 修改。
- `\hittocmode{list}` 选择列表目录；`\hittocmode{block}` 请求色块目录，主题未提供或条目数量不适合时使用列表。

`starter.tex` 明确关闭章节过渡页和子章节显示，两种主题保持相同设置。目录信息需要多次编译，推荐的 `latexmk` 命令会自动处理。

## 图片与图注

起步文件已设置 `\hitfigures{slides/images/}`。图片支持 PDF、PNG、JPG、JPEG：

```latex
\fig{result.png}
\captiontext{图：结果说明。来源：作者、文献或自己的实验。}
```

也可以写完整相对路径，例如 `\fig{example/images/quadratic.jpg}`。默认图片目录为 `assets/figures/`，旧文档中的 `\fig{amdahl}` 仍读取该目录下的 `amdahl.pdf`。省略扩展名时按 PDF、PNG、JPG、JPEG 顺序查找；明确写扩展名可避免同名文件的歧义。

图片默认居中，宽度不超过当前栏宽，高度不超过正文高度的 58%，保持原始宽高比。根据页面内容修改高度上限：

```latex
\fig[height=.45\textheight]{portrait.jpg}
\fig[width=.8\linewidth,height=3cm]{result.pdf}
```

只填写宽度时，高度上限仍然生效。图注占用单独空间，长图注需要相应降低图片高度。

裁剪必须显式指定。`trim` 的顺序为左、下、右、上，`clip` 执行裁剪：

```latex
\fig[trim=5mm 0mm 5mm 0mm,clip]{photo.jpg}
```

含坐标、图例或证据的图片应保留必要信息。随模板提供的[横图、竖图和双图示例](../example/README.md)可直接替换路径。图片不存在时，编译器会报告缺失文件名；检查路径是否相对于项目根目录，以及文件名大小写。

## 常见版式与自由布局

从[版式目录](../example/README.md)选择完整页面并复制到 `slides/content.tex`。双栏页面使用 `\hitcolumnratio{.5}`、`\hitleftwidth` 和 `\hitrightwidth`，设置一次比例便能改变两栏宽度。比例必须大于 0、小于 1，每页默认恢复为 `.5`。

若要自定义宽度，可以直接用标准 Beamer：

```latex
\begin{frame}{自定义双栏}
  \begin{columns}[T,onlytextwidth]
    \begin{column}{.35\textwidth}
      左侧内容。
    \end{column}
    \begin{column}{.60\textwidth}
      右侧内容。
    \end{column}
  \end{columns}
\end{frame}
```

正文组件包括 `\subhead{小标题}`、`\insight{关键判断}`、`\notebox{条件说明}`、`\captiontext{图注}` 和 `\metric{宽度}{数值}{说明}`。这些组件和布局在两种主题中共享。

代码页保留 `\begin{frame}[fragile]`，参照[代码示例](../example/layouts/11-code.tex)。内容太多时可以减少重复文字、拆页或重新分栏；查看 PDF 确认可读性。

## 封面、强调页和附录

- `\subtitle`、`\englishtitle`、`\titlecontext` 均可整行删除。作者、机构和日期可以根据需要填入；不显示日期时使用 `\date{}`。
- `\TitleSlide` 生成主题封面；`\BlueTitleSlide` 保留经典照片封面入口。
- `\FocusSlide[栏目]{核心判断}` 生成强调页；`\EndSlide{结束语}` 生成结束页。
- `\hitappendix` 进入附录；后续章节不会进入主目录。
- 自定义标识使用 `\hitlogo{图片路径}`，页脚文字使用 `\hitfooter{文字}`，经典视觉素材目录使用 `\hitvi{路径/}`。它们写在导言区。

分享源文件时保留样式文件、字体、图片及其许可。个人汇报内容默认可被 Git 跟踪；将私人内容上传到自己的公开仓库前，请检查待提交文件。
