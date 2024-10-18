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
    "서울 잠실(LG)": (37.53934562772943 , 127.214776054013),
    "서울 잠실(두산)" : (37.5162500127349, 127.079283389854) ,
    "서울 고척(키움)": (37.4982125677913, 126.867088741096),
    "인천(SSG)": (37.4350819826381, 126.690759830613)
}

# 각 팀의 구단 로고 이미지 URL (테스트용 외부 이미지 링크)
images = {
    "대구(삼성)": "https://i.namu.wiki/i/nIFLDX1ihQwBVokkFpaaA5_j7lzBn7yxWQTgKnHtWi7T-_n7ZXho4bk25Wr4nln83jp_7UK5HPoj2Y-5C4izWNlmwwk_xuJw9sP8eFVsUo51G5tqHxO4j1d02FueZTsPO3djYZFBMAGVzHWMehVhvw.svg",
    "부산(롯데)": "https://i.namu.wiki/i/qR3opgWyvcqT8O22XmKyMQAsFoaCMmtXH0El-iDBYhXB0RxfEQhbYUdV-TBudx1W3l_bUkK1KAZDFtt172W79c9C6Yc3YbVsklhHEf0_b1mHtqrwuNFXNJ67MsaYIvykptvBl6Nxerxc4mvHS-7z2Q.svg",
    "창원(NC)": "https://i.namu.wiki/i/zsmHt6UT62Ah-_Evr58aDNRFWNfRNKVXhQs35BYUxOPZ3t2MO2OQ_4pSZdYeD2xUSmfWXpUPFA5gJWu7z6GvHGcsz_S8jv9eXgUlwb0HffOi8uYeB-MjQXfVovhThSbjRVDlbSRmWfO70mpbPcFJpg.svg",
    "광주(기아)": "https://i.namu.wiki/i/wFayYt5GXe5x0OlMmalioj7G2c3DeLkLWJiRL2oP_PciuuQ4RiLQrYe2BRLhJ-Cn0ALLzidmj63vDpmMQBo0StbmOcjApJmiP3vRwBrjd0uLxI-Ku6K8LeWT9KP8yTIadM8JBxllf8ZSjrQWUu_Opw.svg",
    "대전(한화)": "https://i.namu.wiki/i/UO3cLQWbNsm-D4ZZ1QpKWsCyjIXvoRBRqF2C3pJz9COiYBQaHXVee1ppuO37g3SqHIiEmEccgPU1SAPxp9Nea-iXfKDFhUJvoFYhtdVFsC7oRjyDsREoCnocWz2ujxmerf_WjL64zrV9FTn69fy2QA.svg",
    "수원(KT)": "https://i.namu.wiki/i/-Op5HRrVtorB9yOdP7e2ZzNvBgE3WHZP0jSn3UZsUzg8z9kZBN2F0r4Nrck-m5aBK30vLEELz8xgsqqx57ddyQ.svg",
    "서울 잠실(LG)": "https://i.namu.wiki/i/N0z9TehLEmQjCo-zLrr3hb88FHRIbgU_ngkEgkd7EKz8ngUhi-1GI_ngwGliBx4G3VzzckRDGKULwM6dLOggqUGV4RFrrqinNz2M2pLgM4FG50vAjZvw2AyhpkrDhq7fZO2khD1hfu0cBKZH50sIWA.svg",
    "서울 잠실(두산)" : "https://i.namu.wiki/i/cDVrQIU8Clo9QtpeOKmnA7uFs3z__ESk80rOtjtEYxjwYAEaoGs39iF1DYg3CVHhcBfq8L6BLUkY4SNzbyzDZOkdf92V3bJHP-_z6a0Q2yLWsaKSEZZi9XxjA0uM9L6c1FIT3aLVY0iSrFooZZqPug.svg" ,
    "서울 고척(키움)": "https://i.namu.wiki/i/-rzSl860TxcORH5L617NnG79AeRq7ZHfkF0JvLfaAh1CyTbIBL_doH024nfTMy6JNBeWRi0bcQzJbtCHKcVPQ4XraLMWAJZGkkAQtRpIuQcAyJIQhcq5kjJTpW_g1hDKUsT--pKIFn0gK8g7gd34vw.svg",
    "인천(SSG)": "https://i.namu.wiki/i/cVYwBLxze1Oy3RGvNpSmeXxgKamX-46qthUbUrS_HVEtXD5wZnBoAi80WlwC-UAYTsZn6LPRyv5G9tjUwPxi6ji-AQSrI5vmY709IGhDNO5FoMiBYNSCHTEpvUXU7mrUrNUS4cD1bynYYQE-xDB6qA.svg"
}

# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)

# 각 지역에 동그란 마커 이미지 추가
for loc_name, coords in locations.items():
    image_url = images[loc_name]
    # HTML로 이미지를 추가하고 CSS로 둥글게 만들기
    html = f'''
    <div style="width: 40px; height: 40px; background-image: url({image_url}); background-size: cover; border-radius: 50%; border: 2px solid white;"></div>
    '''
    icon = folium.DivIcon(html=html)
    
    folium.Marker(
        location=coords,
        popup=loc_name,
        icon=icon
    ).add_to(m)

# 지도 저장
m.save("kbo_team_round_logo_map_image round.html")
