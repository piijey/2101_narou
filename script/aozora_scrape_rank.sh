#!/bin/bash

savefilename="aozora_rank_2020_total"
## ランキングページを取得
curl -fsSL https://www.aozora.gr.jp/access_ranking/2020_txt.html > data/$savefilename.html


## 必要情報を取り出す
mkdir -p data/tmp
cat data/$savefilename.html \
|grep -e '<tr valign=top><td class=normal>.*</td>' \
|sed -e 's|<tr valign=top><td class=normal>||g' -e 's|</td>||g'\
> data/tmp/$savefilename.rank.txt

cat data/$savefilename.html \
|grep -e '<td class=normal><a href="https://www.aozora.gr.jp/cards/' \
|sed -e 's|<td class=normal><a href="||g' -e 's|" target=_blank>||g' \
> data/tmp/$savefilename.url.txt

cat data/$savefilename.html \
|grep -e '^.*</a><br>' \
|sed -e 's|</a><br>| |g' -e 's|</td>||g' -e 's| *$||g' \
> data/tmp/$savefilename.title.txt

cat data/$savefilename.html \
|grep -e '<td class=normal><a href="https://www.aozora.gr.jp/index_pages/person' \
|sed -e 's|html">|\t|g' -e 's|</a>|\t|g'\
|cut -f 2 \
> data/tmp/$savefilename.author.txt


## 必要情報をtsvにまとめる
paste data/tmp/$savefilename.rank.txt data/tmp/$savefilename.url.txt data/tmp/$savefilename.title.txt data/tmp/$savefilename.author.txt \
> data/$savefilename.tsv
rm -rf data/tmp

mkdir -p data/$savefilename
