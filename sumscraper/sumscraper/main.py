from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import psycopg2
import re

with open("tablelist.json","r") as file:
    tables=json.load(file)

process=CrawlerProcess(get_project_settings())

for x in tables:
    process.crawl(x)
process.start()


collated = set()
try:
    with open('scraped_data/collated.jl', 'r',encoding="utf-8") as file:
        for line in file:
            data=json.loads(line)
            collated.add(data["title"])

except FileNotFoundError:
     print("collated jsonlist not found(2)")

for x in tables:
    checker=set ()
    with open(f"scraped_data/{x}.jl",'r',encoding='utf-8') as file:
        for line in file:
            data=json.loads(line)
            checker.add(data["title"])
    for entry in checker:
        print (entry)
        if not entry in collated:
            collated.add(entry)
            print(f"Added ")
        else:
            print(f" Entry is already in the collated JSON")

with open('scraped_data/collated.jl','w',encoding='utf-8') as file:
       for line in collated:
           prepare={"title":line}
           json.dump(prepare,file,ensure_ascii=False, separators=(',',':'))   
           file.write('\n')
        
print("Collation completed")


