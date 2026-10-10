# 开发与验收

普通作者从 [README](../README.md) 开始。这里记录维护命令，均从项目根目录执行。

## 环境

需要 TeX Live（XeLaTeX、latexmk）、Poppler 的 `pdffonts` 和 Python 3.10+。安装检查依赖：

```sh
python -m pip install -r scripts/requirements-dev.txt
```

字体校验使用 fontTools，PDF 结构和链接解析使用 pypdf，页面渲染使用 PyMuPDF。图片已随源码提供；仅重新生成解析函数图时需要额外安装 Matplotlib 和 NumPy。

## 构建

```sh
python scripts/build.py --document starter
python scripts/build.py --document all --theme all
```

普通构建遵循源文件的主题，起步成品输出到 `slides/starter.pdf`。三主题构建只在 `.work/` 生成临时入口，不改动用户源文件；九份正式预览输出到 `examples/`。

## 自动检查

```sh
python scripts/test-suite.py
```

检查包括字体原文件校验、PDF 画幅和嵌入字体、编译日志、三主题内容字段、目录真实跳转、目录边界、接口加载顺序、4:3 画幅和覆盖层。顶部导航检查核对章节名称、当前章节高亮及章节首页链接；构建 Minimalist 起步预览后，也可单独运行 `python scripts/check-navigation.py`。作者流程检查补充常见图片格式、图片比例和结论文字可见性。输出证据保存在 `.work/`。

PDF 渲染成功仅表示渲染器能够读取文件；发布前仍应逐页查看九份预览，检查重叠、裁剪、颜色和可读性。不要将机器检查描述为任意用户内容都不会溢出。

本次从新解压包进行的实际操作与结果见[作者流程验收记录](VALIDATION.md)。详细编译日志、检查结论和文件校验值保存在本地 `.work/`。

## 发布包

```sh
python scripts/package.py
```

发布打包需要 Git，并在项目的 Git 工作区中执行。新文件先纳入版本控制并核对待提交清单。打包前重新生成九份预览，随后仅收集 Git 跟踪的项目文件，未跟踪的个人资料和编译缓存不进入 ZIP。

发布包包含起步文档、示例、主题、字体、图片、指南和维护工具。程序在新的隔离目录中编译三种主题，检查字体、文档链接、作者流程、图片比例、目录跳转及结论框可见性。全部通过后才替换正式 ZIP，并记录每个源文件和压缩包的 SHA-256。

最终 ZIP 为 `dist/hiTouyingBeamer-release.zip`，本地验收记录保存到 `.work/`，均不纳入 Git。

## 重新生成图片

```sh
python scripts/build-sample-images.py
python scripts/build-plots.py
```

Mermaid 源文件为 `assets/figures/pipeline.mmd`。需要重新生成时，在 Windows 上运行：

```powershell
.\scripts\build-diagrams.ps1 -ChromePath 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

普通模板编译无需执行这些命令。

## 提交与贡献

构建、测试和发布验收均在本地执行，仓库不包含 GitHub Actions 工作流。提交前运行上述测试和打包命令，并查看生成的 PDF 与检查结果。

提交前检查文件清单，保留版权和资源许可。改动按独立功能提交，预览随源码更新；本地详细工作记录可以保存在已忽略的 `CHANGELOG.md`。新增布局应在三种主题（classic / touying / minimalist）下使用同一份正文。
