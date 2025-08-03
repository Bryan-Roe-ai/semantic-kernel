import argparse
import sqlite3
from pathlib import Path


def load_decisions(db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    query = "SELECT id, parent_activity_id, timestamp, description FROM ai_activities WHERE activity_type=? ORDER BY timestamp"
    rows = conn.execute(query, ('decision',)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def build_tree(decisions):
    nodes = {d['id']: {**d, 'children': []} for d in decisions}
    roots = []
    for d in decisions:
        pid = d['parent_activity_id']
        node = nodes[d['id']]
        if pid and pid in nodes:
            nodes[pid]['children'].append(node)
        else:
            roots.append(node)
    return roots


def generate_html(trees):
    style = """
    <style>
    body { font-family: Arial, sans-serif; }
    ul { list-style-type: none; padding-left: 1em; }
    li { margin: 0.3em 0; }
    .node { cursor: pointer; }
    .timestamp { color: #666; font-size: 0.9em; margin-left: 0.5em; }
    </style>
    """
    script = """
    <script>
    function toggle(event){
        var next = event.currentTarget.nextElementSibling;
        if(next){
            next.style.display = next.style.display === 'none' ? 'block' : 'none';
        }
    }
    </script>
    """
    html = ["<html><head><meta charset='utf-8'>", style, script, "</head><body>"]
    html.append("<h2>Agent Decision Paths</h2>")
    def render(node):
        label = f"{node['description']}" + f"<span class='timestamp'>{node['timestamp']}</span>"
        part = [f"<li><span class='node' onclick='toggle(event)'>{label}</span>"]
        if node['children']:
            part.append("<ul>")
            for child in node['children']:
                part.append(render(child))
            part.append("</ul>")
        part.append("</li>")
        return ''.join(part)
    html.append("<ul>")
    for t in trees:
        html.append(render(t))
    html.append("</ul></body></html>")
    return ''.join(html)


def main():
    parser = argparse.ArgumentParser(description="Visualize agent decision paths")
    parser.add_argument('--db', default='02-ai-workspace/logs/ai_activities.db', help='Path to activity database')
    parser.add_argument('--output', default='decision_paths.html', help='Output HTML file')
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    decisions = load_decisions(db_path)
    trees = build_tree(decisions)
    html = generate_html(trees)
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"Wrote {args.output} with {len(decisions)} decisions")


if __name__ == '__main__':
    main()
