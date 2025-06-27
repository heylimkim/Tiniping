import os
from gensim.models import Word2Vec
import numpy as np

# 모델 파일들이 저장된 디렉토리
model_dir = './static/model/'  # 모델이 저장된 경로
target_word = '이정현'  # 사용자 입력 단어

best_similarity = -1
best_model_file = None
word_already_in_model = False

# 1. 사용자가 입력한 단어가 모델에 있는지 확인
for model_file in os.listdir(model_dir):
    if model_file.endswith("_word2vec.model"):
        # 모델 파일 로드
        model_path = os.path.join(model_dir, model_file)
        model = Word2Vec.load(model_path)

        if target_word in model.wv:
            word_already_in_model = True
            best_model_file = model_file
            break

# 2. 해당 단어가 모든 모델에 없을 시 학습한 후 유사도를 계산
if not word_already_in_model:
    for model_file in os.listdir(model_dir):
        if model_file.endswith("_word2vec.model"):
            # 모델 파일 로드
            model_path = os.path.join(model_dir, model_file)
            model = Word2Vec.load(model_path)

            # '오준영' 단어를 추가 학습
            model.build_vocab([[target_word]], update=True)
            model.train([[target_word]], total_examples=1, epochs=1)

            # 모델에서 학습된 단어 목록
            words = model.wv.index_to_key

            print(f"모델: {model_file}")
            print(f"'{target_word}'과 모델 내 단어들 간의 유사도가 가장 높은 단어들:")

            similarities = []

            # '오준영'과 각 단어 간의 유사도를 계산
            for word in words:
                try:
                    similarity = model.wv.similarity(target_word, word)
                    similarities.append((word, similarity))
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_model_file = model_file
                except KeyError:
                    continue

            # 유사도가 높은 단어 두 개를 출력
            if similarities:
                sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
                for word, similarity in sorted_similarities[:2]:  # 상위 2개의 유사 단어 출력
                    print(f"{word}: {similarity:.4f}")
            else:
                print("모델에서 유사한 단어를 찾을 수 없습니다.")
            
            print("-" * 40)

# 3. 가장 유사도가 높은 모델 파일의 캐릭터 이름 출력
if best_model_file:
    character_name = best_model_file.replace('_word2vec.model', '')
    print(f"가장 유사도가 높은 모델: {character_name}")

    # 3. 단어 삭제: 단어가 존재하지 않았고 새로 학습한 경우에만 삭제
    if not word_already_in_model:
        for model_file in os.listdir(model_dir):
            if model_file.endswith("_word2vec.model"):
                model_path = os.path.join(model_dir, model_file)
                model = Word2Vec.load(model_path)
                if target_word in model.wv:
                    model.wv.pop(target_word, None)
                    print(f"단어 '{target_word}'이(가) 모델 '{model_file}'에서 삭제되었습니다.")
                    # 모델 저장 (필요 시 활성화)
                    # model.save(model_path)
else:
    print("모든 모델에서 유사한 단어를 찾을 수 없습니다.")
