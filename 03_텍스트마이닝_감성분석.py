from bs4 import BeautifulSoup
import urllib.request as req
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

okt = Okt()
tokenizer = Tokenizer(19417, oov_token = 'OOV')
with open('wordIndex.json') as json_file:
  word_index = json.load(json_file)
  tokenizer.word_index = word_index

loaded_model = load_model('best_model.h5')
def sentiment_predict(new_sentence):
    max_len = 30
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    return score

page_num = 1
sentiment_result = {"매우긍정":0, "긍정":0, "중립":0, "부정":0, "매우부정":0}
while True:
    code = req.urlopen("https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}".format(page_num))
    soup = BeautifulSoup(code, "html.parser")
    comment = soup.select("li > div.score_reple > p > span")
    if len(comment) == 0:
        break
    for i in comment:
        i = i.text.strip()
        if i == "관람객":
            continue

        print(i)
        result = sentiment_predict(i)
        # print(result)
        if result >= 0.5:
            print(f"{result * 100:.2f}% 확률로 긍정입니다.")
        else:
            print(f"{100 - result * 100:.2f}% 확률로 부정입니다.")
        print("----------------------------")
        if result >= 0.8:
            sentiment_result["매우긍정"] += 1
        elif 0.6 <= result < 0.8:
            sentiment_result["긍정"] += 1
        elif 0.4 <= result < 0.6:
            sentiment_result["중립"] += 1
        elif 0.2 <= result < 0.4:
            sentiment_result["부정"] += 1
        elif 0 <= result < 0.2:
            sentiment_result["매우부정"] += 1
    if page_num == 3:
        break
    page_num += 1


from pyecharts import Bar3D

bar3d = Bar3D("감성분석 결과", width=1200, height=600)
x_axis = ["매우긍정", "긍정", "중립", "부정", "매우부정"]
y_axis = []
data = [[0, 0, sentiment_result["매우긍정"]], [0, 1, sentiment_result["긍정"]],
        [0, 2, sentiment_result["중립"]], [0, 3, sentiment_result["부정"]],
        [0, 4, sentiment_result["매우부정"]]]
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
bar3d.add("", x_axis, y_axis, [[d[1], d[0], d[2]] for d in data],
    is_visualmap=True, visual_range=[0, 20], visual_range_color=range_color,
    grid3d_width=200, grid3d_depth=40)
bar3d.render("./bar3d.html")

import os
abs_path = os.path.abspath("./bar3d.html") # 해당 파일의 전체 경로를 가져옴.

import webbrowser
# webbrowser.open(abs_path) # 윈도우
webbrowser.open("file://"+abs_path) # 맥