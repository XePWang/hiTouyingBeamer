# hiTouyingBeamer

用于论文阅读、研究进展与学术答辩的现代哈尔滨工业大学 Beamer 幻灯片模板。

模板原生支持两种风格，**正文、章节、公式、表格、代码、图表与元数据 100% 共享**，用户仅需修改主题声明行即可自由切换：
- `\usetheme{hitacademic}`：**Academic 风格**（蓝色标题栏、浅灰画布、顶部章节导航、双语封面与结构化内容组件）
- `\usetheme{hit}`：**Classic 经典主题**（上游经典白底蓝字风格、校徽校训与大号章节过渡页）

---

## 快速上手（5 步完成汇报）

### 1. 准备 TeX 环境
推荐安装标准 **TeX Live 2024+**（Windows、macOS 或 Linux 均可）。确保系统环境变量中包含 `xelatex` 与 `latexmk`。  
模板自带所需的开源字体与预生成矢量图，普通用户**无需安装** Python、Node.js 或 Chrome。

### 2. 打开推荐起步文档
打开根目录下的唯一推荐起点：**`starter.tex`**。

### 3. 修改标题与正文
在文档头部填写汇报信息，并在正文中填入自己的内容：
```latex
\documentclass[aspectratio=169,11pt,fontset=none]{ctexbeamer}
\usetheme{hitacademic} % 主题选择：hitacademic 或 hit

\title[短标题]{中文研究标题}
\subtitle{标准副标题}
\englishtitle{English Research Title}
\titlecontext{学术汇报 · 快速起步}
\author{汇报人：张三\qquad 学号：2026xxxxxx}
\institute{哈尔滨工业大学}
\date{\today}
```

### 4. 自由切换主题
若希望使用经典风格，只需将主题声明改为：
```latex
\usetheme{hit}
```
正文中的 `\subhead`、`\insight`、`\notebox`、`\metric`、公式、表格与代码均无需改动，编译绝无语法错误或排版溢出。

### 5. 编译并预览
使用提供的跨平台构建脚本进行编译：
```bash
# 跨平台 Python 入口
python build.py --document starter

# 或 Windows PowerShell 入口
.\build.ps1 -Document starter
```
编译完成后，直接在当前目录打开 `starter.pdf` 查看演示文稿预览。

---

## 统一构建与测试入口

模板提供标准化的构建工具，构建产物中间文件集中存放于 `.work/w/`，保持工作区干净：

```bash
# 构建完整 22 页学术示例（包含丰富图表、模型与代码）
python build.py --document example

# 一键构建全部发布成品 PDF
python build.py --document all

# 运行完整的 5 阶段自动化回归测试套件
python test-suite.py
```
> 高级开发、测试与图表生成细节请参阅 [DEVELOPMENT.md](DEVELOPMENT.md)。

---

## 公开配置与内容接口

所有公开接口**均不含 `@` 符号**，支持在文档前导区或正文任意位置直接调用：

### 1. 资产与路径配置
| 配置命令 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `\hitfigures{路径/}` | 矢量插图与图表所在目录 | `assets/figures/` |
| `\hitvi{路径/}` | 经典主题视觉资产目录（校徽、校训等） | `vi/` |
| `\hitlogo{路径}` | 封面与页眉使用的校名/机构标识 | `assets/hit-logo.png` |
| `\hitfooter{文字}` | 页脚左侧自定义文字 | 自动继承机构名或短标题 |
| `\hitoutlinetitle{标题}` | 目录页标题文字 | 默认“目录” |

### 2. 整页命令
- `\TitleSlide`：生成封面页（Academic 主题生成双语标识封面；Classic 主题生成白色主楼封面）；
- `\BlueTitleSlide`：经典校园照片蓝色彩条封面（Academic 主题下自动平滑兼容）；
- `\OutlineSlide` 或 `\OutlineSlide[title=Outline,subtitle=CONTENTS]`：自动收集正文各章节，生成自适应排版的目录页；
- `\AgendaSlide[title=...,subtitle=...]{...}` 与 `\AgendaItem[目标]{标题}`：手动规划路线目录页；
- `\FocusSlide[可选栏目]{核心结论句}`：全页主色强调页，用于突出关键论点；
- `\EndSlide{结束语}`：学术汇报结束致谢页。

### 3. 结构化内容组件
- `\subhead{小标题}`：带主题强调色的小标题；
- `\insight{结论}`：浅色背景重点结论展示区；
- `\notebox{条件与边界}`：左侧带 2 pt 竖线的严谨注记框；
- `\metric{宽度}{数值}{说明}`：大字号量化指标展示卡片；
- `\captiontext{图注说明}`：图表下方的说明文字；
- `\fig[参数]{文件名}`：直接从插图目录引入矢量图；
- `\hitappendix` 或 `\appendix`：标准附录入口，自动管理页码与页眉。

---

## 两种主题特性对比

| 项目 | `hitacademic` (Academic 风格) | `hit` (Classic 经典主题) |
| :--- | :--- | :--- |
| **视觉基调** | 现代扁平，浅灰画布 (`#F7F9FB`) | 经典传统，纯白画布 |
| **标题栏** | 深蓝底白色粗体标题栏 | 顶部圆点导航，标题加下划横线与校训 |
| **页眉装饰** | 校名标识加章节胶囊导航 | 一行章节名配逐帧圆点导航 |
| **目录版式** | 2–6 项自动采用左侧色块+双胶囊横条，其余自动列表 | 大号序号列表，多章节与子章节智能双栏分流 |
| **排版约束** | 统一正文可用区域，同一字号层级 | 统一正文可用区域，同一字号层级 |
| **正文切换** | **仅需更改 `\usetheme`，正文代码完全兼容，零修改** | **仅需更改 `\usetheme`，正文代码完全兼容，零修改** |

---

## 目录结构说明

```text
hiTouyingBeamer/
├── starter.tex                   # 【唯一推荐起点】起步简洁演示文稿
├── starter.pdf                   # 起步文档对应的预览成品 (7 页)
├── example.tex                   # 完整学术汇报示例（含图表、代码、公式与附录）
├── example.pdf                   # 完整示例对应的预览成品 (22 页)
├── agenda-gallery.tex/.pdf       # 目录排版全景图 (6 页)
│
├── beamerthemehitacademic.sty   # Academic 主题视觉样式
├── beamerthemehit.sty           # Classic 经典主题视觉样式
├── beamercmdhit.sty             # 统一公共命令层与模板槽位
├── hit-content.sty              # 共享依赖、统一字号与内容组件核心层
├── hit-outline.sty              # 目录数据收集、多页均分与渲染调度
├── hit-fonts.sty                # 开源字体加载配置
│
├── assets/                      # 矢量图表、校名标识与绘图源码
├── fonts/                       # 随模板分发的开源正版字体 (OFL)
├── vi/                          # 经典主题原有视觉形象素材
├── tests/                       # 单元与矩阵回归测试源码
│
├── build.py / build.ps1         # 统一跨平台构建脚本
├── test-suite.py                # 5 阶段完整自动化回归测试套件
├── check-template.py            # 成品规范与字体嵌入校验脚本
├── check-agenda.py              # 目录系统专属测试脚本
├── requirements-dev.txt         # 开发与 CI 依赖清单
├── DEVELOPMENT.md               # 开发者与维护测试指南
├── CHANGELOG.md                 # 变更记录
└── LICENSE                      # LPPL-1.3c 开源许可证
```

---

## 许可证与致谢

- 模板样式、组件与正文代码采用 **LaTeX Project Public License 1.3c** 或更新版本，详见 [LICENSE](LICENSE)。
- 本项目派生自哈尔滨工业大学 Beamer 模板 `hithesis/hiTouyingBeamer`（提交 `a1b947e`），原作者与维护者为 **SchrodingerBlume**。感谢原作者的杰出贡献。
- 随模板分发的中西文字体（思源黑体、Source Sans 3、JetBrains Mono）均在 **SIL Open Font License 1.1** 下分发，详见 `fonts/README.md`。
- 哈尔滨工业大学校徽、校名标识等视觉资产版权归哈尔滨工业大学所有。
