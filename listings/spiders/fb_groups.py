import scrapy
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep
from w3lib.html import remove_tags
from openpyxl import load_workbook,Workbook
from ..utils import driver_instance , storing_data , scroll_down_page , formate_date
import codecs
import os

class FbGroupsSpider(scrapy.Spider):
    
    name = 'groups'
    allowed_domains = ['www.facebook.com']
    
    def __init__(self, scroll=2 , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_count = int(scroll)
        #Initiating Chrome Driver Instance
        self.driver = driver_instance()

    start_urls = ['https://www.example.com']
    

    def parse(self, response):

        with open('groups.txt','r') as r:
            for group_url in r.readlines():
                self.driver.get(group_url)
                scroll_down_page(self.driver,self.scroll_count)

                html_page = Selector(text = self.driver.page_source)
                html_page = html_page.xpath('//div[@class="x78zum5 xdt5ytf"]')
                
                for each_post in html_page:
                    
                    listing_url = each_post.xpath('(.//a[@class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1rg5ohu x1a2a7pz x1ey2m1c xds687c x10l6tqk x17qophe x13vifvy x1pdlv7q"]/@href)[1]').get()

                    if listing_url:
                        post_id = listing_url.split('/?media_id')[0]
                        post_url = 'https://web.facebook.com'+post_id
                        listing_id = post_id.split('listing/')[-1]+'\n'

                        name = each_post.xpath('.//h2[@class="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz x1gslohp x1yc453h"]//span/text()').get()
                        time_posted  = formate_date(each_post.xpath('//div[@class="xu06os2 x1ok221b"]/span//a/@aria-label').get())

                        try:
                            scraped_file = open('listings_done.txt', 'r') 
                            lines = scraped_file.readlines()
                        except Exception(FileNotFoundError):
                            storing_data([])

                        if listing_id in lines:
                            continue
                                
                        
                        self.driver.get(post_url)
                        sleep(5)

                        

                        #Saving HTML data
                        path_to_save = os.path.join('results',f'{listing_id.strip()}')
                        f = codecs.open(f'{path_to_save}.html', "w", "utf−8")
                        f.write(self.driver.page_source)
                        f.close()

                        #Path to files
                        current_path = os.getcwd()
                        absolute_url = str(os.path.join(f'{current_path}', 'results',f'{listing_id}'))+".html"

                        listing_source = Selector(text = self.driver.page_source)
                        title = listing_source.xpath('//div[1]/h1/span/text()').get()
                        price = listing_source.xpath('//div[@class="x1xmf6yo"]/div/span/text()').get()
                        try:
                            description =remove_tags(listing_source.xpath('//div[@class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]').get())
                        except TypeError: 
                            description = ''
                        
                        source_url = self.driver.current_url

                        #STORING DATA INTO EXCEL FILE
                        storing_data([name,title,price,description,time_posted,absolute_url,source_url])

                        with open("listings_done.txt",'a+') as w:
                            w.write(listing_id)
                        
                        yield{
                            "name":name,
                            "title": title,
                            "price":price,
                            "description":description,
                            "date_posted":time_posted,
                            "path":absolute_url,
                            "source_url" : source_url
                            }
                        
                        
