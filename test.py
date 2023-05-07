import time
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

from pathlib import Path
from PIL import Image
import cv2 as cv

url = 'https://music.163.com/'
browser = webdriver.Chrome()
browser.get(url)

def screenshot() -> str:
    # 保存全屏截图
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    current_time1 = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    print(current_time )
    print(current_time1 )
    pic_path = 'D:\\projs\\scrapy\\music\\image\\' + current_time1 + '_' + current_time + '.png'
    browser.save_screenshot(pic_path)

    #定位验证码
    picture = Image.open(pic_path)
    picture = picture.crop((447, 261, 849, 462))
    picture.save(pic_path)

    return pic_path


def check_code():
    # 获取验证码
    image_path = screenshot()

    image = cv.imread(image_path)
    image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    # blurred = cv.GaussianBlur(image, (5, 5), 0)
    # canny = cv.Canny(blurred, 160, 400)
    canny = cv.Canny(image, 255, 255)
    cv.imshow("canny", canny)
    cv.waitKey(3)
    contours, hierarchy = cv.findContours(canny, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):  
        # 所有轮廓    
        x, y, w, h = cv.boundingRect(contour)  
        # 外接矩形    
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow('image', image)
        cv.waitKey(3)

    
    for i, contour in enumerate(contours):  
        # 所有轮廓    
        if 6000 < cv.contourArea(contour) <= 8000 and 300 < cv.arcLength(contour, True) < 500:        
            x, y, w, h = cv.boundingRect(contour)  
            # 外接矩形        
            print(x, y, w, h)        
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)        
            cv.imshow('image', image)        
            # 找目标缺口，第一个可能是滑块        
            if x <= 200:            
                continue        
            return x + int(w / 2), 675
        
    # cv.destroyAllWindows()

def login(id, passwd):
    
    time.sleep(3)
    
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
    check_code()


if __name__ == '__main__':
    id = '18348360307'
    passwd = '952088z,'
    login(id,passwd)

