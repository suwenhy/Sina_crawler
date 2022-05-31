import imageio
import jieba
import csv
import re
from collections import Counter
import wordcloud
from snownlp import SnowNLP
from snownlp import sentiment

filename = "2022/2022_phase3"  # 评论文件名，应放在resource目录下
filedir = f"resource/{filename}.csv"  # 原文档路径
breakdir = f"output/{filename}_break.csv"  # 分词文件保存路径
wordclouddir = f"output/{filename}_could.png"  # 词云图片保存路径


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('resource/停用词.txt', encoding='UTF-8').readlines()]
    return stopwords


def processing(text):
    """
    数据清洗, 可以根据自己的需求进行重载
    """
    text = re.sub("@.+?( |$)", "", text)  # 去除 @xxx (用户名)
    text = re.sub("【.+?】", "", text)  # 去除 【xx】 (里面的内容通常都不是用户自己写的)
    text = re.sub(".*?:", "", text)  # 去除微博用户的名字
    text = re.sub("#.*#", "", text)  # 去除话题引用
    text = re.sub("\n", "", text)#去掉换行符
    return text


# 对句子进行中文分词
def seg_depart(sentence):
    jieba.load_userdict('resource/保留词.txt')
    sentence_depart = jieba.cut(sentence.strip())
    print(sentence_depart)
    stopwords = stopwordslist()  # 创建一个停用词列表
    outstr = ''  # 输出结果为outstr
    for word in sentence_depart:  # 去停用词
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += "  "
    return outstr


# 对数据进行分词操作,并保存文件至工程output文件夹
def jieba_break():
    outputs = open(breakdir, 'w', encoding='UTF-8')  # 输出文档路径,参数a表示追加文件，w表示覆盖重写
    with open(filedir, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', doublequote=False)
        for line in reader:
            line = processing(line[6])  # 微博在文档的第一列
            print(line)
            line_seg = seg_depart(line)
            outputs.write(line_seg + '\n')  # 将分词结果保存到文件中
    outputs.close()


def getallwords():  # 将分词后的评论读取到内存中，以集合的形式
    cut_words = ""
    for line in open(breakdir, encoding='utf-8'):
        line.strip('\n')
        line = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", line)
        seg_list = jieba.cut(line, cut_all=False)
        cut_words += (" ".join(seg_list))
    all_words = cut_words.split()
    return all_words  # 返回分词集合


def couter(all_words):
    c = Counter()
    # 统计词频
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    print('\n词频统计结果：')
    topcomment = ''
    num = 0;
    for (k, v) in c.most_common(100):  # 输出词频最高的前50个词
        num = num + 1
        if (num % 7 == 0):
            print("")
        print("%s:%d" % (k, v), end=' ')
        topcomment += k + " "
    # print("\n"+topcomment)
    return topcomment


def analysis(allwords):
    cout = 0
    num = 0
    for word in allwords:
        s1 = SnowNLP(word)
        num = num + 1
        cout += s1.sentiments
    avg = cout / num
    print(avg)
    return avg


def creatWordCloud(words):
    mask = imageio.imread_v2('resource/backgroud.png')  # 设置蒙版图片，爱心图
    w = wordcloud.WordCloud(max_font_size=100, width=2000,font_path = "resource/ziti.ttf", height=1400, max_words=100,
                            background_color='white', colormap='cool', mask=mask)
    w.generate(words)  # 为词云注入词组
    w.to_file(wordclouddir)
    print("词云绘制完成")

#使用自有语料训练情感分析模型
def trainNewMoudle():
    sentiment.train("resource/train/neg2.txt", "resource/train/pos2.txt")
    sentiment.save('output/weibo.marshal')


if __name__ == '__main__':
    #jieba_break()  # 进行分词操作
    print("分词成功！！！，下面进行词频统计")
    allwords = getallwords()
    topcomment = couter(allwords)  # 统计出高频词汇
    creatWordCloud(topcomment)#将高频词绘制成词云
    #trainNewMoudle() #使用自带的新语料训练模型
    analysis(allwords)  # 对分词结果进行情感分析打分