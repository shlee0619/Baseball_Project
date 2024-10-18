import pandas as pd
#울산에서의 경기를 사직에서 한 걸로 바꿨습니다.  #distancesdata는 gpt한테서 우선 갖고왔습니다..
distances_data = {
    '잠실': {'문학': 30, '사직': 300, '대구': 350, '창원': 400, '대전': 250, '고척': 20, '광주': 270, '수원': 50},
    '문학': {'잠실': 30, '사직': 270, '대구': 320, '창원': 380, '대전': 220, '고척': 50, '광주': 240, '수원': 80},
    '사직': {'잠실': 300, '문학': 270, '대구': 120, '창원': 220, '대전': 60, '고척': 280, '광주': 150, '수원': 300},
    '대구': {'잠실': 350, '문학': 320, '사직': 120, '창원': 150, '대전': 200, '고척': 350, '광주': 100, '수원': 350},
    '창원': {'잠실': 400, '문학': 380, '사직': 220, '대구': 150, '대전': 300, '고척': 100, '광주': 200, '수원': 370},
    '대전': {'잠실': 250, '문학': 220, '사직': 60, '대구': 200, '창원': 300, '고척': 250, '광주': 200, '수원': 220},
    '고척': {'잠실': 20, '문학': 50, '사직': 280, '대구': 350, '창원': 100, '광주': 230, '수원': 60},
    '광주': {'잠실': 270, '문학': 240, '사직': 150, '대구': 100, '창원': 200, '한화': 160, '키움': 230, '수원': 210},
    '수원': {'잠실': 50, '문학': 80, '사직': 300, '대구': 350, '창원': 370, '대전': 220, '고척': 60, '광주': 210},
}

distances_df = pd.DataFrame(distances_data)

# CSV 파일에서 경기 데이터 읽기
games_df = pd.read_csv('롯데_데이터.csv') #상혁씨 코드에서 가져온 csv

# 거리 계산
previous_ground = None
total_distance = 0

for index, row in games_df.iterrows():
    ground = row['구장']
    
    if previous_ground is not None and previous_ground != ground:
        # 거리 정보를 찾을 수 있는지 확인
        if previous_ground in distances_df.index and ground in distances_df.columns:
            distance = distances_df.at[previous_ground, ground]
            total_distance += distance
            print(f"{previous_ground}에서 {ground}으로 이동: {distance} km")
        else:
            print(f"거리 정보를 찾을 수 없습니다: {previous_ground} -> {ground}")
    
    previous_ground = ground

print(f"총 이동 거리: {total_distance} km")

#아직 연도를 나누지않았음



