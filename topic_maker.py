# -*- coding: utf-8 -*- 
#

import tomotopy as tp # 먼저 모듈을 불러와야겠죠
from tokenizer import tokenize
from multiprocessing import Process
from google.cloud import storage
import os

def make_topic(count_script, video_file_name):
    # 멀티프로세싱으로 다중 lda 수행
    file_names = []
    file_numbers = []
    procs = []
    for i in range(0, count_script):
        file_names.append('script_' + str(i) + '.txt')
        file_numbers.append(str(i))
    for index, file_name in enumerate(file_names): 
        proc = Process(target=core, args=(file_name, file_numbers[index], video_file_name))
        procs.append(proc)
        proc.start()
    for proc in procs: 
        proc.join()
    os.remove("audio.wav")

def core(file_name, file_number, video_file_name):
    # 현재 동작중인 프로세스 표시
    current_proc = os.getpid()
    print('now {0} lda worker running...'.format(current_proc))

    model = tp.LDAModel(k=1, alpha=0.1, eta=0.01, min_cf=3)
    # LDAModel을 생성합니다.
    # 토픽의 개수(k)는 7개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거할 겁니다.
    
    # 다음 구문은 input_file.txt 파일에서 한 줄씩 읽어와서 model에 추가합니다.
    for i, line in enumerate(open(file_name, encoding='utf-8')):
        model.add_doc(tokenize(line)) # 한국어 토크니제이션
        if i % 10 == 0: print('Document #{} has been loaded'.format(i))
    
    # model의 num_words나 num_vocabs 등은 train을 시작해야 확정됩니다.
    # 따라서 이 값을 확인하기 위해서 train(0)을 하여 실제 train은 하지 않고
    # 학습 준비만 시킵니다.
    # num_words, num_vocabs에 관심 없다면 이부분은 생략해도 됩니다.
    model.train(0)
    print('Total docs:', len(model.docs))
    print('Total words:', model.num_words)
    print('Vocab size:', model.num_vocabs)
    
    model.train(200)

    # 학습된 토픽들을 출력해보도록 합시다.
    for i in range(model.k):
        res = model.get_topic_words(i, top_n=5)
        print('Topic #{}'.format(i), end='\t')
        topic = ', '.join(w for w, p in res)
        print(topic)
        upload_topic_file(topic, "output_topic" + file_number + ".txt", video_file_name)
    os.remove(file_name)

# 추출된 토픽으로 파일 생성 -> GCS 업로드 (스크립트, 토픽) -> 로컬 삭제
def upload_topic_file(topic, topic_file_name, video_file_name):
    with open(topic_file_name, "a") as f:
            f.write(topic)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("capstone-test")
    blob = bucket.blob(video_file_name + "/result/" + topic_file_name)
    blob.upload_from_filename(topic_file_name)
    os.remove(topic_file_name)