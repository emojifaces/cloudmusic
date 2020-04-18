# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
import time
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymysql
import csv





class LyricPipeline(object):

    def process_item(self, item, spider):
        return item


class FormatPipeline(object):

    def process_item(self, item, spider):

        item['img_url'] = re.sub(r'\?param=\d+y\d+','',item['img_url'])
        item['lyric'] = re.sub(r'\[.*]','',item['lyric'])
        item['lyric'] = re.sub(r'\s',' ',item['lyric'])
        item['publish_time'] = time.strftime('%Y.%m.%d',time.localtime(int(item['publish_time'])/1000))
        return item

class ImagePipeline(ImagesPipeline):

    name_list = []

    def get_media_requests(self, item, info):

        name = item['artist_name']
        url = item['img_url']
        if name in self.name_list:
            raise DropItem('该图片已下载')
        yield Request(url=url,meta={'name': name})

    def file_path(self, request, response=None, info=None):

        name = request.meta.get('name')
        file_name = name + '.' + request.url.split('.')[-1]
        return file_name

class MysqlPipeline(object):

    def __init__(self,host,port,database,user,password):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into music_EN (%s) values (%s)' % (keys, values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()


class CSVPipeline(object):

    def open_spider(self,spider):
        self.file = open('../cloudmusic.csv','a',encoding='utf-8')

    def process_item(self,item,spider):

        fieldnames = ['artist_id','artist_name','img_url','album_num','album_size','song_name','song_id',
                      'album_name','album_id','publish_time','lyric',]
        writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(dict(item))

        return item

    def close_spider(self,spider):
        self.file.close()