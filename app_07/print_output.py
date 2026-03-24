from IPython.display import display, Markdown

# Read and display the markdown file
with open('ai_research_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

display(Markdown(content))
