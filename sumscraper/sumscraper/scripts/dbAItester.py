import re
import json
import psycopg2
from ollama import chat
from ollama import ChatResponse


with open("../dblogin.json", "r") as dbconfig:
    config =json.load(dbconfig)

conn =psycopg2.connect(
dbname=config["dbname"],
user=config["user"],
password=config["password"],
host=config["host"],
port=config["port"]
    )   

cursor= conn.cursor()

id_query="""
SELECT id FROM Papers
"""

cursor.execute(id_query)

results=(cursor.fetchall())


#ID query returns tuples despite single values per entry in tuple/array
for x in results[0]:
    #for y in x:
        abstract_query=f"""SELECT abstract FROM papers WHERE id={x};"""
        #print(abstract_query)
        cursor.execute(abstract_query)
        abstract=(cursor.fetchone())

        response: ChatResponse = chat(model="Mistral:7B", messages= [
        {
        'role': 'user',
        'content': f'{abstract} Help me summarize this abstract in layman terms, to the level of understanding achieved by an A level student. Explain jargon and key terms in a list below your summary',
        },
        ])
        print(response['message']['content'])