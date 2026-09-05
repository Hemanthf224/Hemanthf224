import urllib.request
import re

USERNAME = "Hemanthf224"

# Fetch contributions
url = f"https://github.com/users/{USERNAME}/contributions"
html = urllib.request.urlopen(url).read().decode("utf-8")
levels = re.findall(r'data-level="([0-4])"', html)

svg_template = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200" viewBox="0 0 800 200">
    <style>
        .bg {{ fill: #161b22; }}
        .block-empty {{ fill: #161b22; stroke: #1b232c; stroke-width: 1; }}
        .block-fill-1 {{ fill: #0e4429; opacity: 0; }}
        .block-fill-2 {{ fill: #006d32; opacity: 0; }}
        .block-fill-3 {{ fill: #26a641; opacity: 0; }}
        .block-fill-4 {{ fill: #39d353; opacity: 0; }}
        .builder {{ width: 14px; height: 14px; fill: #58a6ff; }}
    </style>
    <rect width="800" height="200" class="bg"/>
    <g transform="translate(20, 20)">
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

cols = len(levels) // 7
rows = 7
size = 12
gap = 2

# Generate grid
grid_svg = ""
for c in range(cols):
    for r in range(rows):
        x = c * (size + gap)
        y = r * (size + gap)
        grid_svg += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" class="block-empty" rx="2" ry="2"/>\n'

# Generate path based on real contributions
path = []
for idx, level in enumerate(levels):
    if level != '0':
        c = idx // 7
        r = idx % 7
        path.append((c, r, level))

# If no contributions, fake a small path
if not path:
    path = [(10, 3, '1'), (11, 3, '2')]

dur = max(len(path) * 0.3, 5) # 0.3 seconds per block, minimum 5 seconds
x_vals = ";".join([str(c * (size + gap)) for c, r, l in path]) + ";" + str(path[0][0] * (size + gap))
y_vals = ";".join([str(r * (size + gap)) for c, r, l in path]) + ";" + str(path[0][1] * (size + gap))

# Generate block fills
animations_svg = ""
for i, (c, r, level) in enumerate(path):
    x = c * (size + gap)
    y = r * (size + gap)
    time_pct = (i / len(path)) * 100
    anim = f"""
    <rect x="{x}" y="{y}" width="{size}" height="{size}" class="block-fill-{level}" rx="2" ry="2">
        <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{time_pct/100:.2f};0.95;1" dur="{dur}s" repeatCount="indefinite"/>
    </rect>
    """
    animations_svg += anim

svg_out = svg_template.format(grid=grid_svg, animations=animations_svg, x_vals=x_vals, y_vals=y_vals, dur=dur)

with open("builder.svg", "w") as f:
    f.write(svg_out)
