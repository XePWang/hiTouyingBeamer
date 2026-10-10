# 贡献指南

欢迎提 issue 和 PR。CI（`.github/workflows/ci.yml`）会跑 `tests/ci.sh`，本地也可以先跑一遍。

## 硬规则（CI 会查）

### 1. 新增命令必须在所有主题下都可以用

公开命令统一定义在共用命令层 `beamercmdhit.sty`，不要定义只有某个主题能用的命令；
确实与主题相关的外观，放到 `styles/` 下的主题文件里用模板/颜色实现，而不是新命令。

CI 会扫描所有 `.sty` 里的公开命令（`\newcommand`、`\providecommand`、`\def`，排除带
`@` 的内部名），逐主题用 `\ifcsname` 探测，缺一个就不通过。新命令请同时：

- 加进 `tests/commands.tex`（真实调用一遍）；
- 在 README 的命令表里记一笔；
- 确认它在 `\usetheme{hit}`、`\usetheme[classic]{hit}` 和 `\usetheme[minimalist]{hit}` 下行为一致，除非有意为之。

### 2. 主题输出变化必须人工审核

CI 会把 PR 的每个主题与目标分支逐页对比（同环境各编一遍，渲染成图后逐页比对），
任何一页有变化都会失败，并把两份 PDF 传到 `ci-out/` 供查看。这是设计如此，不是误报。

- 如果是**有意**的视觉改动：维护者审核产物后，给 PR 打上 `theme-output-change`
  标签再跑一次，回归检查放行。合并后，新输出就是后续 PR 的对照基准。
- 如果是**无意**的变化：请修到逐页一致再提交。

### 3. 发布流程

- **版本号**：所有 `.sty` 的 `\ProvidesPackage` 与 `template.tex` 的 `\subtitle`
  同步更新（格式 `v2.2026a` 这样），CI 会核对一致。
- **预览 PDF**：发布前跑一次 `./build-previews.sh`，把 `examples/template.pdf`（现代 16:9）、
  `examples/template-classic.pdf`（经典 4:3）和 `examples/template-minimalist.pdf`（极简 16:9）更新进仓库。README 顶部的预览入口指向它们。
- **新增主题**：在 `styles/` 目录加 `beamerthemehit<名字>.sty`，在文件头写标记
  `%% Preview: theme=<名字> aspectratio=<169|43> output=<预览文件名>`；
  `build-previews.sh` 与 CI 会自动发现，不用改脚本。
- 打 tag（如 `v2.2026a`）并推送。

提交信息用 `feat:` / `fix:` / `docs:` 前缀加中文描述；版本 bump 单独一行
`bump: vX -> vY`。

## 本地自测

```console
./tests/ci.sh                    # 命令跨主题检查 + 各主题编译 + 版本/标记检查
./tests/ci.sh --base <旧版目录>   # 再加逐页回归对比
```

需要 TeX Live（XeLaTeX + biber）和 poppler（`pdftoppm`）。
