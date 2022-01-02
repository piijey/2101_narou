#!/bin/bash

<<"COMMENT"
## ランキングページを取得
curl -fsSL https://yomou.syosetu.com/rank/list/type/total_total/ > data/rank_total_total.html

## 必要情報をtsvにまとめる
mkdir -p data/tmp
cat data/rank_total_total.html \
|grep -e '<span class="ranking_number">.*位</span>' \
|sed -e 's|<span class="ranking_number">||g' -e 's|位</span>||g'\
> data/tmp/rank_total_total.rank.txt

cat data/rank_total_total.html \
|tr "／" "\n" \
|grep -e '作者：' \
|sed -e "s|</a>||g" -e 's|">|\t|g' -e 's|="|\t|g' \
|cut -f 2,3 \
> data/tmp/rank_total_total.author.txt

cat data/rank_total_total.html \
|grep -e '<a class="tl" id="best.*" target="_blank" href="https://ncode.syosetu.com/.*/">.*</a>' \
|sed -e 's|<a class="tl" id="best||g' -e 's|" target="_blank" href="|\t|g' -e 's|">|\t|g' -e 's|</a>||g'\
> data/tmp/rank_total_total.title.txt

cut -f 2,3 data/tmp/rank_total_total.title.txt \
| paste data/tmp/rank_total_total.rank.txt - data/tmp/rank_total_total.author.txt \
> data/rank_total_total.tsv
COMMENT
