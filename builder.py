import random

svg_template = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200" viewBox="0 0 800 200">
    <style>
        .bg {{ fill: #161b22; }}
        .block-empty {{ fill: #0e4429; opacity: 0.3; }}
        .block-fill {{ fill: #39d353; opacity: 0; }}
        .builder {{ width: 14px; height: 14px; fill: #58a6ff; }}
    </style>
    <rect width="800" height="200" class="bg"/>
    <g transform="translate(40, 40)">
        <!-- Grid -->
        {grid}
        
        <!-- Animations -->
        {animations}
        
        <!-- Builder Character -->
        <rect x="0" y="0" class="builder" rx="2" ry="2">
            <animate attributeName="x" values="{x_vals}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>
            <animate attributeName="y" values="{y_vals}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>
        </rect>
    </g>
</svg>"""

cols = 52
rows = 7
size = 12
gap = 2
total = cols * rows

# Generate grid
grid_svg = ""
for c in range(cols):
    for r in range(rows):
        x = c * (size + gap)
        y = r * (size + gap)
        grid_svg += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" class="block-empty" rx="2" ry="2"/>\n'

# Generate path for builder
path = []
for c in range(5, cols - 5, 2):
    r = random.randint(0, rows - 1)
    path.append((c, r))

dur = len(path) * 0.5
x_vals = ";".join([str(c * (size + gap)) for c, r in path]) + ";" + str(path[0][0] * (size + gap))
y_vals = ";".join([str(r * (size + gap)) for c, r in path]) + ";" + str(path[0][1] * (size + gap))

# Generate block fills
animations_svg = ""
for i, (c, r) in enumerate(path):
    x = c * (size + gap)
    y = r * (size + gap)
    time_pct = (i / len(path)) * 100
    anim = f"""
    <rect x="{x}" y="{y}" width="{size}" height="{size}" class="block-fill" rx="2" ry="2">
        <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{time_pct/100:.2f};0.95;1" dur="{dur}s" repeatCount="indefinite"/>
    </rect>
    """
    animations_svg += anim

svg_out = svg_template.format(grid=grid_svg, animations=animations_svg, x_vals=x_vals, y_vals=y_vals, dur=dur)

with open("builder.svg", "w") as f:
    f.write(svg_out)
