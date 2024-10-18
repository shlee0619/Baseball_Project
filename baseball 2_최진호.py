# 거리 마커 아이콘 크기를 축소한 코드 수정
import folium
from geopy.distance import geodesic
import random

# 각 지역의 위도와 경도
locations = {
    "대구(삼성)": (35.8411289243023, 128.6812363722680),
    "부산(롯데)": (35.19403166, 129.06151836),
    "창원(NC)": (35.2219848625101, 128.579580117268),
    "광주(기아)": (35.1694249627668, 126.888805470329),
    "대전(한화)": (36.3173370007388, 127.428013823451),
    "수원(KT)": (37.2978428909635, 127.011348102567),
    "서울 잠실(LG, 두산)": (37.5112525852452, 127.072863377526),
    "서울 고척(키움)": (37.4982125677913, 126.867088741096),
    "인천(SSG)": (37.4350819826381, 126.690759830613)
}

# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)

# 마커 색상을 구분할 수 있게 지정
colors = ["red", "blue", "green", "purple", "orange", "darkred", "lightred", "beige", "darkblue"]

# 각 지역 마커 추가 (아이콘 색상 구분)
for i, (loc_name, coords) in enumerate(locations.items()):
    folium.Marker(location=coords, popup=loc_name, icon=folium.Icon(color=colors[i])).add_to(m)

# 각 지역 간 거리 계산 및 지도에 선 표시 (선의 색상을 랜덤으로 변경)
for loc1, coord1 in locations.items():
    for loc2, coord2 in locations.items():
        if loc1 != loc2:
            # 거리 계산
            distance = geodesic(coord1, coord2).kilometers
            # 지도에 선 표시 (두 지점 연결, 랜덤한 색상 선택)
            line_color = random.choice(colors)
            folium.PolyLine(locations=[coord1, coord2], color=line_color, weight=2, opacity=0.7).add_to(m)
            # 선의 중간에 거리 텍스트 추가 (아이콘 축소)
            midpoint = [(coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2]
            folium.Marker(
                location=midpoint, 
                popup=f"{loc1} ↔ {loc2}: {distance:.2f} km",
                icon=folium.Icon(icon_size=(12, 12), icon_color='white', color="lightgray")
            ).add_to(m)

# 지도 저장
m.save("kbo_team_distance_map_improved_small_icons.html")

