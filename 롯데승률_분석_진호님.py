import folium
import matplotlib.colors as mcolors

# 롯데 자이언츠의 각 구장별 원정 승률 데이터 (예시)
lotte_away_win_rates = {
    'LG 트윈스': {'location': [37.53934562772943 , 127.214776054013], 'away_win_rate': 0.4},
    '두산 베어스' : {'location' : [37.5162500127349, 127.079283389854], 'away_win_rate' : 0.4} ,
    '키움 히어로즈': {'location': [37.4982125677913, 126.867088741096], 'away_win_rate': 0.4125},
    'SSG 랜더스': {'location': [37.4350819826381, 126.690759830613], 'away_win_rate': 0.375},
    'NC 다이노스': {'location': [35.2219848625101, 128.579580117268], 'away_win_rate': 0.425},
    '삼성 라이온즈': {'location': [35.8411289243023, 128.6812363722680], 'away_win_rate': 0.45},
    'KIA 타이거즈': {'location': [35.1694249627668, 126.888805470329], 'away_win_rate': 0.3875},
    '한화 이글스': {'location': [36.3173370007388, 127.428013823451], 'away_win_rate': 0.45},
    'KT 위즈': {'location': [37.2978428909635, 127.011348102567], 'away_win_rate': 0.4875},
    '롯데 홈' :{'location': [35.19403166, 129.06151836], 'away_win_rate': 0.4986},
}


norm = mcolors.Normalize(vmin=0.37, vmax=0.5)
cmap = mcolors.LinearSegmentedColormap.from_list("winrate_gradient", ["red", "yellow", "green"])


def get_color_from_winrate(win_rate):
    # 0.4 ~ 0.6 범위 내에서 색상 계산
    return mcolors.to_hex(cmap(norm(win_rate)))


# 지도 생성 (롯데 자이언츠 홈 구장 기준)
m = folium.Map(location=[35.19403166, 129.06151836], zoom_start=7)

# 두산 베어스의 각 원정 경기 승률을 지도에 표시
for team, data in lotte_away_win_rates.items():
    color = get_color_from_winrate(data['away_win_rate'])
    folium.CircleMarker(
        location=data['location'],
        radius=10,  # 점의 크기
        color=color,  # 경계선 색상
        fill=True,
        fill_color=color,  # 승률에 따른 색상 적용
        fill_opacity=0.9,  # 적절한 불투명도 설정
        popup=f"{team} 원정 승률: {data['away_win_rate']*100:.1f}%"
    ).add_to(m)
    

# 지도를 HTML로 저장
m.save("lotte_away_win_rates_gradient.html")

