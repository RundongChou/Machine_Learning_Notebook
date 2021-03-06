# coding:utf-8
# 中文版的LDA  Demo


import codecs
import gensim
import jieba
import pymysql
from gensim.corpora import Dictionary
from lda.dataFromMysql import get_data_from_mysql, updata


# 获取数据库的原始语料
def get_data_list():
    data_list = get_data_from_mysql()
    return data_list

# 读取停用词
def get_stop_word(stop_word_path=r'model\stopwords.txt'):
    stopwords = codecs.open(stop_word_path,'r',encoding='utf8').readlines()
    stopwords = [ w.strip() for w in stopwords ]
    stopwords.append(" ")
    stopwords.append("  ")
    return stopwords

# 分词，同时过滤掉停用词
def jieba_cut(data_list, stopwords):
    train_set = []
    for line in data_list:
        line = list(jieba.cut(line[2]))
        train_set.append([ w for w in line if w not in stopwords ])
    return train_set

# 构建训练字典库，同时保持字典
def build_dictionary(train_set, file_name=r"model\biu_b_ask_zhihu_1000.dict"):
    dictionary = Dictionary(train_set)
    dictionary.save(file_name)
    return dictionary

# 构建corpus
def build_corpus(dictionary, train_set):
    corpus = [dictionary.doc2bow(text) for text in train_set]
    return corpus

# lda模型训练， 同时保存模型
def lda_train( corpus,dictionary,num_topics=25, file_name=r"model\biu_b_ask_model"):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    lda.save(file_name)
    return lda


# 加载LDA模型
def load_lda( file_name=r"model\biu_b_ask_model"):
    lda = gensim.models.ldamodel.LdaModel.load(file_name)
    return lda

# 加载字典模型
def load_dic( file_name=r"model\biu_b_ask_zhihu_1000.dict"):
    dictionary = Dictionary.load(file_name)
    return dictionary


# lda模型 打印num个主题
def print_topic(lda, num_topics = 25, num_words = 40):
    topic_list = lda.print_topics(num_topics=num_topics, num_words=num_words)
    for topic in topic_list:
        print(topic)


# 给定多个新文档，输出其主题分布
def print_test_doc_top(data_list, train_set, dictionary, lda):
    indx = 0
    while True:
        source_doc = data_list[indx]
        test_doc = train_set[indx]
        indx += 1
        print(source_doc)
        print(test_doc)
        if len(test_doc) > 3:
            doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
            doc_lda = lda[doc_bow]  # 得到新文档的主题分布
            print(source_doc[0])
            print(doc_lda)  # 输出新文档的主题分布
            print(doc_lda[0][0])
            for tmp in doc_lda:
                print("%s\n%f" % (lda.print_topic(tmp[0]), tmp[1]))
        print("")

        if indx >= len(train_set):
            break

def get_test_doc_top(data_list, train_set, dictionary, lda):
    indx = 0
    result_data = []
    while True:
        source_doc = data_list[indx]
        test_doc = train_set[indx]
        indx += 1
        print(source_doc)
        print(test_doc)
        if len(test_doc) > 3:
            document = []
            doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
            doc_lda = lda[doc_bow]                  # 得到新文档的主题分布
            document.append(doc_lda[0][0])                          # 主题类别序号
            document.append(pymysql.escape_string(str(test_doc)))   # lda 提取出来的关键词
            document.append(str(source_doc[0]))                     # mysql对应的id
            result_data.append(document)

        if indx >= len(train_set):
            return result_data


if __name__ == '__main__':

    topic_num = 5                           # 主题数
    num_word = 20                           # 每个主题的单词数
    is_rebuild_model = False                # True 为重新训练， False 读取数据源
    data_list = get_data_list()              # 1 获取原始语料
    stop_word = get_stop_word()              # 2 获取停用词
    train_set = jieba_cut(data_list, stop_word)      # 3 分词，同时过滤掉停用词

    if is_rebuild_model:
        print("重新构建模型：")
        dictionary = build_dictionary(train_set)        # 4 构建字典, copus
        corpus = build_corpus(dictionary, train_set)
        lda = lda_train(corpus, dictionary, num_topics=topic_num)        # 5 构建LDA模型
        print_topic(lda, num_topics = topic_num, num_words = num_word)
        # print_test_doc_top(data_list, train_set, dictionary, lda)       # 6 测试
        resutl_data = get_test_doc_top(data_list, train_set, dictionary, lda)
        for re in resutl_data:
            print(re)
        updata(resutl_data)
    else:
        print("加载旧模型：")
        dictionary = load_dic()         # 4 加载字典, copus
        lda = load_lda()                 # 5 加载LDA模型
        print_topic(lda, num_topics = topic_num, num_words = num_word)
        # print_test_doc_top(data_list, train_set, dictionary, lda)         # 6 测试
        resutl_data = get_test_doc_top(data_list, train_set, dictionary, lda)
        for re in resutl_data:
            print(re)
        updata(resutl_data)
