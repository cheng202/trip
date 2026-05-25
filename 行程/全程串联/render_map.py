#!/usr/bin/env python3
"""Render the 78-day Wuhan grand loop as a static PNG map."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# (lat, lon, label, phase)
POINTS = [
    # ① 湘渝贵滇 自驾 (purple)
    (30.5934, 114.3046, "武汉(起)", "start"),
    (29.3155, 110.4790, "张家界",   "p1"),
    (29.5630, 106.5516, "重庆",     "p1"),
    (26.5832, 107.9774, "千户苗寨", "p1"),
    (26.8721, 100.2299, "丽江",     "p1"),
    (27.6916, 100.7544, "泸沽湖D22","p1"),
    # ★ 衔接 A (teal)
    (25.6938, 100.1645, "大理",     "bridge"),
    (25.0389, 102.7183, "昆明寄车", "bridge"),
    # ② 东南亚 飞行 (amber dashed)
    (21.0285, 105.8542, "河内",     "p2"),
    (10.7769, 106.7009, "胡志明",   "p2"),
    (13.7563, 100.5018, "曼谷",     "p2"),
    (18.7883, 98.9853,  "清迈",     "p2"),
    (3.1390,  101.6869, "吉隆坡",   "p2"),
    (1.2802,  103.8569, "新加坡",   "p2"),
    # ★ 衔接 B (teal)
    (25.0389, 102.7183, "昆明取车", "bridge"),
    (23.6196, 102.8265, "建水",     "bridge"),
    (23.0957, 102.7700, "元阳梯田", "bridge"),
    (23.9021, 106.6404, "百色",     "bridge"),
    (22.8170, 108.3669, "南宁",     "bridge"),
    # ③ 沿海五省 自驾 (red)
    (25.27,   110.30,   "桂林",     "p3"),
    (21.48,   109.12,   "北海",     "p3"),
    (23.13,   113.27,   "广州",     "p3"),
    (22.54,   114.09,   "深圳",     "p3"),
    (22.20,   113.54,   "澳门",     "p3"),
    (23.66,   116.62,   "潮汕",     "p3"),
    (24.48,   118.09,   "厦门",     "p3"),
    (29.33,   120.08,   "义乌",     "p3"),
    (30.27,   120.15,   "杭州",     "p3"),
    (31.24,   121.50,   "上海",     "p3"),
    (31.30,   120.62,   "苏州",     "p3"),
    (32.06,   118.80,   "南京",     "p3"),
    (30.5934, 114.3046, "武汉(终)", "end"),
]

COLORS = {
    "start":  "#3B6D11",
    "end":    "#A32D2D",
    "p1":     "#534AB7",
    "bridge": "#0F6E56",
    "p2":     "#BA7517",
    "p3":     "#c0392b",
}

# Set Chinese font (macOS)
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Hiragino Sans GB", "Songti SC", "STHeiti", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(14, 11), dpi=140)
ax.set_facecolor("#f5f3ee")
fig.patch.set_facecolor("#ffffff")

# Draw subtle latitude/longitude grid box
ax.set_xlim(96, 124)
ax.set_ylim(-2, 33)
ax.set_aspect(1.15)  # rough mercator-ish stretch

# Add background "ocean" rectangle and "land" hint
ax.axhspan(-5, 35, color="#e8eef3", zorder=0)

# Phase line segments
def draw_segment(idx_from, idx_to, color, dashed=False, linewidth=3.0, alpha=0.85):
    xs = [POINTS[i][1] for i in range(idx_from, idx_to + 1)]
    ys = [POINTS[i][0] for i in range(idx_from, idx_to + 1)]
    style = "--" if dashed else "-"
    ax.plot(xs, ys, style, color=color, linewidth=linewidth, alpha=alpha, zorder=2,
            solid_capstyle="round", solid_joinstyle="round",
            dash_capstyle="round")

# ① P1: 0-5 (武汉 → 泸沽湖)
draw_segment(0, 5, COLORS["p1"])
# ★ A: 5-7 (泸沽湖 → 昆明寄车), teal
draw_segment(5, 7, COLORS["bridge"], dashed=False, linewidth=2.5)
# ② P2: 7-13 (昆明寄车 → 新加坡), amber dashed (flight)
draw_segment(7, 13, COLORS["p2"], dashed=True, linewidth=2.0, alpha=0.7)
# Special: SG → KMG return flight (13 → 14)
ax.plot([POINTS[13][1], POINTS[14][1]], [POINTS[13][0], POINTS[14][0]],
        "--", color=COLORS["p2"], linewidth=2.0, alpha=0.7, zorder=2)
# ★ B: 14-18 (昆明取车 → 南宁)
draw_segment(14, 18, COLORS["bridge"], dashed=False, linewidth=2.5)
# ③ P3: 18-31 (南宁 → 武汉)
draw_segment(18, 31, COLORS["p3"])

# Plot points
for i, (lat, lon, name, phase) in enumerate(POINTS):
    c = COLORS[phase]
    # Bigger marker for start/end
    if phase in ("start", "end"):
        size = 280
        edge = "white"
        ew = 2.5
    else:
        size = 140
        edge = "white"
        ew = 1.5
    ax.scatter(lon, lat, s=size, color=c, edgecolors=edge, linewidth=ew, zorder=5)
    # number label inside dot
    no = i + 1
    ax.text(lon, lat, str(no), ha="center", va="center", color="white",
            fontsize=7.5, fontweight="bold", zorder=6)

# Custom label positions to avoid overlap
LABEL_OFFSETS = {
    "武汉(起)":   (0.6, 0.6),
    "张家界":     (-1.0, 0.5),
    "重庆":       (-1.0, 0.5),
    "千户苗寨":   (-1.4, -0.5),
    "丽江":       (-1.4, 0.5),
    "泸沽湖D22":  (0.5, 0.5),
    "大理":       (-1.3, -0.7),
    "昆明寄车":   (0.5, -0.7),
    "河内":       (0.5, 0.4),
    "胡志明":     (0.5, 0.0),
    "曼谷":       (-1.4, 0.4),
    "清迈":       (-1.3, 0.4),
    "吉隆坡":     (0.5, 0.0),
    "新加坡":     (0.5, -0.6),
    "昆明取车":   (-1.6, 0.5),
    "建水":       (-1.3, -0.6),
    "元阳梯田":   (-1.8, -0.6),
    "百色":       (-0.5, -0.7),
    "南宁":       (-1.3, -0.7),
    "桂林":       (-1.3, 0.4),
    "北海":       (-1.3, -0.7),
    "广州":       (-1.2, -0.7),
    "深圳":       (0.5, -0.7),
    "澳门":       (-1.3, -0.7),
    "潮汕":       (0.5, -0.6),
    "厦门":       (0.5, -0.4),
    "义乌":       (0.5, 0.5),
    "杭州":       (0.5, 0.0),
    "上海":       (0.5, 0.4),
    "苏州":       (-1.3, 0.5),
    "南京":       (-1.3, 0.5),
    "武汉(终)":   (-1.4, -0.7),
}

for lat, lon, name, phase in POINTS:
    dx, dy = LABEL_OFFSETS.get(name, (0.4, 0.4))
    ax.annotate(name, xy=(lon, lat), xytext=(lon + dx, lat + dy),
                fontsize=8.5, color="#2c2c2a", zorder=7,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.75))

# Title
fig.suptitle("武汉大环线 · 78 天全串联", fontsize=20, fontweight="bold", y=0.97, color="#2c2c2a")
ax.set_title("湘渝贵滇 22 天 + 云南衔接 2 天 + 东南亚 4 国 20 天 + 云南→广西 5 天 + 沿海五省 29 天",
             fontsize=11, color="#5f5e5a", pad=10)

# Legend
legend_items = [
    Line2D([0], [0], color=COLORS["p1"], lw=3, label="① 湘渝贵滇 自驾 (22d)"),
    Line2D([0], [0], color=COLORS["bridge"], lw=2.5, label="★ 云南衔接段 (6d 含两段)"),
    Line2D([0], [0], color=COLORS["p2"], lw=2.0, linestyle="--", label="② 东南亚 飞行 (20d)"),
    Line2D([0], [0], color=COLORS["p3"], lw=3, label="③ 沿海五省 自驾 (29d)"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["start"],
           markersize=11, label="起点 武汉"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["end"],
           markersize=11, label="终点 武汉"),
]
ax.legend(handles=legend_items, loc="lower left", fontsize=9.5, frameon=True,
          facecolor="white", edgecolor="#d0d0d0", framealpha=0.95)

# Footnote
ax.text(0.99, 0.005, "数据来源：高德 MCP + 携程问道  ·  生成：travel 仓 render_map.py",
        transform=ax.transAxes, fontsize=8, color="#888780",
        ha="right", va="bottom")

# Grid + axis styling
ax.grid(True, color="#d0d0d0", linewidth=0.4, alpha=0.6, linestyle=":")
ax.set_xlabel("经度 °E", fontsize=9, color="#888780")
ax.set_ylabel("纬度 °N", fontsize=9, color="#888780")
ax.tick_params(colors="#888780", labelsize=8)
for spine in ax.spines.values():
    spine.set_color("#cccccc")
    spine.set_linewidth(0.5)

plt.tight_layout()
output_path = "/Users/snowwang/work/travel/行程/全程串联/wuhan-grand-loop-map.png"
plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Generated: {output_path}")
