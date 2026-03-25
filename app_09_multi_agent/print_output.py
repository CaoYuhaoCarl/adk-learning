from rich.console import Console
from rich.markdown import Markdown

with open('ai_research_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

console = Console()
console.print(Markdown(content))
