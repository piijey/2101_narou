
### narou
# python script/reba_filter.py data/rank_total_total.fetched.txt > note/220122_log.note.txt

echo "\c" > note/rank_total_total.reba.tsv
echo "\c" > note/rank_total_total.reba.filtered.tsv

IFS=$'\n'
for line in $(cat data/rank_total_total.fetched.txt) ; do
    name=$(echo $line |cut -f 6 |cut -d"/" -f 3 |cut -d"." -f 1)
    if [ -e rank_total_total.reba/$name.reba ];then
        wc -l rank_total_total.reba/$name.reba
        cat rank_total_total.reba/$name.reba |sed -e "s|$|\t$line|g" >> note/rank_total_total.reba.tsv
        cat rank_total_total.reba/$name.reba.filtered |sed -e "s|$|\t$line|g" >> note/rank_total_total.reba.filtered.tsv
    else
        break
    fi
done
wc -l note/rank_total_total.reba.tsv
wc -l note/rank_total_total.reba.filtered.tsv

### aozora
# python script/reba_filter_aozora.py data/aozora_rank_2020_total.fetched.txt > note/220122_log.note.a.txt
