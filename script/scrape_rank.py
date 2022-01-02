# from https://karupoimou.hatenablog.com/entry/2019/04/28/064159
# edited by piijey
# python script/scrape.py > test/rank_total_total.html
import requests
from bs4 import BeautifulSoup

# URLの指定
url = "https://yomou.syosetu.com/rank/list/type/total_total/"

#ユーザーエージェントの設定
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}

# URLにアクセスする 戻り値にはアクセスした結果やHTMLなどが入ったinstanceが帰ってきます
response = requests.get(url=url, headers=headers)
html = response.content

# instanceからHTMLを取り出して、BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# CSSセレクターを使って指定した場所のtextを取得
selector = "#main_rank > div.rankmain_box > div.ranking_inbox"

print(soup.select_one(selector))         #html形式
#print(soup.select_one(selector).text)    #Text形式

with open("test/rank_total_total.txt", "w", encoding="utf-8") as f:
    f.write(soup.select_one(selector).text)

#print('end')#終了の表示（消しても別によい）

