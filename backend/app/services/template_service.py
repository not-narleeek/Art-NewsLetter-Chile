from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import List, Dict, Any

# Points to 'backend/app/templates'
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_newsletter(events: List[Any], title: str, preview_text: str = "") -> str:
    template = env.get_template("newsletter/base.html")
    return template.render(events=events, title=title, preview_text=preview_text)
