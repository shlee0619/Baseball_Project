import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib

font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

import matplotlib as mpl 
mpl.rc('axes', unicode_minus=False)
mpl.rcParams['axes.unicode_minus'] = False


# CSV 파일 경로 (파일 경로를 실제 CSV 파일 경로로 변경하세요)
file_path = 'c:/Mtest/TeamPJ/data/구단별_10년_이동거리.csv'

# CSV 파일 읽기
df1 = pd.read_csv(file_path,encoding='cp949')


# input으로 연도설정 데이터 필터링
year = int(input(('연도를 입력하세요ex)2015>>>> ')))
filtered_data = df1[df1['연도'] == year]

# 팀명, 누적 이동거리, 승률 추출
teams = filtered_data['팀명']
cumulative_distance = filtered_data['누적이동거리']
win_rate = filtered_data['승률']

#데이터 정렬
sorted_indices = cumulative_distance.argsort()
sorted_teams = teams.iloc[sorted_indices]
sorted_distance = cumulative_distance.iloc[sorted_indices]
sorted_win_rate = win_rate.iloc[sorted_indices]

# 그래프 그리기
plt.figure(figsize=(12, 6))

# 막대 그래프
bar_width = 0.4  # 막대 너비
x = range(len(teams))  # x축 위치

# 누적 이동거리 막대 그래프
plt.bar(x, sorted_win_rate * 100, width=bar_width, label='승률 (%)', color='lightcoral', alpha=0.7)

# 승률 막대 그래프 (누적 이동거리 그래프 위에 겹쳐서 그리기 위해 오프셋)
plt.xticks(x, sorted_teams)

# 각 막대 위에 누적 이동거리 표시
for i in range(len(sorted_teams)):
    plt.text(i, sorted_win_rate.iloc[i] * 100 + 1, f'{sorted_distance.iloc[i]} km', 
             ha='center', va='bottom')


# 그래프 설정
plt.title( f'{year}년 팀별 승률', fontsize=16)
plt.xlabel('팀명', fontsize=12)
plt.ylabel('승률 (%)', fontsize=12)
plt.grid(axis='y')

# y축 범위 설정 (10%에서 80%까지)
plt.ylim(10, 80)

# 범례 추가
plt.legend()
plt.show()