# Machine_Learning_Notebook
# algorithm and coding with Python
### 1、监督学习
### 2、无监督学习
### 3、半监督学习


# !usr/bin/python3
import jieba
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import matplotlib
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import wordcloud
import warnings
warnings.filterwarnings("ignore")

def load_csv_data(path):
    """加载csv文件，指定对应的路径，列名分别对应文章ID，标题，内容，分类，文章链接，作者"""
    dataset = pd.read_csv(path, error_bad_lines=False, encoding='utf-8', header=None)
    column_list = ['index', 'title', 'content', 'terrace', 'href', 'author']
    dataset.columns = column_list
    print ('开始加载')
    print ('*'*60)
    print(dataset.head(10))
    print('*' * 60)
    print('加载完成')
    return dataset

def title_word_list(file_path, discard_stopwords, stopwords_path):
    """生成标题词库
    参数：path 数据路径 discard_stopwords 是否去停用词
    """
    dataset = load_csv_data(file_path)
    print('*' * 60)
    print ('开始生成标题词库')
    print('*' * 60)
    title = dataset.title.values.tolist()
    error_line = []
    word_list = []
    for line in title:
        try:
            if discard_stopwords:   # 如果需要去停用词，需要加载停用词词表，并判断分好的词是否在停用词表中，完成过滤
                stopwords = [line.strip() for line in open(stopwords_path, 'r', encoding='gbk').readlines()]
                sentence_seged = jieba.cut(line.strip())
                for word in sentence_seged:
                    if len(word) > 1:
                        if word not in stopwords:
                            word_list.append(word)
            else:                   # 如果不需要去停用词，直接生成词表
                sentence_seged = jieba.cut(line.strip())
            for word in sentence_seged:
                if len(word) > 1:
                    word_list.append(word)
        except:
            error_line.append(line)
            continue
    print ("加载标题词库完成")
    print('*' * 60)
    return word_list

def content_word_list(file_path, discard_stopwords, stopwords_path):
    """生成文章词库，使用自定义停用词表"""
    dataset = load_csv_data(file_path)
    content = dataset.content.values.tolist()
    error_line = []
    word_list = []
    for line in content:
        try:
            if discard_stopwords:   # 如果需要去停用词，需要加载停用词词表，并判断分好的词是否在停用词表中，完成过滤
                stopwords = [line.strip() for line in open(stopwords_path, 'r', encoding='gbk').readlines()]
                sentence_seged = jieba.cut(line.strip())
                for word in sentence_seged:
                    if len(word) > 1:
                        if word not in stopwords:
                            word_list.append(word)
            else:                   # 如果不需要去停用词，直接生成词表
                sentence_seged = jieba.cut(line.strip())
            for word in sentence_seged:
                if len(word) > 1:
                    word_list.append(word)
        except:
            error_line.append(line)
            continue
    return word_list

def words_count(word_list):
    """提供词库词频统计功能"""
    words_df = pd.DataFrame({'word_list':word_list})
    words_stat = words_df.groupby(by=['word_list'])['word_list'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    return words_stat

def worldcloud_pure(font_path, word_count, number,length=10, width=5):
    """提供素色的背景的词云展示
    参数：font_path 字体路径  word_count 统计后的词库 number 词云显示的数量 length 画布长度 width 画布宽度
     'C:\\Users\\dell\\RundongZhou\\NLP_project\\data\\simhei.ttf'
     """
    word_cloud = WordCloud(font_path=font_path, background_color='white', max_font_size=80)
    word_frequence = {word[0]:word[1] for word in word_count.head(number).values}
    print (word_frequence)
    word_cloud = wordcloud.fit_words(word_frequence)
    plt.axis("off")
    matplotlib.rcParams['figure.figsize'] = (length, width)
    plt.imshow(word_cloud)
    plt.savefig('C:\\Users\\dell\\Desktop\\output.jpg')

def wordcloud_picture(font_path, pic_path, word_count, number,length=10, width=5):
    """提供有背景图的词云展示
    参数：font_path 字体路径  pic_path 图片路劲 word_count 统计后的词库 number 词云显示的数量
    length 画布长度 width 画布宽度
    'C:\\Users\\dell\\RundongZhou\\NLP_project\\data\\simhei.ttf'
    'C:\\Users\\dell\\RundongZhou\\NLP_project\\image\\entertainment.jpeg'
    """
    img = imread(pic_path) #导入自定义图片
    word_cloud = WordCloud(background_color="white", mask=img, font_path=font_path, max_font_size=20)
    word_frequence = {word[0]:word[1] for word in word_count.head(number).values}
    word_cloud = wordcloud.fit_words(word_frequence)
    img_Colors = ImageColorGenerator(img)
    plt.axis("off")
    plt.imshow(wordcloud.recolor(color_func = img_Colors))
    plt.savefig('C:\\Users\\dell\\Desktop\\output.jpg')

if __name__ == '__main__':

    file_path = 'C:\\Users\\dell\\Desktop\\database5.csv'
    stopwords_path = 'C:\\Users\\dell\\RundongZhou\\stopwords\\stopwords\\自定义中文停用词表.txt'
    pic_path = 'C:\\Users\\dell\\RundongZhou\\NLP_project\\image\\entertainment.jpeg'
    font_path = 'C:\\Users\\dell\\RundongZhou\\NLP_project\\data\\simhei.ttf'
    number = 500                           # 词云选取的词的数量
    is_title_wordcloud = True               # True 为生成标题词云， False 为生成内容词云
    discard_stopwords = True                # Ture 去除停用词， False 保留停用词
    output_word_frequence = True            # True 输出词频统计，False 不输出词频统计
    has_picture = True                      # True 输出以图片为背景的词云， False 以素色为背景

    if is_title_wordcloud:
        print("开始生成标题词云：")
        # 1 加载数据,利用jieba完成分词（精确模式），选择是否去除停用词，生成词表
        word_title_list = title_word_list(file_path=file_path, discard_stopwords=discard_stopwords,
                                          stopwords_path=stopwords_path )
        # 2 生成词频统计表
        words_stat = words_count(word_title_list)
        if output_word_frequence:
            words_stat.to_csv('C:\\Users\\dell\\Desktop\\words_title_count.csv')
        else:
            pass

        # 3 生成词云图片,10*10的图片，并输出
        if has_picture:
            wordcloud_picture(font_path=font_path, pic_path=pic_path, word_count=words_stat,
                              number=number, length=10, width=10)
        else:
            worldcloud_pure(font_path=font_path, word_count=words_stat, number=number, length=10, width=10)
