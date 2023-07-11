import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from matplotlib import colors
import os

class Word_Cloud(object):
    def run(self):
        f = open(r'D:/Dataspace/mysql/Uploads/text.txt',"r",encoding="utf-8")
        text = f.read()
        f.close()
        words_list_jieba = jieba.lcut(text)

        def findifhave(demo,stop):
            for ret in stop:
                if(demo == ret):
                    return 'T'


        stop = ['\n']
        with open("comments/stop.txt",'r',encoding='utf-8') as f1:
            for line in f1:
                stop.append(line.replace("\n",""))
        f1.close()

        dict = {}
        for key in words_list_jieba:
            dict[key] = dict.get(key,0) + 1
            
        for demo in list(dict.keys()):
            if('T' == findifhave(demo,stop)):
                del dict[demo]

        dict1 = sorted(dict.items(),key = lambda d:d[1] , reverse = True)
        print(dict1)


        background_image = np.array(Image.open('comments/cloud_bg.png'))
        colormaps = colors.ListedColormap(['#871A84', '#BC0F6A', '#BC0F60', '#CC5F6A', '#AC1F4A'])
        wordcloud = WordCloud(font_path='comments/STCAIYUN.TTF',  # 字体
                                prefer_horizontal=0.99,
                                background_color='white',  # 背景色
                                max_words=30,  # 显示单词数
                                max_font_size=400,  # 最大字号
                                stopwords=stop,  # 过滤噪声词
                                mask=background_image,  # 背景轮廓
                                colormap=colormaps,  # 使用自定义颜色
                                collocations=False
                                ).fit_words(dict)
        image = wordcloud.to_image()
        image.show()  # 展示图片
        wordcloud.to_file('G:/chatbot/chatbot-master/static/images/wc.png')  # 保存图片

        os.remove('D:/Dataspace/mysql/Uploads/text.txt')

if __name__ == "__main__":
    wc = Word_Cloud()
    wc.run()