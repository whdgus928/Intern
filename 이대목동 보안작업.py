# pip install sqlalchemy
# pip install chromedriver_autoinstaller
# pip install psycopg2
import os
import traceback
import re
from urllib.parse import quote
import sqlalchemy as db
from sqlalchemy.engine import create_engine
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller as AutoChrome
from logging.config import dictConfig
import logging
import datetime
import sys
from selenium.webdriver.common.keys import Keys
filePath, fileName = os.path.split(__file__)
logFolder = os.path.join(filePath , 'logs')
os.makedirs(logFolder, exist_ok = True)
logfilepath = os.path.join(logFolder, fileName.split('.')[0] + '_' +re.sub('-', '', str(datetime.date.today())) + '.log')
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s --- %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': logfilepath,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})         
# 로그 메시지 출력
def log(msg):
    logging.info(msg)
# 웹 알람 승인
def alarm_accept(driver):
    try:
        da = Alert(driver)
        da.accept()
    except:
        pass
# XPATH 이용 클릭(클릭이 가능할 때까지 암묵적 대기 3초)
def click_by_xpath(driver, xpath):
    try:
        target = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        target.click()
        return target
    except:
        log(f'######## ERROR : CLICK_BY_XPATH : {xpath}')
        log(traceback.format_exc())
        raise
# XPATH 이용 클릭(엘리먼트가 보일 때 까지)
def click_by_visible_xpath(driver, xpath):
    try:
        target =WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        target.click()
        return target
    except:
        log('######## ERROR : CLICK_BY_VISIBLE_XPATH')
        log(traceback.format_exc())
        raise
# 크롬드라이버 실행 및 옵션 설정 코드
def start_driver(driver_path, url, down_path = None):
    try:
        log('#### Start Driver')
        chrome_options = webdriver.ChromeOptions()
        # 서버 전용 옵션 활성화
        chrome_options.add_argument('--headless') # 보이지 않는 상태에서 작업
        chrome_options.add_argument('--window-size=1920x1080') # 보이지 않는 상태의 창 크기 설정
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--blink-setting=imagesEnable=false") ##페이지 로딩에서 이미지 제외
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--disable-gpu")
        # 다운로드 경로 변경 및 기타 옵션 설정
        if down_path == None:
            prefs = {
                'download.prompt_for_download': False,
                'download.directory_upgrade': True
                }
            chrome_options.add_experimental_option('prefs', prefs)
        else:
            prefs = {
                'download.default_directory': down_path,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
                }
            chrome_options.add_experimental_option('prefs', prefs)
        # 드라이브 시작
        driver = webdriver.Chrome(service = Service(driver_path), options = chrome_options)
        driver.implicitly_wait(100) # 대기 시작 설정
        driver.get(url) # URL 적용
        # 로딩 대기
        return driver
    except:
        log('######## ERROR :START DRIVER')
        log(traceback.format_exc())
        raise
# 어노테이션툴 로그인
def login(driver, id, password):
    try:
        click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/input').send_keys(id) # 아이디 입력 
        click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/div[2]/input').send_keys(password) # 비밀번호 입력
        click_by_xpath(driver, '/html/body/div[2]/div/div/div/div/div/div[2]/div/form/a[1]') # 로그인 클릭
    except:
        log('######## ERROR : LOGIN')
        log(traceback.format_exc())
        raise
# 키포인트 클릭하기
def keypoint_clicker(driver, count_number):
    try:
        # 첫번째 구역 클릭
        click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div/div[1]/span[2]/span/li')
        time.sleep(0.25)
        # 라벨이 한개 보다 많으면, 계속해서 다음 라벨 클릭
        if count_number > 1:
            i = 2
            for i in range(2, count_number + 1):
                # log(f'#### Count Number : {count_number}, i : {i}')
                try :
                    click_by_xpath(driver, f'/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[{i}]/span[2]/span/li/span')
                    time.sleep(0.25)
                except Exception as E:
                    log(E)
                    raise
            log('반복문 탈출')
    except :
        log('######## ERROR : KEYPOINT_CLICKER')
        log(traceback.format_exc())
        raise
# 저장 텍스트 찾아서, 클릭해주는 함수
def save_finder(driver):
    try :
        find_format = re.compile('[가-힣]+')
        bars = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/div[1]')
        options = bars.find_elements(By.TAG_NAME, "button")
        for option in options:
            option_text = find_format.search(option.get_attribute('innerHTML')).group()
            if  option_text == '저장':
                option.click()
                time.sleep(3)
                click_by_xpath(driver,'/html/body/div[6]/div/div/div[2]/button') # 확인 버튼 누르기
                break
    except Exception as E:
        log('######## ERROR : SAVE FINDER')
        log(traceback.format_exc())
        raise
# 완료 텍스트 찾아서 클릭해주는 함수
def wanryo_finder(driver):
    try :
        find_format = re.compile('[가-힣]+')
        bars = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/div[1]')
        options = bars.find_elements(By.TAG_NAME, "button")
        for option in options:
            option_text = find_format.search(option.get_attribute('innerHTML')).group()
            if  option_text == '완료':
                option.click()
                time.sleep(1.5)
                # click_by_xpath(driver,'/html/body/div[6]/div/div/div[2]/button')
                break
    except Exception as E:
        log('######## ERROR : WANRYO_FINDER')
        log(traceback.format_exc())
        raise
# 어노테이션툴 내 라벨 개수 가져오는 코드
def att_checker(driver, xpath, df, index, column_name):
    try:
        bars = driver.find_elements(by=By.XPATH, value= xpath)
        find_format = re.compile('[0-9]+')
        for bar in bars:
            bar_text = find_format.search(bar.get_attribute('innerHTML')).group()
            if  bar_text != '':
                df.loc[index,column_name] = bar_text
                return int(bar_text)
    except :
        log('######## ERROR : ATT_CHECKER')
        log(traceback.format_exc())
        raise
# 크롬드라이버 자동 다운로드
def driver_downloader():
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0] # 현재 버전의 앞 두숫자
    current_list = os.listdir(os.getcwd())          #현재 디렉토리 내 파일/폴더의 리스트
    if not chrome_ver in current_list:              # 버전명으로 된 폴더가 있는지 확인.
        print("크롬드라이버 다운로드 실행")
        AutoChrome.install(True)
        print("크롬드라이버 다운로드 완료")
    else: print("크롬드라이버 버전이 최신입니다.")
    return chrome_ver
def main():
    vin_df = pd.DataFrame(columns = ['image_id', 'bf_rectangle', 'bf_polygon', 'bf_keypoint', 'att_rectangle', 'att_polygon', 'att_keypoint', 'af_rectangle', 'af_polygon', 'af_keypoint', 'result'])
    # db 연결
    engine = create_engine('postgresql://mruser:%s@192.168.2.185:6343/mr_db' % quote('y^5hEXwpQYqXM%A3'))
    # 아이디 - 작업자 고유 아이디 입력 필요(숫자형태로 입력), 로그인 아이디 - 작업자 로그인 아이디 입력(문자열 형태), 패스워드 - 작업자 비밀번호 입력(문자열 형태)
    id = 402
    login_id = 'dent008'
    password = 'qwert12345'
    # df_추출
    sql_query = f"select * from issues where assigned_to_id = '{id}';"
    df_comp = pd.read_sql(sql_query, engine)
    # 상태가 완료거나 1차 검수, 작업중인 데이터 뽑기 | (df_comp['status_id'] == 2)  | (df_comp['status_id'] == 3) 
    df_comp = df_comp[(df_comp['status_id'] == 4)].reset_index(drop = True)
    log(df_comp)
    # 크롬 접속, 로그인
    chrome_ver = driver_downloader()
    driver_path = os.path.join(filePath, chrome_ver,'chromedriver.exe')
    url = 'http://192.168.2.189:8282/login'
    driver = start_driver(driver_path, url)
    login(driver, login_id, password)
    # 작업관리 클릭
    click_by_xpath(driver, '/html/body/div[1]/ul/li/a/span')
    # 작업진행관리 클릭
    click_by_xpath(driver, '/html/body/div[1]/ul/li/div/div/a[1]')
    index = 0
    while index < len(df_comp):
        try :
            if index % 30 == 0 and index != 0:
                log(f'#### {index}')
                try:
                    driver.close()
                except:
                    log('30번째 : 드라이버 이미 종료')
                    pass
                # 크롬 접속, 로그인
                try:
                    chrome_ver = driver_downloader()
                except:
                    log('30번째 : 드라이버 재설치 시도 실패')
                try:
                    driver_path = os.path.join(filePath, chrome_ver,'chromedriver.exe')
                    url = 'http://192.168.2.189:8282/login'
                    driver = start_driver(driver_path, url)
                    login(driver, login_id, password)
                except:
                    log('30번째 : 드라이버 재시작 시도 실패')
                # 작업관리 클릭
                click_by_xpath(driver, '/html/body/div[1]/ul/li/a/span')
                # 작업진행관리 클릭
                click_by_xpath(driver, '/html/body/div[1]/ul/li/div/div/a[1]')
                log("#### 크롬 드라이버 재시작")
            image_path = df_comp.loc[index , 'subject']
            time.sleep(1.3)
            # 이미지 아이디 추출
            md_file_id = int(df_comp.loc[index,'subject'][-6:])
            log(f'####################{md_file_id} START')
            # 작업전 DB 데이터 입력
            df_examin = pd.read_sql(f"SELECT * FROM meta_dental md WHERE md.file_id = '{md_file_id}'", engine)
            vin_df.loc[index,'image_id'] = md_file_id
            bf_rt = len(df_examin[df_examin['lbl_type'] == 'rectanglelabels'])
            bf_pg = len(df_examin[df_examin['lbl_type'] == 'polygonlabels'])
            bf_kp = len(df_examin[df_examin['lbl_type'] == 'keypointlabels'])
            vin_df.loc[index,'bf_rectangle'] = bf_rt
            vin_df.loc[index,'bf_polygon'] = bf_pg
            vin_df.loc[index,'bf_keypoint'] = bf_kp
            log('1. 작업 전 DB 데이터 추출 성공')
            # 이미지명 검색
            try:
                click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/input').clear() # 텍스트 비우기
                log('2. 검색창 텍스트 비우기 성공')
            except :
                log('2. 검색창 텍스트 비우기 에러')
                raise
            try:
                click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/input').send_keys(image_path) # 텍스트 입력하기
                log('3. 검색창 텍스트 입력하기 성공')
            except:
                log('2. 검색창 텍스트 입력하기 에러')
                raise
            time.sleep(1)
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[6]/a[1]/span') # 검색 클릭
            log('4. 검색창 검색 클릭 성공')
            time.sleep(1)
            # 이미지 클릭
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]/img')
            log("5. 작업창 접속 위해 이미지 클릭 성공")
            ### 사각형 탭 클릭
            time.sleep(2)
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/button[1]')
            count_rectangle = att_checker(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/span/span/span', vin_df, index, 'att_rectangle')
            if count_rectangle != 0:
                keypoint_clicker(driver, count_rectangle)
                save_finder(driver)
            log("6. 사각형 작업 성공")
            ### 다각형 탭 클릭
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/button[2]')
            time.sleep(2)
            count_polygon = att_checker(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/span/span/span', vin_df, index, 'att_polygon')
            if count_polygon != 0:
                keypoint_clicker(driver, count_polygon)
                save_finder(driver)
            log("7. 다각형 작업 성공")
            ### 키포인트 탭 클릭
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/button[3]')
            time.sleep(2)
            count_keypoint = att_checker(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/span/span/span', vin_df, index, 'att_keypoint')
            if count_keypoint != 0:
                keypoint_clicker(driver, count_keypoint)
                save_finder(driver)
            log("8. 키포인트 작업 성공")
            time.sleep(1)
            # 작업 후 DB 데이터, 데이터 입력
            df_examin = pd.read_sql(f"SELECT * FROM meta_dental md WHERE md.file_id = '{md_file_id}'", engine)
            af_rt = len(df_examin[df_examin['lbl_type'] == 'rectanglelabels'])
            af_pg = len(df_examin[df_examin['lbl_type'] == 'polygonlabels'])
            af_kp = len(df_examin[df_examin['lbl_type'] == 'keypointlabels'])
            vin_df.loc[index,'af_rectangle'] = af_rt
            vin_df.loc[index,'af_polygon'] = af_pg
            vin_df.loc[index,'af_keypoint'] = af_kp
            if (count_rectangle == int(af_rt)) & (count_polygon == int(af_pg)) & (count_keypoint == int(af_kp)):
                vin_df.loc[index,'result'] = True
            else :
                vin_df.loc[index,'result'] = False
            log("9. 작업 후 DB 데이터 추출 성공")
            click_by_xpath(driver, '/html/body/div[1]/div/div/div/div[5]/div/div/div[1]/button/span')
            log("10. 작업창 닫기 성공")
            today = datetime.datetime.now().strftime('%Y%m%d')
            vin_df.to_csv(filePath + f'/recovery_info_{id}_{today}.csv', encoding = 'utf-8-sig', index = False)
            log("11. 레포트 업데이트 성공")
            index += 1
        except Exception as E:
            log(f'#### {image_path} : 에러 발생')
            log(E)
            try:
                driver.close()
            except:
                log('에러복구 : 드라이버 이미 종료')
                pass
            # 크롬 접속, 로그인
            try:
                chrome_ver = driver_downloader()
            except:
                log('에러 복구 : 드라이버 재설치 시도 실패')
            try:
                driver_path = os.path.join(filePath, chrome_ver,'chromedriver.exe')
                url = 'http://192.168.2.189:8282/login'
                driver = start_driver(driver_path, url)
                login(driver, login_id, password)
            except:
                log('에러 복구 : 드라이버 재시작 시도 실패')
            # 작업관리 클릭
            click_by_xpath(driver, '/html/body/div[1]/ul/li/a/span')
            # 작업진행관리 클릭
            click_by_xpath(driver, '/html/body/div[1]/ul/li/div/div/a[1]')
            log("#### 크롬 드라이버 재시작 성공")
            continue
    log('.........@@@@@@@@@@@@@@@@@@@@...............')
    log('.................@..........@...............')
    log('.................@..........@...............')
    log('.................@..........@...............')
    log('.................@..........@...............')
    log('.................@..........@...............')
    log('.............................................')
    log('...@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@....')
    log('.............................................')
    log('.............@@@@@@@@@@@@@.............')
    log('.............@................................')
    log('.............@................................')
    log('.............@@@@@@@@@@@@@.............')
    log('.............@................................')
    log('.............@................................')
    log('.............@@@@@@@@@@@@@.............')
    time.sleep(5)
if __name__=="__main__":
    main()