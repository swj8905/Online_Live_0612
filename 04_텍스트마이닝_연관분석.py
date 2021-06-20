from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

def show_me_the_graph(df):
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    g = nx.Graph()
    g.add_edges_from(df)
    pr = nx.pagerank(g)
    fm._rebuild()
    nsize = np.array([v for v in pr.values()])
    nsize = 10000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))
    pos = nx.kamada_kawai_layout(g)
    font_name = fm.FontProperties(fname="./NanumMyeongjoBold.ttf").get_name()
    plt.figure(figsize=(16, 12))
    plt.axis("off")
    nx.draw_networkx(g, font_family=font_name, font_size=16,
                     pos=pos, node_color=list(pr.values()), edge_color='.5', node_size=nsize,
                     alpha=0.7, cmap=plt.cm.Blues)
    plt.show()

keyword = "사회"
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
output_list = []
while True:
    url = "https://news.joins.com/Search/JoongangNews?page={}&Keyword={}&SortType=New&SearchCategoryType=JoongangNews".format(page_num, encoded)
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline.mg > a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text)
        output_list.append(i.text)

    if page_num == 1:
        break
    page_num += 1

from konlpy.tag import Okt
okt = Okt()
dataset = []
for title in output_list:
    result = okt.nouns(title)
    # 불용어 지우기
    temp = result.copy()
    for i in temp:
        if len(i) == 1:
            result.remove(i)
    dataset.append(result)

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
df_apr = apriori(df, use_colnames=True, min_support=0.01)
df_apr["length"] = df_apr["itemsets"].str.len()
df_apr = df_apr[df_apr["length"]==2]

show_me_the_graph(df_apr["itemsets"])
