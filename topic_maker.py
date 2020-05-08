# -*- coding: utf-8 -*- 
#

import tomotopy as tp # 먼저 모듈을 불러와야겠죠
from tokenizer import tokenize
from multiprocessing import Process, Manager
from google.cloud import storage
from collections import OrderedDict
import os

def make_topic(count_script, video_file_name):
    # 멀티프로세싱으로 다중 lda 수행
    manager = Manager()
    numbers = manager.list()
    results = manager.list()

    file_names = []
    file_numbers = []
    procs = []
    for i in range(0, count_script):
        file_names.append('script_' + str(i) + '.txt')
        file_numbers.append(str(i))
    for index, file_name in enumerate(file_names):
        proc = Process(target=core, args=(file_name, file_numbers[index], video_file_name, numbers, results))
        procs.append(proc)
        proc.start()
    for proc in procs: 
        proc.join()
    os.remove("audio.wav")
    
    return make_json(numbers, results)

def core(file_name, file_number, video_file_name, numbers, results):
    # 현재 동작중인 프로세스 표시
    current_proc = os.getpid()
    print('now {0} lda worker running...'.format(current_proc))

    model = tp.LDAModel(k=1, alpha=0.1, eta=0.01, min_cf=3)
    # LDAModel을 생성합니다.
    # 토픽의 개수(k)는 1개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거
    
    # 다음 구문은 input_file.txt 파일에서 한 줄씩 읽어와서 model에 추가
    for i, line in enumerate(open(file_name, encoding='utf-8')):
        model.add_doc(tokenize(line)) # 한국어 토크니제이션
        if i % 10 == 0: print('Document #{} has been loaded'.format(i))
    
    # model의 num_words나 num_vocabs 등은 train을 시작해야 확정됩니다.
    # 따라서 이 값을 확인하기 위해서 train(0)을 하여 실제 train은 하지 않고
    # 학습 준비만 시킵니다.
    model.train(0)
    print('Total docs:', len(model.docs))
    print('Total words:', model.num_words)
    print('Vocab size:', model.num_vocabs)
    
    model.train(200)

    # 학습된 토픽들을 출력 -> k는 1이기 때문에 한 번 수행
    for i in range(model.k):
        res = model.get_topic_words(i, top_n=5)
        print('Topic #{}'.format(i), end='\t')
        topic = ', '.join(w for w, p in res)
        print(topic)
        numbers.append(file_number)
        results.append(topic)
      
    os.remove(file_name)

def make_json(numbers, results):
    print(numbers)
    print(results)

    topic_list = []
    # file number -> script time
    for num, result in zip(numbers, results):
        detail = OrderedDict()
        topic = OrderedDict()
        detail["start"] = int(num) * 177
        detail["end"] = (int(num)+1) * 177
        detail["topic"] = result
        topic["topicEditItem"] = detail
        topic_list.append(topic)
        print(topic)
    
    print(topic_list)
    return topic_list
