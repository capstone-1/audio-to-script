from summa.summarizer import summarize
from google.cloud import storage
import os

# 분석하고자 하는 텍스트 읽기
def script_to_summary(video_name):
    fileName = 'total_script.txt'
    texts = ''
    with open(fileName, encoding='utf-8-sig') as file:
        for line in file:
            texts += line.split(',')[-1] # 텍스트 구조에 따라 달라집니다.

    # 문장 출력부분
    with open('main_sentence_output.txt',mode='w',encoding='utf-8-sig') as file:
        file.write(summarize(texts, language='english', ratio=0.1)) # ratio -> 전체 문장중 요약으로 뽑을 비율
    
    upload_total_script_file(video_name)

# 토탈 스크립트 파일 생성, Summary sentence 파일 생성 -> GCS 업로드 -> 로컬 삭제
def upload_total_script_file(video_file_name):
    total_script = "total_script.txt"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("capstone-test")
    blob = bucket.blob(video_file_name + "/result/" + total_script)
    blob.upload_from_filename(total_script)

    sentence = "main_sentence_output.txt"
    blob = bucket.blob(video_file_name + "/result/" + sentence)
    blob.upload_from_filename(sentence)

    os.remove(total_script)
    os.remove(sentence)