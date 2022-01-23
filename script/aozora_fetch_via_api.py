#python script/aozora_fetch_via_api.py data/aozora_rank_2020_total.tsv data/aozora_rank_2020_total
import sys
import re
import time
import requests
from bs4 import BeautifulSoup


def fetch_via_api(book_id, savefilename):
    title = ""
    with open(savefilename, "w", encoding="utf-8") as f:
        res = requests.get("http://pubserver2.herokuapp.com/api/v0.1/books/{}/content?format=html".format(book_id))
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup.find_all(["rt", "rp"]):
            tag.decompose() # ルビを削除
        
        # タイトル取得
        if soup.find("title") is None:
            print("-"*10, book_id, "no title", "-"*10)
            print(soup)
            title = "[None]"
        else:
            title = soup.find("title").get_text()

        # 本文取得
        if soup.find("div","main_text") is None:
            print("-"*10, book_id, "no main_text", "-"*10)
            print(soup)
            return title+"\t[Failed]"
        
        main_text = soup.find("div","main_text").text
        f.write(main_text)

    return title


if __name__ == "__main__":
    fetched_rank_list = []
    try: 
        with open(sys.argv[2]+".fetched.txt", "r") as logfile:
            for line in logfile:
                fetched_rank_list.append(int(line.strip().split("\t")[0]))
    except FileNotFoundError:
        pass
    with open(sys.argv[1], "r") as infile:
        for line in infile:
            book_rank = int(line.strip().split("\t")[0])

            # 取得済みの場合は飛ばす
            if book_rank in fetched_rank_list:
                print(book_rank)
                continue

            book_url = line.strip().split("\t")[1]
            
            book_url_cut = book_url.split("/")[-1]
            m = re.search(r"\d+", book_url_cut)
            book_id = m.group()

            outfilename = sys.argv[2]+"/"+book_id+".txt"

            title = fetch_via_api(book_id, outfilename)
            with open(sys.argv[2]+".fetched.txt", "a") as logfile:
                logfile.write(line.strip()+"\t"+outfilename+"\t"+str(title)+"\n")
            
            print("book_rank {:d} downloaded".format(book_rank))
