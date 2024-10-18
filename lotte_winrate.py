import pandas as pd


file_path = 'C:\Mtest\개인연습\롯데_데이터.csv'
df = pd.read_csv(file_path)

year_changes = df['연도'].diff() !=0

winsum = year_changes[year_changes].index -1

valid_indices = winsum[winsum >= 0]

result = df.loc[valid_indices]

result.rename(columns={'Losses': 'Wins', 'Wins': 'Losses'},inplace=True)
result['승률'] = (result['Wins'] / (result['Wins'] + result['Losses'])) * 100
result['승률'] = result['승률'].round(1).astype(str) + '%' #소수첫째자리 반올림후 %추가
final_result = result[['연도', 'Wins', 'Losses', '승률']]

final_result.reset_index(drop=True, inplace=True)  # 인덱스 제거
final_result.insert(0, '팀명', '롯데')  # 첫 번째 열에 '팀명' 추가

print(final_result)