#!/usr/bin/env python3
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "assets/finance-telemetry/finance-repo-telemetry.json"
OUT_DIR = ROOT / "assets/finance-telemetry"

def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)

def generate_telemetry_html(data: dict) -> str:
    scan = data["scan"]
    loc = f"{scan['tracked_lines']:,}".replace(",", " ")
    files = scan["tracked_files"]
    commits_30d = data["activity"]["commits_last_30_days"]
    total_commits = data["activity"]["total_commits"]
    
    # Hier baust du dein Design mit HTML & CSS auf. 
    # Da du HTML/CSS kannst, kannst du das hier perfektionieren!
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
                width: 920px;
                height: 332px;
                background-color: #050505;
                color: #FFFFFF;
                font-family: 'JetBrains Mono', monospace;
                border-top: 3px solid #FFFFFF;
                box-sizing: border-box;
            }}
            .header {{
                background-color: #090909;
                height: 52px;
                border-bottom: 1px solid #1C1C1C;
                display: flex;
                align-items: center;
                padding: 0 30px;
            }}
            .pill {{
                background: #111111;
                border: 1px solid #252525;
                padding: 4px 12px;
                border-radius: 3px;
                color: #7A7A7A;
                font-size: 9px;
                letter-spacing: 1.8px;
            }}
            .title {{
                margin-left: 20px;
                font-size: 13px;
                font-weight: 700;
                color: #F0F0F0;
            }}
            .metrics-band {{
                display: flex;
                background: #070707;
                height: 104px;
                border-bottom: 1px solid #181818;
                padding: 20px 40px;
                box-sizing: border-box;
            }}
            .metric {{
                flex: 1;
                border-right: 1px solid #181818;
                padding-left: 20px;
            }}
            .metric:first-child {{ padding-left: 0; }}
            .metric:last-child {{ border-right: none; }}
            .metric-label {{
                color: #424242;
                font-size: 9px;
                letter-spacing: 2.4px;
                margin-bottom: 15px;
            }}
            .metric-value {{
                font-size: 44px;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="pill">SIGNAL ENGINE</div>
            <div class="title">FINANCE SIGNAL ENGINE <span style="color:#303030; font-weight:normal;">· CODE TELEMETRY</span></div>
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
             <div class="metric">
                <div class="metric-label">TOTAL COMMITS</div>
                <div class="metric-value" style="font-size: 22px; color: #B8B8B8;">{total_commits}</div>
            </div>
        </div>
        </body>
    </html>
    """
    return html

def main() -> None:
    data = load_data()
    
    html_telemetry = generate_telemetry_html(data)
    
    # Playwright starten, um das HTML unsichtbar zu rendern und abzufotografieren
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 920, 'height': 332})
        
        # Telemetry Image generieren
        page.set_content(html_telemetry)
        # Wartet kurz, damit Google Fonts zu 100% geladen sind
        page.wait_for_load_state('networkidle') 
        page.screenshot(path=str(OUT_DIR / "finance-repo-telemetry.png"))
        print("Written: finance-repo-telemetry.png")
        
        # Hier würdest du das Gleiche für das Activity Image machen...
        
        browser.close()

if __name__ == "__main__":
    main()
