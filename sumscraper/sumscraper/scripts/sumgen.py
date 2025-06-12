import re
import arxiv
import psycopg2
import json

with open("../dblogin.json", "r") as dbconfig:
    config =json.load(dbconfig)

print("dblogin loaded")

conn =psycopg2.connect(
    dbname=config["dbname"],
    user=config["user"],
    password=config["password"],
    host=config["host"],
    port=config["port"]
)

cursor=conn.cursor()
id_query= f"""
  SELECT id FROM papers ORDER BY id Desc Limit 1;
"""
cursor.execute(id_query)
print("ID query executed")
total=cursor.fetchone()[0]

robot_tries=0
for x in range(3,4):
    sum_validate=f"""
    SELECT summary FROM papers WHERE id={x};
    """
    exists=cursor.fetchone()

    print("In for loop")
    
    if not exists:
      title_query=f"""
      SELECT title FROM papers WHERE id={x};
      """
      cursor.execute(title_query)
      title=cursor.fetchone()[0]
      print(title)
      print("Downloading Paper")
      current_paper=f"""
      SELECT pdf_url FROM papers WHERE id={x};
      """
      cursor.execute(current_paper)
      url= cursor.fetchone()[0]
      paper=next(arxiv.Client().results(arxiv.Search(id_list=[re.sub("https://export.arxiv.org/pdf/",'',url)])))
      paper.download_pdf(filename=f"{x}:{title}.pdf")
      robot_tries+=1

      print(f"{robot_tries} request has been processed")


