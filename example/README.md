# 选择页面版式

先看 [Minimalist 预览](../examples/layouts-minimalist.pdf)、[Touying 预览](../examples/layouts-touying.pdf) 或 [Classic 预览](../examples/layouts-classic.pdf)，再打开对应源码。每份源码都是一个完整的 `frame`，复制到 `slides/content.tex` 即可使用。只复制页面，不需要复制导言区。

| 预览页 | 版式和源码 | 适用场景 | 常用调整 |
| --- | --- | --- | --- |
| 1 | [单栏要点](layouts/01-bullets.tex) | 问题、概念、结论 | 要点数量、小标题 |
| 2 | [左文右图](layouts/02-text-image.tex) | 解释图中机制或结果 | 左栏占比、图片高度 |
| 3 | [左图右文](layouts/03-image-text.tex) | 竖图、照片及说明 | 左栏占比、垂直对齐 |
| 4 | [上图下文](layouts/04-image-top.tex) | 宽图与简短解释 | 图片高度 |
| 5 | [双图对比](layouts/05-two-images.tex) | 条件或结果比较 | 两侧比例、相同高度上限 |
| 6 | [双栏内容](layouts/06-two-columns.tex) | 两个方案或两个方面 | 左栏占比 |
| 7 | [三栏内容](layouts/07-three-columns.tex) | 简短并列信息 | 每栏宽度 |
| 8 | [大图加图注](layouts/08-full-image.tex) | 需要细读的结果图 | 图片高度、图注 |
| 9 | [公式与说明](layouts/09-equation.tex) | 定义、模型、符号 | 公式、说明、左右比例 |
| 10 | [表格与说明](layouts/10-table.tex) | 数值或条件比较 | 表头、行和列 |
| 11 | [代码与说明](layouts/11-code.tex) | 解释实现 | 语言和代码；保留 `fragile` |

每页注释标明适用场景和替换位置。图注中的“来源”需要随自己的图片一起修改。函数图来自明确的解析关系，未表示实验测量结果。

## 常用调整

- `\hitcolumnratio{.6}` 表示左栏占两栏可用宽度的 60%；左右宽度和栏间距自动计算。每页默认 `.5`，只在需要时修改。
- `columns` 的 `[T,onlytextwidth]` 为顶部对齐，`[c,onlytextwidth]` 为垂直居中。
- `\fig[height=.45\textheight]{图片路径}` 设置图片高度上限；同时保留栏宽限制，图片等比缩放。
- 三栏示例沿用标准 `column` 宽度，宽度之和小于 `\textwidth`，留下栏间距。

所有页面均可继续使用标准 Beamer 的 `frame`、`columns`、`block`、`itemize`。内容超出一页时，优先减少重复文字、调整分栏或拆页，并查看生成的 PDF。

## 文件用途

`layouts/` 保存可复制的页面，`layouts.tex` 用来编译整套版式预览。`images/` 保存随附函数图，`../examples/` 保存三种主题的成品。作者自己的页面和图片放在 `slides/`。

| 成品 | Minimalist | Touying | Classic | 源文件 |
| --- | --- | --- | --- | --- |
| 起步文档 | [预览](../examples/starter-minimalist.pdf) | [预览](../examples/starter-touying.pdf) | [预览](../examples/starter-classic.pdf) | [starter.tex](../starter.tex) |
| 完整学术示例 | [预览](../examples/example-minimalist.pdf) | [预览](../examples/example-touying.pdf) | [预览](../examples/example-classic.pdf) | [main.tex](main.tex)、`report/` |
| 常见页面版式 | [预览](../examples/layouts-minimalist.pdf) | [预览](../examples/layouts-touying.pdf) | [预览](../examples/layouts-classic.pdf) | [layouts.tex](layouts.tex)、`layouts/` |

[agenda.tex](agenda.tex) 展示不同目录排版，[legacy.tex](legacy.tex) 保留经典接口的使用示例。它们用于参考，日常写作继续从 `starter.tex` 开始。
