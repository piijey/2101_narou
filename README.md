# 2101_narou
なろう小説と青空文庫をスクレイピングして、コーパスとして使う

# なろう小説をスクレイピング
人気の小説300作品を使う
## 累計ランキングBEST300から、作品URLを取得する
- 累計ランキングのページ 👉 [小説を読もう！ || 小説ランキング[累計]](https://yomou.syosetu.com/rank/list/type/total_total/)
- 📚 [Pythonスクレイピングを使って『小説家になろう』のランキングからテキストデータを取得するサンプルコード - なろう分析記録](https://karupoimou.hatenablog.com/entry/2019/04/28/064159)
- 順位、作品URL、タイトル、作者URL、作者名 を取り出す（泥臭いスクリプト）👉 `script/scrape_rank.sh` 
    ```
    # data/rank_total_total.tsv
    1	https://ncode.syosetu.com/n6316bn/	転生したらスライムだった件	https://mypage.syosetu.com/311735/	伏瀬
    2	https://ncode.syosetu.com/n9669bk/	無職転生　- 異世界行ったら本気だす -	https://mypage.syosetu.com/288399/	理不尽な孫の手
    ...
    ```


## 小説本文を取得する
- 📚 [Pythonによるスクレイピングで『小説家になろう』から小説本文を取得する - スコルの知恵袋](https://scol.hatenablog.com/entry/2019/04/04/193000)
- 📚 [urllib パッケージを使ってインターネット上のリソースを取得するには — Python 3.10.0b2 ドキュメント](https://docs.python.org/ja/3/howto/urllib2.html)
- 作品の全部分数数がパッとわからないので、1ページから順に開いていって、ページがなかったら終わりにする
- Python コード `script/fetch_novel.py` 引数は、ランキング一覧 `data/rank_total_total.tsv` と、保存先ディレクトリ `data/rank_total_total`
- 半日ぐらいかけて300作品を取得する感じですな。もっと速くしてもよかったんちゃうか？

<!-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -->
# 青空文庫をスクレイピング
人気の小説300作品を使う


## 2020年ランキングから、作品カードURLを取得する
- [テキスト版 アクセスランキング (2020.01.01 - 2020.12.31)](https://www.aozora.gr.jp/access_ranking/2020_txt.html)
- 作品名にはられているリンクが、作品カードのURL
- 順位、作品カードURL、タイトル、作者名 を取り出す（泥臭いスクリプト）👉 `script/aozora_scrape_rank.sh`
    ```
    1	https://www.aozora.gr.jp/cards/000148/card773.html	こころ	夏目 漱石
    2	https://www.aozora.gr.jp/cards/000035/card301.html	人間失格	太宰 治
    ```

### 上記と同じようなことを BeautifulSoup を使ってシュッとやる
- 📚 [Beautiful Soupでテーブル(表)操作いろいろ | ハイパー猫背](https://creepfablic.site/2020/12/09/python-beautiful-soup-table/#index_id3)
- 📚 [逆引きUNIXコマンド/sedで列の順序を入れ替える方法 - Linuxと過ごす](https://linux.just4fun.biz/?逆引きUNIXコマンド/sedで列の順序を入れ替える方法)
- 📚 [【Python】BeautifulSoupを使ってテーブルをスクレイピング - Qiita](https://qiita.com/hujuu/items/b0339404b8b0460087f9)
- 順位、作品カードURL、タイトル、作者名、作家別作品リスト、アクセス数 を取り出す 👉 `script/aozora_scrape2_rank.sh` & `script/aozora_scrape2_rank.py`
    ```
    1	https://www.aozora.gr.jp/cards/000148/card773.html	こころ	夏目 漱石	https://www.aozora.gr.jp/index_pages/person148.html	63939
    2	https://www.aozora.gr.jp/cards/000035/card301.html	人間失格	太宰 治	https://www.aozora.gr.jp/index_pages/person35.html	53013
    ```

## 小説本文を取得する
- 作品カードURLで `cardxxxx.html` となっている `xxx` が作品ナンバー（`https://www.aozora.gr.jp/cards/000148/card773.html` であれば、No. 773）。この作品ナンバーを使ってAPIを叩く。
- 📚 [【2020年版】青空文庫から本文をスクレイピングして加工する - Qiita](https://qiita.com/silloi/items/73e51b480645a9ee6cfe)
- Python コード `script/aozora_fetch_via_api.py` 引数は、ランキング一覧 `data/aozora_rank_2020_total.tsv` と、保存先ディレクトリ `data/aozora_rank_2020_total`
- うまくいかなかった分
    ```
    162	https://www.aozora.gr.jp/cards/000182/card946.html	善の研究	西田 幾多郎	data/aozora_rank_2020_total/946.txt	『善の研究』・第一編	[Failed]
    ```
- そういえば、古文は除いたほうがよさそうだよなあ…
