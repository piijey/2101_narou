import sys
import os
import reba_filter


def main(fetched_list, datadir):
    #print(fetched_list)
    with open(fetched_list, "r") as rf:
        for i, line in enumerate(rf):
            lines = line.strip().split("\t")
            if int(lines[0]) not in range(1,101): #[1,2,3,4,5,108]
                continue
            readfile = lines[4]
            writedir = datadir+".reba"
            os.makedirs(writedir, exist_ok=True)
            writefile = writedir+"/"+lines[4].split("/")[-1].replace(".txt", ".reba")
            reba_filter.get_sentences(readfile, writefile)
            #if i > 10:
            #    break
            #print(lines)

if __name__ == '__main__':
    fetched_list = sys.argv[1]
    main(fetched_list, "aozora_rank_2020_total")

