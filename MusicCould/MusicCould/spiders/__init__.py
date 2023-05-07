# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import json
import requests
import time
import re
from MusicCould.items import MusiccouldItem

class MusicCouldSpider(scrapy.Spider):
    name = "Music_Could"
    start_urls = ['https://music.163.com/#/my/m/music/playlist?id=3222324942']
    
    # def start_requests(self):
    #     log_url = "https://music.163.com"
    #     print("login...")
    #     yield scrapy.Request(url=log_url)

    def parse(self, response):
        print("loading...")
        songslist = response.xpath('//table[@class="m-table "]/tbody/tr/@id').extract()
        for s in songslist:
            
            item = MusiccouldItem()
            item['table_name'] = 'info'
            item['table_fields'] = ['songid','title','singer','belong','contents','loadurl']

            # id
            songId = response.xpath('//tr[@id="'+s+'"]/td[2]/div/div/div[@class="ttc"]/span[@class="txt"]/a/@href').extract()[0]
            item['songid']=songId.split('=')[1]

            # title
            title=response.xpath('//tr[@id="'+s+'"]/td[2]/div/div/div[@class="ttc"]/span[@class="txt"]/a/b/@title').extract()
            item['title'] = title[0].replace(u'\xa0', u' ')

            # singer
            singer = response.xpath('//tr[@id="'+s+'"]/td[4]/div[@class="text"]/span/@title').extract()
            item['singer'] = singer[0].replace(u'\xa0', u' ')

            # belong
            belong = response.xpath('//tr[@id="'+s+'"]/td[5]/div[@class="text"]/a/@title').extract()
            item['belong'] = belong[0].replace(u'\xa0', u' ')

            # loadurl
            item['loadurl']='https://music.163.com/song/media/outer/url?id='+item['songid']+'.mp3'

            # contents
            content_url = 'http://music.163.com/api/song/lyric?'+ songId.split('?')[1] + '&lv=1&kv=1&tv=-1'
            r = requests.get(content_url)
            json_obj = r.text
            obj = json.loads(json_obj)
            str_obj=obj['lrc']['lyric']
            content=re.sub(r'\[.*\]','',str_obj)
            content=content.replace(u'\n', u'<br>')
            item['contents'] = content

            yield item
            time.sleep(10)

        yield
