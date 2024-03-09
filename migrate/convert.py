import xml.etree.ElementTree as ET
from pathlib import Path
import re
import markdownify
import wpparser

TEMPLATE =  """---
layout: page
title: {title}
permalink: /{title}/
---
{contents}
"""


xml = "dartmoorrunners.WordPress.2024-03-09.xml"
data = wpparser.parse(xml)


output = Path("../_previous_series")

for post in data["posts"]:
    title = post["title"]
    print(title)
    contents = post["content"]
    # contents = markdownify.markdownify(contents)

    if "table" in contents:
        # print(contents)
        tables = re.search(r"<table(.+)((?:\n.+)+)table>", contents, re.MULTILINE)
        # print(tables)
        if tables:
            print("Convert table")
            table = tables.group()
            contents = contents.replace(table, markdownify.markdownify(table))

    # contents = ""
    markdown = TEMPLATE.format(title=title, contents=contents)

    match = re.search(r"\d{4}", title)
    if not match:
        continue
    year = match.group()
    # season = "summer" if "summer" in title.lower() else "winter"
    title_no_year = title.replace(year, "").replace(" ", "-").lower()
    filename = f"{year}{title_no_year}.md"

    file = output / filename

    with open(file, "w+") as f:
        f.write(markdown)




