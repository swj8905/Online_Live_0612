from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np  # pip install numpy
from PIL import Image  # pip install pillow
import matplotlib.pyplot as plt # pip install matplotlib

keyword = "사회"
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
output_total = ""
while True:
    url = "https://news.joins.com/Search/JoongangNews?page={}&Keyword={}&SortType=New&SearchCategoryType=JoongangNews".format(page_num, encoded)
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline.mg > a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text)
        print("링크 :", i.attrs["href"])
        code_news = req.urlopen(i.attrs["href"])
        soup_news = BeautifulSoup(code_news, "html.parser")
        content = soup_news.select_one("div#article_body")
        result = content.text.strip().replace("     ", " ").replace("   ", "")
        print(result)
        print()
        output_total += result


    if page_num == 1:
        break
    page_num += 1

print("형태소를 분석 중 입니다...")
okt = Okt()
print("명사만 추출합니다...")
nouns_list = okt.nouns(output_total)
print(nouns_list)
temp = nouns_list.copy()
for i in temp:
    if len(i) == 1:
        nouns_list.remove(i)

print(nouns_list)
# 단어 빈도수 카운트
count = Counter(nouns_list)
print(count)
# 단어구름 만들기
wc = WordCloud(font_path="./NanumMyeongjoBold.ttf",
          background_color="white").generate_from_frequencies(count)
# 단어구름 띄우기
plt.figure(figsize=(10,10)) # 창 띄우기
plt.imshow(wc, interpolation="bilinear") # 창에 이미지 띄우기
plt.axis("off") # 축 나타내는 선 없애기!
plt.show() # 실제로 그 창을 화면에 띄우기!