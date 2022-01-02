import sys
import time
import urllib.request
from bs4 import BeautifulSoup
import csv

def scrape_rank(ranking_url, savefilename):
    with open(savefilename, "w", encoding="utf-8") as file:
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")

        table = soup.findAll("table", {"class":"list"})[0]
        rows = table.findAll("tr")

        writer = csv.writer(file, delimiter="\t")
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                ctext = cell.get_text().strip()
                if cell.find("a") is not None:
                    ctext = ctext +","+ cell.find("a").get("href")
                csvRow.append(ctext)
            writer.writerow(csvRow)
        

if __name__ == '__main__':
    url = "https://www.aozora.gr.jp/access_ranking/2020_txt.html"
    scrape_rank(url, "data/aozora_rank_2020_total2.tsv")
