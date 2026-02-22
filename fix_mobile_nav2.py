import os

files = [
    r"D:\Проект первый Модульные сооружения\catalog.html",
    r"D:\Проект первый Модульные сооружения\production.html",
    r"D:\Проект первый Модульные сооружения\docs.html",
    r"D:\Проект первый Модульные сооружения\sro-gost.html",
    r"D:\Проект первый Модульные сооружения\contacts.html",
    r"D:\Проект первый Модульные сооружения\configurator.html",
]

# Pattern used in these files: 4-space indentation
old_pattern = "        </nav>\n    </div>\n\n    <script"

new_pattern = (
    "        </nav>\n"
    "\n"
    "        <div class=\"mobile-nav-phone\">\n"
    "            <a href=\"tel:+73952000000\" class=\"mobile-nav-phone-link\">+7.3952.00.00.00</a>\n"
    "            <span class=\"mobile-nav-location\">РЕГИОН_38 / ИРКУТСК</span>\n"
    "        </div>\n"
    "    </div>\n"
    "\n"
    "    <script"
)

for filepath in files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        count = content.count(old_pattern)
        if count == 0:
            print(f"PATTERN NOT FOUND: {os.path.basename(filepath)}")
        elif count > 1:
            print(f"MULTIPLE MATCHES ({count}), skipping: {os.path.basename(filepath)}")
        else:
            new_content = content.replace(old_pattern, new_pattern)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"SUCCESS: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"ERROR: {os.path.basename(filepath)} - {e}")
