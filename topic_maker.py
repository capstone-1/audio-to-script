# -*- coding: utf-8 -*- 
#
import tomotopy as tp
from tokenizer import tokenize
from multiprocessing import Process, Manager
from collections import OrderedDict
import os

def make_topic(count_script):
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
        proc = Process(target=core, args=(file_name, file_numbers[index], numbers, results))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

    os.remove("audio.wav")
    
    return make_json(numbers, results)

def core(file_name, file_number, numbers, results):
    # 현재 동작중인 프로세스 표시
    current_proc = os.getpid()
    print('now {0} lda worker running...'.format(current_proc))

    model = tp.LDAModel(k=3, alpha=0.1, eta=0.01, min_cf=5)
    # LDAModel을 생성
    # 토픽의 개수(k)는 10개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거
    
    # 다음 구문은 input_file.txt 파일에서 한 줄씩 읽어와서 model에 추가
    for i, line in enumerate(open(file_name, encoding='cp949')):
        token = tokenize(line)
        model.add_doc(token)
        if i % 10 == 0: print('Document #{} has been loaded'.format(i))
    
    model.train(0) 
    print('Total docs:', len(model.docs))
    print('Total words:', model.num_words)
    print('Vocab size:', model.num_vocabs)
    
    model.train(200)

    # 학습된 토픽들을 출력
    for i in range(model.k):
        res = model.get_topic_words(i, top_n=5)
        print('Topic #{}'.format(i), end='\t')
        topic = ', '.join(w for w, p in res)
        print(topic)
        numbers.append(file_number)
        results.append(topic)
      

def make_json(numbers, results):
    print(numbers)
    print(results)

    topic_list = []
    # file number -> script time
    for num, result in zip(numbers, results):
        detail = OrderedDict()
        detail["start"] = int(num) * 590
        detail["end"] = (int(num)+1) * 590
        detail["topic"] = result
        topic_list.append(detail)
    
    print(topic_list)
    return topic_list