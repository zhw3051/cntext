#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import numpy as np
import pathlib
import re
from cntext.dictionary.dictionary import *


def init_jieba(diydict=dict()):
    """
    jieba词典初始化, 为防止情感词被错分，需要在调用情感函数前，先运行init_jieba()
    :param diydict: 自定义词典，默认空字典； 当使用senti_by_diydict时，才设置diydict
    :return:
    """

    for key in diydict.keys():
        for word in diydict[key]:
            jieba.add_word(word)
    dictlists = [DUTIR_Ais, DUTIR_Wus, DUTIR_Haos, DUTIR_Jings,
             DUTIR_Jus, DUTIR_Les, DUTIR_Nus, HOWNET_deny,
             HOWNET_extreme, HOWNET_ish, HOWNET_more, HOWNET_neg,
             HOWNET_pos, HOWNET_very]
    for wordlist in dictlists:
        for word in wordlist:
            jieba.add_word(word)





def judgeodd(num):
    """
    判断奇数偶数。当情感词前方有偶数个否定词，情感极性方向不变。奇数会改变情感极性方向。
    """
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'






def Adj_senti(text):
    """
    简单情感分析，仅计算各个情绪形容词出现次数(占比)， 未考虑强度副词、否定词对情感的复杂影响。
    :param text:  待分析的中文文本数据
    :return: 返回情感信息
    """
    length, sentences, pos, neg, stopword_num = 0, 0, 0, 0, 0
    sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
    sentence_num = len(sentences)
    words = jieba.lcut(text)
    length = len(words)
    for w in words:
        if w in STOPWORDS_zh:
            stopword_num += 1
        if w in HOWNET_pos:
            pos+=1
        elif w in HOWNET_neg:
            neg+=1
        else:
            pass
    return {'word_num': length,
            'stopword_num': stopword_num,
            'sentence_num': sentence_num,
            'pos_word_num': pos,
            'neg_word_num': neg}



def AdjAdv_senti(text):
    """
    情感分析，考虑副词对情绪形容词的修饰作用和否定词的反转作用，
    其中副词对情感形容词的情感赋以权重，
    否定词确定情感值正负。

    :param text:  待分析的中文文本数据
    :return: 返回情感信息
    """
    sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
    wordnum = len(jieba.lcut(text))
    count1 = []
    count2 = []
    stopword_num = 0
    for sen in sentences:
        segtmp = jieba.lcut(sen)
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        poscount = 0  # 积极词的第一次分值
        poscount2 = 0  # 积极词反转后的分值
        poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for w in segtmp:
            if w in STOPWORDS_zh:
                stopword_num+=1
            if w in HOWNET_pos:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in HOWNET_extreme:
                        poscount *= 4.0
                    elif w in HOWNET_very:
                        poscount *= 3.0
                    elif w in HOWNET_more:
                        poscount *= 2.0
                    elif w in HOWNET_ish:
                        poscount *= 0.5
                    elif w in HOWNET_deny:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif w in HOWNET_neg:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in HOWNET_extreme:
                        negcount *= 4.0
                    elif w in HOWNET_very:
                        negcount *= 3.0
                    elif w in HOWNET_more:
                        negcount *= 2.0
                    elif w in HOWNET_ish:
                        negcount *= 0.5
                    elif w in HOWNET_deny:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif w == '！' or w == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in HOWNET_pos or HOWNET_neg:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1  # 扫描词位置前移

            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    pos_result = []
    neg_result = []
    for sentence in count2:
        score_array = np.array(sentence)
        pos = np.sum(score_array[:, 0])
        neg = np.sum(score_array[:, 1])
        pos_result.append(pos)
        neg_result.append(neg)

    pos_score = np.sum(np.array(pos_result))
    neg_score = np.sum(np.array(neg_result))
    score = {'sentence_num': len(count2),
             'word_num':wordnum,
             'stopword_num': stopword_num,
             'pos_score': pos_score,
             'neg_score': neg_score}
    return score



def senti_by_hownet(text, adj_adv=False):
    """
    使用知网Hownet词典进行(中)文本数据的情感分析;
    :param text:  待分析的中文文本数据
    :param adj_adv:  是否考虑副词（否定词、程度词）对情绪形容词的反转和情感强度修饰作用，默认False。默认False只统计情感形容词出现个数；
    :return:  返回情感信息
    """
    if adj_adv==True:
        return AdjAdv_senti(text)
    else:
        return Adj_senti(text)



def senti_by_dutir(text):
    """
    使用大连理工大学情感本体库DUTIR，仅计算文本中各个情绪词出现次数
    :param text:  中文文本字符串
    :return: 返回文本情感统计信息，类似于这样{'words': 22, 'sentences': 2, '好': 0, '乐': 4, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
    """
    wordnum, sentences, hao, le, ai, nu, ju, wu, jing, stopwords =0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    sentences = len(re.split('[\.。！!？\?\n;；]+', text))
    words = jieba.lcut(text)
    wordnum = len(words)
    for w in words:
        if w in STOPWORDS_zh:
            stopwords+=1
        if w in DUTIR_Haos:
            hao += 1
        elif w in DUTIR_Les:
            le += 1
        elif w in DUTIR_Ais:
            ai += 1
        elif w in DUTIR_Nus:
            nu += 1
        elif w in DUTIR_Jus:
            ju += 1
        elif w in DUTIR_Wus:
            wu += 1
        elif w in DUTIR_Jings:
            jing += 1
        else:
            pass
    result = {'word_num':wordnum,
            'sentence_num':sentences,
            'stopword_num':stopwords,
            '好_num':hao, '乐_num':le, '哀_num':ai, '怒_num':nu, '惧_num':ju, '恶_num': wu, '惊_num':jing}
    return result





"""
    简单情感分析，未考虑强度副词、否定词对情感的复杂影响。仅仅计算各个情绪词出现次数(占比)
    :param text:  中文文本字符串
    :return: 返回文本情感统计信息
    """

def senti_by_diydict(text, sentiwords):
    """
    使用diy词典进行情感分析，计算各个情绪词出现次数，未考虑强度副词、否定词对情感的复杂影响，
    :param text:  待分析中文文本
    :param sentiwords:  情感词字典；
    {'category1':  'category1 词语列表',
     'category2': 'category2词语列表',
     'category3': 'category3词语列表',
     ...
    }

    :return:
    """
    result_dict = dict()
    senti_categorys = sentiwords.keys()

    for senti_category in senti_categorys:
        result_dict[senti_category+'_num'] = 0

    word_num, sentence_num, stopword_num = 0,0,0
    sentence_num = len(re.split('[\.。！!？\?\n;；]+', text))
    words = jieba.lcut(text)
    wordnum = len(words)
    for word in words:
        if word in STOPWORDS_zh:
            stopword_num+=1
        for senti_category in senti_categorys:
            if word in sentiwords[senti_category]:
                result_dict[senti_category+'_num'] += result_dict[senti_category+'_num'] + 1
    result_dict['stopword_num'] = stopword_num
    result_dict['sentence_num'] = sentence_num
    result_dict['word_num'] = wordnum
    return result_dict






