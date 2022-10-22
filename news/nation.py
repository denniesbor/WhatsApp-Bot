import datetime
from bs4 import BeautifulSoup
import requests
import re


class SCRAPENATION:
    num_articles = None
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}
    web_url = None
    delta = None
    http = 'https://nation.africa'
    
    def __init__(self):
        self.get_article = requests.get(SCRAPENATION.web_url,headers=SCRAPENATION.headers)
        self.soup = BeautifulSoup(self.get_article.content,'html.parser')
        
    def all_page_links(self):
        page_links = []
        try:
            links = self.soup.find_all('a')
            for link in links:
                if 'href' in link.attrs:
                    link_ = link['href']
                    pat = re.compile(r'\D\-\d{7}$')
                if link_ not in page_links and re.search(pat,link_):
                    if 'https' in link_:
                        page_links.append(link_)
                    else:
                        page_links.append(SCRAPENATION.http + link_)
        except:
            return None
        return page_links
    
    def get_paragraphs(self):
        pars = []
        try:
            if self.soup != None:
                text_block = self.soup.find_all('div',class_="paragraph-wrapper")
                if text_block == []:
                    text_block = self.soup.find('article', class_="article").find_all('p')
            for par in text_block:
                try:
                    pars.append(par.p.get_text().strip())
                except AttributeError:
                    pars.append(par.get_text().strip())
                except:
                    pass
        except:
            try:
                paragraphs = []
                article = self.soup.find('p',class_="card-text").find_next_siblings('p')
                for paragraph in article:
                  if paragraph.get_text().strip() != '\n' or paragraph.get_text().strip() != ' ':
                    pars.append(paragraph.get_text().strip())
            except AttributeError:
                return None
      # return entire article
    
        return '\n'.join(pars)
    
    def get_author_time(self):
        try:
            time = self.soup.find('time').get_text().strip()
            author = self.soup.find('div','article-authors_texts').p.a.get_text().strip()
        except AttributeError:
            try:
                author = self.soup.find('article', class_="article").find('strong').get_text()
                time = self.soup.find('header').find('h6').get_text()
            except AttributeError:
                return None,None
        return time,author
    
    def get_country_cat(self):
        web_add = SCRAPENATION.web_url.lower().split('/')
        country = web_add[3]
        try:
            if 'historical-flashback' in web_add:
                cat = 'historical-flashback'
            elif 'east-africa' in web_add:
                cat = 'east-africa'
            elif 'africa' in web_add:
                cat = 'africa'
            elif 'counties' in web_add:
                cat = 'counties'
            elif 'news' in web_add:
                cat = 'news'
            elif 'sports' in web_add:
                cat = 'sports'
            elif 'blogs-opinion' in web_add:
                cat = 'blogs-opinion'
            else:
                cat = web_add[4]
            return country.capitalize(),cat.capitalize()
        except:
            return country.capitalize(),None

    def get_title(self):
        try:
            title = self.soup.find('header',class_="article-header").find('h1').get_text().strip()
        except AttributeError:
            title = self.soup.find('title').get_text().strip()
        except Exception:
            title = self.soup.find('header').find('h2').get_text()
        except:
            return None
        return title
    
    def get_article_links(self):
        pat = re.compile(r'\D\-\d{7}$')
        pat1 = re.compile(r'=https')
        pat3 = re.compile(r'/audio/')
        article_links = []
#         try:
        nation_links = SCRAPENATION().all_page_links()
        for link in nation_links:
            SCRAPENATION.parse_url_num_articles_delta(link,SCRAPENATION.num_articles,SCRAPENATION.delta)
            nation = SCRAPENATION()
            time_delta = nation.get_time_delta()
            links = nation.all_page_links()
            nation_links = nation_links+links
            if link not in article_links and time_delta <= SCRAPENATION.delta:
                if re.search(pat,link):
                    if not re.search(pat1,link) and not re.search(pat3,link):
                        article_links.append(link)
                        nation_links.append(link)
                        print(link)
                else:
                    nation_links.append(link)
            if len(article_links) > SCRAPENATION.num_articles:
                break
        return article_links
#         except:
#             return article_links

    def get_time_delta(self):
        time,author =  SCRAPENATION().get_author_time()
        if time == None:
            return 0
        else:
            try:
                date_time = datetime.datetime.strptime(time,'%A, %B %d, %Y')
                today = datetime.datetime.now()
                time_delta = (today - date_time).days
                return time_delta
            except ValueError:
                try:
                    date_time = datetime.datetime.strptime(time,'%A %B %d %Y')
                    today = datetime.datetime.now()
                    time_delta = (today - date_time).days
                    return time_delta
                except ValueError:
                    return 5
#     @staticmethod

    def get_articles(self):
        news = []
        history = []
        articles = []
        counties = []
        africa = []
        east_africa = []
        sports = []
        opinion = []
        business = []
#         try:
        articlelinks = SCRAPENATION().get_article_links()
        for article in articlelinks:
            SCRAPENATION.parse_url_num_articles_delta(article,SCRAPENATION.num_articles,SCRAPENATION.delta)
            nation = SCRAPENATION()
            title = nation.get_title()
            par = nation.get_paragraphs()
            country,cat = nation.get_country_cat()
            time,author =  nation.get_author_time()
            cate= cat.lower()
            if par != None and cate != 'audio':
                if len(par) > 500:
                    if time == None:
                        time = 'UnKnown Date'
                    if author == None:
                        author = 'Unknown Author'
                    if title == None:
                        title = 'Untitled'
                    if cate== 'historical-flashback':
                        history.append([title,cat,author,time,par])
                    elif cate== 'east-africa':
                        east_africa.append([title,cat,author,time,par])
                    elif cate== 'africa':
                        africa.append([title,cat,author,time,par])
                    elif cate== 'counties':
                        counties.append([title,cat,author,time,par])
                    elif cate== 'news':
                        news.append([title,cat,author,time,par])
                    elif cate== 'sports':
                        sports.append([title,cat,author,time,par])
                    elif cate== 'blogs-opinion':
                        opinion.append([title,cat,author,time,par])
                    elif cate == 'business':
                        business.append([title,cat,author,time,par])
                    else:
                        articles.append([title,cat,author,time,par])
        return news+counties+opinion+east_africa+africa+history+sports+articles
#         except:
#             return news+counties+opinion+east_africa+africa+history+sports+articles

    @classmethod
    def parse_url_num_articles_delta(cls,url,num,time_delta):
        cls.web_url = url
        cls.num_articles = num
        cls.delta= time_delta
        
        
        
