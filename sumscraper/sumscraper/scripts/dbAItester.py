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
        print(x)
        summary_check_query=f"""
        SELECT summary FROM papers WHERE id={x};
        """
        cursor.execute(summary_check_query)
        summary_check=cursor.fetchone()
        #print(summary_check[0])
        if summary_check[0] == None:
              print("No summary, generating now")
        else:
              continue
        abstract_query=f"""SELECT abstract FROM papers WHERE id={x};"""
        #print(abstract_query)
        cursor.execute(abstract_query)
        abstract=(cursor.fetchone())
        print("Generating AI response")
        response: ChatResponse = chat(model="Mistral:7B-instruct", messages= [
        {
        'role': 'user',
        'content': f'{abstract} \n Summarize this  research paper abstract into three parts : 1. Summary (Explain this abstract in plain layman language. Dont use a header for this section) 2.Key Findings(List Major contributions and conclusions in list form below,use header)3.Key Jargon and Definitions(List Jargon and Domain specific terms and their definitions in bullet points below,use header). Use an impersonal tone when writing',
        },
        ])
        print(f"Response retrieved for paper id={x}")
        sumgen= response['message']['content']
        print(sumgen)
        suminsert_query=f"""
        UPDATE papers SET summary= %s WHERE id=%s;
        """
        cursor.execute(suminsert_query,(sumgen,x))
        print(f"Summary added for paper id {x}")
        conn.commit()
cursor.close()
conn.close()