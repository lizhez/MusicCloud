from scrapy import cmdline
import os

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cmdline.execute(['scrapy','crawl','Music_Could'])
