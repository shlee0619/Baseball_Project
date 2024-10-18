import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.distance import geodesic
import matplotlib
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

# 거리 데이터 정의
distances_data = {
    '잠실': {'문학': 54, '사직': 400, '대구': 297, '창원': 363, '대전': 172, '고척': 31, '광주': 261, '수원': 36, '울산': 448},
    '문학': {'잠실': 54, '사직': 417, '대구': 320, '창원': 386, '대전': 156, '고척': 24, '광주': 269, '수원': 43, '울산': 450},
    '사직': {'잠실': 400, '문학': 417, '대구': 101, '창원': 59, '대전': 260, '고척': 414, '광주': 262, '수원': 379, '울산': 56},
    '대구': {'잠실': 297, '문학': 320, '사직': 101, '창원': 103, '대전': 163, '고척': 316, '광주': 238, '수원': 235, '울산': 98},
    '창원': {'잠실': 363, '문학': 386, '사직': 59, '대구': 103, '대전': 224, '고척': 364, '광주': 212, '수원': 345, '울산': 68},
    '대전': {'잠실': 172, '문학': 156, '사직': 260, '대구': 163, '창원': 224, '고척': 188, '광주': 187, '수원': 149, '울산': 318},
    '고척': {'잠실': 31, '문학': 24, '사직': 414, '대구': 316, '대전': 188, '창원': 364, '광주': 313, '수원': 33, '울산': 455},
    '광주': {'잠실': 261, '문학': 269, '사직': 262, '대구': 238, '창원': 212, '대전': 187, '고척': 313, '수원': 240, '울산' : 211},
    '수원': {'잠실': 36, '문학': 43, '사직': 379, '대구': 235, '창원': 345, '대전': 149, '고척': 33, '광주': 240, '울산': 400},
    '울산': {'잠실': 448, '문학': 450, '사직': 56, '대구': 98, '창원': 68, '대전': 318, '고척': 455, '광주': 211, '수원': 400}
}


# 거리 데이터를 DataFrame으로 변환
distances_df = pd.DataFrame(distances_data)

# CSV 파일에서 경기 데이터 읽기
file_path = 'C:\Mtest\개인연습\팀플\야구\롯데_데이터.csv'
games_df = pd.read_csv(file_path)
lotte_data = pd.read_csv(file_path)

total_distance = 0
#누적 거리와 승률 계산
previous_ground = None

years = []
distances = []
winrates = []
# 연도별 이동 거리 계산 함수
def calculate_distance_by_year(year):
    # 해당 연도 데이터 필터링
    year_data = games_df[games_df['연도'] == year]
    
    previous_ground = None
    total_distance = 0
    
    for index, row in year_data.iterrows():
        ground = row['구장']
        
        if previous_ground is not None and previous_ground != ground:
            # 거리 정보를 찾을 수 있는지 확인
            if previous_ground in distances_df.index and ground in distances_df.columns:
                distance = distances_df.at[previous_ground, ground]
                total_distance += distance

                years.append(year)
                distances.append(total_distance)
                winrates.append(lotte_data['누적승률'].iloc[index])

                print(f"{year}: {previous_ground}에서 {ground}으로 이동: {distance} km")
            else:
                print(f"{year}: 거리 정보를 찾을 수 없습니다: {previous_ground} -> {ground}")
        
        previous_ground = ground

    # 마지막 원정 경기 후 홈으로 돌아가는 경우 이동 추가
    if previous_ground != '사직':  # 예를 들어 홈이 '사직'이라면
        if previous_ground in distances_df.index and '사직' in distances_df.columns:
            return_distance = distances_df.at[previous_ground, '사직']
            total_distance += return_distance
            print(f"{year} 마지막 경기 후 {previous_ground}에서 사직으로 이동: {return_distance} km")
            
    print(f"{year} 총 이동 거리: {total_distance} km")

# 2023년과 2024년 거리 계산
calculate_distance_by_year(2023)
calculate_distance_by_year(2024)
print(len(distances))
total = pd.DataFrame({
    '연도':years, 
    '누적이동거리': distances, 
    '승률': winrates})
year2023 = total[total['연도'] == 2023]
year2024 = total[total['연도'] == 2024]
print(year2023)

print()
print(year2024)

# 산점도: 누적 이동 거리와 승률 (2023)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=year2023, x='누적이동거리', y='승률', s=100, color='dodgerblue', edgecolor='black')
plt.title('누적 이동 거리와 승률 (2023)')
plt.xlabel('누적 이동 거리 (km)')
plt.ylabel('승률')
plt.grid(True)
plt.show()

# 라인 플롯: 시간에 따른 누적 이동 거리와 승률 (2023)
fig, ax1 = plt.subplots(figsize=(12, 6))

# 누적 이동 거리 그래프
ax1.set_xlabel('경기 인덱스')
ax1.set_ylabel('누적 이동 거리 (km)', color='tab:blue')
ax1.plot(year2023.index, year2023['누적이동거리'], color='tab:blue', label='누적 이동 거리', linewidth=2)
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.legend(loc='upper left')

# 보조 y축: 승률 그래프
ax2 = ax1.twinx()
ax2.set_ylabel('승률', color='tab:green')
ax2.plot(year2023.index, year2023['승률'], color='tab:green', linestyle='--', label='승률', linewidth=2)
ax2.tick_params(axis='y', labelcolor='tab:green')
ax2.legend(loc='upper right')

fig.tight_layout()
plt.title('시간에 따른 누적 이동 거리와 승률 (2023)')
plt.show()

# 1. Line Plot for Cumulative Travel Distance and Win Rate Over Time (2023 and 2024)
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot cumulative distance for 2023
ax1.plot(year2023.index, year2023['누적이동거리'], color='blue', label='누적 이동 거리 (2023)', linewidth=2)
# Plot cumulative distance for 2024
ax1.plot(year2024.index, year2024['누적이동거리'], color='skyblue', linestyle='--', label='누적 이동 거리 (2024)', linewidth=2)

ax1.set_xlabel('경기 인덱스')
ax1.set_ylabel('누적 이동 거리 (km)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Secondary y-axis for Win Rate (2023 and 2024)
ax2 = ax1.twinx()
ax2.plot(year2023.index, year2023['승률'], color='green', label='승률 (2023)', linestyle='--', linewidth=2)
ax2.plot(year2024.index, year2024['승률'], color='lightgreen', label='승률 (2024)', linestyle=':', linewidth=2)

ax2.set_ylabel('승률')
ax2.legend(loc='upper right')

fig.tight_layout()
plt.title('경기 순서에 따른 누적 이동 거리와 승률 변화 (2023 vs 2024)')
plt.show()

# 2. Bar Chart for Yearly Cumulative Travel Distance Comparison (2023 and 2024)
yearly_distances = {
    '2023': year2023['누적이동거리'].max(), 
    '2024': year2024['누적이동거리'].max()
}
plt.figure(figsize=(8, 6))
sns.barplot(x=list(yearly_distances.keys()), y=list(yearly_distances.values()), palette='Blues')
plt.title('연도별 누적 이동 거리 비교')
plt.xlabel('연도')
plt.ylabel('총 누적 이동 거리 (km)')
plt.show()

# 3. Histogram of Win Rate Distribution (2023 and 2024)
plt.figure(figsize=(10, 6))
sns.histplot(year2023['승률'], color='blue', bins=10, kde=True, label='2023', alpha=0.6)
sns.histplot(year2024['승률'], color='green', bins=10, kde=True, label='2024', alpha=0.6)
plt.title('승률 분포 (2023 vs 2024)')
plt.xlabel('승률')
plt.ylabel('빈도')
plt.legend()
plt.show()

