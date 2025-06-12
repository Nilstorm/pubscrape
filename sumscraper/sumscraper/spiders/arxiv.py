from pathlib import Path
import scrapy
import re
import json
from pylatexenc.latex2text import LatexNodes2Text


class arxivAll(scrapy.Spider):
     name="arxiv"
     allowed_domains=['arxiv.org']
     start_urls=["https://export.arxiv.org/"]

     custom_settings ={
         'FEED_URI': 'scraped_data/arxiv.jl',
         'FEED_FORMAT':'jsonlines',
         'FEED_EXPORT_ENCODING': 'utf-8',
         'FEED_STORE_APPEND': True,
         'FEED_EXPORT_FIELDS': ['subject','title','pdf_url','authors','date','license','publisher','abstract'],
         'LOG_FILE':'arxiv_output.log',
         'LOG_LEVEL':'INFO'
     }
     def parse(self,response):
         #Starts at landing page of URL
         for subject in response.css("li"):
                 #Get Subject name
                 subject_name=subject.css("b::text").get()

                 #Query String
                 query="?skip=0&show=50"
                 
                 #Get link to follow to newest (appended with query string to yield recent 50)
                 subject_link=subject.xpath(".//a[contains(text(), 'new')]/@href").get()
                 print(subject_link)

                 if subject_link:
                     subject_link_with_query=response.urljoin(subject_link) + query
                     yield response.follow(
                        subject_link_with_query,
                        callback=self.subjectdivination,
                    #   headers
                        meta={"subject": subject_name,}
                     )
                 else:
                  self.logger.warning(f"No 'new' link found for subject: {subject_name}")


                 
     def subjectdivination(self, response):
        # Called back per 'Subject' values block yielded from landing page in 'parse' method

        # Loop through each <dl> block    
            subject_name=response.meta['subject']
            for paper in response.css("dl"):
                ## Initialize empty lists to store the papers' data
             
                #tags=[]

                # Loop through the dt/dd pairs inside each <dl> block
                for dt, dd in zip(paper.css("dt"), paper.css("dd")):
                    # Extract PDF link from <dt>
                    pdf_link = response.urljoin(dt.css("a[title='Download PDF']::attr(href)").get())

                    # get follow URL to acquire Date
                    date_link = dt.css("a[title='Abstract']::attr(href)").get()
                    
                    # Extract title from <dd>
                    title = dd.css("div.list-title.mathjax::text").getall()

                    # Extract authors from <dd> - all <a> tags inside <dd> for authors
                    author_list = dd.css("a::text").getall()

                    abstract= dd.css("p.mathjax::text").get()

                    # Extract Subjects for tags
                    #     tag = dd.css("span.primary-subject::text").get()

                    self.logger.info(f"Processing paper: {title}, date_link: {date_link}")


                    if date_link:
                        yield response.follow(
                              date_link,
                              callback=self.parse_post,
                    #          headers=headers
                              meta={"subject": subject_name,"title": title, "pdf_link": pdf_link, "authors": author_list, "abstract": abstract}
                     )
                    else:
                        self.logger.warning(f"No date link found for {title}")


     def parse_post(self, response):
          datefollow=re.sub('[()]','',response.css("div.dateline::text").get())
          abstract=response.meta['abstract']
          subject=response.meta['subject']
          license=response.css("div.abs-license a::attr(href)").get()
          title =re.sub('\n','',response.meta['title'][1])
          pdf_link=response.meta["pdf_link"]
          author=response.meta["authors"] 
          date=datefollow.replace("Submitted on","")

          

          if not re.search("/by/4.0", license):
              print(f"{title} Not the right license\n")
              return
          
          try:
            print(abstract)
          except:
            print("No Abstract") 
          

          def clean_text(title):
               title=title.replace("'\\'","'\'")
               return LatexNodes2Text().latex_to_text(title)

          
          title_sanitized=clean_text(title)
          print(f"Original title={title}")
          print(f"Sanitized title={title_sanitized}")
          
          existing_titles=set()
          collated_titles=set()

          try:
               with open("scraped_data/arxiv.jl","r",encoding="utf-8") as f:
                    for line in f:
                         data=json.loads(line)
                         existing_titles.add(clean_text(data["title"]))
          except:
               print("arxiv.jl not found, creating.")

          
          try:
               with open("scraped_data/collated.jl","r",encoding="utf-8") as f:
                    for line in f:
                         data=json.loads(line)
                         collated_titles.add(clean_text(data["title"]))
          except:
               print("collated_data.jl not found.")

                         
          if title_sanitized in existing_titles:
                print("Duplicate Found, not yielding")
                return

          elif title_sanitized in collated_titles:
                print("Duplicate found in collated titles, not yielding")
                return
            
          yield {
                "subject": subject,
                "title": title_sanitized,
                "abstract":abstract,
                "pdf_url": pdf_link,
                "authors": author,
                "date": date,  # Use the date from the follow-up page if available, else fallback to main page date
                "license":license,
                "publisher":"arxiv"
          }
          print("Added Paper to JSON")
          return

               
            