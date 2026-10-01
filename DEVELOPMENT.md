# 开发与测试指南 (Development & Testing)

本文档面向模板维护者与高级开发者，介绍构建体系、测试套件、插图重新生成以及持续集成配置。
普通模板使用者只需参考根目录下的 [README.md](README.md)，使用随模板分发的预编译资源即可正常编译文档。

---

## 1. 开发环境依赖

本项目在 Windows 和 Linux (Ubuntu) 下均经过完整验证。

### 1.1 系统与 TeX 工具
- **TeX Live 2024+**：必须包含 `xelatex`、`latexmk`、`ctex`、`beamer` 及相关宏包。
- **Poppler**（可选但推荐）：提供 `pdffonts` 工具用于字体嵌入验证。

### 1.2 Python 依赖
执行自动化验证脚本需 Python 3.10+。依赖清单见 `requirements-dev.txt`：
```bash
pip install -r requirements-dev.txt
```
主要依赖包：
- `fonttools`：检查字体文件 SHA-256 与 `OS/2.fsType` 嵌入元数据；
- `pypdf`：解析 PDF 结构、命名目标跳转与页码；
- `pymupdf`：执行像素级页面光栅化渲染测试。

---

## 2. 统一构建与测试入口

### 2.1 构建命令
支持跨平台的 Python 脚本与 Windows PowerShell 脚本：
```bash
# 使用 Python 构建全部发布成品
python build.py --document all

# 或构建单个文档
python build.py --document starter
python build.py --document example

# Windows PowerShell 入口（内部自动处理路径与 UTF-8 编码）
.\build.ps1 -Document all
.\build.ps1 -Document starter
```

### 2.2 运行全量回归测试套件
```bash
python test-suite.py
```
测试套件由 5 个阶段组成，任何异常均会产生非零退出码并报错：
1. **Stage 1 (check-template.py)**：校验 10 个原始字体文件 SHA-256、fsType、分发 PDF 页数、16:9 画幅、编译日志 0 告警，以及字体全部嵌入且无非法系统字体；
2. **Stage 2 (check-agenda.py)**：测试 0、1、2..6、7、9 个章节的目录生成、首次无缓存状态、手动目录、命名目标 1:1 跳转、子章节及 4 类无效输入防御；
3. **Stage 3 (无损切换与语义核对)**：将完整 `example.tex` 与 `starter.tex` 分别在 `hit` 与 `hitacademic` 两个主题下编译，核对 24 项关键语义字段（标题、英文标题、补充信息、重点页、注记、指标、三线表、代码等），确保 0 字段丢失、0 排版溢出告警；
4. **Stage 4 (辅助与矩阵测试)**：验证 4:3 画幅 (`tests/classic-43.tex`)、覆盖层 (`tests/overlay-pages.tex`) 以及 6 组宏包加载顺序矩阵 (`tests/if-*.tex`)；
5. **Stage 5 (光栅化渲染测试)**：使用 PyMuPDF 对所有生成的 123 个页面进行像素级光栅化渲染，验证渲染引擎无崩溃、尺寸有效且无异常空白。

---

## 3. 矢量插图与模型图重新生成

随仓库分发的 `assets/figures/*.pdf` 均为预生成矢量图，普通编译无需重新生成。如需修改绘图模型：

### 3.1 Python 解析模型图 (Amdahl & Roofline)
需要 Python 3 环境及 `matplotlib`、`numpy`：
```bash
python build-plots.py
```
生成的矢量图将直接保存至 `assets/figures/amdahl.pdf` 与 `assets/figures/roofline.pdf`。

### 3.2 Mermaid 流程图 (pipeline.mmd)
流程图源文件为 `assets/figures/pipeline.mmd`。如需重新生成：
```powershell
.\build-diagrams.ps1 -ChromePath 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

---

## 4. 持续集成 (CI)

仓库已配置 GitHub Actions 持续集成工作流 (`.github/workflows/ci.yml`)：
- 在 `ubuntu-latest` 上干净检出；
- 自动化安装 TeX Live 核心宏包与 Python 依赖；
- 自动构建全部文档并运行 `python test-suite.py` 进行端到端回归验证。
