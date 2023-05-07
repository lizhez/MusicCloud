import time
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

url = 'http://localhost:80/'
browser = webdriver.Chrome()
browser.get(url)



def login(id, passwd):
    
    time.sleep(3)

    # 输入用户名和密码
    browser.find_element(By.XPATH,'//input[@class="form-control uname"]').clear()
    browser.find_element(By.XPATH,'//input[@class="form-control uname"]').send_keys(id)
    browser.find_element(By.XPATH,'//input[@class="form-control pword"]').clear()
    browser.find_element(By.XPATH,'//input[@class="form-control pword"]').send_keys(passwd)
    login = browser.find_element(By.ID,'btnSubmit')
    ActionChains(browser).move_to_element(login).click(login).perform()
    time.sleep(1)

def getData():
    li = browser.find_elements(By.XPATH,'//ul[@id="side-menu"]/li')[2]
    ActionChains(browser).move_to_element(li).click(li).perform()
    time.sleep(1)
    user = browser.find_element(By.XPATH,'//a[@href="/system/user"]')
    ActionChains(browser).move_to_element(user).click(user).perform()
    time.sleep(3)
    browser.switch_to.frame("iframe2")
    trs = browser.find_elements(By.XPATH,'//tbody/tr')
    th = browser.find_elements(By.XPATH,'//thead/tr/th') # 1,2,3,4,5,7
    f = open('./rouyi_data.txt','a')
    for i in range(len(trs)):
        tr = browser.find_elements(By.XPATH,'//tbody/tr['+str(i+1)+']/td')
        print('第'+str(i+1)+'个用户：')
        
        f.write('第'+str(i+1)+'个用户：\n')
        for item in range(len(tr)):
            if item==0:continue
            if item==6:continue
            if item==8:continue
            print(th[item].text+': '+tr[item].text)
            f.write(th[item].text+': '+tr[item].text+'\n')
    f.close()
    print('用户信息爬取完成！')
        
    


if __name__ == '__main__':
    id = 'admin'
    passwd = 'admin123'
    login(id,passwd)
    getData()

