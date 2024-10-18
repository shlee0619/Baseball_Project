import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# Set Korean font
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

# File paths and locations for teams
file_paths = {
    'KIA': r'C:\Mtest\개인연습\KIA_데이터.csv',
    'KT': r'C:\Mtest\개인연습\KT_데이터.csv',
    'LG': r'C:\Mtest\개인연습\LG_데이터.csv',
    'NC': r'C:\Mtest\개인연습\NC_데이터.csv',
    'SSG': r'C:\Mtest\개인연습\SSG_데이터.csv',
    '두산': r'C:\Mtest\개인연습\두산_데이터.csv',
    '롯데': r'C:\Mtest\개인연습\롯데_데이터.csv',
    '삼성': r'C:\Mtest\개인연습\삼성_데이터.csv',
    '키움': r'C:\Mtest\개인연습\키움_데이터.csv',
    '한화': r'C:\Mtest\개인연습\한화_데이터.csv'
}

# Load all team data
all_teams_data = pd.concat([pd.read_csv(file_paths[team]) for team in file_paths], ignore_index=True)
all_teams_data['연도'] = all_teams_data['연도'].astype(int)

# Clean data by removing duplicates
all_teams_data_clean = all_teams_data.drop_duplicates(subset=['Date', '원정팀', '홈팀', '연도'])

# Define a function for plotting
def plot_graph(data, x, y, title, xlabel, ylabel, kind='scatter', hue=None, bins=None):
    plt.figure(figsize=(10, 6))
    if kind == 'scatter':
        sns.scatterplot(data=data, x=x, y=y, hue=hue)
    elif kind == 'line':
        sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o')
    elif kind == 'bar':
        sns.barplot(data=data, x=x, y=y, estimator='mean')
    elif kind == 'box':
        sns.boxplot(data=data, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45 if kind == 'bar' else 0)
    plt.show()

# Correlation analysis: 누적 원정거리와 누적 승률 간 상관관계
plot_graph(all_teams_data_clean, '누적이동거리', '누적승률', '누적 원정거리와 누적 승률 간 상관관계', '누적 이동 거리 (km)', '누적 승률', kind='scatter', hue='원정팀')
correlation_clean = all_teams_data_clean[['누적이동거리', '누적승률']].corr()

# Yearly change analysis: 팀별 연도별 승률 변화
plot_graph(all_teams_data_clean, '연도', '누적승률', '팀별 연도별 승률 변화', '연도', '누적 승률', kind='line', hue='원정팀')

# Team comparison analysis: 팀 간 누적 승률 비교
plot_graph(all_teams_data_clean, '원정팀', '누적승률', '팀 간 누적 승률 비교', '팀', '평균 누적 승률', kind='bar')

# 승률 analysis by distance range
all_teams_data_clean['거리구간'] = pd.cut(all_teams_data_clean['누적이동거리'], 
                                          bins=[0, 1000, 3000, 5000, 7000, 10000, 20000], 
                                          labels=['0-1000km', '1001-3000km', '3001-5000km', '5001-7000km', '7001-10000km', '10001km 이상'])
plot_graph(all_teams_data_clean, '거리구간', '누적승률', '특정 거리 구간에 따른 승률', '거리 구간', '누적 승률', kind='box')

