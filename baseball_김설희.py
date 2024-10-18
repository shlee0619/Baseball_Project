import folium
import pandas as pd
# 각 지역의 위도와 경도
locations = {
    "대구": (35.8411289243023, 128.6812363722680),
    "사직": (35.19403166, 129.06151836),
    "창원": (35.2219848625101, 128.579580117268),
    "광주": (35.1694249627668, 126.888805470329),
    "대전": (36.3173370007388, 127.428013823451),
    "수원": (37.2978428909635, 127.011348102567),
    "잠실": (37.5112525852452, 127.072863377526),
    "고척": (37.4982125677913, 126.867088741096),
    "문학": (37.4350819826381, 126.690759830613)
}
# 데이터프레임 생성
df = pd.DataFrame(
    [(key, value[0], value[1]) for key, value in locations.items()],
    columns=['경기장', '위도', '경도']
)
print(df)
# 경기장 별 승률 불러오기
LG_data = pd.read_csv('C:\Mtest\개인연습\팀플\야구\LG_데이터.csv', encoding='utf-8-sig')
print(LG_data)
# Merge df with LG_data on 경기장 and 구장
merged = df.set_index('경기장').join(LG_data.set_index('구장')[['누적승률']])

# Reset index to clean up DataFrame and remove indexing artifacts
merged.reset_index(inplace=True)

# Sort based on 누적승률 (cumulative win rate)
merged = merged.sort_values(by='누적승률', ascending=False)

# 마커 색상을 구분할 수 있게 지정

map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)

# Define colors for win rates
colors = ["#800000", "#B90000", "#CD0000", "#FF0000", "#FF5050", "#F06464", "#FAB7B7", "#F5AAAA", "#FFF0F0"]



for i, (index, row) in enumerate(merged.iterrows()):
    icon_color = colors[i % len(colors)]
    
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        popup=f"{row['경기장']}: {row['누적승률']}",
        color=icon_color,
        fill=True,
        fill_color=icon_color,
        fill_opacity=0.9,
        radius=10,
    ).add_to(m)

# Save the updated map
map_output_path = "LG_team_distance_map_updated.html"
m.save(map_output_path)

map_output_path