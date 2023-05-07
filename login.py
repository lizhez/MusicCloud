import urllib.request
import os
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

def load_checkcodeimgs(bg_img,tg_img):
    
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    bg_path = 'D:\\projs\\scrapy\\checkcode\\bg\\' + current_time + '.png'
    tg_path = 'D:\\projs\\scrapy\\checkcode\\tg\\' + current_time + '.png'
    
    urllib.request.urlretrieve(bg_img, bg_path)
    urllib.request.urlretrieve(tg_img, tg_path)

    return bg_path,tg_path


def get_checkcode(bg_img,tg_img):
    # 获取验证码
    bg_path,tg_path = load_checkcodeimgs(bg_img,tg_img)

    bg = cv.imread(bg_path)
    tg = cv.imread(tg_path)

    bg_eage = cv.Canny(bg, 255, 255)
    tg_eage = cv.Canny(tg, 255, 255)

    bg_pic = cv.cvtColor(bg_eage,cv.COLOR_GRAY2RGB)
    tg_pic = cv.cvtColor(tg_eage,cv.COLOR_GRAY2RGB)

    # cv.imshow("bg", bg_eage)
    # cv.waitKey(3)
    # cv.imshow("tg", tg_eage)
    # cv.waitKey(3)

    # 缺口匹配
    res = cv.matchTemplate(bg_pic, tg_pic, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res) # 寻找最优匹配
    
    # 绘制方框
    # th, tw = tg_pic.shape[:2] 
    # tl = max_loc # 左上角点的坐标
    # br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    # cv.rectangle(bg, tl, br, (0, 0, 255), 2) # 绘制矩形
    # cv.imwrite(out, bg_img) # 保存在本地
    # cv.imshow("bg_get", bg)
    # cv.waitKey(3)
        
    # cv.destroyAllWindows()

    return max_loc[0]

def slider_checkcode(distance):
    # 移动轨迹计算
    # distance += 10
    track = []# 移动轨迹，里面保留的是每次移动的距离
    current = 0# 当前位移
    start = distance / 10 # 减速阈值，前面4/5做匀加速移动，后面1/5做匀减速移动
    mid = distance * 4 / 5
    t = 0.4# 计算间隔，每次移动两秒
    v = 0# 初速度
    while current < distance:#当移动的距离超过，目标距离后，就停止循环
        if current < start:
            a = 5#前面匀加速的加速度为正2
        elif current < mid:
            a = 2
        else:
            a = -3#后面匀减速的加速度为负3
        v0 = v# 初速度 v0
        v = v0 + a * t #当前速度 v = v0 + at
        move = v0 * t + 1 / 2 * a * t * t # 移动距离 x = v0t + 1/2 * a * t^2
        current = current + move#总位移
        track.append(round(move))#每次移动的距离
    track[-1]=distance-sum(track[0:-1])#上面计算的总距离，会超过目标距离，所以最后一个移动距离需要修正一下

    # 移动滑块
    actions = ActionChains(browser)#创建动作链
    slider = browser.find_element(By.XPATH,'//div[@class="yidun_slider  yidun_slider--hover "]')#运用Xpath方法获取滑块元素
    actions.click_and_hold(slider).perform()#点击滑块，并保持点击动作
    for x in track:
        actions.move_by_offset(xoffset=x, yoffset=0).perform()#拖动滑块
    time.sleep(1)
    actions.release().perform()#松开滑块，验证完成。



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
    bg_img = browser.find_element(By.XPATH,'//img[@class="yidun_bg-img"]').get_attribute("src")
    tg_img = browser.find_element(By.XPATH,'//img[@class="yidun_jigsaw"]').get_attribute("src")
    bg_location = get_checkcode(bg_img,tg_img)+10
    slider_checkcode(bg_location)


if __name__ == '__main__':
    id = '18348360307'
    passwd = '952088z,'
    login(id,passwd)

