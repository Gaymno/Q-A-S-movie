from MachineLearning.analyze_question import AnalysisQuestion
from KnowledgeGraph.get_answer import Get_answer
from py2neo import *

if __name__ == "__main__":
    aq = AnalysisQuestion()
    ga = Get_answer()
    while True:
        question = input('请输入你想查询的信息：')
        index, params = aq.analysis_question(question)
        print(index, params)
        answers = ga.get_data(index, params)
        print(type(answers))
        print('答案:')
        ls = []
        for ans in answers:
            ls.append(ans[0])
        print(str(ls))