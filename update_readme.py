"Run this after build_database.py - it needs til.db"
import pathlib
import sqlite_utils
import sys
import re
import os
import urllib.parse
from urllib.parse import urlparse
import json
from pathlib import Path

root = pathlib.Path(__file__).parent.resolve()

index_re = re.compile(r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
count_re = re.compile(r"<!\-\- count starts \-\->.*<!\-\- count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"

db = sqlite_utils.Database(root / "til.db")
by_topic = {}
for row in db["til"].rows_where(order_by="created_utc"):
    by_topic.setdefault(row["topic"], []).append(row)
index = ["<!-- index starts -->"]
for topic, rows in by_topic.items():
    index.append("## {}\n".format(topic))
    for row in rows:
        date = row["created"].split("T")[0]
        url = "https://" + urllib.parse.quote(row['url'].replace("https://", ""))
        path = row['url'].replace("https://github.com/Coding4Hours/Til/tree/master/", "") 
        
        # Parse the URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        directory_path = os.path.dirname(path).split('/')[-1]
        file_name = os.path.basename(path)

        if file_name != "index.md":
            with open(f"{directory_path}/index.md", "w") as file:
                file.write("---\nlayout: default\ntitle: Python\n---\nThis is python stuff")
            with open(f"{directory_path}/index.md", "a") as file:
                file.write(f"\n<br>* [{row['title']}](https://coding4hours.github.io/Til/{directory_path}/{file_name}) - {date}")
        
        index.append(
            f"* [{row['title']}]({url}) - {date}"
        )
    index.append("")
if index[-1] == "":
    index.pop()
index.append("<!-- index ends -->")
readme = root / "README.md"
index_txt = "\n".join(index).strip()
readme_contents = readme.open().read()
rewritten = index_re.sub(index_txt, readme_contents)
rewritten = count_re.sub(COUNT_TEMPLATE.format(db["til"].count), rewritten)
print(rewritten)
readme.open("w").write(rewritten)    
