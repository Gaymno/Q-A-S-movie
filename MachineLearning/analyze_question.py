import json
import joblib
import numpy as np
import jieba.posseg as pseg

class AnalysisQuestion():
    def __init__(self):
        self.vocab_path = './MachineLearning/model/vocabulary.json'
        self.model_path = './MachineLearning/model/clf.model'
        self.question_classification_path = './MachineLearning/model/question_classification.json'
        self.vocab = self.load_vocab()
        self.question_class = self.load_question_classification()

    def load_vocab(self):
        with open(self.vocab_path, "r", encoding='utf-8') as f:
            vocab = json.loads(f.read())
        return vocab

    def load_question_classification(self):
        with open(self.question_classification_path, "r", encoding='utf-8') as f:
            question_classification = json.loads(f.read())
        return question_classification

    def abstract_question(self, question):
        """
        使用jieba进行分词，将关键词进行词性抽象
        :param question:
        :RETURN:
        """
        
        self.abstractMap = {}
        list_word = pseg.lcut(question)  # 中文分词
        print(question)
        abstractQuery = ''
        nr_count = 0
        for item in list_word:
            word = item.word
            print("word=" + word)
            pos = str(item)
            print(pos)
            if 'nm' in pos:  # 电影名
                abstractQuery += "nm "
                self.abstractMap['nm'] = word
                print(self.abstractMap)
                print("1")
            elif 'nr' in pos and nr_count == 0:
                abstractQuery += 'nnt '
                self.abstractMap['nnt'] = word
                nr_count += 1
                print(self.abstractMap)
                print("2")
            elif 'nr' in pos and nr_count == 1:  # nr再一次出现，改成nnr
                abstractQuery += "nnr "
                self.abstractMap['nnr'] = word
                nr_count += 1
                print(self.abstractMap)
                print("3")
            elif 'x' in pos:
                abstractQuery += "x "
                self.abstractMap['x'] = word
                print(self.abstractMap)
                print("4")
            else:
                abstractQuery += word + " "
                print(self.abstractMap)
                print("5")
        return abstractQuery

    def query_classify(self, sentence):
        """
        获取模板索引
        :param sentence:
        :RETURN:
        """
        tmp = np.zeros(len(self.vocab))
        list_sentence = sentence.split(' ')
        for word in list_sentence:
            if word in self.vocab:
                tmp[int(self.vocab[word])] = 1
        clf = joblib.load(self.model_path)
        index = clf.predict(np.expand_dims(tmp, 0))[0]
        return int(index), self.question_class[index]

    def query_extention(self, temp):
        """
        模板中的实体值
        :param sentence:
        :RETURN:
        """
        params = []
        print("abstractMap=" + str(self.abstractMap))
        for abs_key in self.abstractMap:
            if abs_key in temp:
                params.append(self.abstractMap[abs_key])
        return params

    def analysis_question(self, question):
        print('原始句子：{}'.format(question))
        abstr = self.abstract_question(question)
        print('句子抽象化结果：{}'.format(abstr))
        index, strpatt = self.query_classify(abstr)
        print('句子对应的索引{}\t模板：{}'.format(index, strpatt))
        finalpatt = self.query_extention(strpatt)
        return index, finalpatt


if __name__ == "__main__":
    aq = AnalysisQuestion()
    question = input('请输入你想查询的信息：')
    index, params = aq.analysis_question(question)
    print(index, params)