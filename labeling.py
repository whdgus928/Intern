# pip install keyboard
import pyautogui
import time
import keyboard
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import re
import os
import sys
filePath = os.getcwd().replace('\\','/')
driver_path ='C:\\Users\\user\\Desktop\\python\\test\\chromedriver.exe'

def click_by_xpath(driver, xpath):
    try:
        target = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))  
        #target = driver.find_element(by=By.XPATH, value= xpath)
        target.click()
        return target
    except:
        pass
def login(driver, id, password):
    click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/input').send_keys()
    click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[2]/input').send_keys(password)
    click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/a[1]')
def keypoint_clicker(driver):
    target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div/div[1]/span[2]/span/li').click()
    i = 2
    while True:
        try :
            target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[{i}]/span[2]/span/li/span')
            target.click()
            i += 1
        except Exception as E:
            print(E)
            break
        
def hider(driver):
    try :
        element1 =  driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div')
    except :
        element1 =  driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/div')
    options = element1.find_elements(By.TAG_NAME, "button")
    for option in options:
        if option.get_attribute('innerHTML').split(' ')[2] == 'aria-label="eye"':
            option.click()
def expresser(driver):
    try :
        element1 =  driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div')
    except :
        element1 =  driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/div')
    options = element1.find_elements(By.TAG_NAME, "button")
    for option in options:
        if option.get_attribute('innerHTML').split(' ')[2] == 'aria-label="eye-invisible"':
            option.click()
         
#치아 앞번호 추출
# def teeth_number(text):
#     a=int(text[3])
#     teeth_count+=str(a)
#     target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[{teeth_count}]')
#     target.click()
#     print('click')
#     teeth_count+= 1 

def numbering(driver):
    try :
        target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/button[3]')
        target.click()
    except Exception as E:
        pass
    teeth_count = 1
    teeth_count2 =1
    teeth_count3 = 1
    teeth_count4 = 1
    find_format = re.compile('[0-9]+')
    number = int(find_format.search(driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/span/span/span').get_attribute('innerHTML')).group())
    for i in range(1, number + 1):
        try :
            try: 
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[{i}]')
                target.click()
                time.sleep(0.065)
            except :
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div/div[{i}]')
                target.click()
                time.sleep(0.065)
                pass
            text = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span/span').get_attribute('innerHTML')
            if text=='치아[11~18]':
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[{teeth_count}]')
                target.click()
                #print(teeth_count)
                teeth_count+= 1  
            elif text=='치아[21~28]':
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[{teeth_count2}]')
                target.click()
                teeth_count2+=1
            elif text=='치아[31~38]':
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[{teeth_count3}]')
                target.click()
                teeth_count3+=1
            elif text=='치아[41~48]':
                target = driver.find_element(by=By.XPATH, value= f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[{teeth_count4}]')
                target.click()
                teeth_count4+=1
            else :
                pass
        except Exception as E:
            pass
    save_finder(driver)

# driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span/span')


def save_finder(driver):
    try :
        find_format = re.compile('[가-힣]+')
        bars = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/div[1]')
        options = bars.find_elements(By.TAG_NAME, "button")
        for option in options:
            print(option)
            option_text = find_format.search(option.get_attribute('innerHTML')).group()
            print(option_text)
            if  option_text == '저장':
                option.click()
                break
    except Exception as E:
        print('save_finder Error')
        pass
def imagepath_finder(driver):
    try :
        find_format = re.compile('[0-9][0-9][0-9][0-9][0-9][0-9]')
        image_path = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[1]/h6')
        image_path_text = find_format.search(image_path.get_attribute('innerHTML')).group()
        return image_path_text
    except Exception as E:
        pass
def numberling():
    print()   
    
try :
    driver = webdriver.Chrome(driver_path)
    
except :
    print('######## Chrome Driver Error')
try :
    driver.get('http://192.168.2.179:8282/login')
except :
    print('#### Get URL Error')

try :
    time.sleep(0.5)
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/input')
    SearchInput.send_keys("nuri004")
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[2]/input')
    SearchInput.send_keys("qwert12345")
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/a[1]')
    SearchInput.click() 
except :
    print('#### Get login Error')
try :
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/ul/li/a')
    SearchInput.click() 
except :
    print('#### enter Error')
try :
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/ul/li/div/div/a[1]')
    SearchInput.click() 
except :
    print('#### enter2 Error')
try :
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[3]/select/option[2]')
    SearchInput.click()
except :
    print('#### enter3 Error')
try :
    time.sleep(0.5)
    SearchInput = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[6]/a[1]/span')
    SearchInput.click() 
except :
    print('#### enter4 Error')

while True:
    try:
        if keyboard.is_pressed('`'):
            try :
                pyautogui.keyDown('`')
                pyautogui.click(clicks = 1)
            except Exception as E:
                print('` Pressing Error')
                pass
        elif keyboard.is_pressed('j'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[4]/td[2]/select/option[2]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('j Pressing Error')
                pass
        elif keyboard.is_pressed('k'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[4]/td[2]/select/option[3]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('k Pressing Error')
                pass
        elif keyboard.is_pressed('l'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[4]/td[2]/select/option[4]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('l Pressing Error')
                pass
        elif keyboard.is_pressed('z'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[1]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('1 Pressing Error')
                pass
        elif keyboard.is_pressed('x'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[2]')
                
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('2 Pressing Error')
                pass
        elif keyboard.is_pressed('c'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[3]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('3 Pressing Error')
                pass
        elif keyboard.is_pressed('v'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[4]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('4 Pressing Error')
                pass
        elif keyboard.is_pressed('b'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[5]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('5 Pressing Error')
                pass
        elif keyboard.is_pressed('n'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[6]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('6 Pressing Error')
                pass
        elif keyboard.is_pressed('m'):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[7]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('7 Pressing Error')
                pass
        elif keyboard.is_pressed(','):
            try :
                target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td[2]/select/option[8]')
                target.click()
                #target = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div')
                #target.click()
                time.sleep(0.05)
            except Exception as E:
                print('8 Pressing Error')
                pass
        
        # elif keyboard.is_pressed('spacebar'):
        #     try :
        #         save_finder(driver)
        #         time.sleep(0.05)
        #     except Exception as E:
        #         print('SpaceBar Pressing Error')
        #         pass
        elif keyboard.is_pressed('f9'):
            try :
                keypoint_clicker(driver)
                time.sleep(0.15)
                save_finder(driver)
            except Exception as E:
                print('F9 Pressing Error')
                pass
        #치아번호 자동입력
        elif keyboard.is_pressed('f8'):
            try :
                numbering(driver)
            except Exception as E:
                print('F8 Pressing Error')
                pass
        # 숨기기
        elif keyboard.is_pressed('f2'):
            try :
                hider(driver)
            except Exception as E:
                print('F8 Pressing Error')
                pass
        # 보여주기
        elif keyboard.is_pressed('f3'):
            try :
                expresser(driver)
            except Exception as E:
                print('F6 Pressing Error')
                pass
        # 종료
        elif keyboard.is_pressed('pause break'):
            try :
                exit_ = input("프로그램을 종료하시겠습니까?('yes'를 입력한 뒤 엔터를 누르시면 종료됩니다): ")
                if exit_ == 'yes':
                    break
            except Exception as E:
                print(E)
                print('Pause Break Pressing Error')
        else:
            pass
    except:
        pass
sys.exit()