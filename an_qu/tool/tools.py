from pkuseg import pkuseg
from gensim import corpora, models, similarities
import sys
sys.path.append('/home/ai/PycharmProjects/an_qu/an_qu/config')
from config import config
stop_path = config.stop_path
ans_path = config.ans_path
que_path = config.que_path
mydict_path = config.mydict_path
sym_path = config.sym_path
seg = pkuseg(user_dict=mydict_path)


# 获取停用词表
def stop_words_list(filepath):
    wlst = [w.strip() for w in open(filepath, 'r', encoding='utf8').readlines()]
    return wlst


# 返回去停用词之后的分词结果
def seg_sentence(sentence, stop_words):
    sentence_seged = seg.cut(sentence)
    outstr = []
    for word in sentence_seged:
        # if word not in stop_words:
        if word not in stop_words:
            outstr.append(word)
    return outstr


# 返回某个词的同义词列表
def get_sym(w, word_set):
    '''
    从同义词词林.txt文件中，获取某一词的同义词列表
    :param w:input 关键词
    :param word_set: 同义词词集（同义词词林.txt）
    :return:results,该关键词同义词列表
    '''
    for each in word_set:
        for word in each:
            if w == word:
                return each

            # 返回所有匹配的语句中关键词重合最多的一句
            def get_better_one(list1, list2):
                max = 0
                _list = []
                str = "正在为您转人工服务,请稍等......"
                for x, text in enumerate(list1):
                    r = 0
                    text = list(set(text))
                    for i in text:
                        if i in list2:
                            r += 1
                    if r == len(list2):
                        return x
                    if r > max:
                        max = r
                        _list.append(x)
                    if r == 0:
                        return str
                if list1 != []:
                    return _list[-1]


# 返回问句和语料问句的相似度
def instead_word(text, sym_words):
    for x, words in enumerate(text):
        for each in sym_words:
            for word in each:
                if words == word:
                    text[x] = each[0]
    return text


# 返回所有词的同义词表
def get_sym_words():
    f = open(sym_path, 'r', encoding="utf8")
    lines = f.readlines()
    sym_words = []  # 同义词表
    for line in lines:
        line = line.replace('\n', '')
        items = line.split(' ')
        index = items[0]
        if (index[-1] == '='):
            sym_words.append(items[1:])
    return sym_words


# 返回一个字典
def get_dictionary():
    sym_words = get_sym_words()
    # 将问题经过分词以后转换为列表
    texts = [seg_sentence(seg, stop_path) for seg in open(que_path, 'r', encoding='utf8').readlines()]
    samilar_text = []
    # 将同义词替换的句子返回
    for text in texts:
        answer_list = instead_word(text, sym_words)
        samilar_text.append(answer_list)
    # 一、建立词袋模型
    dictionary = corpora.Dictionary(samilar_text)
    return dictionary, samilar_text


# 返回问题和答案的矩阵相似度的数值的列表
def get_samilar(keyword, dictionary, texts):
    sym_words = get_sym_words()
    stop_words = stop_words_list(stop_path)
    # 2、基于文件集建立【词典】，并提取词典特征数
    feature_cnt = len(dictionary.token2id.keys())
    # 3、基于词典，将【分词列表集】转换为【稀疏向量集】，也就是【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 4、使用“TF-TDF模型”处理【语料库】
    tfidf = models.TfidfModel(corpus)
    # 5、构建一个query文本，利用词袋模型的字典将其映射到向量空间,同理，用词典把搜索词也转换为稀疏向量
    keywords = seg_sentence(keyword, stop_words)
    keyword_list = instead_word(keywords, sym_words)
    kw_vector = dictionary.doc2bow(keyword_list)
    # 6、对稀疏向量建立索引,# similarities 相似之处,# SparseMatrixSimilarity 稀疏矩阵相似度
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
    # 7、相似的计算,返回的是用户提问的句子和每一个问句的矩阵的相似度
    sim = index[tfidf[kw_vector]]
    return sim


# 返回所有匹配的语句中关键词重合最多的三句
def get_better_three(list1, list2):
    max = 0
    dict = {}
    for x, text in enumerate(list1):
        r = 0
        text = list(set(text))
        for i in text:
            if i in list2:
                r += 1
        dict[x] = r
    result = sorted(dict, key=dict.__getitem__, reverse=True)
    return result[0:3]
    #     if r==len(list2):
    #         return x
    #     if r>max:
    #         max=r
    #         _list.append(x)
    # if list1!=[]:
    #     return _list[-1]


# 分词的时候读取我自己定义的词典
def read_mydict():
    mydict = []
    mydictfile = open(mydict_path, "r", encoding="utf8").readlines()
    for i in mydictfile:
        mydict.append(i)
    return mydict


# 对相似度矩阵进行搜索
def search(que_txt, ans_txt, dictionary, texts, keyword):
    result_list = []
    answer = []
    _list = []
    sym_words = get_sym_words()
    stop_words = stop_words_list(stop_path)
    sim = get_samilar(keyword, dictionary, texts)
    for i in range(len(sim)):
        if sim[i] > 0.1:
            result_list.append(instead_word(seg.cut(que_txt[i]), sym_words))
            _list.append(i)
    x = get_better_three(result_list, instead_word(seg_sentence(keyword, stop_words), sym_words))

    for i in x:
        answer.append(ans_txt[_list[i]])
        # print(_list[x] + 1)
    return answer
if __name__=="__main__":
	dict=read_mydict()
	print(dict)
