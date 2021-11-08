from cntext.dictionary.dictionary import ADV_words, CONJ_words, STOPWORDS_zh
import re
import jieba
from collections import Counter
import numpy as np


def term_freq(text):
    text = ''.join(re.findall('[\u4e00-\u9fa5]+', text))
    words = jieba.lcut(text)
    words = [w for w in words if w not in STOPWORDS_zh]
    return Counter(words)



def readability(text, language='chinese'):
    """
    文本可读性，指标越大，文章复杂度越高，可读性越差。
    ------------
    【英文可读性】公式 4.71 x (characters/words) + 0.5 x (words/sentences) - 21.43；
    【中文可读性】  参考自   【徐巍,姚振晔,陈冬华.中文年报可读性：衡量与检验[J].会计研究,2021(03):28-44.】
                 readability1 ---每个分句中的平均字数
                 readability2  ---每个句子中副词和连词所占的比例
                 readability3  ---参考Fog Index， readability3=(readability1+readability2)×0.5
                 以上三个指标越大，都说明文本的复杂程度越高，可读性越差。

    """
    if language=='english':
        text = text.lower()
        num_of_characters = len(text)
        num_of_words = len(text.split(" "))
        num_of_sentences = len(re.split('[\.!\?\n;]+', text))
        ari = (
                4.71 * (num_of_characters / num_of_words)
                + 0.5 * (num_of_words / num_of_sentences)
                - 21.43
        )

        return {"readability": ari}
    if language=='chinese':
        adv_conj_words = set(ADV_words+CONJ_words)
        zi_num_per_sent = []
        adv_conj_ratio_per_sent = []
        sentences = re.split('[\.。！!？\?\n;；]+', text)
        for sent in sentences:
            adv_conj_num = 0
            zi_num_per_sent.append(len(sent))
            words = jieba.lcut(sent)
            for w in words:
                if w in adv_conj_words:
                    adv_conj_num+=1
            adv_conj_ratio_per_sent.append(adv_conj_num/len(words))
        readability1 = np.mean(zi_num_per_sent)
        readability2 = np.mean(adv_conj_ratio_per_sent)
        readability3 = (readability1+readability2)*0.5
        return {'readability1': readability1,
                'readability2': readability2,
                'readability3': readability3}







