# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import urllib.request
import time
import cv2 as cv
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MusiccouldSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class Login:

    def load_checkcodeimgs(self,bg_img,tg_img):
        
        current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        bg_path = 'D:\\projs\\scrapy\\checkcode\\bg\\' + current_time + '.png'
        tg_path = 'D:\\projs\\scrapy\\checkcode\\tg\\' + current_time + '.png'
        
        urllib.request.urlretrieve(bg_img, bg_path)
        urllib.request.urlretrieve(tg_img, tg_path)

        return bg_path,tg_path


    def get_checkcode(self,bg_img,tg_img):
        # 获取验证码
        bg_path,tg_path = self.load_checkcodeimgs(bg_img,tg_img)

        bg = cv.imread(bg_path)
        tg = cv.imread(tg_path)

        bg_eage = cv.Canny(bg, 255, 255)
        tg_eage = cv.Canny(tg, 255, 255)

        bg_pic = cv.cvtColor(bg_eage,cv.COLOR_GRAY2RGB)
        tg_pic = cv.cvtColor(tg_eage,cv.COLOR_GRAY2RGB)

        res = cv.matchTemplate(bg_pic, tg_pic, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res) # 寻找最优匹配

        return max_loc[0]

    def slider_checkcode(self,distance,browser):
        # 移动轨迹计算
        track = []
        current = 0
        start = distance / 10 
        mid = distance * 4 / 5
        t = 0.4
        v = 0
        while current < distance:
            if current < start:
                a = 5
            elif current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t 
            move = v0 * t + 1 / 2 * a * t * t 
            current = current + move
            track.append(round(move))
        track[-1]=distance-sum(track[0:-1])

        # 移动滑块
        actions = ActionChains(browser)
        slider = browser.find_element(By.XPATH,'//div[@class="yidun_slider  yidun_slider--hover "]')
        actions.click_and_hold(slider).perform()
        for x in track:
            actions.move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(1)
        actions.release().perform()

    def getList(self,browser):
        pass

    def login(self,id, passwd,browser):
        
        time.sleep(5)
        
        # 定位手机号登陆
        a_el = browser.find_element(By.XPATH,'//a[@class="link s-fc3"]')
        ActionChains(browser).move_to_element(a_el).click(a_el).perform()
        time.sleep(1)
        phone1 = browser.find_element(By.XPATH,'//a[@class="_3xIXD0Q6"]')
        ActionChains(browser).move_to_element(phone1).click(phone1).perform()
        time.sleep(1)
        phone2 = browser.find_element(By.ID,'j-official-terms')
        ActionChains(browser).move_to_element(phone2).click(phone2).perform()
        phone3 = browser.find_element(By.XPATH,'//a[@class="_3fo6oHZe _10mxG2UY _1Gh25bMk"]')
        ActionChains(browser).move_to_element(phone3).click(phone3).perform()
        time.sleep(1)
        phone4 = browser.find_element(By.XPATH,'//div[@class="_3Mb1fXSG"]/a')
        ActionChains(browser).move_to_element(phone4).click(phone4).perform()
        time.sleep(1)

        # 输入用户名和密码
        browser.find_element(By.XPATH,'//input[@class="_2OT0mQUQ"]').clear()
        browser.find_element(By.XPATH,'//input[@class="_2OT0mQUQ"]').send_keys(id)
        browser.find_element(By.XPATH,'//input[@class="sR89MU1J"]').clear()
        browser.find_element(By.XPATH,'//input[@class="sR89MU1J"]').send_keys(passwd)
        login = browser.find_element(By.XPATH,'//a[@class="_3fo6oHZe _10mxG2UY _19WWNTbu"]')
        ActionChains(browser).move_to_element(login).click(login).perform()
        time.sleep(1)

        # 验证码破解
        bg_img = browser.find_element(By.XPATH,'//img[@class="yidun_bg-img"]').get_attribute("src")
        tg_img = browser.find_element(By.XPATH,'//img[@class="yidun_jigsaw"]').get_attribute("src")
        bg_location = self.get_checkcode(bg_img,tg_img)+10
        self.slider_checkcode(bg_location,browser)
        time.sleep(5)

class MusiccouldDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        browser = webdriver.Chrome()

        if "https://music.163.com" == request.url:
            browser.get(request.url)
            logining = Login()
            logining.login('18348360307','952088z,',browser)
            cookies = browser.get_cookies()
            jsonData = json.dumps(cookies)
            with open("./cookie.json", 'w') as fp:
                fp.write(jsonData)
                print("cookie存储成功")
                return None
            
        # 正常请求，加载 cookie
        with open("./cookie.json", "r") as fp2:
            list_cookies = json.loads(fp2.read())
 
        browser.get(request.url)  # 预请求
        for cookie in list_cookies:
            browser.add_cookie(cookie)
        
        browser.get(request.url)  # 携带cookie的真实请求
        browser.refresh()  # 刷新页面
        time.sleep(2)    # 等待页面加载 
        browser.switch_to.frame("contentFrame")

        data = browser.page_source # 获取页面
        browser.close()
        # 封装返回对象
        response = HtmlResponse(url=request.url, body=data, encoding='utf-8', request=request)
        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
