import pandas as pd
import matplotlib
from matplotlib import font_manager
import matplotlib.pyplot as plt
import seaborn as sns
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)
# Load all the provided CSV files to inspect their structure and data.
file_paths = {
    'team_data': r'C:\Mtest\개인연습\팀플\야구\data\한화_데이터.csv',
    'defense_data': r'C:\Mtest\개인연습\팀플\야구\data\한화_수비_기록.csv',
    'hitter_data': r'C:\Mtest\개인연습\팀플\야구\data\한화_타자_기록.csv',
    'pitcher_data': r'C:\Mtest\개인연습\팀플\야구\data\한화_투수_기록.csv'
}

team_data = pd.read_csv(file_paths['team_data'])
defense_data = pd.read_csv(file_paths['defense_data'])
hitter_data = pd.read_csv(file_paths['hitter_data'])
pitcher_data = pd.read_csv(file_paths['pitcher_data'])


team_data_grouped = team_data.groupby('연도').tail(1)[['연도', '누적승률']].reset_index(drop=True)
print(team_data_grouped)


hitter_data['타율'] = pd.to_numeric(hitter_data['타율'], errors='coerce')  # 타율이 수치로 변환되지 않는 값들을 NaN으로 처리

# 다시 그룹화 및 상관분석을 위한 데이터 통합 진행
hitter_data_grouped = hitter_data.groupby('연도').agg({'타율': 'mean', '득점': 'sum', '홈런': 'sum'}).reset_index()




# 투수 데이터에서 문제가 있는 열들에 대해 수치 변환 시도
pitcher_data['ERA'] = pd.to_numeric(pitcher_data['ERA'], errors='coerce')
pitcher_data['이닝'] = pd.to_numeric(pitcher_data['이닝'], errors='coerce')
pitcher_data['자책점'] = pd.to_numeric(pitcher_data['자책점'], errors='coerce')

# 다시 투수 데이터 요약 후 재처리
pitcher_data_grouped = pitcher_data.groupby('연도').agg({'ERA': 'mean', '이닝': 'sum', '자책점': 'sum'}).reset_index()



# 수비 데이터에서 수치로 변환되지 않은 값들 확인 및 처리
defense_data['실책'] = pd.to_numeric(defense_data['실책'], errors='coerce')
defense_data['풋아웃'] = pd.to_numeric(defense_data['풋아웃'], errors='coerce')
defense_data['어시스트'] = pd.to_numeric(defense_data['어시스트'], errors='coerce')

# 수비 데이터 요약 후 재처리
defense_data_grouped = defense_data.groupby('연도').agg({'풋아웃': 'sum', '어시스트': 'sum'}).reset_index()

# 데이터 병합
merged_data = pd.merge(team_data_grouped, hitter_data_grouped, on='연도')
merged_data = pd.merge(merged_data, pitcher_data_grouped, on='연도')
merged_data = pd.merge(merged_data, defense_data_grouped, on='연도')

# 상관관계 분석을 위한 상관계수 계산
correlation_matrix = merged_data.corr()

# 1. 상관관계 히트맵
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Hitter, Pitcher, Defense Stats with Cumulative Win Rate')
plt.show()

# 2. 타자, 투수 기록과 누적 승률의 산점도 (실책 제외)
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# 타율 vs 누적 승률
sns.scatterplot(x='타율', y='누적승률', data=merged_data, ax=axes[0])
axes[0].set_title('Batting Average vs Cumulative Win Rate')

# ERA vs 누적 승률
sns.scatterplot(x='ERA', y='누적승률', data=merged_data, ax=axes[1])
axes[1].set_title('ERA vs Cumulative Win Rate')

plt.tight_layout()
plt.show()

# 3. 연도별 주요 기록과 승률의 변화 추세 (실책 제외)
fig, ax = plt.subplots(figsize=(10, 6))

# 연도별 타율, ERA, 누적 승률 비교
sns.lineplot(x='연도', y='타율', data=merged_data, label='Batting Average', marker='o')
sns.lineplot(x='연도', y='ERA', data=merged_data, label='ERA', marker='o')
sns.lineplot(x='연도', y='누적승률', data=merged_data, label='Cumulative Win Rate', marker='o')

ax.set_title('Yearly Trends: Batting Average, ERA, and Cumulative Win Rate')
ax.set_ylabel('Value')
ax.set_xlabel('Year')

plt.legend()
plt.show()

