import re
import json
import psycopg2
import scrapy
from scrapy.crawler import CrawlerProcess


with open("../dblogin.json", "r") as dbconfig:
    config =json.load(dbconfig)

with open("../domain.json","r") as file:
    tables=json.load(file)

conn =psycopg2.connect(
    dbname=config["dbname"],
    user=config["user"],
    password=config["password"],
    host=config["host"],
    port=config["port"]
)
cursor= conn.cursor()
for x in tables:
    data=[]
    if not re.match(r'^[a-zA-Z0-9_]+$', x):
        print(f"Invalid table name: {x} (contains special characters)")
        continue
    with open(f"../scraped_data/{x}.jl", "r",encoding='utf-8') as file:
        for line in file:
            datum= json.loads(line)
            data.append(datum)   
        for paper in data:
            title=paper["title"]
            abstract=paper['abstract']
            if not title:
                print(f"Skipping entry")
                continue  # Skip this iteration if title is invalid
            if abstract == None:
                print('No abstract skipping entry')
                continue
            table_string=f"""
                SELECT 2 FROM papers WHERE title=%s
                """
            cursor.execute(table_string,(title,))
            exists=cursor.fetchone()
            if not exists:
                query_string=f"""
                    INSERT INTO papers (subject,title,pdf_url,authors,date,publisher,abstract)
                    VALUES (%s, %s, %s, %s, %s, %s,%s);
                """
                cursor.execute(query_string, (paper["subject"],paper["title"], paper["pdf_url"], paper["authors"],paper["date"].lstrip(),paper["publisher"],paper['abstract']))        
            conn.commit()

cursor.close()
conn.close()
print("Ingestion Activity Complete")
