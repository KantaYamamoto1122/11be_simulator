import main
import config
import csv
import numpy as np
import os
import OutNetworkImage
import myclass
import joblib


Resultlist = []
#   結果格納用のフォルダを作成
dirname = "OutFiles"
os.makedirs(dirname,exist_ok=True)

if os.path.exists("throughput.csv"):
    os.remove("throughput.csv")

#config.END_TIME  = config.USEC

config.END_TIME  = 1 * config.USEC
config.NUM_TRIAL = 10
first = 0.5
dif = 0.5
last = 8.0

#端末台数ごとにシミュレーション
for n in np.arange(3,4,1):
    Resultlist = []
    config.NUM_NODE = n
    sta = config.NUM_NODE - 1
    # オファードロードを指定
    for i in np.arange(0.5, 8.0, 0.5):
        config.LOAD= i
        config.LOG = 0
        main.main(Resultlist)
    
    #全ての結果を格納    
    filename = "./"+dirname+"/Output_nSTA="+str(sta)+"_Off"+str(first)+"to"+str(last)+"Mbps.out"
    
    joblib.dump(Resultlist, filename,compress=3)


print("Simulation End")