#!/usr/bin/env python3
"""
Generate finance-terminal SVGs for Linux5Real GitHub profile.
Reads: assets/finance-telemetry/finance-repo-telemetry.json
Writes: assets/finance-telemetry/finance-repo-telemetry.svg
        assets/finance-telemetry/finance-repo-activity.svg
"""
import json
from datetime import datetime, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "assets/finance-telemetry/finance-repo-telemetry.json"
OUT_DIR = ROOT / "assets/finance-telemetry"

MONO = "font-family='IBM Plex Mono, JetBrains Mono, Fira Code, Consolas, monospace'"


def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def fmt_number(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")


def activity_color(commits: int, max_commits: int) -> str:
    if commits == 0:
        return "#0D0D0D"
    ratio = commits / max_commits
    if ratio < 0.25:
        return "#2A2A2A"
    elif ratio < 0.5:
        return "#525252"
    elif ratio < 0.75:
        return "#9C9C9C"
    return "#ECECEC"


def fmt_date_label(d: datetime) -> str:
    return d.strftime("%b %d").replace(" 0", "  ")


def generate_telemetry_svg(data: dict) -> str:
    scan = data["scan"]
    activity = data["activity"]
    loc = escape(fmt_number(scan["tracked_lines"]))
    files = escape(str(scan["tracked_files"]))
    commits_30d = escape(str(activity["commits_last_30_days"]))
    total_commits = escape(str(activity["total_commits"]))
    last_commit = escape(activity["last_commit_date"])
    contributors = escape(str(activity["contributors"]))

    langs = scan["language_lines"]
    sorted_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:4]
    max_lines = sorted_langs[0][1] if sorted_langs else 0

    # Full-width bars: x=40 to x=880 (BAR_W=840)
    BAR_X = 40
    BAR_W = 840
    # Lang section starts at y=189, rows stride=34:
    # row0 text=202, bar=209-216  bottom=216
    # row1 text=236, bar=243-250  bottom=250
    # row2 text=270, bar=277-284  bottom=284
    # row3 text=304, bar=311-318  bottom=318
    # footer line at y=326, total height=340

    lang_rows = ""
    ry = 202
    for i, (lang, lines) in enumerate(sorted_langs):
        bar_fill = min(BAR_W, int(BAR_W * lines / max_lines)) if max_lines > 0 else 0
        gray = 238 - int(96 * i / max(len(sorted_langs) - 1, 1))
        color = f"#{gray:02X}{gray:02X}{gray:02X}"
        lang_rows += f"""
  <text x="{BAR_X}" y="{ry}" {MONO} fill="#CCCCCC" font-size="11" font-weight="500">{escape(lang)}</text>
  <text x="878" y="{ry}" {MONO} fill="#4A4A4A" font-size="10" text-anchor="end">{escape(fmt_number(lines))} lines</text>
  <rect x="{BAR_X}" y="{ry + 7}" width="{BAR_W}" height="7" fill="#0F0F0F" />
  <rect x="{BAR_X}" y="{ry + 7}" width="{bar_fill}" height="7" fill="{color}" />"""
        ry += 34

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="340" viewBox="0 0 920 340" role="img" aria-label="Finance Signal Engine — Code Telemetry">
  <title>Finance Signal Engine — Code Telemetry</title>

  <!-- flat dark background -->
  <rect width="920" height="340" fill="#050505" />

  <!-- white top accent — Bloomberg-style -->
  <rect x="0" y="0" width="920" height="3" fill="#FFFFFF" />

  <!-- header band -->
  <rect x="0" y="3" width="920" height="52" fill="#090909" />
  <line x1="0" y1="55" x2="920" y2="55" stroke="#1C1C1C" />

  <!-- tag pill -->
  <rect x="28" y="15" width="118" height="22" rx="3" fill="#111111" stroke="#252525" />
  <text x="87" y="30" {MONO} fill="#7A7A7A" font-size="9" letter-spacing="1.8" text-anchor="middle">SIGNAL ENGINE</text>

  <!-- title -->
  <text x="160" y="35" {MONO} fill="#F0F0F0" font-size="13" font-weight="700" letter-spacing="0.3">FINANCE SIGNAL ENGINE</text>
  <text x="344" y="35" {MONO} fill="#303030" font-size="13">·  CODE TELEMETRY</text>

  <!-- scan timestamp -->
  <text x="886" y="29" {MONO} fill="#303030" font-size="9" text-anchor="end">SCAN</text>
  <text x="886" y="43" {MONO} fill="#424242" font-size="10" text-anchor="end">{last_commit}</text>

  <!-- ── METRICS BAND ── -->
  <rect x="0" y="55" width="920" height="104" fill="#070707" />
  <line x1="0" y1="159" x2="920" y2="159" stroke="#181818" />

  <!-- LOC -->
  <text x="40" y="88" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">CODEBASE  ·  LOC</text>
  <text x="40" y="134" {MONO} fill="#FFFFFF" font-size="44" font-weight="700">{loc}</text>

  <!-- rule 1 -->
  <line x1="328" y1="68" x2="328" y2="152" stroke="#181818" />

  <!-- FILES -->
  <text x="352" y="88" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">TRACKED FILES</text>
  <text x="352" y="134" {MONO} fill="#FFFFFF" font-size="44" font-weight="700">{files}</text>

  <!-- rule 2 -->
  <line x1="548" y1="68" x2="548" y2="152" stroke="#181818" />

  <!-- COMMITS 30D -->
  <text x="572" y="88" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">COMMITS  /  30D</text>
  <text x="572" y="134" {MONO} fill="#FFFFFF" font-size="44" font-weight="700">{commits_30d}</text>

  <!-- rule 3 -->
  <line x1="724" y1="68" x2="724" y2="152" stroke="#181818" />

  <!-- secondary stats -->
  <text x="748" y="90" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">TOTAL COMMITS</text>
  <text x="748" y="114" {MONO} fill="#B8B8B8" font-size="22" font-weight="700">{total_commits}</text>
  <text x="748" y="132" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">CONTRIBUTORS</text>
  <text x="748" y="150" {MONO} fill="#B8B8B8" font-size="18" font-weight="700">{contributors}</text>

  <!-- ── LANGUAGE SECTION ── -->
  <rect x="0" y="159" width="920" height="30" fill="#080808" />
  <text x="40" y="180" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">LANGUAGE DISTRIBUTION</text>
  <text x="878" y="180" {MONO} fill="#303030" font-size="9" text-anchor="end">BY NON-EMPTY LINES</text>
  <line x1="0" y1="189" x2="920" y2="189" stroke="#161616" />

{lang_rows}

  <!-- footer strip -->
  <line x1="0" y1="328" x2="920" y2="328" stroke="#141414" />
  <rect x="0" y="328" width="920" height="12" fill="#060606" />
  <text x="40" y="337" {MONO} fill="#303030" font-size="8" letter-spacing="0.5">source-safe  ·  activity exposed, code withheld  ·  last scan {last_commit}</text>
</svg>"""


def generate_activity_svg(data: dict) -> str:
    activity = data["activity"]
    commits_30d = activity["commits_last_30_days"]
    last_commit_str = activity["last_commit_date"]

    COLS, ROWS = 12, 7
    # Grid starts at GRID_X=402, must end before x=900
    # Available = 900 - 402 = 498px for 12 cols
    # COL_STRIDE = 41 → 12*41 = 492, last cell ends at 402+11*41+26 = 879 ✓
    CELL_W, CELL_H = 26, 20
    COL_GAP, ROW_GAP = 15, 9
    COL_STRIDE = CELL_W + COL_GAP   # 41
    ROW_STRIDE = CELL_H + ROW_GAP   # 29

    series = list(activity["activity_series"])[-COLS * ROWS:]
    active_days = sum(1 for x in series if x > 0)
    peak = max(series) if series else 0
    streak = 0
    for x in reversed(series):
        if x > 0:
            streak += 1
        else:
            break
    max_commits = max(series) if series else 1

    padded = ([0] * (COLS * ROWS - len(series))) + series

    # Date labels
    last_date = datetime.strptime(last_commit_str, "%Y-%m-%d")
    start_date = last_date - timedelta(days=len(padded) - 1)
    mid_date = last_date - timedelta(days=len(padded) // 2)
    start_label = escape(fmt_date_label(start_date))
    mid_label = escape(fmt_date_label(mid_date))
    end_label = escape(fmt_date_label(last_date))

    # Grid position — right side of a two-panel layout
    GRID_X = 402
    GRID_Y = 80

    cells = []
    for col in range(COLS):
        for row in range(ROWS):
            idx = col * ROWS + row
            color = activity_color(padded[idx], max_commits)
            cx = GRID_X + col * COL_STRIDE
            cy = GRID_Y + row * ROW_STRIDE
            cells.append(
                f'<rect x="{cx}" y="{cy}" width="{CELL_W}" height="{CELL_H}" rx="3" fill="{color}" />'
            )
    grid = "\n  ".join(cells)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_els = ""
    for i, day in enumerate(days):
        label_y = GRID_Y + i * ROW_STRIDE + CELL_H // 2 + 4
        day_els += (
            f'\n  <text x="{GRID_X - 10}" y="{label_y}" {MONO}'
            f' fill="#404040" font-size="9" text-anchor="end">{day}</text>'
        )

    x_start = GRID_X
    x_mid = GRID_X + (COLS // 2) * COL_STRIDE
    x_end = GRID_X + (COLS - 1) * COL_STRIDE + CELL_W

    last_commit = escape(last_commit_str)
    LEG_X = GRID_X
    # Grid bottom: GRID_Y + ROWS*ROW_STRIDE - ROW_GAP = 80 + 7*30 - 8 = 282
    # Legend at y=294
    # Footer at y=300
    # SVG height: 308

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="308" viewBox="0 0 920 308" role="img" aria-label="Finance Signal Engine — Execution Tape">
  <title>Finance Signal Engine — Execution Tape</title>

  <!-- flat dark background -->
  <rect width="920" height="308" fill="#050505" />

  <!-- white top accent -->
  <rect x="0" y="0" width="920" height="3" fill="#FFFFFF" />

  <!-- header band -->
  <rect x="0" y="3" width="920" height="52" fill="#090909" />
  <line x1="0" y1="55" x2="920" y2="55" stroke="#1C1C1C" />

  <!-- tag pill -->
  <rect x="28" y="15" width="126" height="22" rx="3" fill="#111111" stroke="#252525" />
  <text x="91" y="30" {MONO} fill="#7A7A7A" font-size="9" letter-spacing="1.8" text-anchor="middle">EXECUTION TAPE</text>

  <!-- title -->
  <text x="168" y="35" {MONO} fill="#F0F0F0" font-size="13" font-weight="700" letter-spacing="0.3">COMMIT LOG</text>
  <text x="244" y="35" {MONO} fill="#303030" font-size="13">·  84-DAY WINDOW</text>

  <!-- last exec timestamp -->
  <text x="886" y="29" {MONO} fill="#303030" font-size="9" text-anchor="end">LAST EXEC</text>
  <text x="886" y="43" {MONO} fill="#424242" font-size="10" text-anchor="end">{last_commit}</text>

  <!-- panel divider -->
  <line x1="368" y1="55" x2="368" y2="296" stroke="#161616" />

  <!-- ── LEFT PANEL: commit stats ── -->

  <text x="40" y="92" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">30D SESSIONS</text>
  <text x="40" y="126" {MONO} fill="#FFFFFF" font-size="36" font-weight="700">{escape(str(commits_30d))}</text>

  <text x="210" y="92" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">ACTIVE DAYS</text>
  <text x="210" y="126" {MONO} fill="#FFFFFF" font-size="36" font-weight="700">{escape(str(active_days))}</text>

  <text x="40" y="170" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">PEAK SESSION</text>
  <text x="40" y="204" {MONO} fill="#FFFFFF" font-size="36" font-weight="700">{escape(str(peak))}</text>

  <text x="210" y="170" {MONO} fill="#424242" font-size="9" letter-spacing="2.4">STREAK</text>
  <text x="210" y="204" {MONO} fill="#FFFFFF" font-size="36" font-weight="700">{escape(str(streak))}<tspan {MONO} fill="#383838" font-size="14"> days</tspan></text>

  <line x1="40" y1="222" x2="352" y2="222" stroke="#161616" />
  <text x="40" y="244" {MONO} fill="#3C3C3C" font-size="10">last execution  {last_commit}</text>

  <!-- ── RIGHT PANEL: heatmap ── -->

  <!-- date column labels -->
  <text x="{x_start}" y="{GRID_Y - 10}" {MONO} fill="#404040" font-size="9">{start_label}</text>
  <text x="{x_mid}" y="{GRID_Y - 10}" {MONO} fill="#404040" font-size="9">{mid_label}</text>
  <text x="{x_end}" y="{GRID_Y - 10}" {MONO} fill="#404040" font-size="9" text-anchor="end">{end_label}</text>

  <!-- day labels -->{day_els}

  <!-- commit grid -->
  {grid}

  <!-- intensity legend -->
  <text x="{LEG_X}" y="300" {MONO} fill="#343434" font-size="9">INACTIVE</text>
  <rect x="{LEG_X + 68}" y="291" width="10" height="10" rx="2" fill="#2A2A2A" />
  <rect x="{LEG_X + 83}" y="291" width="10" height="10" rx="2" fill="#525252" />
  <rect x="{LEG_X + 98}" y="291" width="10" height="10" rx="2" fill="#9C9C9C" />
  <rect x="{LEG_X + 113}" y="291" width="10" height="10" rx="2" fill="#ECECEC" />
  <text x="{LEG_X + 128}" y="300" {MONO} fill="#343434" font-size="9">PEAK</text>
</svg>"""


def main() -> None:
    data = load_data()
    (OUT_DIR / "finance-repo-telemetry.svg").write_text(generate_telemetry_svg(data), encoding="utf-8")
    print("Written: finance-repo-telemetry.svg")
    (OUT_DIR / "finance-repo-activity.svg").write_text(generate_activity_svg(data), encoding="utf-8")
    print("Written: finance-repo-activity.svg")


if __name__ == "__main__":
    main()
