import re, sys, pathlib
from bs4 import BeautifulSoup

# Usage: python unused_css_report.py style.css page1.html page2.html ...
css_path = pathlib.Path(sys.argv[1])
html_paths = [pathlib.Path(p) for p in sys.argv[2:]]

# Collect all classes/ids in HTML
classes, ids, tags = set(), set(), set()
for p in html_paths:
    html = p.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for el in soup.find_all(True):
        tags.add(el.name)
        if el.get("id"): ids.add(el["id"])
        for c in (el.get("class") or []):
            classes.add(c)

css = css_path.read_text(encoding="utf-8", errors="ignore")

# Naive extract of simple selectors (.class, #id, tag)
class_sel = set(re.findall(r"\.([a-zA-Z0-9_-]+)", css))
id_sel    = set(re.findall(r"#([a-zA-Z0-9_-]+)", css))
tag_sel   = set(re.findall(r"(^|[^\w-])([a-zA-Z][\w-]*)\s*(?=[.{:#,\s>+~])", css))

# tag_sel returns tuples; grab group 1 = separator, group 2 = tag
tag_sel   = {t[1] for t in tag_sel if t[1] not in {'.', '#', ':'}}

unused_classes = sorted([c for c in class_sel if c not in classes])
unused_ids     = sorted([i for i in id_sel    if i not in ids])
unused_tags    = sorted([t for t in tag_sel   if t not in tags])

print("=== Possibly Unused .classes ===")
for c in unused_classes: print(c)
print("\n=== Possibly Unused #ids ===")
for i in unused_ids: print(i)
print("\n=== Possibly Unused tags (be careful) ===")
for t in unused_tags: print(t)

print("\nHINTS:")
print("- Dynamic or conditional classes (JS/Tailwind) may be flagged wrongly—keep them.")
print("- Complex selectors (e.g., `.a .b:hover > li`) aren’t fully resolved by this quick scan.")
