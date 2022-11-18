# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import signals
from pydispatch import dispatcher
import pandas as pd
import os

from sqlalchemy.orm import sessionmaker
from itemadapter import ItemAdapter
import psycopg2


class ListingsPipeline:
    
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def process_item(self, item, spider):
        return item

    def spider_closed(self, spider):
      # second param is instance of spder about to be closed.
        df = pd.read_excel(os.path.join('results','output-listings.xlsx'))
        df.drop_duplicates(inplace=True)
        df.to_excel(os.path.join('results','output-listings.xlsx'), index=False)



class PostgresFBPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'khanbbbb' # your password
        database = 'fb_data'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create listings table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS listings(
            name VARCHAR(255), 
            title VARCHAR(1000),
            price VARCHAR(100),
            description text,
            date_posted text,
            path text,
            source_url VARCHAR(2000)
        )
        """)
    
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into listings (name, title, price, description, date_posted, path,source_url) values (%s,%s,%s,%s,%s,%s,%s)""", (
            item["name"],
            str(item["title"]),
            item["price"],
            item["description"],
            item["date_posted"],
            item["path"],
            item["source_url"],
           
        ))

        ## Execute insert of data into database
        self.connection.commit()
        
        return item
        
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()


      