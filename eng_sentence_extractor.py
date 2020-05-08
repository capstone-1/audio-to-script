from summa.summarizer import summarize
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

    return summarize(texts, language='english', ratio=0.1)

# 토탈 스크립트 파일 업로드 및 삭제
def upload_total_script_file(video_file_name):
    total_script = "total_script.txt"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("capstone-test")
    blob = bucket.blob(video_file_name + "/result/" + total_script)
    blob.upload_from_filename(total_script)

    os.remove(total_script)