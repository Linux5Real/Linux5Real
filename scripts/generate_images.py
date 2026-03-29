#!/usr/bin/env python3
import json
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "assets/finance-telemetry/finance-repo-telemetry.json"
OUT_DIR = ROOT / "assets/finance-telemetry"

# Stell sicher, dass das Ausgabe-Verzeichnis existiert
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)

# Gemeinsame CSS-Klassen und Fonts für beide Bilder
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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
    }
    .title {
        margin-left: 20px;
        font-size: 14px;
        font-weight: 700;
        color: #F0F0F0;
    }
    .subtitle {
        color: #303030;
        font-weight: 300;
    }
</style>
"""

def generate_telemetry_html(data: dict) -> str:
    scan = data["scan"]
    # LOC formatieren (z.B. 12 345)
    loc = f"{scan['tracked_lines']:,}".replace(",", " ")
    files = scan["tracked_files"]
    commits_30d = data["activity"]["commits_last_30_days"]
    total_commits = data["activity"]["total_commits"]

    # Sprachen und Farben aus dem alten SVG-Skript rekonstruiert
    # In Zukunft kannst du diese Daten dynamisch aus der JSON laden, falls sie dort verfügbar sind.
    languages = [
        {"name": "Python", "pct": 48.2, "color": "#3572A5"},
        {"name": "CSS", "pct": 21.1, "color": "#563D7C"},
        {"name": "HTML", "pct": 19.3, "color": "#E34C26"},
        {"name": "JavaScript", "pct": 11.4, "color": "#F1E05A"}
    ]

    # HTML für die Language Bar Segmente
    bar_segments = "".join([f'<div style="width: {lang["pct"]}%; background-color: {lang["color"]};"></div>' for lang in languages])
    
    # HTML für die Legende unter der Bar
    legend_items = "".join([
        f'<div class="legend-item">'
        f'<div class="dot" style="background-color: {lang["color"]};"></div>'
        f'{lang["name"]} · {lang["pct"]}%'
        f'</div>'
        for lang in languages
    ])

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        {GLOBAL_CSS}
        <style>
            body {{
                width: 920px;
                height: 332px;
                border-top: 3px solid #FFFFFF;
            }}
            .metrics-band {{
                display: flex;
                height: 110px;
                border-bottom: 1px solid var(--border-color);
                padding: 20px 40px;
                box-sizing: border-box;
            }}
            .metric {{
                flex: 1;
                border-right: 1px solid var(--border-color);
                padding-left: 20px;
            }}
            .metric:first-child {{ padding-left: 0; }}
            .metric:last-child {{ border-right: none; }}
            .metric-label {{
                color: var(--text-secondary);
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2.4px;
                text-transform: uppercase;
                margin-bottom: 12px;
            }}
            .metric-value {{
                font-size: 48px;
                font-weight: 700;
                line-height: 1;
            }}
            .metric-total {{
                font-size: 14px;
                color: #B8B8B8;
                font-weight: 400;
            }}
            .languages-section {{
                padding: 30px 40px;
            }}
            .section-label {{
                color: var(--text-secondary);
                font-size: 11px;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 18px;
            }}
            .progress-bar {{
                height: 24px;
                border-radius: 4px;
                overflow: hidden;
                background: #111111;
                display: flex;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
            }}
            .legend {{
                display: flex;
                margin-top: 15px;
                gap: 25px;
            }}
            .legend-item {{
                font-size: 12px;
                color: #A0A0A0;
                display: flex;
                align-items: center;
                font-weight: 400;
            }}
            .dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="pill">SIGNAL ENGINE</div>
            <div class="title">FINANCE SIGNAL ENGINE <span class="subtitle">· CODE TELEMETRY</span></div>
        </div>
        <div class="metrics-band">
            <div class="metric">
                <div class="metric-label">CODEBASE · LOC</div>
                <div class="metric-value">{loc}</div>
            </div>
            <div class="metric">
                <div class="metric-label">TRACKED FILES</div>
                <div class="metric-value">{files}</div>
            </div>
            <div class="metric">
                <div class="metric-label">COMMITS / 30D</div>
                <div class="metric-value">{commits_30d}</div>
            </div>
            <div class="metric" style="align-self: flex-end;">
                <div class="metric-label" style="margin-bottom: 5px;">TOTAL COMMITS</div>
                <div class="metric-total">{total_commits}</div>
            </div>
        </div>
        <div class="languages-section">
            <div class="section-label">Language Distribution</div>
            <div class="progress-bar">
                {bar_segments}
            </div>
            <div class="legend">
                {legend_items}
            </div>
        </div>
    </body>
    </html>
    """
    return html

def generate_activity_html() -> str:
    # Platzhalter für das zweite Bild ("Execution Tape" / Activity)
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        {GLOBAL_CSS}
        <style>
            body {{
                width: 920px;
                height: 150px;
                border-top: 3px solid #A0A0A0;
            }}
            .tape-container {{
                padding: 20px 40px;
                color: #444;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="pill">EXECUTION TAPE</div>
            <div class="title">RECENT SIGNAL ACTIVITY <span class="subtitle">· LIVE FEED [Placeholder]</span></div>
        </div>
        <div class="tape-container">
            // LIVE SIGNAL FEED WILL APPEAR HERE<br>
            // waiting for signal engine deployment...
        </div>
    </body>
    </html>
    """
    return html

def main() -> None:
    print("Starting PNG generation...")
    data = load_data()
    
    html_telemetry = generate_telemetry_html(data)
    html_activity = generate_activity_html()
    
    # Playwright starten
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Telemetry Image generieren (größer)
        page_tele = browser.new_page(viewport={'width': 920, 'height': 332})
        page_tele.set_content(html_telemetry)
        page_tele.wait_for_load_state('networkidle') # Warten auf Fonts
        page_tele.screenshot(path=str(OUT_DIR / "finance-repo-telemetry.png"))
        print("Generated: finance-repo-telemetry.png")
        
        # Activity Image generieren (flacher)
        page_acti = browser.new_page(viewport={'width': 920, 'height': 150})
        page_acti.set_content(html_activity)
        page_acti.wait_for_load_state('networkidle') # Warten auf Fonts
        page_acti.screenshot(path=str(OUT_DIR / "finance-repo-activity.png"))
        print("Generated: finance-repo-activity.png")
        
        browser.close()
    print("All images updated.")

if __name__ == "__main__":
    main()
