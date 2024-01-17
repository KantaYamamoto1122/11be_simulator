import main
import config
import csv
import numpy as np
import os
import OutNetworkImage
import myclass
import joblib

Resultlist = []

if os.path.exists("throughput.csv"):
    os.remove("throughput.csv")

#config.END_TIME  = config.USEC
config.NUM_NODE = 4
HOP = config.NUM_NODE - 1
config.END_TIME  = 10 * config.USEC
config.LOG = 0
config.DEBUG = 0
config.QL = 0
config.PAYLOAD = 700
first = 3.5
dif = 0.1
last = 4.5
sta = config.NUM_NODE - 1

for i in np.arange(first, last, dif):
    config.LOAD= i
    config.LOG = 0
    main.main(Resultlist)

filename = "./OutFiles/Output_"+str(HOP)+"hop_Off"+str(first)+"to"+str(last)+"Mbps_pay"+str(config.PAYLOAD)+"bytes.out"
joblib.dump(Resultlist, filename,compress=3)
OutNetworkImage.MakeThroughputImage(Resultlist)
OutNetworkImage.MakeCollisionImage(Resultlist)
print("Simulation End")