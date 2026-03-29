#!/usr/bin/env python3
"""
Generate telemetry SVGs for Linux5Real GitHub profile.
Reads: assets/finance-telemetry/finance-repo-telemetry.json
Writes: assets/finance-telemetry/finance-repo-telemetry.svg
        assets/finance-telemetry/finance-repo-activity.svg
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "assets/finance-telemetry/finance-repo-telemetry.json"
OUT_DIR = ROOT / "assets/finance-telemetry"

STYLE = """  <style>
    .ui { font-family: 'Segoe UI', Arial, sans-serif; }
    .mono { font-family: 'IBM Plex Mono', 'JetBrains Mono', 'Fira Code', Consolas, monospace; }
    .eyebrow { fill: #FAFAFA; font-size: 11px; font-weight: 700; letter-spacing: 2.4px; text-transform: uppercase; }
    .label { fill: #A8A8A8; font-size: 10px; letter-spacing: 1.6px; text-transform: uppercase; }
    .value { fill: #FFFFFF; font-size: 26px; font-weight: 700; }
    .muted { fill: #8C8C8C; font-size: 11px; }
  </style>"""


def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def fmt_number(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")


def activity_color(commits: int, max_commits: int) -> str:
    if commits == 0:
        return "#101010"
    ratio = commits / max_commits
    if ratio < 0.25:
        return "#333333"
    elif ratio < 0.5:
        return "#666666"
    elif ratio < 0.75:
        return "#B5B5B5"
    return "#FFFFFF"


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
    BAR_W = 258

    lang_rows = ""
    y = 164
    for i, (lang, lines) in enumerate(sorted_langs):
        bar_fill = min(BAR_W, int(BAR_W * lines / max_lines)) if max_lines > 0 else 0
        gray = 255 - int(80 * i / max(len(sorted_langs) - 1, 1))
        color = f"#{gray:02X}{gray:02X}{gray:02X}"
        lang_rows += f"""
    <text x="490" y="{y}" class="ui" fill="#F1F1F1" font-size="14" font-weight="600">{escape(lang)}</text>
    <text x="820" y="{y}" class="mono" fill="#999999" font-size="12" text-anchor="end">{escape(fmt_number(lines))} lines</text>
    <rect x="490" y="{y + 8}" width="{BAR_W}" height="9" rx="4" fill="#1A1A1A" />
    <rect x="490" y="{y + 8}" width="{bar_fill}" height="9" rx="4" fill="{color}" />"""
        y += 38

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="340" viewBox="0 0 920 340" role="img" aria-label="Finance Repo Telemetry">
  <title>Finance Repo Telemetry</title>
{STYLE}
  <rect width="920" height="340" rx="24" fill="#020202" />
  <rect x="20" y="20" width="880" height="300" rx="18" fill="#070707" stroke="#2D2D2D" />
  <line x1="40" y1="44" x2="880" y2="44" stroke="#1F1F1F" />

  <text x="48" y="66" class="mono eyebrow">PRIVATE REPO TELEMETRY</text>
  <text x="48" y="100" class="ui" fill="#FAFAFA" font-size="28" font-weight="700">Finance Repo Telemetry</text>
  <text x="48" y="122" class="ui" fill="#D4D4D4" font-size="14">Finance Signal Engine</text>
  <text x="48" y="144" class="ui muted">Source-safe telemetry only — activity exposed, code withheld.</text>

  <text x="48" y="186" class="ui label">Tracked LOC</text>
  <text x="48" y="218" class="ui value">{loc}</text>
  <text x="210" y="186" class="ui label">Tracked Files</text>
  <text x="210" y="218" class="ui value">{files}</text>
  <text x="368" y="186" class="ui label">Commits 30D</text>
  <text x="368" y="218" class="ui value">{commits_30d}</text>

  <text x="48" y="262" class="ui muted">Contributors: {contributors}</text>
  <text x="190" y="262" class="ui muted">Last commit: {last_commit}</text>
  <text x="370" y="262" class="ui muted">Total commits: {total_commits}</text>

  <rect x="468" y="56" width="372" height="248" rx="14" fill="#070707" stroke="#2A2A2A" />
  <text x="490" y="86" class="mono eyebrow">CODE MIX</text>
  <text x="490" y="106" class="ui muted" font-size="11">Top languages by non-empty tracked lines</text>
  <line x1="490" y1="116" x2="820" y2="116" stroke="#1E1E1E" />
{lang_rows}
</svg>"""


def generate_activity_svg(data: dict) -> str:
    activity = data["activity"]
    commits_30d = activity["commits_last_30_days"]
    last_commit = activity["last_commit_date"]

    GRID_X, GRID_Y = 448, 116
    CELL, GAP = 14, 6
    COLS, ROWS = 12, 7

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
    cells = []
    for col in range(COLS):
        for row in range(ROWS):
            idx = col * ROWS + row
            color = activity_color(padded[idx], max_commits)
            cx = GRID_X + col * (CELL + GAP)
            cy = GRID_Y + row * (CELL + GAP)
            cells.append(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="3" fill="{color}" />')

    grid = "\n  ".join(cells)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="296" viewBox="0 0 920 296" role="img" aria-label="Finance Repo Activity">
  <title>Finance Repo Activity</title>
{STYLE}
  <rect width="920" height="296" rx="24" fill="#020202" />
  <rect x="20" y="20" width="880" height="256" rx="18" fill="#070707" stroke="#2B2B2B" />

  <text x="48" y="54" class="mono eyebrow">REPO ACTIVITY</text>
  <text x="48" y="74" class="ui label">SESSION SUMMARY</text>
  <text x="48" y="100" class="ui" fill="#FAFAFA" font-size="16" font-weight="700">Finance Repo Telemetry</text>
  <text x="48" y="120" class="ui" fill="#D4D4D4" font-size="12">Finance Signal Engine</text>
  <text x="48" y="140" class="ui muted">84-day repo activity &#x2014; {escape(str(commits_30d))} commits in the last 30 days</text>

  <line x1="376" y1="36" x2="376" y2="260" stroke="#232323" />

  <text x="48" y="180" class="ui label">30D COMMITS</text>
  <text x="48" y="200" class="mono" fill="#FFFFFF" font-size="17" font-weight="700">{escape(str(commits_30d))} commits</text>
  <text x="210" y="180" class="ui label">ACTIVE DAYS</text>
  <text x="210" y="200" class="mono" fill="#FFFFFF" font-size="17" font-weight="700">{escape(str(active_days))} sessions</text>
  <text x="48" y="232" class="ui label">PEAK SESSION</text>
  <text x="48" y="252" class="mono" fill="#FFFFFF" font-size="17" font-weight="700">{escape(str(peak))} commits</text>
  <text x="210" y="232" class="ui label">CURRENT STREAK</text>
  <text x="210" y="252" class="mono" fill="#FFFFFF" font-size="17" font-weight="700">{escape(str(streak))} days</text>
  <text x="48" y="270" class="ui muted">Last print: {escape(last_commit)}</text>

  <text x="408" y="54" class="mono eyebrow">SESSION TAPE</text>
  <text x="408" y="72" class="ui muted">84 trading days &#x2014; execution-style activity grid.</text>

  <text x="718" y="54" class="ui label">LOW</text>
  <rect x="754" y="44" width="11" height="11" rx="2" fill="#101010" />
  <rect x="772" y="44" width="11" height="11" rx="2" fill="#333333" />
  <rect x="790" y="44" width="11" height="11" rx="2" fill="#666666" />
  <rect x="808" y="44" width="11" height="11" rx="2" fill="#B5B5B5" />
  <rect x="826" y="44" width="11" height="11" rx="2" fill="#FFFFFF" />
  <text x="846" y="54" class="ui label">HIGH</text>

  <text x="{GRID_X - 20}" y="{GRID_Y + 10}" class="ui" fill="#9E9E9E" font-size="10" text-anchor="end">Mon</text>
  <text x="{GRID_X - 20}" y="{GRID_Y + 50}" class="ui" fill="#9E9E9E" font-size="10" text-anchor="end">Wed</text>
  <text x="{GRID_X - 20}" y="{GRID_Y + 90}" class="ui" fill="#9E9E9E" font-size="10" text-anchor="end">Fri</text>
  <text x="{GRID_X - 20}" y="{GRID_Y + 130}" class="ui" fill="#9E9E9E" font-size="10" text-anchor="end">Sun</text>

  {grid}
</svg>"""


def main() -> None:
    data = load_data()
    (OUT_DIR / "finance-repo-telemetry.svg").write_text(generate_telemetry_svg(data), encoding="utf-8")
    print("Written: finance-repo-telemetry.svg")
    (OUT_DIR / "finance-repo-activity.svg").write_text(generate_activity_svg(data), encoding="utf-8")
    print("Written: finance-repo-activity.svg")


if __name__ == "__main__":
    main()
