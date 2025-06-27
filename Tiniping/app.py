from flask import Flask, request, render_template, url_for
import os
import json
from gensim.models import Word2Vec
import numpy as np

app = Flask(__name__)

# 모델 파일들이 저장된 디렉토리
model_dir = './static/model/'  # 캐릭터 모델이 저장된 경로
json_dir = './static/json/'  # 캐릭터 정보가 담긴 JSON 파일이 저장된 경로

def load_character_info(character_name):
    """JSON 파일에서 캐릭터 정보를 로드합니다."""
    file_path = os.path.join(json_dir, f'{character_name}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None

def find_most_similar_models(target_word):
    best_similarity = -1
    best_characters = []

    characters = list(target_word)

    for model_file in os.listdir(model_dir):
        if model_file.endswith("_word2vec.model"):
            try:
                model_path = os.path.join(model_dir, model_file)
                model = Word2Vec.load(model_path)

                model_similarity_sum = 0
                model_word_count = 0

                for char in characters:
                    if char in model.wv:
                        similarities = []
                        for word in model.wv.index_to_key:
                            similarity = model.wv.similarity(char, word)
                            similarities.append(similarity)

                        if similarities:
                            avg_similarity = np.mean(similarities)
                            model_similarity_sum += avg_similarity
                            model_word_count += 1

                if model_word_count > 0:
                    final_similarity = model_similarity_sum / model_word_count
                    character_name = model_file.replace('_word2vec.model', '')
                    if final_similarity > best_similarity:
                        best_similarity = final_similarity
                        character_info = load_character_info(character_name)
                        if character_info:
                            character_info['name'] = character_name
                            best_characters.append(character_info)  # 기존 리스트에 추가
                    elif final_similarity == best_similarity:
                        character_info = load_character_info(character_name)
                        if character_info:
                            character_info['name'] = character_name
                            best_characters.append(character_info)  # 기존 리스트에 추가
            except Exception as e:
                print(f"Error processing model {model_file}: {e}")
                continue

    print(f"Final best characters: {[character['name'] for character in best_characters]}")  # 최종 선택된 캐릭터 이름들만 출력
    return best_characters


@app.route('/')
def home():
    return render_template('Tiniping.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    target_word = request.form.get('target_word')  # 사용자 입력 단어 받아오기

    if not target_word:
        return render_template('result.html', error="단어를 입력해주세요.")

    best_models = find_most_similar_models(target_word)

    if best_models:
        return render_template('result.html', characters=best_models, user_name=target_word)  # 사용자가 입력한 단어를 user_name 변수로 전달
    else:
        # 트러핑 정보 로드
        character_info = load_character_info('트러핑')
        return render_template('result.html', characters=[character_info], user_name=target_word)  # 트러핑 정보와 사용자 이름 전달

if __name__ == '__main__':
    app.run(debug=True)
