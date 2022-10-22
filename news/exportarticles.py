import datetime
import os

from nation import SCRAPENATION
from articles2pdf import PDF

# link to get articles
web = 'https://nation.africa/kenya'
SCRAPENATION.parse_url_num_articles_delta(web,1000,0)
nation = SCRAPENATION()

# get article dimensions
par = nation.get_paragraphs()
country,cat = nation.get_country_cat()
time,author =  nation.get_author_time()
time_delta = nation.get_time_delta()
title = nation.get_title()
links = nation.all_page_links()

# combine the articles
print('fetching articles...')
articlez = nation.get_articles()
print('articles fetched.')

# print the pdf copy of the scraped articles
pdf =PDF()
n= 0

print('initializing export to pdf')
print(os.getcwd())

for article in articlez:
    title,category,author,date,article = article
    author_date = author+' | ' +  date
    PDF.title_topic_date(title,category,author_date)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True,margin=10)
    pdf.chapter_body(article)
    n = n+1
    
# export
pdf.output(f'{os.getcwd()}/WhatsApp-Bot/static/articles/{datetime.datetime.today().strftime("%Y-%m-%d-%H")}-nation.pdf')
print('articles export complete')