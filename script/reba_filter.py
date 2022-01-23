import sys
import os
import re
import subprocess
from subprocess import PIPE

class Sentence:
    def __init__(self, sent):
        self.str = sent
    def add_morphemes(self):
        self.morphs = mecab(self.str)
        _wakati = [_m.surface for _m in self.morphs]
        self.wakati = " ".join(_wakati)
        

class Morpheme:
    def __init__(self, line):
        self.surface = line.split("\t")[0]
        self.info = line.split("\t")[1].split(",")    

def mecab(sentence):
    command = "echo "+sentence+" |mecab" 
    proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    ret = proc.stdout
    return [Morpheme(_m) for _m in ret.split("\n") if "\t" in _m]


def reba_in(s):
    if "ば" not in s.str:
        return False
    
    s.add_morphemes()
    for ip, morph in enumerate(s.morphs):
        if (morph.surface == "ば" and morph.info[0] == "助詞" and morph.info[1] == "接続助詞"):
            return True
    return False


def reba_position(s):
    if "ば" not in s.str:
        return False
    pos = []
    s.add_morphemes()
    for ip, morph in enumerate(s.morphs):
        if (morph.surface == "ば" and morph.info[0] == "助詞" and morph.info[1] == "接続助詞"):
            pos.append(ip)
    if pos != 0 and len(pos) > 0:
        return pos
    return False


def reba_class(s, pos):
    # 「ば」の直前は、仮定形の動詞に限定する
    if s.morphs[pos-1].info[0] != "動詞": 
        return " ".join(s.morphs[pos-1].info[:2])
    if s.morphs[pos-1].info[5] != "仮定形":
        return "Err"

    # 「ば」の直後に句点以外の記号（「…」など）があるか、終助詞、「と」がある場合    
    exceptions = ["記号",] ### 「ば」の1個後 part-of-speech-0
    for e in exceptions:
        if s.morphs[pos+1].info[0] == e and (s.morphs[pos+1].surface not in ["、", "，"]):
            return "End:記号"
    
    exceptions = ["終助詞",] ### 「ば」の1個後 part-of-speech-1
    for e in exceptions:
        if s.morphs[pos+1].info[1] == e:
            return "End:終助詞"

    exceptions = [["助詞","格助詞","引用","*","*","*","と","ト","ト"],] ### 「ば」の1個後 part-of-speech-1
    for e in exceptions:
        if s.morphs[pos+1].info == e:
            return "End:と"

    """
    # 「〜ばいい」を除く
    ### 「ば」の1個後 base
    exceptions = [
        "良い",
        "よい",
        "いい",
    ]
    for e in exceptions:
        if s.morphs[pos+1].info[6] == e:
            return "良い"
        if s.morphs[pos+1].info[6] in ["、", "，"] and pos < len(s.morphs) - 2:
            if s.morphs[pos+2].info[6] == e:
                return "良い"
    """

    # 前件に仮定の手がかり表現
    zenken_base = " ".join([_m.info[6] for _m in s.morphs[:pos]])
    tegakari = [
        "さえ",
        "いっそ",
    ]
    for t in tegakari:
        if t in zenken_base:
            return "前件:"+t

    # 後件に仮定の手がかり表現
    kouken_base = " ".join([_m.info[6] for _m in s.morphs[pos:]])
    tegakari = [
        "のに",
        "はず", "筈",
        "違い ない",
        "ところ だ た",
        "かも しれる ない", "かも 知れる ない",
        "です う", "だ う", #"で ある う"
        "まい",
        "きっと", "必ず", 
        "良い", "好い", "善い", "よい", "いい",
    ]
    for t in tegakari:
        if t in kouken_base:
            return "後件:"+t

    ### VればVるほど
    hodo = ["ほど", "程"]
    for h in hodo:
        if s.morphs[pos-1].info[6]+" "+h in kouken_base:
            return "VればVるほど"
    
    ### もいれば・もいる／もあれば・もある
    if pos-2 > -1:
        if s.morphs[pos-1].info[6] in ["いる", "ある"] and s.morphs[pos-2].surface == "も":
            if "も "+s.morphs[pos-1].info[6] in kouken_base:
                return "もいれば・もいる／もあれば・もある"


    ### 「ば」の1個前 surface
    exceptions = [
        "あれ",
        "と なれ", #いざ と なれ, 何 と なれ
        "と すれ", "から すれ",
        "に よれ", "に すれ",
        "できれ", "出来れ",
        "でき て いれ", "出来 て いれ",
        "気付け",
        "気づけ",
        "気がつけ",
        "気 が 付け",
        "比べれ",
        "そう なれ", "そう すれ", 
        "どう すれ", "どう やれ",
        "言い換えれ", 
        "言え", "いえ", "云え",
        #"そう 言え", "そう いえ", "そう 云え", 
        #"どちら か と いえ", "どちら か と 言え", "どちら か と 云え",
        "考え て みれ", "考え て 見れ",
        "思え",
        "考えれ",
        "見れ",
        "聞け",
        "思い返せ",
    ]
    for e in exceptions:
        elen = len(e.split(" "))
        if pos - elen < 0:
            continue
        surs = " ".join([_m.surface for _m in s.morphs[pos-elen:pos]])
        if surs == e:
            return e
    return ""


def ta_in(s, pos):
    ### ta
    for im, _m in enumerate(s.morphs[pos:]):
        if _m.info in[
            ["助動詞","*","*","*","特殊・タ","基本形","だ","ダ","ダ"],
            ["助動詞","*","*","*","特殊・タ","基本形","た","タ","タ"],
        ]:
            if "連用" in s.morphs[pos+im-1].info[5]:
                #print(s.str)
                #print(s.morphs[pos+im-1].surface, s.morphs[pos+im-1].info)
                #print(_m.surface, _m.info)
                #print("")
                return True
    return False


def get_sentences(filename, writefile):
    sentences = []
    with open(filename, "r") as sf:
        for si, sline in enumerate(sf):
            sline = sline.strip()
            if len(sline) < 1:
                continue
            sents_inline = re.split("(?<=[。\n])", sline)
            for sent in sents_inline:
                if len(sent) > 1:
                    sentences.append(sent)

    with open(writefile, "w") as wf, open(writefile+".filtered", "w") as wff:
        count_all = 0
        count_reba = 0
        count_ta = 0
        count_filtered = 0
        count_not_filtered = 0
        for iis, sent in enumerate(sentences):
            s = Sentence(sent)
            if len(s.str) > 0:
                count_all += 1
                reba_poss = reba_position(s)
                if reba_poss is not False:
                    for p in reba_poss:
                        count_reba += 1
                        if ta_in(s, p):
                            count_ta += 1
                            cl = reba_class(s, p)
                            begin = max(0,iis-2)
                            end = min(iis+3, len(sentences)-1)
                            write_list = [str(iis), s.str, " ".join(sentences[begin:end]), str(p), cl]
                            if cl == "":
                                wf.write("\t".join(write_list)+"\n")
                                count_not_filtered += 1
                            else:
                                wff.write("\t".join(write_list)+"\n")
                                count_filtered += 1
            #if count_all > 20000:
            #    break
    print(writefile, count_all, count_reba, count_ta, count_filtered, count_not_filtered, sep="\t")


def main(fetched_list, datadir):
    #print(fetched_list)
    print("writefile", "count_all", "count_reba", "count_ta", "count_filtered", "count_not_filtered", "count_not_filtered/count_reba", sep="\t")
    with open(fetched_list, "r") as rf:
        for i, line in enumerate(rf):
            lines = line.strip().split("\t")
            #if int(lines[0]) not in range(1,11):
            if int(lines[0]) not in [108]:  #debug
                continue
            readfile = lines[5]
            writedir = datadir+".reba"
            os.makedirs(writedir, exist_ok=True)
            writefile = writedir+"/"+lines[5].split("/")[-1].replace(".txt", ".reba")
            get_sentences(readfile, writefile)
            #if i > 10:
            #    break
            #print(lines)
    

if __name__ == '__main__':
    fetched_list = sys.argv[1]
    main(fetched_list, "rank_total_total")
# $ python script/reba_filter.py data/rank_total_total.fetched.txt > test/220122_log.note.txt &
