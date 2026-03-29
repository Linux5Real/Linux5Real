#!/usr/bin/env python3
"""
Generate telemetry SVGs for Linux5Real GitHub profile.
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

STYLE = """  <style>
    .mono { font-family: 'IBM Plex Mono', 'JetBrains Mono', 'Fira Code', Consolas, monospace; }
  </style>"""


def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def fmt_number(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")


def activity_color(commits: int, max_commits: int) -> str:
    if commits == 0:
        return "#0E0E0E"
    ratio = commits / max_commits
    if ratio < 0.25:
        return "#2C2C2C"
    elif ratio < 0.5:
        return "#565656"
    elif ratio < 0.75:
        return "#9E9E9E"
    return "#F0F0F0"


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
    BAR_W = 268

    lang_rows = ""
    row_y = 118
    for i, (lang, lines) in enumerate(sorted_langs):
        bar_fill = min(BAR_W, int(BAR_W * lines / max_lines)) if max_lines > 0 else 0
        gray = 255 - int(88 * i / max(len(sorted_langs) - 1, 1))
        color = f"#{gray:02X}{gray:02X}{gray:02X}"
        lang_rows += f"""
    <text x="494" y="{row_y}" class="mono" fill="#E8E8E8" font-size="12" font-weight="500">{escape(lang)}</text>
    <text x="852" y="{row_y}" class="mono" fill="#525252" font-size="10" text-anchor="end">{escape(fmt_number(lines))}</text>
    <rect x="494" y="{row_y + 7}" width="{BAR_W}" height="6" rx="2" fill="#131313" />
    <rect x="494" y="{row_y + 7}" width="{bar_fill}" height="6" rx="2" fill="{color}" />"""
        row_y += 44

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="308" viewBox="0 0 920 308" role="img" aria-label="Finance Signal Engine — Code Telemetry">
  <title>Finance Signal Engine — Code Telemetry</title>
{STYLE}
  <!-- outer shell -->
  <rect width="920" height="308" rx="18" fill="#020202" />
  <!-- inner card -->
  <rect x="18" y="18" width="884" height="272" rx="12" fill="#070707" stroke="#1D1D1D" />

  <!-- header band -->
  <rect x="18" y="18" width="884" height="46" rx="12" fill="#0B0B0B" />
  <rect x="18" y="52" width="884" height="12" fill="#0B0B0B" />
  <line x1="18" y1="64" x2="902" y2="64" stroke="#1A1A1A" />

  <!-- header: tag pill -->
  <rect x="36" y="29" width="120" height="20" rx="3" fill="#0F0F0F" stroke="#272727" />
  <text x="96" y="43" class="mono" fill="#888888" font-size="9" letter-spacing="1.6" text-anchor="middle">SIGNAL ENGINE</text>

  <!-- header: title -->
  <text x="168" y="44" class="mono" fill="#EFEFEF" font-size="11" font-weight="700" letter-spacing="0.4">FINANCE SIGNAL ENGINE</text>
  <text x="338" y="44" class="mono" fill="#383838" font-size="11">·  CODE TELEMETRY</text>

  <!-- header: scan date -->
  <text x="878" y="44" class="mono" fill="#383838" font-size="9" letter-spacing="0.5" text-anchor="end">SCAN  {last_commit}</text>

  <!-- panel divider -->
  <line x1="466" y1="64" x2="466" y2="290" stroke="#161616" />

  <!-- ── LEFT PANEL: key metrics ── -->

  <!-- LOC -->
  <text x="40" y="100" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">CODEBASE  ·  LOC</text>
  <text x="40" y="136" class="mono" fill="#FFFFFF" font-size="38" font-weight="700">{loc}</text>

  <!-- FILES + COMMITS 30D -->
  <text x="40" y="174" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">TRACKED FILES</text>
  <text x="40" y="200" class="mono" fill="#FFFFFF" font-size="27" font-weight="700">{files}</text>

  <text x="216" y="174" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">COMMITS  /  30D</text>
  <text x="216" y="200" class="mono" fill="#FFFFFF" font-size="27" font-weight="700">{commits_30d}</text>

  <!-- left panel separator -->
  <line x1="40" y1="220" x2="448" y2="220" stroke="#161616" />

  <!-- metadata row -->
  <text x="40" y="242" class="mono" fill="#404040" font-size="10">contributors  {contributors}</text>
  <text x="40" y="260" class="mono" fill="#404040" font-size="10">total commits  {total_commits}</text>
  <text x="40" y="278" class="mono" fill="#404040" font-size="10">last scan  {last_commit}</text>

  <!-- ── RIGHT PANEL: language distribution ── -->

  <text x="494" y="96" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">LANGUAGE DISTRIBUTION</text>
  <line x1="494" y1="103" x2="860" y2="103" stroke="#161616" />

{lang_rows}
</svg>"""


def generate_activity_svg(data: dict) -> str:
    activity = data["activity"]
    commits_30d = activity["commits_last_30_days"]
    last_commit_str = activity["last_commit_date"]

    CELL = 20
    ROW_GAP = 7
    COL_GAP = 10
    COLS = 12
    ROWS = 7
    ROW_STRIDE = CELL + ROW_GAP   # 27
    COL_STRIDE = CELL + COL_GAP   # 30

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

    # Date range labels from series length and last commit
    last_date = datetime.strptime(last_commit_str, "%Y-%m-%d")
    start_date = last_date - timedelta(days=len(padded) - 1)
    mid_date = last_date - timedelta(days=len(padded) // 2)
    start_label = escape(fmt_date_label(start_date))
    mid_label = escape(fmt_date_label(mid_date))
    end_label = escape(fmt_date_label(last_date))

    GRID_X = 456
    GRID_Y = 86

    # Build grid cells
    cells = []
    for col in range(COLS):
        for row in range(ROWS):
            idx = col * ROWS + row
            color = activity_color(padded[idx], max_commits)
            cx = GRID_X + col * COL_STRIDE
            cy = GRID_Y + row * ROW_STRIDE
            cells.append(
                f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="3" fill="{color}" />'
            )
    grid = "\n  ".join(cells)

    # Day labels (centered vertically per row)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_els = ""
    for i, day in enumerate(days):
        label_y = GRID_Y + i * ROW_STRIDE + CELL // 2 + 4
        day_els += (
            f'\n  <text x="{GRID_X - 10}" y="{label_y}" class="mono"'
            f' fill="#424242" font-size="9" text-anchor="end">{day}</text>'
        )

    # Date column x positions
    x_start = GRID_X
    x_mid = GRID_X + (COLS // 2) * COL_STRIDE
    x_end = GRID_X + (COLS - 1) * COL_STRIDE

    last_commit = escape(last_commit_str)
    streak_days_label = "day" if streak == 1 else "days"

    # Legend x anchor
    LEG_X = GRID_X

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="282" viewBox="0 0 920 282" role="img" aria-label="Finance Signal Engine — Execution Tape">
  <title>Finance Signal Engine — Execution Tape</title>
{STYLE}
  <!-- outer shell -->
  <rect width="920" height="282" rx="18" fill="#020202" />
  <!-- inner card -->
  <rect x="18" y="18" width="884" height="246" rx="12" fill="#070707" stroke="#1D1D1D" />

  <!-- header band -->
  <rect x="18" y="18" width="884" height="46" rx="12" fill="#0B0B0B" />
  <rect x="18" y="52" width="884" height="12" fill="#0B0B0B" />
  <line x1="18" y1="64" x2="902" y2="64" stroke="#1A1A1A" />

  <!-- header: tag pill -->
  <rect x="36" y="29" width="124" height="20" rx="3" fill="#0F0F0F" stroke="#272727" />
  <text x="98" y="43" class="mono" fill="#888888" font-size="9" letter-spacing="1.6" text-anchor="middle">EXECUTION TAPE</text>

  <!-- header: title -->
  <text x="172" y="44" class="mono" fill="#EFEFEF" font-size="11" font-weight="700" letter-spacing="0.4">COMMIT LOG</text>
  <text x="243" y="44" class="mono" fill="#383838" font-size="11">·  84-DAY WINDOW</text>

  <!-- header: last exec -->
  <text x="878" y="44" class="mono" fill="#383838" font-size="9" letter-spacing="0.5" text-anchor="end">LAST EXEC  {last_commit}</text>

  <!-- panel divider -->
  <line x1="430" y1="64" x2="430" y2="264" stroke="#161616" />

  <!-- ── LEFT PANEL: commit stats ── -->

  <text x="40" y="100" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">30D SESSIONS</text>
  <text x="40" y="128" class="mono" fill="#FFFFFF" font-size="30" font-weight="700">{escape(str(commits_30d))}</text>

  <text x="216" y="100" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">ACTIVE DAYS</text>
  <text x="216" y="128" class="mono" fill="#FFFFFF" font-size="30" font-weight="700">{escape(str(active_days))}</text>

  <text x="40" y="166" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">PEAK SESSION</text>
  <text x="40" y="194" class="mono" fill="#FFFFFF" font-size="30" font-weight="700">{escape(str(peak))}</text>

  <text x="216" y="166" class="mono" fill="#484848" font-size="9" letter-spacing="2.4">STREAK</text>
  <text x="216" y="194" class="mono" fill="#FFFFFF" font-size="30" font-weight="700">{escape(str(streak))} <tspan fill="#404040" font-size="13">{streak_days_label}</tspan></text>

  <line x1="40" y1="212" x2="412" y2="212" stroke="#161616" />
  <text x="40" y="234" class="mono" fill="#404040" font-size="10">last execution  {last_commit}</text>

  <!-- ── RIGHT PANEL: activity grid ── -->

  <!-- date column labels -->
  <text x="{x_start}" y="{GRID_Y - 10}" class="mono" fill="#424242" font-size="9">{start_label}</text>
  <text x="{x_mid}" y="{GRID_Y - 10}" class="mono" fill="#424242" font-size="9">{mid_label}</text>
  <text x="{x_end + CELL}" y="{GRID_Y - 10}" class="mono" fill="#424242" font-size="9" text-anchor="end">{end_label}</text>

  <!-- day row labels -->{day_els}

  <!-- commit grid -->
  {grid}

  <!-- intensity legend -->
  <text x="{LEG_X}" y="270" class="mono" fill="#363636" font-size="9">INACTIVE</text>
  <rect x="{LEG_X + 68}" y="261" width="9" height="9" rx="2" fill="#2C2C2C" />
  <rect x="{LEG_X + 82}" y="261" width="9" height="9" rx="2" fill="#565656" />
  <rect x="{LEG_X + 96}" y="261" width="9" height="9" rx="2" fill="#9E9E9E" />
  <rect x="{LEG_X + 110}" y="261" width="9" height="9" rx="2" fill="#F0F0F0" />
  <text x="{LEG_X + 124}" y="270" class="mono" fill="#363636" font-size="9">PEAK</text>
</svg>"""


def main() -> None:
    data = load_data()
    (OUT_DIR / "finance-repo-telemetry.svg").write_text(generate_telemetry_svg(data), encoding="utf-8")
    print("Written: finance-repo-telemetry.svg")
    (OUT_DIR / "finance-repo-activity.svg").write_text(generate_activity_svg(data), encoding="utf-8")
    print("Written: finance-repo-activity.svg")


if __name__ == "__main__":
    main()
