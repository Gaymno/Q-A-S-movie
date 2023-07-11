import os
import re
import json
import jieba
import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB

#问题分类器的字典类，用于将问题类别和数字标签相互映射
class GenerQuestionClassification():
    def __init__(self):
        self.question_classification_path = "./model/question_classification.json"
        if not os.path.isfile(self.question_classification_path):
            self.save_vocab()

    def save_vocab(self):
        '''这部分 dict 需要和训练数据顺序对应'''
        dic = {'0': 'nm 评分',
               '1': 'nm 上映时间',
               '2': 'nm 类型',
               '3': 'nm 简介',
               '4': 'nm 演员列表',
               '5': 'nnt 介绍',
               '6': 'nnt ng 电影作品',
               '7': 'nnt 电影作品',
               '8': 'nnt 参演评分 大于 x',
               '9': 'nnt 参演评分 小于 x',
               '10': 'nnt 电影类型',
               '11': 'nnt nnr 合作 电影列表',
               '12': 'nnt 电影数量',
               '13': 'nnt 出生日期',
               }
        with open(self.question_classification_path, 'w') as f:
            json.dump(dic, f, ensure_ascii=False)  # 会在目录下生成一个*.json的文件，文件内容是dict数据转成的json数据  ensure_ascii=False
        print("save question classification success...")

#生成所有训练数据的vocab文件，其中包含了训练数据集中所有出现过的单词。
class GenerVocab():
    '''生成所有训练数据的vocab文件, 使用模型的时候需要. 变更数据的时候需要重新生成.'''
    def __init__(self):
        self.data_path = "./data/"
        self.save_vocab_path = "./model/vocabulary.json"
        if not os.path.isfile(self.save_vocab_path):
            self.save_vocab()

    def cut_word(self, file_path):
        result_list = []
        with open(file_path, "r") as temp_f:
            for sentence in temp_f.readlines():
                sentence = sentence.strip()
                temp = jieba.lcut(sentence)
                result_list += temp
        return result_list

    def get_all_word(self):
        all_word_list = []
        for path in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, path)
            result_word_list = self.cut_word(file_path)
            all_word_list += result_word_list
        all_word_set = set(all_word_list)
        result_dict = {}
        for index, cont in enumerate(all_word_set):
            result_dict[cont] = index
        return result_dict

    def save_vocab(self):
        dic = self.get_all_word()
        with open(self.save_vocab_path, 'w') as f:
            json.dump(dic, f, ensure_ascii=False)  # 会在目录下生成一个*.json的文件，文件内容是dict数据转成的json数据  ensure_ascii=False
        print("save vocab success...")


#
class Trainer(GenerVocab):
    def __init__(self):
        super().__init__()
        self.vocab = self.load_vocab()

    def load_vocab(self):
        with open(self.save_vocab_path, "r", encoding='utf-8') as f:
            vocab = json.loads(f.read())
        return vocab

    def load_data(self):
        X = []
        Y = []
        list_file = os.listdir(self.data_path)
        for file_name in list_file:
            file_path = os.path.join(self.data_path, file_name)
            result = re.match('【[0-9]*】', file_name).span()
            start = result[0]
            end = result[1]
            with open(file_path, 'r', encoding='utf-8')as fread:
                for line in fread:
                    tmp = np.zeros(len(self.vocab))
                    Y.append(file_name[start + 1:end - 1])  # label
                    list_sentence = jieba.lcut(line.rstrip())
                    for word in list_sentence:
                        if word in self.vocab:
                            tmp[int(self.vocab[word])] = 1
                    X.append(tmp)
        return X, Y

    def train(self):
        X, Y = self.load_data()
        clf = GaussianNB().fit(X, Y)
        joblib.dump(clf, 'model/clf.model')


if __name__ == "__main__":
    gqc = GenerQuestionClassification()
    t = Trainer()
    t.train()