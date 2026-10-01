from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.work/matplotlib'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

font_manager.fontManager.addfont(ROOT / 'fonts/source-sans/SourceSans3-Regular.ttf')
plt.rcParams.update({'font.family': 'Source Sans 3', 'font.size': 13,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'pdf.fonttype': 42})
target = ROOT / 'example/images'
target.mkdir(parents=True, exist_ok=True)
x = np.linspace(0, 1, 101)
for name, y, size, label, extensions in [
    ('linear', x, (6.4, 3.6), 'y = x', ('png', 'pdf')),
    ('quadratic', x ** 2, (3.2, 4.8), 'y = x squared', ('jpg', 'jpeg')),
]:
    fig, ax = plt.subplots(figsize=size, layout='constrained')
    ax.plot(x, y, color='#0070BE', linewidth=2.5)
    ax.set(xlabel='x', ylabel='y', xlim=(0, 1), ylim=(0, 1), title=label)
    ax.grid(alpha=.2)
    for extension in extensions:
        fig.savefig(target / f'{name}.{extension}', dpi=160)
    plt.close(fig)
print('已生成横向线性函数图与竖向平方函数图；均为解析曲线。')
