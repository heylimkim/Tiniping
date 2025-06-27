import os
from gensim.models import Word2Vec
import numpy as np

# 모델 파일들이 저장된 디렉토리
model_dir = './static/model/'  # 모델이 저장된 경로
target_word = '김혜림'  # 사용자 입력 단어

best_similarity = -1
best_models = []

# 1. 사용자가 입력한 단어를 한 글자씩 분리
characters = list(target_word)

# 2. 각 글자에 대해 유사도 계산
for model_file in os.listdir(model_dir):
    if model_file.endswith("_word2vec.model"):
        # 모델 파일 로드
        model_path = os.path.join(model_dir, model_file)
        model = Word2Vec.load(model_path)
        
        model_similarity_sum = 0
        model_word_count = 0
        
        for char in characters:
            if char in model.wv:
                # 해당 글자와 모델 내 단어들 간의 유사도 계산
                similarities = []
                for word in model.wv.index_to_key:
                    similarity = model.wv.similarity(char, word)
                    similarities.append(similarity)
                
                if similarities:
                    # 평균 유사도 계산
                    avg_similarity = np.mean(similarities)
                    model_similarity_sum += avg_similarity
                    model_word_count += 1
            else:
                # 해당 글자가 모델에 없으면 pass
                continue
        
        if model_word_count > 0:
            final_similarity = model_similarity_sum / model_word_count
            if final_similarity > best_similarity:
                best_similarity = final_similarity
                best_models = [model_file.replace('_word2vec.model', '')]
            elif final_similarity == best_similarity:
                best_models.append(model_file.replace('_word2vec.model', ''))

# 3. 가장 유사도가 높은 모델 파일들의 캐릭터 이름 출력
if best_models:
    print("가장 유사도가 높은 모델들:")
    for model in best_models:
        print(f"- {model}")
else:
    print("모든 모델에서 유사한 단어를 찾을 수 없습니다.")
