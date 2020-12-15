from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import random
import time


def get_rss(url):
    article_list = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')        
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            article = {
                'title': title,
                'link': link,
                'published': published
                }
            article_list.append(article)
        return article_list
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


def set_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    # print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=options)

if __name__ == '__main__':
    print('Starting scraping')
    data = get_rss('https://rss.blog.naver.com/webyoukyung.xml')
    # print(data)
    print('Finished scraping')
    for i,item in enumerate(data):
        wd = set_driver() 
        print(i,'/',len(data), item['title'])
        wd.get(item['link'])
        time.sleep(random.uniform(1,10) * random.randint(1,5))
        wd.quit()
