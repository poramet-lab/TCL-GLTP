from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "tci_gltp.sqlite3"

SESSION_ROOTS = {
    "poramet": Path("/home/poramet/.codex/sessions"),
    "support": Path("/home/support/.codex/sessions"),
    "first": Path("/home/first/.codex/sessions"),
}
