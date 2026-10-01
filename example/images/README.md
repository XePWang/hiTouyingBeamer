# 示例图片

| 文件 | 内容 | 比例与格式 |
| --- | --- | --- |
| `linear.png`、`linear.pdf` | $y=x$，$0\leq x\leq1$ | 16:9 横图，PNG / PDF |
| `quadratic.jpg`、`quadratic.jpeg` | $y=x^2$，$0\leq x\leq1$ | 2:3 竖图，JPG / JPEG |

这些图由 `scripts/build-sample-images.py` 根据函数定义生成，采用项目的 LPPL-1.3c 或更新版本许可，使用随附的 Source Sans 3 字体。图片用于演示插图比例和格式，函数曲线由公式计算。

维护者重新生成时需要 Python、Matplotlib 和 NumPy；普通作者直接使用已生成的文件即可。
