# hiTouyingBeamer

哈尔滨工业大学 Beamer 幻灯片模板。两种主题共用正文和内容组件，通过一行主题声明切换风格。

## 开始写作

1. 安装含 XeLaTeX、latexmk 的 TeX Live 2024 或更新版本。模板附带字体和示例图片，普通编译无需 Python、Node.js 或浏览器。
2. 打开唯一推荐起点 **[starter.tex](starter.tex)**，填写标题、作者、单位和日期。副标题、英文标题和汇报类别均可整行删除。
3. 编辑 **[slides/content.tex](slides/content.tex)**，增删章节和页面。自己的图片放在 `slides/images/`。
4. 按下面的编译命令生成 PDF，检查文字、图片和图注。

## 设置标题层级

| 写法 | 用途 |
| --- | --- |
| `\title[短标题]{完整标题}` | 整份汇报的标题 |
| `\section{章节}` | 章节、目录和导航 |
| `\subsection{子章节}` | 可选的二级分组 |
| `\begin{frame}{页面标题}` | 当前页标题 |
| `\subhead{页内小标题}` | 页内内容分组 |

起步文件默认只显示章节目录并关闭章节过渡页。在主题声明后，使用 `\hitoutlinesubs` 显示子章节，使用 `\hitsectionpages` 开启过渡页。目录标题用 `\OutlineSlide[title={汇报提纲}]` 设置。[完整层级示例与配置说明](docs/USAGE.md#标题层级)。

## 选择版式

打开 **[版式目录](example/README.md)**，查看两种主题的预览，再复制对应的完整页面到正文。

包含单栏要点、左右图文、上图下文、双图对比、双栏与三栏、大图、公式、表格和代码。双栏比例用 `\hitcolumnratio{.6}` 调整，图片高度和对齐方式可单独设置。也可以沿用标准 Beamer 自定义布局。

## 放入图片

```latex
\fig{result.png} % 图片位于 slides/images/，支持 PDF、PNG、JPG、JPEG
\captiontext{图：结果说明。来源：文献或自己的实验。}
```

图片默认等比缩放，并同时限制宽度和高度。调整高度可以写 `\fig[height=.45\textheight]{result.png}`。[路径、竖图、双图和显式裁剪说明](docs/USAGE.md#图片与图注)。

## 切换主题

在 `starter.tex` 中修改这一行，正文保持不变：

```latex
\usetheme{hitacademic} % Academic：蓝色标题栏、浅灰背景
% 或 \usetheme{hit}    % Classic：白底蓝字、校训和经典封面
```

两种主题保留各自的封面、标题栏和导航风格。更换主题或增加内容后查看 PDF，内容超出页面时调整布局或拆页。

## 编译与预览

以下命令均在**项目根目录**运行，只依赖 TeX 工具：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error "-outdir=.work/build" starter.tex
```

输出为 `.work/build/starter.pdf`。使用编辑器时，将 `starter.tex` 设为主文件、选择 XeLaTeX；新增章节后需要多次编译以更新目录。

Windows 可以直接运行：

```powershell
.\build.ps1
```

此入口将成品放到 `slides/starter.pdf`，中间文件仍留在 `.work/`。它也支持 `-Document example`、`-Document layouts` 和 `-Document all`；示例成品放入 `example/preview/`。

## 文件与成品

| 位置 | 用途 |
| --- | --- |
| `starter.tex`、`slides/` | 封面设置、自己的正文与图片 |
| [example/](example/README.md) | 页面版式、完整示例及两种主题的 PDF 预览 |
| [docs/USAGE.md](docs/USAGE.md) | 标题、图片、布局和常用组件 |
| `*.sty`、`fonts/`、`assets/`、`vi/` | 共享功能、主题、字体与素材 |
| `scripts/`、`tests/`、[开发指南](docs/DEVELOPMENT.md) | 构建、验收与维护 |

下载仓库 ZIP 后解压即可使用。维护者也可生成 `dist/hiTouyingBeamer-release.zip`，其中包含源码、指南、字体、图片和双主题预览。分享完整源文件时保留资源的相对目录结构。

编译缓存、日常生成的 PDF、发布压缩包和本地 `CHANGELOG.md` 由 Git 忽略。正式示例预览在 `example/preview/` 随源码提供。

## 许可与来源

模板代码采用 [LPPL-1.3c 或更新版本](LICENSE)，派生自 `hithesis/hiTouyingBeamer`（提交 `a1b947e`），保留上游作者 SchrodingerBlume 的署名。修改历史见 Git 提交记录。

随附字体使用 SIL Open Font License 1.1，详见 [字体说明](fonts/README.md)；图表与校园素材来源见 [资源说明](assets/README.md) 和 [示例图片说明](example/images/README.md)。校徽、校名和校园视觉素材的权利归相应权利人。
