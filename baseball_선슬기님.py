import time
from selenium import webdriver
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
try:
    driver.get("https://www.koreabaseball.com/Futures/Schedule/GameList.aspx")
    time.sleep(3)
    contents = driver.find_element(by=By.ID, value='contents')  # ul
    subcontents = contents.find_element(by=By.CLASS_NAME, value = 'sub-content')
    date_wrap_schedule = subcontents.find_element(by=By.CLASS_NAME, value = 'date-wrap schedule')
    scheduleBoard = date_wrap_schedule.find_elements(by=By.ID, value='cphContents_cphContents_cphContents_udpRecord')  # li
    print('KBO 경기 결과 정보 크롤링 출력')
    for item in scheduleBoard:  # 이 부분 수정
        # 각 정보를 추출
        infoDate = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[1]').text
        infoTime = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[2]').text
        infoGame = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[3]').text
        infoGameScoring = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[4]').text
        infoStadium = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[7]').text
        infoVigo = item.find_element(by=By.XPATH, value='/html/body/form/div[3]/section/div/div[2]/div/div[2]/div/table/thead/tr/th[8]').text
        # 출력 형식 수정
        print('롯데 자이언츠 경기 정보:')
        print('날짜: {}\n시간: {}\n경기: {}\n득점: {}\n경기장: {}\n비고: {}\n'.format(
            infoDate, infoTime, infoGame, infoGameScoring, infoStadium, infoVigo
        ))
        print(':' * 130)
        time.sleep(2)
        
except Exception as ex:
    print('에러 이유 = ', ex)
time.sleep(10)
driver.quit()