import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "scripts" / "generate_images.py"


def load_generate_images_module():
    playwright_module = types.ModuleType("playwright")
    sync_api_module = types.ModuleType("playwright.sync_api")
    sync_api_module.sync_playwright = lambda: None
    playwright_module.sync_api = sync_api_module
    sys.modules["playwright"] = playwright_module
    sys.modules["playwright.sync_api"] = sync_api_module

    spec = importlib.util.spec_from_file_location("generate_images", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generate_activity_html_uses_real_activity_data(monkeypatch):
    module = load_generate_images_module()
    sample_data = {
        "activity": {
            "commits_last_30_days": 17,
            "total_commits": 137,
            "last_commit_date": "2026-03-29",
            "activity_series": [0, 1, 0, 2, 1, 0, 3] * 12,
        }
    }

    monkeypatch.setattr(module, "load_data", lambda: sample_data)

    html = module.generate_activity_html()

    assert "Placeholder" not in html
    assert "waiting for signal engine deployment" not in html
    assert "84-day commit grid" in html
    assert "30D Commits" in html
    assert "Active Days" in html
    assert "Total Commits" in html
    assert "17" in html
    assert "137" in html
