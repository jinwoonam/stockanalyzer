import urllib.request
import csv
import time
from bs4 import BeautifulSoup
import sys

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_stock_info(code, info):
    url_base="http://finance.naver.com/item/main.nhn?code=" + code
    #print(url_base)
    req = urllib.request.Request(url_base);
    data = urllib.request.urlopen(req).read()

    bs = BeautifulSoup(data, 'html.parser')
    #print(bs.prettify())

    invest = bs.find(id="tab_con1")
    #print(invest.prettify())

    for em in invest.find_all('em'):
        #print(em.string.strip())
        str = em.string.strip()
        #print(str)
        info.append(str)

    try:
        if (is_float(info[16]) and is_float(info[25])):
            ratio = float(row[16]) * 100 / float(row[25])  # PER(WISEfn) / 동일업종 PER
            info.append("%.2f%%" % ratio)
        else:
            info.append("N/A")
    except:
        info.append("exception")

    #for each in stock
    #print(info)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

####

#parameter = sys.argv[0].split('.')
if len(sys.argv) == 1:          # 옵션 없으면 도움말 출력하고 종료
    print("use test.csv")
    input_flename = 'test1.csv'
    exit()
else:
    sys.argv[1]
    #input_flename = sys.argv[1].split('.')[0]
    input_flename = sys.argv[1]
    print("using ", sys.argv[1])

# Read csv file
#input_flename = "test.csv"
#input_flename = "kospi.csv"
try:
    linelen = file_len(input_flename)
except:
    print(input_flename + " have problem")
    exit()

f = open(input_flename, 'r')

try:
    reader = csv.reader(f)

    # open output csv file
    today = time.strftime("(%y%m%d_%H%M)")
    #today = "" # testing
    output_filename = "stock" + today + ".csv"
    # print(output_filename)

    header = ["회사명", "종목명", "시가총액", "시가총액순위", "상장주식수", "액면가", "매매단위", "주총일",
        "전자투표전자투표", "외국인한도주식수(A)", "외국인보유주식수(B)", "외국인소진율(B/A)", "투자의견",
        "목표주가", "52주최고", "52주최저", "PER(WISEfn)", "EPS(WISEfn)", "PER(KRX)", "EPS(KRX)", "추정PER",
        "EPS", "PBR(WISEfn)", "BPS(WISEfn)", "배당수익률", "동일업종 PER", "동일업종 등락률", "업종PER비율"]

    with open(output_filename, 'wt', newline="\n") as fout:
        csvout = csv.writer(fout)
        csvout.writerow(header)

        # write start time
        csvout.writerow(["start", time.strftime("%y/%m/%d_%H:%M:%S") ])
        csvout.writerow(["weekday", time.strftime("%A")])

        for row in reader:
            print("handling " + str(reader.line_num) +  " of " + str(linelen) + " : " + row[1])
            if (is_int(row[1])):  # stock code
                #print(row[1])
                get_stock_info(row[1], row)
                csvout.writerow(row)
            #elif (row[0] == "title"):    # title
            #    csvout.writerow(row)
            else:
                csvout.writerow(row)

        # write end time
        csvout.writerow(["end", time.strftime("%y/%m/%d_%H:%M:%S")])

finally:
    print("\nAll done.\nCheck " + output_filename)
    f.close()


stock_info = []
#get_stock_info("004090", stock_info)
#print(stock_info)

# 상장종목 리스트 가져오기
# http://bigdatapy.tistory.com/141