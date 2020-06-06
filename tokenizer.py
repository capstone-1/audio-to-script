from konlpy.tag import Hannanum

hannanum = Hannanum()

def tokenize(sent):
    token = hannanum.nouns(sent)
    stop_words = ['그것', '이것', '저것', '이다', '때문', '하다', '그거', '이거', '저거', '되는', '그게', '아니', '저게', '이게', '지금', '여기', '저기', '거기']
    return [word for word in token if len(word) != 1 and word not in stop_words]