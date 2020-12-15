from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import random
import time
import json


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

def get_proxies():
    print('Starting scraping proxies')
    driver = webdriver.Chrome(options=basic_options())
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])
    driver.quit()
    print('Finished scraping proxies',proxies)
    return proxies
    
def basic_options():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])#
    options.add_experimental_option('useAutomationExtension', False)#
#     options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    return options

def set_driver(proxies):
    options = basic_options()
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    proxy = proxies[random.randint(0,len(proxies)-1)]
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--proxy-server={proxies[random.randint(0,len(proxies)-1)]}')
    print(user_agent,"ip:", proxy, end=" ")
    return webdriver.Chrome(options=options)


if __name__ == '__main__':
    print('Starting scraping rss')
    data = get_rss('https://rss.blog.naver.com/webyoukyung.xml')
    print('Finished scraping rss')
    proxies = get_proxies()
    for i,item in enumerate(data):
        wd= set_driver(proxies)
        try:
            print(' ',i,'/',len(data), item['title'])
            wd.get(item['link'])
            if "Proxy Type" in WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))):
                break
        except Exception:
            wd.quit()
        try:
            wd.quit()
        except:
            break