# -*- coding: utf-8 -*- 
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import nltk.stem, nltk.corpus, nltk.tokenize, re
stemmer = nltk.stem.porter.PorterStemmer() 
# 영어 단어의 어근만 남겨주는 포터 스테머입니다.
stopwords = set(nltk.corpus.stopwords.words('english')) 
# 영어 단어의 불용어 집합입니다.
rgxWord = re.compile('[a-zA-Z][-_a-zA-Z0-9.]*') 
# 특수문자를 제거하기 위해 일반적인 형태의 단어를 나타내는 정규식입니다.
# 알파벳으로 시작하고 그 뒤에 알파벳 혹은 숫자, -,_, .가 뒤따라오는 경우만 단어로 취급합니다.
 
# tokenize 함수를 정의합니다. 문장을 입력하면 단어 단위로 분리하고, 
# 불용어 및 특수 문자 등을 제거한 뒤, 어근만 추출하여 list로 반환합니다.
def tokenize(sent):
    def stem(w):
        try: return stemmer.stem(w)
        except: return w
 
    return [stem(w) for w in nltk.tokenize.word_tokenize(sent.lower()) if w not in stopwords and rgxWord.match(w)]

# 한국어 전처리 -- 사용하지 않음
# from kiwipiepy import Kiwi
 
# kiwi = Kiwi()
# kiwi.prepare()
 
# # tokenize 함수를 정의합니다. 한국어 문장을 입력하면 형태소 단위로 분리하고, 
# # 불용어 및 특수 문자 등을 제거한 뒤, list로 반환합니다.
# def tokenize(sent):
#     res, score = kiwi.analyze(sent)[0] # 첫번째 결과를 사용
#     return [word + ('다' if tag.startswith('V') else '') # 동사에는 '다'를 붙여줌
#             for word, tag, _, _ in res
#             if not tag.startswith('E') and not tag.startswith('J') and not tag.startswith('S')] # 조사, 어미, 특수기호는 제거