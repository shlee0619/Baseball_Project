import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# 웹드라이버 초기화
url = "https://www.koreabaseball.com/Schedule/Schedule.aspx"
driver = webdriver.Chrome()
driver.get(url)

# 선택자 초기화
year_select = Select(driver.find_element(By.ID, 'ddlYear'))
month_select = Select(driver.find_element(By.ID, 'ddlMonth'))
series_select = Select(driver.find_element(By.ID, 'ddlSeries'))

# 초기 값 설정
year_select.select_by_value('2024')
month_select.select_by_value('04')
series_select.select_by_value("0,9,6")

driver.find_element(By.XPATH, '//*[@id="boxList"]/ul/li[8]/a').click()

# 데이터 저장을 위한 리스트 초기화
days, ballparks, farteams, farteam_points, hometeam_points, hometeams, years = [], [], [], [], [], [], []

# 시작 연도와 월 설정
year = 2015  # 시작 연도
month = 3    # 시작 월
end_year = 2024  # 종료 연도

def scrape_month(year, month):
    # 연도와 월 설정
    year_select = Select(driver.find_element(By.ID, 'ddlYear'))
    month_select = Select(driver.find_element(By.ID, 'ddlMonth'))
    series_select = Select(driver.find_element(By.ID, 'ddlSeries'))

    year_select.select_by_value(str(year))
    month_select.select_by_value(f"{month:02d}")
    series_select.select_by_value("0,9,6")

    # 페이지 로딩 대기
    time.sleep(1)

    # 테이블의 모든 행을 가져옵니다
    rows = driver.find_elements(By.XPATH, '//*[@id="tblScheduleList"]/tbody/tr')

    current_day = ''
    for idx, row in enumerate(rows):
        try:
            # 각 행의 셀을 가져옵니다
            cells = row.find_elements(By.TAG_NAME, 'td')

            if '데이터가 없습니다.' in cells[0].text:
                break


            # 날짜 셀이 존재하는지 확인합니다
            if 'day' in cells[0].get_attribute('class'):
                current_day = cells[0].text
                time_idx = 1
                team_idx = 2
                ballpark_idx = 7
                status_idx = 8
            else:
                time_idx = 0
                team_idx = 1
                ballpark_idx = 6
                status_idx = 7

            # 경기가 진행 중인지 확인합니다
            if cells[status_idx].text != '-':
                continue

            # 팀 정보와 점수를 추출합니다
            farteam = cells[team_idx].find_element(By.XPATH, './span[1]').text
            farteam_point = cells[team_idx].find_element(By.XPATH, './em/span[1]').text
            hometeam_point = cells[team_idx].find_element(By.XPATH, './em/span[3]').text
            hometeam = cells[team_idx].find_element(By.XPATH, './span[2]').text
            ballpark = cells[ballpark_idx].text

            # 데이터를 리스트에 추가합니다
            days.append(current_day)
            ballparks.append(ballpark)
            farteams.append(farteam)
            farteam_points.append(farteam_point)
            hometeam_points.append(hometeam_point)
            hometeams.append(hometeam)
            years.append(year)
            print(current_day, ballpark, farteam, farteam_point, hometeam_point, hometeam)
        except Exception as e:
            print(f"Error processing row {idx} on {year}-{month}: {e}")

# 월별로 데이터를 스크래핑합니다
while True:
    if year > end_year:
        break
    scrape_month(year, month)
    month += 1
    if month > 10:
        month = 3  # 다음 해의 3월로 넘어갑니다
        year += 1

# 데이터프레임 생성 및 저장
df = pd.DataFrame({
    'Date': days,
    '구장': ballparks,
    '원정팀': farteams,
    '원정팀점수': farteam_points,
    '홈팀점수': hometeam_points,
    '홈팀': hometeams,
    '연도': years
})

df.to_csv("롯데_데이터10년치.csv", index=False, encoding='utf-8-sig')
# print(df)


driver.quit()
###############################################################################################
# Define functions to calculate game result based on scores
file_path = 'C:\Mtest\TeamPj\data\롯데_데이터10년치.csv'
lotte_data = pd.read_csv(file_path)


def away_team_result(row):
    return '승' if row['원정팀점수'] > row['홈팀점수'] else '패' if row['원정팀점수'] < row['홈팀점수'] else '무'

def home_team_result(row):
    return '승' if row['홈팀점수'] > row['원정팀점수'] else '패' if row['홈팀점수'] < row['원정팀점수'] else '무'

# Apply these functions to add results columns
lotte_data['원정팀결과'] = lotte_data.apply(away_team_result, axis=1)
lotte_data['홈팀결과'] = lotte_data.apply(home_team_result, axis=1)

lotte_data['Wins'] = 0
lotte_data['Losses'] = 0

lotte_data['Wins'] = (lotte_data['원정팀결과'] == '승').cumsum()   #cumsum은 cumulative sum의 약자로 누적합계를 계산하는 기능
lotte_data['Losses'] = (lotte_data['원정팀결과'] == '패').cumsum()

#연도가 바뀔 때 win/losses 나누기

for year in lotte_data['연도'].unique():
    year_data = lotte_data[lotte_data['연도'] == year]
    
    # 누적 승리와 패배 계산
    wins_count = 0
    losses_count = 0
    for index, row in year_data.iterrows():
        if row['홈팀결과'] == '승':
            wins_count += 1
        else:
            losses_count += 1
            
        lotte_data.at[index, 'Wins'] = wins_count
        lotte_data.at[index, 'Losses'] = losses_count

lotte_data.to_csv(file_path, index=False, encoding='utf-8-sig')