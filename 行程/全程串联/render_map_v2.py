#!/usr/bin/env python3
"""V2 render — larger canvas, smart label routing, callout lines for clusters."""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# (lat, lon, label, phase, day-tag)
POINTS = [
    (30.5934, 114.3046, "武汉", "start", "D1 / D78"),
    (29.3155, 110.4790, "张家界",   "p1", "D1-3"),
    (29.5630, 106.5516, "重庆",     "p1", "D5-7"),
    (26.5832, 107.9774, "千户苗寨", "p1", "D11"),
    (26.8721, 100.2299, "丽江",     "p1", "D20-21"),
    (27.6916, 100.7544, "泸沽湖",   "p1", "D22"),
    (25.6938, 100.1645, "大理",     "bridge", "D23"),
    (25.0389, 102.7183, "昆明寄车", "bridge", "D24"),
    (21.0285, 105.8542, "河内",     "p2", "D25"),
    (10.7769, 106.7009, "胡志明",   "p2", "D31"),
    (13.7563, 100.5018, "曼谷",     "p2", "D32-34"),
    (18.7883, 98.9853,  "清迈",     "p2", "D35-36"),
    (3.1390,  101.6869, "吉隆坡",   "p2", "D39-40"),
    (1.2802,  103.8569, "新加坡",   "p2", "D42-44"),
    (25.0389, 102.7183, "昆明取车", "bridge", "D45"),
    (23.6196, 102.8265, "建水",     "bridge", "D46"),
    (23.0957, 102.7700, "元阳",     "bridge", "D47"),
    (23.9021, 106.6404, "百色",     "bridge", "D48"),
    (22.8170, 108.3669, "南宁",     "bridge", "D49"),
    (25.27,   110.30,   "桂林",     "p3", "D50-52"),
    (21.48,   109.12,   "北海",     "p3", "D53-54"),
    (23.13,   113.27,   "广州",     "p3", "D56-57"),
    (22.54,   114.09,   "深圳",     "p3", "D60-61"),
    (22.20,   113.54,   "澳门",     "p3", "D64-65"),
    (23.66,   116.62,   "潮汕",     "p3", "D66-67"),
    (24.48,   118.09,   "厦门",     "p3", "D68"),
    (29.33,   120.08,   "义乌",     "p3", "D70"),
    (30.27,   120.15,   "杭州",     "p3", "D71"),
    (31.24,   121.50,   "上海",     "p3", "D73-74"),
    (31.30,   120.62,   "苏州",     "p3", "D76"),
    (32.06,   118.80,   "南京",     "p3", "D77"),
]

COLORS = {
    "start":  "#3B6D11",
    "end":    "#A32D2D",
    "p1":     "#534AB7",
    "bridge": "#0F6E56",
    "p2":     "#BA7517",
    "p3":     "#c0392b",
}

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Hiragino Sans GB",
                                    "Songti SC", "STHeiti", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# Wider canvas, lower aspect ratio so labels breathe
fig = plt.figure(figsize=(18, 13), dpi=150)
fig.patch.set_facecolor("#ffffff")

# Use gridspec: main map left, sidebar right
import matplotlib.gridspec as gridspec
gs = gridspec.GridSpec(1, 5, figure=fig, wspace=0.05)
ax = fig.add_subplot(gs[0, :4])
ax_side = fig.add_subplot(gs[0, 4])
ax_side.axis("off")

ax.set_facecolor("#eef3f8")  # subtle ocean blue
ax.set_xlim(96, 124)
ax.set_ylim(-2, 33)
ax.set_aspect(1.15)

# Light continent hint (overlay land color)
import matplotlib.patches as mpatches
# Rough China + SE Asia landmass rectangle (visual hint only)
land = mpatches.Rectangle((96, 18), 28, 17, color="#f5f1e8", alpha=0.7, zorder=0)
ax.add_patch(land)
land2 = mpatches.Rectangle((96, -2), 18, 22, color="#f0ede1", alpha=0.5, zorder=0)
ax.add_patch(land2)

# Helper: draw a path through a slice of points
def draw_segment(idx_from, idx_to, color, dashed=False, lw=3.5, alpha=0.9):
    xs = [POINTS[i][1] for i in range(idx_from, idx_to + 1)]
    ys = [POINTS[i][0] for i in range(idx_from, idx_to + 1)]
    style = "--" if dashed else "-"
    ax.plot(xs, ys, style, color=color, linewidth=lw, alpha=alpha, zorder=2,
            solid_capstyle="round", solid_joinstyle="round", dash_capstyle="round")

# Segments
draw_segment(0, 5, COLORS["p1"])                           # P1 武汉→泸沽湖
draw_segment(5, 7, COLORS["bridge"], lw=3.0)               # Bridge A
draw_segment(7, 13, COLORS["p2"], dashed=True, lw=2.5, alpha=0.75)  # SE Asia flights
# Return flight SG → KMG
ax.plot([POINTS[13][1], POINTS[14][1]], [POINTS[13][0], POINTS[14][0]],
        "--", color=COLORS["p2"], lw=2.5, alpha=0.75, zorder=2)
draw_segment(14, 18, COLORS["bridge"], lw=3.0)             # Bridge B
draw_segment(18, 30, COLORS["p3"])                          # P3 sea provinces
# Close loop: 南京 → 武汉
ax.plot([POINTS[30][1], POINTS[0][1]], [POINTS[30][0], POINTS[0][0]],
        "-", color=COLORS["p3"], lw=3.5, alpha=0.9, zorder=2,
        solid_capstyle="round")

# Plot dots + numbers
for i, (lat, lon, name, phase, _) in enumerate(POINTS):
    c = COLORS[phase]
    if phase in ("start",):
        size = 380
    else:
        size = 220
    ax.scatter(lon, lat, s=size, color=c, edgecolors="white", linewidth=2.2, zorder=5)
    no = i + 1
    ax.text(lon, lat, str(no), ha="center", va="center", color="white",
            fontsize=9, fontweight="bold", zorder=6)

# Callout label routing
# Each entry: (anchor_offset_x, anchor_offset_y, halign)
# For dense Yangtze delta cluster, route labels outward with callout lines
CALLOUTS = {
    "武汉":       (-1.0,  1.4, "right"),
    "张家界":     (-1.4,  0.6, "right"),
    "重庆":       (-1.6,  0.4, "right"),
    "千户苗寨":   (-1.8, -0.6, "right"),
    "丽江":       (-1.8,  0.4, "right"),
    "泸沽湖":     ( 0.5,  0.7, "left"),
    "大理":       (-1.6, -0.6, "right"),
    "昆明寄车":   ( 0.5, -1.0, "left"),
    "河内":       ( 0.6,  0.6, "left"),
    "胡志明":     ( 0.6,  0.0, "left"),
    "曼谷":       (-1.6,  0.4, "right"),
    "清迈":       (-1.6,  0.4, "right"),
    "吉隆坡":     ( 0.6,  0.0, "left"),
    "新加坡":     ( 0.6, -0.8, "left"),
    "昆明取车":   (-1.8,  0.6, "right"),
    "建水":       (-1.5, -0.7, "right"),
    "元阳":       (-1.5, -1.2, "right"),
    "百色":       (-0.4, -1.0, "right"),
    "南宁":       (-1.4, -0.9, "right"),
    "桂林":       (-1.4,  0.6, "right"),
    "北海":       (-1.4, -0.9, "right"),
    "广州":       (-1.3, -0.9, "right"),
    "深圳":       ( 0.6, -0.7, "left"),
    "澳门":       (-1.4, -1.4, "right"),
    "潮汕":       ( 0.6, -0.6, "left"),
    "厦门":       ( 0.6, -0.3, "left"),
    "义乌":       ( 1.5,  0.8, "left"),  # callout to east
    "杭州":       ( 2.0,  0.0, "left"),  # callout east
    "上海":       ( 1.0,  0.8, "left"),
    "苏州":       ( 1.5, -0.8, "left"),
    "南京":       (-1.4,  0.6, "right"),
}

# Draw labels with optional leader lines for dense areas
DENSE_NAMES = {"义乌", "杭州", "上海", "苏州"}

for lat, lon, name, phase, day in POINTS:
    dx, dy, ha = CALLOUTS.get(name, (0.5, 0.5, "left"))
    tx, ty = lon + dx, lat + dy
    label_text = f"{name}\n{day}"

    # Draw leader line for dense names
    if name in DENSE_NAMES:
        ax.plot([lon, tx + (0.15 if ha == "left" else -0.15)],
                [lat, ty],
                "-", color="#888780", linewidth=0.6, alpha=0.6, zorder=4)

    ax.annotate(
        label_text,
        xy=(lon, lat),
        xytext=(tx, ty),
        fontsize=9.5,
        color="#2c2c2a",
        ha=ha,
        va="center",
        zorder=7,
        bbox=dict(
            boxstyle="round,pad=0.32",
            fc="white",
            ec="#cccccc",
            lw=0.6,
            alpha=0.95,
        ),
    )

# Title block
fig.text(0.5, 0.96, "武汉大环线 · 78 天全串联", fontsize=24, fontweight="bold",
         ha="center", color="#2c2c2a")
fig.text(0.5, 0.928,
         "湘渝贵滇 22d  +  云南衔接 2d  +  东南亚 4 国 20d  +  云南→广西 5d  +  沿海五省 29d",
         fontsize=12, ha="center", color="#5f5e5a")

# Sidebar: phase summary boxes
def phase_box(y, color, num, title, days, route):
    ax_side.add_patch(FancyBboxPatch(
        (0.02, y - 0.07), 0.96, 0.10,
        boxstyle="round,pad=0.01,rounding_size=0.015",
        facecolor=color, edgecolor="none", alpha=0.95,
        transform=ax_side.transAxes
    ))
    ax_side.text(0.10, y - 0.02, num, fontsize=20, fontweight="bold",
                 color="white", ha="center", va="center", transform=ax_side.transAxes)
    ax_side.text(0.20, y + 0.005, title, fontsize=11, fontweight="bold",
                 color="white", va="center", transform=ax_side.transAxes)
    ax_side.text(0.20, y - 0.025, f"{days} · {route}", fontsize=8.5,
                 color="white", va="center", alpha=0.92, transform=ax_side.transAxes)

ax_side.text(0.5, 0.94, "阶段拆解", fontsize=13, fontweight="bold",
             ha="center", color="#2c2c2a", transform=ax_side.transAxes)

phase_box(0.84, COLORS["p1"], "①", "湘渝贵滇 自驾", "22 天 D1-22", "武汉→泸沽湖")
phase_box(0.72, COLORS["bridge"], "★", "衔接段 A", "2 天 D23-24", "泸沽湖→昆明寄车")
phase_box(0.60, COLORS["p2"], "②", "东南亚 飞行", "20 天 D25-44", "越南→新加坡")
phase_box(0.48, COLORS["bridge"], "★", "衔接段 B", "5 天 D45-49", "昆明→建水→南宁")
phase_box(0.36, COLORS["p3"], "③", "沿海五省 自驾", "29 天 D50-78", "南宁→上海→武汉")

# Legend
ax_side.text(0.5, 0.27, "图例", fontsize=12, fontweight="bold",
             ha="center", color="#2c2c2a", transform=ax_side.transAxes)
legend_items = [
    Line2D([0], [0], color=COLORS["p1"],     lw=3.5, label="自驾·湘渝贵滇"),
    Line2D([0], [0], color=COLORS["bridge"], lw=3.0, label="自驾·云南衔接"),
    Line2D([0], [0], color=COLORS["p2"],     lw=2.5, linestyle="--", label="飞行·东南亚"),
    Line2D([0], [0], color=COLORS["p3"],     lw=3.5, label="自驾·沿海五省"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["start"],
           markersize=13, label="起点/终点 武汉"),
]
ax_side.legend(handles=legend_items, loc="upper center",
               bbox_to_anchor=(0.5, 0.25), fontsize=9.5, frameon=True,
               facecolor="white", edgecolor="#d0d0d0", framealpha=0.95)

# Stats
ax_side.text(0.5, 0.04,
             "总长：78 天\n2 人节俭：¥45k · 标准：¥62k",
             fontsize=10, ha="center", color="#5f5e5a", transform=ax_side.transAxes,
             linespacing=1.6,
             bbox=dict(boxstyle="round,pad=0.5", fc="#eaf3de", ec="#3B6D11", lw=0.8))

# Footnote
fig.text(0.5, 0.015,
         "数据来源：高德 MCP + 携程问道  ·  原始 HTML：行程/全程串联/wuhan-grand-loop.html",
         fontsize=8.5, color="#888780", ha="center")

# Main map styling
ax.grid(True, color="#cccccc", linewidth=0.3, alpha=0.5, linestyle=":")
ax.set_xlabel("经度 °E", fontsize=10, color="#888780")
ax.set_ylabel("纬度 °N", fontsize=10, color="#888780")
ax.tick_params(colors="#888780", labelsize=9)
for spine in ax.spines.values():
    spine.set_color("#cccccc")
    spine.set_linewidth(0.5)

plt.subplots_adjust(top=0.91, bottom=0.05, left=0.05, right=0.97)

output_path = "/Users/snowwang/work/travel/行程/全程串联/wuhan-grand-loop-map-v2.png"
plt.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
print(f"Generated: {output_path}")
