import json
import shutil
import os.path

src=os.path.join(os.getcwd(), "sumscraper","arxiv.json")
dst=os.path.join(os.getcwd(), "arxivsanitized.json")
shutil.copyfile(src, dst)

with open(dst, "r", encoding="utf-8") as file:
    data = json.load(file)

for paper in data:
    if "date" in paper and isinstance(paper["date"], str):
        paper["date"] = paper["date"].replace(" ", "")

with open(src, "w", encoding="utf-8") as file:
    json.dump(data,file,indent=0)

