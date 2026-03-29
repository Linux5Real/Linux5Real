#!/usr/bin/env python3
import json
from datetime import date, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "assets/finance-telemetry/finance-repo-telemetry.json"
OUT_DIR = ROOT / "assets/finance-telemetry"
MONTH_ABBREVIATIONS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
WEEKDAY_LABELS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)

def format_compact_date(value: date) -> str:
    return f"{MONTH_ABBREVIATIONS[value.month - 1]} {value.day:02d}"

def count_active_days(series: list[int]) -> int:
    return sum(1 for count in series if count > 0)

def current_activity_streak(series: list[int]) -> int:
    streak = 0
    for count in reversed(series):
        if count > 0:
            streak += 1
        elif streak:
            break
    return streak

def color_for_count(count: int, max_count: int) -> str:
    if count <= 0:
        return "#0d0d0d"
    if max_count <= 1:
        return "#ffffff"
    ratio = count / max_count
    if ratio < 0.25:
        return "#252525"
    if ratio < 0.5:
        return "#404040"
    if ratio < 0.75:
        return "#7a7a7a"
    return "#ffffff"

GLOBAL_CSS = """
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap" rel="stylesheet">
<style>
    :root {
        --bg-color: #050505;
        --border-color: #181818;
        --text-primary: #FFFFFF;
        --text-secondary: #424242;
        --header-bg: #090909;
        --pill-bg: #111111;
        --pill-text: #7A7A7A;
        --font-mono: 'JetBrains Mono', monospace;
    }
    body {
        margin: 0;
        padding: 0;
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: var(--font-mono);
        box-sizing: border-box;
    }
    .header {
        background-color: var(--header-bg);
        height: 52px;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        padding: 0 30px;
    }
    .pill {
        background: var(--pill-bg);
        border: 1px solid #252525;
        padding: 5px 12px;
        border-radius: 4px;
        color: var(--pill-text);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .pill-dot { width: 6px; height: 6px; border-radius: 50%; background: #fff; flex-shrink: 0; }
    .title {
        margin-left: 20px;
        font-size: 14px;
        font-weight: 700;
        color: #F0F0F0;
    }
    .subtitle { color: #303030; font-weight: 300; }
    .label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        color: #424242;
        margin-bottom: 8px;
    }
</style>
"""


def generate_hero_html() -> str:
    # Icon URLs from skillicons.dev — each icon fetched individually for layout control
    icons = [
        ("https://skillicons.dev/icons?i=python", "Python"),
        ("https://skillicons.dev/icons?i=js", "JS"),
        ("https://skillicons.dev/icons?i=html", "HTML"),
        ("https://skillicons.dev/icons?i=css", "CSS"),
        ("https://skillicons.dev/icons?i=vscode", "VSCode"),
        ("https://skillicons.dev/icons?i=git", "Git"),
        ("https://skillicons.dev/icons?i=github", "GitHub"),
        ("https://skillicons.dev/icons?i=linux", "Linux"),
        ("https://skillicons.dev/icons?i=postgresql", "Postgres"),
        ("https://skillicons.dev/icons?i=bash", "Bash"),
    ]

    icon_cells = ""
    for url, label in icons:
        icon_cells += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:5px;">
          <img src="{url}" width="36" height="36" style="border-radius:8px;" />
          <span style="font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:600;color:#2a2a2a;letter-spacing:0.5px;text-transform:uppercase;">{label}</span>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
{GLOBAL_CSS}
<style>
  body {{ width: 920px; height: 320px; border-top: 3px solid #fff; }}
  .body-wrap {{ display: flex; height: 268px; }}
  .col-left {{
    width: 320px; flex-shrink: 0;
    border-right: 1px solid #181818;
    padding: 22px 28px;
    display: flex; flex-direction: column; justify-content: space-between;
  }}
  .col-mid {{
    flex: 1;
    border-right: 1px solid #181818;
    display: flex; flex-direction: column;
  }}
  .col-mid-inner {{ display: flex; flex: 1; }}
  .col-mid-sub {{
    flex: 1;
    padding: 18px 20px;
    border-right: 1px solid #181818;
  }}
  .col-mid-sub:last-child {{ border-right: none; }}
  .icon-strip {{
    border-top: 1px solid #181818;
    padding: 10px 20px;
    display: flex; align-items: center; gap: 16px;
    height: 68px; box-sizing: border-box;
  }}
  .col-right {{
    width: 180px; flex-shrink: 0;
    padding: 18px 20px;
    display: flex; flex-direction: column; gap: 7px;
  }}
  .tag-bright {{
    display: inline-flex; align-items: center;
    background: #fff; border-radius: 4px;
    padding: 4px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 700; color: #000;
    letter-spacing: 1px; text-transform: uppercase;
    white-space: nowrap;
  }}
  .tag-mid {{
    display: inline-flex; align-items: center;
    background: #111; border: 1px solid #2a2a2a; border-radius: 4px;
    padding: 4px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 600; color: #888;
    letter-spacing: 1px; text-transform: uppercase;
    white-space: nowrap;
  }}
  .tag-dim {{
    display: inline-flex; align-items: center;
    background: #0d0d0d; border: 1px solid #1e1e1e; border-radius: 4px;
    padding: 4px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 600; color: #555;
    letter-spacing: 1px; text-transform: uppercase;
    white-space: nowrap;
  }}
  .big-name {{
    font-size: 58px; font-weight: 900; color: #fff;
    letter-spacing: -2px; line-height: 0.95;
    margin-bottom: 12px;
  }}
  .bio {{ font-size: 12px; color: #555; line-height: 1.6; }}
  .footer-mono {{ font-size: 9px; color: #222; letter-spacing: 1.2px; text-transform: uppercase; }}
  .col-label {{ font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #424242; margin-bottom: 8px; }}
  .col-value {{ font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 6px; }}
  .col-detail {{ font-size: 11px; color: #444; line-height: 1.7; }}
</style>
</head>
<body>
  <div class="header">
    <div class="pill"><span class="pill-dot"></span>PROFILE</div>
    <div class="title">Linus <span class="subtitle">&middot; @Linux5Real</span></div>
    <div style="flex:1;"></div>
    <div style="font-size:10px;color:#2a2a2a;">Germany &middot; Age 18</div>
  </div>

  <div class="body-wrap">
    <!-- LEFT -->
    <div class="col-left">
      <div>
        <div class="col-label">Builder &middot; Trader</div>
        <div class="big-name">Linus</div>
        <div class="bio">Building private finance AI systems<br>for market context and execution.</div>
      </div>
      <div class="footer-mono">Private Systems &middot; Market Context</div>
    </div>

    <!-- MIDDLE -->
    <div class="col-mid">
      <div class="col-mid-inner">
        <div class="col-mid-sub">
          <div class="col-label">Focus</div>
          <div class="col-value">Finance AI</div>
          <div class="col-detail">Market context<br>Execution workflow<br>Signal routing</div>
        </div>
        <div class="col-mid-sub">
          <div class="col-label">Trading</div>
          <div class="col-value">Swing &rarr; Day</div>
          <div class="col-detail">Stocks &amp; catalysts<br>US equities<br>Chart-driven</div>
        </div>
        <div class="col-mid-sub">
          <div class="col-label">Current Build</div>
          <div class="col-value">Signal Engine</div>
          <div class="col-detail">DeepSeek &amp; Grok<br>Private trading desk<br>AI model routing</div>
        </div>
      </div>
      <!-- ICON STRIP -->
      <div class="icon-strip">
        {icon_cells}
      </div>
    </div>

    <!-- RIGHT -->
    <div class="col-right">
      <div class="col-label">Identity</div>
      <span class="tag-bright">Private Builder</span>
      <span class="tag-mid">Finance AI</span>
      <span class="tag-dim">Market Context</span>
      <span class="tag-dim">Exec. Discipline</span>
      <span class="tag-dim">Swing &rarr; Day</span>
      <span class="tag-dim">Germany</span>
    </div>
  </div>
</body></html>"""


def generate_telemetry_html(data: dict) -> str:
    scan = data["scan"]
    loc = f"{scan['tracked_lines']:,}".replace(",", " ")
    files = scan["tracked_files"]
    commits_30d = data["activity"]["commits_last_30_days"]
    total_commits = data["activity"]["total_commits"]

    languages = [
        {"name": "Python", "pct": 48.2, "color": "#3572A5"},
        {"name": "CSS", "pct": 21.1, "color": "#563D7C"},
        {"name": "HTML", "pct": 19.3, "color": "#E34C26"},
        {"name": "JavaScript", "pct": 11.4, "color": "#F1E05A"}
    ]
    bar_segments = "".join([f'<div style="width: {lang["pct"]}%; background-color: {lang["color"]};"></div>' for lang in languages])
    legend_items = "".join([
        f'<div class="legend-item"><div class="dot" style="background-color: {lang["color"]};"></div>{lang["name"]} &middot; {lang["pct"]}%</div>'
        for lang in languages
    ])

    html = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    {GLOBAL_CSS}
    <style>
        body {{ width: 920px; height: 332px; border-top: 3px solid #FFFFFF; }}
        .metrics-band {{ display: flex; height: 110px; border-bottom: 1px solid var(--border-color); padding: 20px 40px; box-sizing: border-box; }}
        .metric {{ flex: 1; border-right: 1px solid var(--border-color); padding-left: 20px; }}
        .metric:first-child {{ padding-left: 0; }}
        .metric:last-child {{ border-right: none; }}
        .metric-label {{ color: var(--text-secondary); font-size: 10px; font-weight: 700; letter-spacing: 2.4px; text-transform: uppercase; margin-bottom: 12px; }}
        .metric-value {{ font-size: 48px; font-weight: 700; line-height: 1; }}
        .metric-total {{ font-size: 14px; color: #B8B8B8; font-weight: 400; }}
        .languages-section {{ padding: 30px 40px; }}
        .section-label {{ color: var(--text-secondary); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 18px; }}
        .progress-bar {{ height: 24px; border-radius: 4px; overflow: hidden; background: #111111; display: flex; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); }}
        .legend {{ display: flex; margin-top: 15px; gap: 25px; }}
        .legend-item {{ font-size: 12px; color: #A0A0A0; display: flex; align-items: center; font-weight: 400; }}
        .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
    </style></head><body>
        <div class="header">
            <div class="pill">SIGNAL ENGINE</div>
            <div class="title">FINANCE SIGNAL ENGINE <span class="subtitle">&middot; CODE TELEMETRY</span></div>
        </div>
        <div class="metrics-band">
            <div class="metric"><div class="metric-label">CODEBASE &middot; LOC</div><div class="metric-value">{loc}</div></div>
            <div class="metric"><div class="metric-label">TRACKED FILES</div><div class="metric-value">{files}</div></div>
            <div class="metric"><div class="metric-label">COMMITS / 30D</div><div class="metric-value">{commits_30d}</div></div>
            <div class="metric" style="align-self: flex-end;"><div class="metric-label" style="margin-bottom: 5px;">TOTAL COMMITS</div><div class="metric-total">{total_commits}</div></div>
        </div>
        <div class="languages-section">
            <div class="section-label">Language Distribution</div>
            <div class="progress-bar">{bar_segments}</div>
            <div class="legend">{legend_items}</div>
        </div>
    </body></html>"""
    return html


def generate_activity_html(data: dict | None = None) -> str:
    data = data or load_data()
    activity = data["activity"]
    series = activity.get("activity_series", [])[-84:]
    if len(series) < 84:
        series = ([0] * (84 - len(series))) + series

    max_count = max(series) if series else 0
    active_days = count_active_days(series)
    streak = current_activity_streak(series)
    peak = max_count
    total_commits = activity.get("total_commits", 0)
    commits_30d = activity.get("commits_last_30_days", 0)
    last_commit_raw = activity.get("last_commit_date")
    end_date = date.fromisoformat(last_commit_raw) if last_commit_raw else date.today()
    start_date = end_date - timedelta(days=83)
    grid_start = start_date - timedelta(days=start_date.weekday())
    week_count = ((end_date - grid_start).days // 7) + 1
    count_by_date = {start_date + timedelta(days=i): count for i, count in enumerate(series)}

    cell = 16; gap = 4; step = cell + gap; grid_y = 22
    cells = []; month_labels = []; seen_months: set[int] = set()
    current_date = grid_start
    grid_end = grid_start + timedelta(days=week_count * 7 - 1)
    while current_date <= grid_end:
        week_index = (current_date - grid_start).days // 7
        day_index = current_date.weekday()
        x = week_index * step; y = grid_y + day_index * step
        count = count_by_date.get(current_date, 0)
        color = color_for_count(count, max_count)
        cells.append(f'<div title="{format_compact_date(current_date)}: {count} commit{"s" if count != 1 else ""}" style="position:absolute;left:{x}px;top:{y}px;width:{cell}px;height:{cell}px;border-radius:3px;background:{color};"></div>')
        if current_date.month not in seen_months:
            seen_months.add(current_date.month)
            month_labels.append(f'<div style="position:absolute;left:{week_index*step}px;top:0;font-size:10px;color:#3a3a3a;font-family:var(--font-mono);font-weight:600;letter-spacing:0.06em;white-space:nowrap;">{MONTH_ABBREVIATIONS[current_date.month-1]}</div>')
        current_date += timedelta(days=1)

    grid_width = week_count * step
    grid_height = grid_y + 7 * step
    weekday_labels = ""
    for index, weekday in enumerate(WEEKDAY_LABELS):
        if index % 2 == 0:
            weekday_labels += f'<div style="position:absolute;right:0;top:{grid_y+index*step}px;height:{cell}px;display:flex;align-items:center;font-size:9px;color:#2a2a2a;font-family:var(--font-mono);font-weight:600;letter-spacing:0.06em;">{weekday}</div>'

    html = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    {GLOBAL_CSS}
    <style>
        body {{ width: 920px; height: 320px; border-top: 3px solid #FFFFFF; }}
        .activity-wrap {{ display: flex; height: 268px; }}
        .activity-stats {{ width: 300px; flex-shrink: 0; border-right: 1px solid var(--border-color); padding: 20px 24px; display: flex; flex-direction: column; justify-content: space-between; }}
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px 24px; }}
        .metric-label {{ color: var(--text-secondary); font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }}
        .metric-value {{ font-size: 36px; font-weight: 700; line-height: 1; }}
        .total-block {{ border-top: 1px solid var(--border-color); padding-top: 14px; }}
        .total-value {{ font-size: 28px; font-weight: 800; line-height: 1; }}
        .total-sub {{ font-size: 10px; color: #2A2A2A; letter-spacing: 1px; margin-top: 6px; }}
        .activity-grid {{ flex: 1; padding: 16px 24px; display: flex; align-items: center; overflow: hidden; }}
    </style></head><body>
        <div class="header">
            <div class="pill">EXECUTION TAPE</div>
            <div class="title">RECENT SIGNAL ACTIVITY <span class="subtitle">&middot; 84-day commit grid</span></div>
        </div>
        <div class="activity-wrap">
            <div class="activity-stats">
                <div class="stats-grid">
                    <div><div class="metric-label">30D Commits</div><div class="metric-value">{commits_30d}</div></div>
                    <div><div class="metric-label">Active Days</div><div class="metric-value">{active_days}</div></div>
                    <div><div class="metric-label">Peak Day</div><div class="metric-value">{peak}</div></div>
                    <div><div class="metric-label">Streak</div><div class="metric-value">{streak}d</div></div>
                </div>
                <div class="total-block">
                    <div class="metric-label">Total Commits</div>
                    <div class="total-value">{total_commits}</div>
                    <div class="total-sub">LAST SIGNAL &middot; {format_compact_date(end_date)}</div>
                </div>
            </div>
            <div class="activity-grid">
                <div style="display:flex;align-items:flex-start;gap:10px;width:100%;">
                    <div style="position:relative;width:28px;flex-shrink:0;height:{grid_height}px;">{weekday_labels}</div>
                    <div style="position:relative;width:{grid_width}px;height:{grid_height}px;flex-shrink:0;">{''.join(month_labels)}{''.join(cells)}</div>
                </div>
            </div>
        </div>
    </body></html>"""
    return html


def main() -> None:
    print("Starting PNG generation...")
    data = load_data()

    html_hero = generate_hero_html()
    html_telemetry = generate_telemetry_html(data)
    html_activity = generate_activity_html(data)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Hero — 2x scale for sharp quality
        page_hero = browser.new_page(viewport={'width': 920, 'height': 320}, device_scale_factor=2)
        page_hero.set_content(html_hero)
        page_hero.wait_for_load_state('networkidle')
        page_hero.screenshot(path=str(OUT_DIR / "finance-hero.png"))
        print("Generated: finance-hero.png")

        page_tele = browser.new_page(viewport={'width': 920, 'height': 332}, device_scale_factor=2)
        page_tele.set_content(html_telemetry)
        page_tele.wait_for_load_state('networkidle')
        page_tele.screenshot(path=str(OUT_DIR / "finance-repo-telemetry.png"))
        print("Generated: finance-repo-telemetry.png")

        page_acti = browser.new_page(viewport={'width': 920, 'height': 320}, device_scale_factor=2)
        page_acti.set_content(html_activity)
        page_acti.wait_for_load_state('networkidle')
        page_acti.screenshot(path=str(OUT_DIR / "finance-repo-activity.png"))
        print("Generated: finance-repo-activity.png")

        browser.close()
    print("All images updated.")


if __name__ == "__main__":
    main()
