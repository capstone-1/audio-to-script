import tomotopy as tp # 먼저 모듈을 불러와야겠죠
from tokenizer import tokenize

def make_topic():
    model = tp.LDAModel(k=7, alpha=0.1, eta=0.01, min_cf=3)
    # LDAModel을 생성합니다.
    # 토픽의 개수(k)는 5개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거할 겁니다.
    
    # 다음 구문은 input_file.txt 파일에서 한 줄씩 읽어와서 model에 추가합니다.
    for i, line in enumerate(open('script_0.txt', encoding='utf-8')):
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
    
    # 다음 구문은 train을 총 200회 반복하면서, 
    # 매 단계별로 로그 가능도 값을 출력해줍니다.
    # 혹은 단순히 model.train(200)으로 200회 반복도 가능합니다.
    for i in range(200):
        print('Iteration {}\tLL per word: {}'.format(i, model.ll_per_word))
        model.train(1)
    
    # 학습된 토픽들을 출력해보도록 합시다.
    for i in range(model.k):
        # 토픽 개수가 총 20개이니, 0~19번까지의 토픽별 상위 단어 10개를 뽑아봅시다.
        res = model.get_topic_words(i, top_n=10)
        print('Topic #{}'.format(i), end='\t')
        print(', '.join(w for w, p in res))