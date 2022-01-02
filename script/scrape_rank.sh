#!/bin/bash

savefilename="rank_total_total"
## ランキングページを取得
curl -fsSL https://yomou.syosetu.com/rank/list/type/total_total/ > data/$savefilename.html


## 必要情報を取り出す
mkdir -p data/tmp
cat data/$savefilename.html \
|grep -e '<span class="ranking_number">.*位</span>' \
|sed -e 's|<span class="ranking_number">||g' -e 's|位</span>||g'\
> data/tmp/$savefilename.rank.txt

cat data/$savefilename.html \
|grep -e '<a class="tl" id="best.*" target="_blank" href="https://ncode.syosetu.com/.*/">.*</a>' \
|sed -e 's|<a class="tl" id="best||g' -e 's|" target="_blank" href="|\t|g' -e 's|">|\t|g' -e 's|</a>||g'\
> data/tmp/$savefilename.title.txt

cat data/$savefilename.html \
|tr "／" "\n" \
|grep -e '作者：' \
|sed -e "s|</a>||g" -e 's|">|\t|g' -e 's|="|\t|g' \
|cut -f 2,3 \
> data/tmp/$savefilename.author.txt


## 必要情報をtsvにまとめる
cut -f 2,3 data/tmp/$savefilename.title.txt \
| paste data/tmp/$savefilename.rank.txt - data/tmp/$savefilename.author.txt \
> data/$savefilename.tsv
rm -rf data/tmp

mkdir -p data/$savefilename
