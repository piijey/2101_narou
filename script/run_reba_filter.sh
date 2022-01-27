
### narou
# python script/reba_filter.py data/rank_total_total.fetched.txt > note/220122_log.note.txt
<<"COMMENT"
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
COMMENT

### aozora
# python script/reba_filter_aozora.py data/aozora_rank_2020_total.fetched.txt > note/220122_log.note.a.txt
echo "\c" > note/aozora_rank_2020_total.reba.tsv
echo "\c" > note/aozora_rank_2020_total.reba.filtered.tsv

IFS=$'\n'
for line in $(cat data/aozora_rank_2020_total.fetched.txt) ; do
    name=$(echo $line |cut -f 5 |cut -d"/" -f 3 |cut -d"." -f 1)
    if [ -e aozora_rank_2020_total.reba/$name.reba ];then
        wc -l aozora_rank_2020_total.reba/$name.reba
        cat aozora_rank_2020_total.reba/$name.reba |sed -e "s|$|\t$line|g" >> note/aozora_rank_2020_total.reba.tsv
        cat aozora_rank_2020_total.reba/$name.reba.filtered |sed -e "s|$|\t$line|g" >> note/aozora_rank_2020_total.reba.filtered.tsv
    else
        break
    fi
done
wc -l note/aozora_rank_2020_total.reba.tsv
wc -l note/aozora_rank_2020_total.reba.filtered.tsv