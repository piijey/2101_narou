## python script/fetch_novel.py data/rank_total_total.tsv data/rank_total_total
import sys
import time
import urllib.request
from bs4 import BeautifulSoup

def fetch_novel(novel_url, savefilename):
    num_parts = 100000  # ここに作品の全部分数を指定

    with open(savefilename, "w", encoding="utf-8") as f:
        for part in range(1, num_parts+1):
            # 作品本文ページのURL
            url = "{}{:d}/".format(novel_url, part)

            ## ページがなかったら終了
            try: res = urllib.request.urlopen(url)
            except urllib.error.HTTPError:
                return part - 1

            soup = BeautifulSoup(res, "html.parser")

            # CSSセレクタで本文を指定
            honbun = soup.select_one("#novel_honbun").text
            honbun += "\n"  # 次の部分との間は念のため改行しておく
            
            # 保存
            f.write(honbun)
            
            #if part % 50 == 0:
            #    print("part {:d} downloaded".format(part))  # 進捗を表示
            
            time.sleep(0.1)  # 次の部分取得までは0.1秒間の時間を空ける


if __name__ == '__main__':
    with open(sys.argv[1], "r") as infile, open(sys.argv[2]+".fetched.txt", "w") as logfile:
        for line in infile:
            novel_rank = int(line.strip().split("\t")[0])
            novel_url = line.strip().split("\t")[1]
            outfilename = sys.argv[2]+"/"+novel_url.split("/")[-2]+".txt"

            pages = fetch_novel(novel_url, outfilename)
            logfile.write(line.strip()+"\t"+outfilename+"\t"+str(pages)+"\n")
            
            print("novel_rank {:d} downloaded".format(novel_rank))
