from konlpy.tag import Hannanum

hannanum = Hannanum()

# kiwi = Kiwi()
# kiwi.prepare()
# stopwords = set(["사람", "것"])
# # tokenize 함수를 정의합니다. 한국어 문장을 입력하면 형태소 단위로 분리하고, 
# # 불용어 및 특수 문자 등을 제거한 뒤, list로 반환합니다.
# def tokenize(sent):
#     res, score = kiwi.analyze(sent)[0] # 첫번째 결과를 사용
#     return [word + ('다' if tag.startswith('V') else '') # 동사에는 '다'를 붙여줌
#             for word, tag, _, _ in res
#             if not tag.startswith('E') and not tag.startswith('J') and not tag.startswith('S') and word not in stopwords] # 조사, 어미, 특수기호 및 stopwords에 포함된 단어는 제거
def tokenize(sent):
    return hannanum.nouns(sent)