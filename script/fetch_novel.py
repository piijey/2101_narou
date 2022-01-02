#from https://scol.hatenablog.com/entry/2019/04/04/193000
import time
from urllib import request
from bs4 import BeautifulSoup

num_parts = 478  # ここに作品の全部分数を指定

with open("test/novel.txt", "w", encoding="utf-8") as f:
    for part in range(1, num_parts+1):
        # 作品本文ページのURL
        url = "https://ncode.syosetu.com/n2267be/{:d}/".format(part)

        res = request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")

        # CSSセレクタで本文を指定
        honbun = soup.select_one("#novel_honbun").text
        honbun += "\n"  # 次の部分との間は念のため改行しておく
        
        # 保存
        f.write(honbun)
        
        print("part {:d} downloaded".format(part))  # 進捗を表示

        time.sleep(1)  # 次の部分取得までは1秒間の時間を空ける
