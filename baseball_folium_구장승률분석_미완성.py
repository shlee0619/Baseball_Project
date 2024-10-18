import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.distance import geodesic
import matplotlib
import folium
# 폰트 설정
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

# CSV 파일 불러오기
file_path = 'C:/Mtest/개인연습/롯데_데이터.csv'
lotte_data = pd.read_csv(file_path)
locations = {
    "대구(삼성)": (35.8411289243023, 128.6812363722680),
    "부산(롯데)": (35.19403166, 129.06151836),
    "창원(NC)": (35.2219848625101, 128.579580117268),
    "광주(기아)": (35.1694249627668, 126.888805470329),
    "대전(한화)": (36.3173370007388, 127.428013823451),
    "수원(KT)": (37.2978428909635, 127.011348102567),
    "서울 잠실(LG, 두산)": (37.5112525852452, 127.072863377526),
    "서울 고척(키움)": (37.4980879456876, 126.867026290623)
}

lotte_home_location = locations.get("부산(롯데)")
# Calculate winning percentages for 롯데 at each stadium
lotte_data['승리여부'] = lotte_data.apply(lambda row: 1 if row['원정팀'] == '롯데' and row['원정팀결과'] == '승' else 0, axis=1)

# Group by stadium and calculate winning percentage
stadium_win_rates = lotte_data.groupby('구장')['승리여부'].mean().reset_index()
stadium_win_rates.columns = ['구장', '승률']

# Add location coordinates for each stadium
stadium_win_rates['위도'] = stadium_win_rates['구장'].map({
    "대구": locations["대구(삼성)"][0],
    "부산": locations["부산(롯데)"][0],
    "창원": locations["창원(NC)"][0],
    "광주": locations["광주(기아)"][0],
    "대전": locations["대전(한화)"][0],
    "수원": locations["수원(KT)"][0],
    "잠실": locations["서울 잠실(LG, 두산)"][0],
    "고척": locations["서울 고척(키움)"][0]
})

stadium_win_rates['경도'] = stadium_win_rates['구장'].map({
    "대구": locations["대구(삼성)"][1],
    "부산": locations["부산(롯데)"][1],
    "창원": locations["창원(NC)"][1],
    "광주": locations["광주(기아)"][1],
    "대전": locations["대전(한화)"][1],
    "수원": locations["수원(KT)"][1],
    "잠실": locations["서울 잠실(LG, 두산)"][1],
    "고척": locations["서울 고척(키움)"][1]
})

# Display the processed data
stadium_win_rates.head()
print(stadium_win_rates)
# Adding missing coordinates for the '문학' stadium
locations["문학"] = (37.435, 126.685)  # Example coordinates for Munhak stadium in Incheon

# Update any missing values in the stadium data
stadium_win_rates['위도'] = stadium_win_rates.apply(lambda row: locations.get(row['구장'], (None, None))[0], axis=1)
stadium_win_rates['경도'] = stadium_win_rates.apply(lambda row: locations.get(row['구장'], (None, None))[1], axis=1)

# Verifying data again for any remaining NaN values
stadium_win_rates.dropna(inplace=True)

# Display processed data to confirm it is ready for mapping
print(stadium_win_rates)

map_center = [36.5, 127.5]
map_folium = folium.Map(location=map_center, zoom_start=7)

# Adding markers for each stadium with win percentage information
for _, row in stadium_win_rates.iterrows():
    stadium_name = row['구장']
    win_rate = row['승률']
    latitude = row['위도']
    longitude = row['경도']
    
    # Create a color based on win rate (higher win rate = darker green)
    color = 'green' if win_rate >= 0.5 else 'orange' if win_rate >= 0.3 else 'red'
    
    # Add marker with win rate information
    folium.CircleMarker(
        location=(latitude, longitude),
        radius=10 + (win_rate * 10),  # Size varies with win rate
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        tooltip=f"{stadium_name}: 승률 {win_rate:.2%}"
    ).add_to(map_folium)

# Saving the map to an HTML file for display
map_path = 'lotte_stadium_win_rates_map.html'
map_folium.save(map_path)
map_path

map_center = [36.5, 127.5]
map_folium = folium.Map(location=map_center, zoom_start=7)

# Adding markers for each stadium with win percentage information
for _, row in stadium_win_rates.iterrows():
    stadium_name = row['구장']
    win_rate = row['승률']
    latitude = row['위도']
    longitude = row['경도']
    
    # Create a color based on win rate (higher win rate = darker green)
    color = 'green' if win_rate >= 0.5 else 'orange' if win_rate >= 0.3 else 'red'
    
    # Add marker with win rate information
    folium.CircleMarker(
        location=(latitude, longitude),
        radius=10 + (win_rate * 10),  # Size varies with win rate
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        tooltip=f"{stadium_name}: 승률 {win_rate:.2%}"
    ).add_to(map_folium)

# Saving the map to an HTML file for display
map_path = 'lotte_stadium_win_rates_map_further.html'
map_folium.save(map_path)
map_path