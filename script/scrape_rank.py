import sys
import time
import urllib.request
from bs4 import BeautifulSoup
import csv

def scrape_rank(ranking_url, savefilename):
    with open(savefilename, "w", encoding="utf-8") as file:
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")

        table = soup.findAll("table", {"class":"rank_table"})[0]
        rows = table.findAll("tr")

        writer = csv.writer(file)
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            writer.writerow(csvRow)
        

if __name__ == '__main__':
    url = "https://yomou.syosetu.com/rank/list/type/total_total/"
    scrape_rank(url, "data/narou_rank_total_total.tsv")
