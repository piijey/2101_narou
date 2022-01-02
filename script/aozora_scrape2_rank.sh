#!/bin/bash

savefilename="aozora_rank_2020_total"
python script/aozora_scrape_rank.py
header=1

tail -n +2 data/${savefilename}2.tsv \
|sed 's/\(.*\)\t\(.*\),\(.*\)\t\(.*\),\(.*\)\t\(.*\)/\1\t\3\t\2\t\4\t\5\t\6/g' \
> data/$savefilename.scrape.tsv
