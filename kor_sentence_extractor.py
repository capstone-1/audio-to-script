from krwordrank.word import KRWordRank
from krwordrank.sentence import make_vocab_score
from krwordrank.sentence import MaxScoreTokenizer
from krwordrank.sentence import keysentence
from google.cloud import storage
import os

# 토탈 스크립트 읽기 -> 개요 추출 -> 개요 반환
def script_to_summary(video_name):
    fileName = 'total_script.txt'
    texts = ''
    with open(fileName, encoding='utf-8-sig') as file:
        for line in file:
            texts += line.split(',')[-1] # 텍스트 구조에 따라 달라집니다.
    
    upload_total_script_file(video_name)

    # 키워드 학습
    wordrank_extractor = KRWordRank(
        min_count=5,  # 단어의 최소 출현 빈도수
        max_length=10,  # 단어의 최대길이
        verbose = True
    )
    beta = 0.85
    max_iter = 10

    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, num_keywords=100)

    stopwords = {}
    vocab_score = make_vocab_score(keywords, stopwords, scaling=lambda x : 1)
    tokenizer = MaxScoreTokenizer(vocab_score)  # 문장 내 단어 추출기

    #  패널티 설정 및 핵심 문장 추출
    penalty = lambda x: 0 if 25 <= len(x) <= 80 else 1
    sentencses = keysentence(
        vocab_score, texts, tokenizer.tokenize,
        penalty=penalty,
        diversity=0.3,
        topk=10  # 추출 핵심 문장 갯수 설정
    )

    summary = ""
    # 문장 출력부분
    for sentence in sentencses:
        summary += (sentence + '\n')

    return summary

# 토탈 스크립트 파일 업로드 및 삭제
def upload_total_script_file(video_file_name):
    total_script = "total_script.txt"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("capstone-test")
    blob = bucket.blob(video_file_name + "/result/" + total_script)
    blob.upload_from_filename(total_script)

    os.remove(total_script)