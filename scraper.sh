#!/bin/bash


scrapy runspider arxiv_spiderCS.py -o scrapedJSON/arxivcsnew.json 

#python3 arxiv_csingest.py

#rm scrapedJSON/arxivcsnew.json