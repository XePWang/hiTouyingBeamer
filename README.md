# hiTouyingBeamer

**预览**：[现代主题（默认，16:9）](template.pdf)　·　[经典主题（`classic` 选项，4:3）](template-classic.pdf)

哈尔滨工业大学 Beamer 幻灯片模板。各主题共用正文和内容组件，仅通过一行主题声明即可切换外观风格。

本主题的现代风格灵感来自于上海交通大学 Touying 幻灯片主题（[touying-simpl-sjtu](https://github.com/sjtug/touying-sjtu)）。

## 开始写作

1. 安装含 XeLaTeX、latexmk 的 TeX Live 2023 或更新版本。模板采用标准 TeX 环境，普通编译无需 Python、Node.js 或外部依赖。
2. 打开推荐起步入口 **[starter.tex](starter.tex)**，填写标题、作者、单位和日期。副标题、英文标题等均可按需选填或整行删除。
3. 编辑 **[slides/content.tex](slides/content.tex)**，增删章节和页面。自己的图片放置在 `slides/images/`。
4. 按下方常规编译命令生成 PDF，检查文字、图片和排版效果。

## 设置标题层级

| 写法 | 用途 |
| --- | --- |
| `\title[短标题]{完整标题}` | 整份汇报的标题（方括号短标题用于页脚或导航） |
| `\section{章节}` | 章节划分，自动生成目录条目与顶部导航 |
| `\subsection{子章节}` | 可选的二级分组 |
| `\begin{frame}{页面标题}` | 当前幻灯片页面标题 |
| `\subhead{页内小标题}` | 页面内部的内容小标题 |

起步文件默认只显示一级章节目录，不自动插入多余过渡页。在主题声明后，使用 `\hitoutlinesubs` 显示子章节，使用 `\hitsectionpages` 开启过渡页。目录标题可通过 `\renewcommand{\hitoutlinetitle}{汇报提纲}` 或 `\OutlineSlide[title={汇报提纲}]` 设置。详见 [使用文档](docs/USAGE.md#标题层级)。

## 选择版式

打开 **[版式目录](example/README.md)**，查看版式效果并复制完整页面代码到自己的正文：

涵盖单栏要点、左右图文、左图右文、上图下文、双图对比、双栏与三栏、大图加图注、公式说明、表格以及代码展示。双栏比例可用 `\hitcolumnratio{.6}` 调整，图片高度上限与对齐方式均支持自定义，同时完全兼容标准 Beamer 环境。

## 放入图片

```latex
\fig{result.png} % 图片位于 slides/images/，支持 PDF、PNG、JPG、JPEG
\captiontext{图：结果说明。来源：文献或实验结果。}
```

图片默认等比缩放并限制在可用版心尺寸内。设置高度上限可写 `\fig[height=.45\textheight]{result.png}`。详见 [图片与图注说明](docs/USAGE.md#图片与图注)。

## 切换主题

在导言区仅需修改主题声明，正文内容保持完全一致：

```latex
\usetheme{hit}                 % 现代主题（默认，等同于 \usetheme[touying]{hit}）
\usetheme[classic]{hit}        % 经典主题（移植自旧 HITBeamer 观感）
\usetheme[minimalist]{hit}     % 极简主题（带顶部章节导航与浅灰画布，原 Academic 风格）
```

### 通用选项

选项写在 `\usetheme[...]` 方括号内，支持叠加组合：

```latex
\usetheme[classic,minted]{hit} % 经典主题 + minted 代码高亮
\usetheme[top]{hit}            % 正文顶端对齐（默认垂直居中）
\usetheme[serif]{hit}          % 启用衬线字体（经典主题默认）
\usetheme[sans]{hit}           % 启用非衬线字体（现代主题默认）
\usetheme[navsymbols]{hit}     % 显示右下角翻页按钮（默认隐藏）
\usetheme[nosectionpage]{hit}  % 不自动生成章节过渡页
```

## 专用命令

| 命令 | 说明 |
| --- | --- |
| `\TitleSlide` / `\BlueTitleSlide` | 默认风格标题页 / 蓝色照片封面页 |
| `\OutlineSlide` | 目录页（支持 `\OutlineSlide[title={...}]` 或 `\hitoutlinetitle` 修改标题） |
| `\FocusSlide{...}` | 强调过渡页（全屏主色底、大字提示，可选 `\FocusSlide[标签]{...}`） |
| `\EndSlide{...}` | 致谢结束页 |
| `\subhead{...}` | 内容小标题 |
| `\captiontext{...}` | 图表或说明注释 |
| `\insight{...}` | 核心结论高亮块 |
| `\notebox{...}` | 带竖线的说明提示框 |
| `\fig[选项]{路径}` | 等比受限插图命令 |
| `\hitcolumnratio{比例}` | 调整左右分栏比例（例如 `.6` 表示左栏占 60%） |
| `\hitfooter{...}` | 自定义页脚文字 |
| `\themetitle` / `\themeauthor` | 当前主题预置的标题与作者 |

## 编译方法

常规编译仅依赖标准 TeX Live 工具，在项目根目录下执行：

```sh
# 编译起步文档
latexmk -xelatex starter.tex

# 编译完整回归模板（含 biber 参考文献）
latexmk -xelatex template.tex
```

若开启 `minted` 选项，编译命令需增加 `-shell-escape`：
```sh
latexmk -xelatex -shell-escape template.tex
```

Windows 环境亦可直接运行提供的辅助脚本：
```powershell
.\build.ps1
```

## 发布与测试

- **生成预览**：发布前运行 `./build-previews.sh`，脚本将自动检测各主题头部的 `%% Preview:` 标记并在临时目录中完成编译并更新对应预览 PDF。
- **本地自测**：运行 `./tests/ci.sh` 进行跨主题公开命令覆盖率检查与主题编译验证；使用 `./tests/ci.sh --base <上游基线目录>` 进行逐页回归像素比对。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 文件结构

| 路径 | 说明 |
| --- | --- |
| `starter.tex` | 唯一推荐起步文件 |
| `slides/` | 用户正文（`content.tex`）与插图目录（`images/`） |
| `example/` | 页面版式库（`layouts/`）、示例报告与预览产物 |
| `beamerthemehit.sty` | 主题统一入口与选项分派 |
| `beamercmdhit.sty` | 跨主题共享公开命令层 |
| `beamerthemehitouying.sty` | 现代主题实现（默认） |
| `beamerthemehitclassic.sty` | 经典主题实现 |
| `beamerthemehitminimalist.sty` | 极简主题实现（原 Academic 风格） |
| `vi/` | 哈工大视觉形象基础素材（矢量校徽、主楼等） |
| `tests/` | 命令可用性测试与回归验证套件 |

## 许可与来源

本模板代码遵循 [LaTeX Project Public License (LPPL) 1.3c 或更新版本](LICENSE)，派生自 [hithesis/hiTouyingBeamer](https://github.com/hithesis/hiTouyingBeamer)，保留上游作者 SchrodingerBlume 的署名与维护声明。修改历史详见 Git 提交记录。

随附字体遵循 SIL Open Font License 1.1（详见 `fonts/README.md`）；视觉标识资源版权归哈尔滨工业大学所有。
