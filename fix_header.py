
import re

files = [
    r"D:\Проект первый Модульные сооружения\index.html",
    r"D:\Проект первый Модульные сооружения\catalog.html",
    r"D:\Проект первый Модульные сооружения\production.html",
    r"D:\Проект первый Модульные сооружения\docs.html",
    r"D:\Проект первый Модульные сооружения\sro-gost.html",
    r"D:\Проект первый Модульные сооружения\contacts.html",
    r"D:\Проект первый Модульные сооружения\configurator.html",
    r"D:\Проект первый Модульные сооружения\presentation.html",
]

def extract_block_with_depth(text, start_pos, open_tag_prefix, close_tag):
    """Extract a block starting at start_pos, tracking open/close tag depth."""
    depth = 0
    i = start_pos
    while i < len(text):
        if text[i:].startswith(open_tag_prefix):
            depth += 1
            i += len(open_tag_prefix)
        elif text[i:].startswith(close_tag):
            depth -= 1
            if depth == 0:
                end = i + len(close_tag)
                return text[start_pos:end], end
            i += len(close_tag)
        else:
            i += 1
    raise ValueError(f"No matching {close_tag} found starting at {start_pos}")


def restructure_header(html):
    header_pattern = re.compile(
        r'(<header\s+role="banner">)(.*?)(</header>)',
        re.DOTALL
    )

    def replace_header(m):
        open_tag  = m.group(1)
        inner     = m.group(2)
        close_tag = m.group(3)

        # Extract logo block
        logo_m = re.search(r'<a\b[^>]*class="logo"[^>]*>.*?</a>', inner, re.DOTALL)
        if not logo_m:
            raise ValueError("logo <a> not found")
        logo_block = logo_m.group(0)

        # Extract burger-menu block
        burger_m = re.search(r'<button\b[^>]*class="burger-menu"[^>]*>.*?</button>', inner, re.DOTALL)
        if not burger_m:
            raise ValueError("burger-menu <button> not found")
        burger_block = burger_m.group(0)

        # Extract nav block
        nav_m = re.search(r'<nav\b.*?</nav>', inner, re.DOTALL)
        if not nav_m:
            raise ValueError("<nav> not found")
        nav_block = nav_m.group(0)

        # Extract header-right block (depth-aware for nested divs)
        hr_start_m = re.search(r'<div\s+class="header-right">', inner)
        if not hr_start_m:
            raise ValueError("header-right <div> not found")
        header_right_block, _ = extract_block_with_depth(inner, hr_start_m.start(), '<div', '</div>')

        # Detect indentation
        indent_m = re.search(r'^(\s+)<a\b', inner, re.MULTILINE)
        indent = indent_m.group(1) if indent_m else '        '

        new_inner = (
            '\n'
            + indent + '<div class="header-top-row">\n'
            + indent + '    ' + logo_block.strip() + '\n'
            + indent + '    ' + burger_block.strip() + '\n'
            + indent + '    ' + header_right_block.strip() + '\n'
            + indent + '</div>\n'
            + indent + nav_block.strip() + '\n'
        )

        return open_tag + new_inner + close_tag

    new_html, count = header_pattern.subn(replace_header, html)
    if count == 0:
        raise ValueError('No <header role="banner"> match found')
    return new_html, count


results = []
for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()

        new_html, count = restructure_header(original)

        if new_html == original:
            results.append((path, 'SKIPPED', 'Content unchanged (already restructured?)'))
            continue

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        results.append((path, 'OK', f'{count} header(s) rewritten'))

    except Exception as e:
        results.append((path, 'ERROR', str(e)))

for path, status, msg in results:
    fname = path.split("\\")[-1]
    print(f"[{status:7s}] {fname}: {msg}")
