import requests
from bs4 import BeautifulSoup
import json
import os
from gensim.models import Word2Vec

# URL에서 데이터를 가져오기
url = "https://namu.wiki/w/%ED%8A%B8%EB%9F%AC%ED%95%91"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 캐릭터 데이터를 저장할 딕셔너리
character_data = {}

# 1. 캐릭터 이름 추출
name_tag = soup.find('span', attrs={'data-v': True})
if name_tag:
    character_name = name_tag.get_text(strip=True)
else:
    name_tag = soup.find('h1') or soup.find('h2')
    character_name = name_tag.get_text(strip=True) if name_tag else "Unknown"

character_data['name'] = character_name


# 3. 성별, 소품, 좋아하는 것, 싫어하는 것 등의 정보 수집
def extract_info(label):
    element = soup.find(string=label)
    if element:
        value = element.find_next('div').get_text(strip=True)
        return value
    return "None"

character_data['gender'] = extract_info("성별")
character_data['accessory'] = extract_info("소품")
character_data['likes'] = extract_info("좋아하는 것")
character_data['dislikes'] = extract_info("싫어하는 것")
character_data['magic'] = extract_info("마법")  # 마법 정보 추가

# 4. 기타 리스트에 학습한 내용 외의 나머지 정보 수집
other_info = []

# HTML에서 모든 텍스트를 가져오기
page_text = soup.get_text(separator=' ', strip=True)

# 이미 수집된 정보는 기타 리스트에서 제외
for key, value in character_data.items():
    if key != "name" and value != "None":
        page_text = page_text.replace(value, '')

# 기타 리스트에 나머지 정보를 추가
other_info.extend(page_text.split())

# 기타 정보도 캐릭터 데이터에 추가 (필요에 따라 저장할 수 있음)
character_data['other_info'] = ' '.join(other_info)

# 스크래핑한 데이터 출력
print(json.dumps(character_data, ensure_ascii=False, indent=4))

# JSON 파일로 저장
json_filename = f"{character_name.replace(' ', '_')}.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(character_data, f, ensure_ascii=False, indent=4)

# Word2Vec 모델 학습
sentences = []
for key, value in character_data.items():
    if key != "name":
        sentences.append(value.split())

# '기타' 리스트를 학습 문장에 추가
sentences.append(other_info)

# Word2Vec 모델 학습
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# 학습된 모델 저장
model.save(f"{character_name.replace(' ', '_')}_word2vec.model")
