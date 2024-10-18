import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 파일 경로 지정
file_path = 'KBO_light.csv'
data = pd.read_csv(file_path, encoding='utf-8')
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)


# 롯데 원정 및 홈 데이터 필터링
away, home = data[data['원정팀'] == '롯데'], data[data['홈팀'] == '롯데']

# CSV 저장 경로
away_path, home_path = 'lotte_away.csv', 'lotte_home.csv'
away.to_csv(away_path, index=False, encoding='euc-kr')
home.to_csv(home_path, index=False, encoding='euc-kr')

print(f"원정팀 데이터: {away_path} 저장 완료")
print(f"홈팀 데이터: {home_path} 저장 완료")

# 년, 월 컬럼 추가
for df in [away, home]:
    df.loc[:, 'Year'] = pd.to_datetime(df['Date']).dt.year
    df.loc[:, 'Month'] = pd.to_datetime(df['Date']).dt.month
    result_col = '원정팀결과' if df is away else '홈팀결과'
    df.loc[:, 'Win'] = df[result_col].apply(lambda x: 1 if x == '승' else 0)

# 년, 월별 승률 계산 및 저장
away_rate = away.groupby(['Year', 'Month'])['Win'].mean().reset_index().rename(columns={'Win': 'Rate'})
home_rate = home.groupby(['Year', 'Month'])['Win'].mean().reset_index().rename(columns={'Win': 'Rate'})

away_rate.to_csv('away_rate.csv', index=False, encoding='euc-kr')
home_rate.to_csv('home_rate.csv', index=False, encoding='euc-kr')

print("월별 승률 데이터 저장 완료")

# 1. 연도별 승률 추세
plt.figure(figsize=(12, 6))
plt.plot(away_rate.groupby('Year')['Rate'].mean(), marker='o', label='Away Win Rate')
plt.plot(home_rate.groupby('Year')['Rate'].mean(), marker='s', label='Home Win Rate')
plt.xlabel('Year')
plt.ylabel('Win Rate')
plt.title('년도별 승률')
plt.legend()
plt.show()

# 2. 월별 승률 추세
plt.figure(figsize=(12, 6))
plt.plot(away_rate.groupby('Month')['Rate'].mean(), marker='o', label='Away Win Rate')
plt.plot(home_rate.groupby('Month')['Rate'].mean(), marker='s', label='Home Win Rate')
plt.xlabel('Month')
plt.ylabel('Win Rate')
plt.title('월별 승률')
plt.legend()
plt.show()

# 3. 월별 승률 분포 (박스 플롯)
plt.figure(figsize=(12, 6))
sns.boxplot(data=away_rate, x='Month', y='Rate', color='skyblue')
plt.title('원정 월별 승률 분포 (박스 플롯)')
plt.xlabel('Month')
plt.ylabel('Win Rate')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(data=home_rate, x='Month', y='Rate', color='lightgreen')
plt.title('홈 월별 승률 분포 (박스 플롯)')
plt.xlabel('Month')
plt.ylabel('Win Rate')
plt.show()

# Away 히트맵
away_pivot = away_rate.pivot(index='Year', columns='Month', values='Rate')
plt.figure(figsize=(12, 8))
sns.heatmap(away_pivot, annot=True, cmap='Blues', fmt=".2f")
plt.title('원정 히트맵')
plt.show()

# Home 히트맵
home_pivot = home_rate.pivot(index = 'Year', columns = 'Month', values = 'Rate')
plt.figure(figsize=(12, 8))
sns.heatmap(home_pivot, annot=True, cmap='Greens', fmt=".2f")
plt.title('홈경기 히트맵')
plt.show()

# 월별 경기수 

# 연-월 컬럼 생성
file_path1, file_path2 = 'lotte_away.csv' , 'lotte_home.csv'
lotte_away, lotte_home  = pd.read_csv(file_path1, encoding='euc-kr'), pd.read_csv(file_path2, encoding='euc-kr')
lotte_away['Year-Month'] = pd.to_datetime(lotte_away['Date']).dt.to_period('M').astype(str)
lotte_home['Year-Month'] = pd.to_datetime(lotte_home['Date']).dt.to_period('M').astype(str)

# 데이터프레임 결합 후 경기 유형을 나타내는 컬럼 추가
lotte_away['GameType'] = 'Away'
lotte_home['GameType'] = 'Home'
combined_data = pd.concat([lotte_away, lotte_home])

# 연-월별 경기수 시각화
plt.figure(figsize=(15, 8))
sns.countplot(x='Year-Month', data=combined_data, hue='GameType', palette=['skyblue', 'lightgreen'])
plt.title('연-월별 홈 경기수와 원정 경기수 비교')
plt.xlabel('연-월')
plt.ylabel('경기 수')
plt.xticks(rotation=90)
plt.legend(title='경기 종류')
plt.show()

# 연별 경기수 시각화
lotte_away['Year'] = pd.to_datetime(lotte_away['Date']).dt.year
lotte_home['Year'] = pd.to_datetime(lotte_home['Date']).dt.year

# 데이터프레임 결합 후 경기 유형을 나타내는 컬럼 추가
lotte_away['GameType'] = 'Away'
lotte_home['GameType'] = 'Home'
combined_data = pd.concat([lotte_away, lotte_home])

# 년도별 경기 수 시각화
plt.figure(figsize=(12, 6))
sns.countplot(x='Year', data=combined_data, hue='GameType', palette=['skyblue', 'lightgreen'])
plt.title('년도별 홈 경기수와 원정 경기수 비교')
plt.xlabel('년도')
plt.ylabel('경기 수')
plt.legend(title='경기 종류')
plt.show()