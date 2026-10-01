import os
from pathlib import Path

root = Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(root / '.work' / 'matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

font_manager.fontManager.addfont(root / 'fonts/source-sans/SourceSans3-Regular.ttf')
font_manager.fontManager.addfont(root / 'fonts/source-sans/SourceSans3-Bold.ttf')
plt.rcParams.update({
    'font.family': 'Source Sans 3', 'font.size': 11, 'axes.labelsize': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#93A6B4', 'text.color': '#263B4D',
    'axes.labelcolor': '#263B4D', 'xtick.color': '#526779', 'ytick.color': '#526779',
    'figure.facecolor': '#F7F9FB', 'axes.facecolor': '#F7F9FB',
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.axisbelow': True,
})
target = root / 'assets' / 'figures'
target.mkdir(parents=True, exist_ok=True)

p = np.linspace(1, 64, 400)
fig, ax = plt.subplots(figsize=(7.0, 3.6), layout='constrained')
for f, color in [(0.90, '#BD5A32'), (0.95, '#0070BE'), (0.99, '#287763')]:
    ax.plot(p, 1 / (1 - f + f / p), color=color, lw=2.4, label=f'f = {f:.2f}')
ax.set(xlim=(1, 64), ylim=(0, 42), xlabel='Parallel resources  p', ylabel='Speedup  S(p)')
ax.set_xticks([1, 8, 16, 32, 48, 64])
ax.grid(axis='y', color='#D5E0E8', linewidth=.7)
ax.legend(frameon=False, loc='upper left', ncol=1)
ax.text(.98, .03, 'Analytical model: zero overhead', transform=ax.transAxes,
        ha='right', va='bottom', fontsize=9, color='#526779')
fig.savefig(target / 'amdahl.pdf', metadata={'Title': 'Amdahl analytical model', 'Creator': 'hiTouyingBeamer'})
plt.close(fig)

x = np.logspace(-2, 2, 400)
fig, ax = plt.subplots(figsize=(6.8, 3.8), layout='constrained')
ax.loglog(x, np.minimum(1, x), color='#0070BE', lw=3)
ax.axvline(1, color='#BD5A32', ls='--', lw=1.3)
ax.fill_between(x, .006, np.minimum(1, x), color='#0070BE', alpha=.07)
ax.text(.14, .45, 'Bandwidth bound', transform=ax.transAxes, color='#0070BE', fontsize=12)
ax.text(.64, .87, 'Compute bound', transform=ax.transAxes, color='#0070BE', fontsize=12)
ax.set(xlim=(.01, 100), ylim=(.008, 1.8),
       xlabel='Normalized arithmetic intensity  x = B I / Pmax',
       ylabel='Normalized performance  r = P / Pmax')
ax.grid(which='major', color='#D5E0E8', linewidth=.7)
fig.savefig(target / 'roofline.pdf', metadata={'Title': 'Normalized Roofline analytical model', 'Creator': 'hiTouyingBeamer'})
plt.close(fig)
print('已生成 Amdahl 与归一化 Roofline 解析模型图。')
