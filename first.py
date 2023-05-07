import scrapy

class MusicSpider(scrapy.Spider):
    name = "music"
    allowed_domains = ["www.csdn.net"]
    start_urls = ['https://www.csdn.net']

    def parse(self, response):
        # item = MusicItem()
        # item['title']=response.xpath("/html/head/title/text()").extract()[0]
        # item['content'] = response.xpath('//div[@id="content"]/text()').extract()

        print("发起页面信息请求")
        yield scrapy.Request(url=self.start_urls[0], callback=self.test, dont_filter=True)
   
     # 解析页面数据，打印输出测试结果
    def test(self, response):
        resp = response.xpath('//div[@class="tit"]/h2/text()').extract()[0]
        print(resp)
