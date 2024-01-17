import joblib
import OutNetworkImage
import numpy as np
import csv

"""
統計処理プログラム
OutFilesフォルダ内の.outファイルから結果出力
"""

first = 0.1
last = 3.0
hop = 3
pay = 400
off_list = []
thr_list = []
filename = "./OutFiles/Output_"+str(hop)+"hop_Off"+str(first)+"to"+str(last)+"Mbps_pay"+str(pay)+"bytes.out"
Resultlist = joblib.load(filename)
out_filename = "./csv/out_throughput_"+str(hop)+"hop_pay"+str(pay)+".csv"

file = open(out_filename, "w", newline="")
writer = csv.writer(file)

for result_i in Resultlist:
    result_csv=[result_i.Off,result_i.Thr[0]]
    writer.writerow(result_csv)
    off_list.append(result_i.Off)
    thr_list.append(result_i.Thr)
    
file.close



print("test")