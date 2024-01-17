import main
import config
import csv
import numpy as np
import os
import OutNetworkImage
import myclass
import sys
import joblib
import ieee80211

args = sys.argv

Resultlist = []

if os.path.exists("throughput.csv"):
    os.remove("throughput.csv")


config.NUM_NODE = 9
STA = config.NUM_NODE - 1
config.START_TIME = 0 * config.USEC
config.END_TIME = 1 * config.USEC
config.NUM_TRIAL = 1
config.LOG = 0
config.DEBUG = 0
config.Q_LOG = 0
config.QL = 0
config.PAYLOAD = 1000
config.DISTANCE = 10
config.PRINT = 0
first = 14.0
dif = 0.2
last = 14.2
sta = config.NUM_NODE - 1
pay = config.PAYLOAD

if len(args) > 1:
    ieee80211.CWMIN = int(args[1])
    STA = int(args[2]) 
    config.NUM_NODE = STA + 1


print("Simulation STA_"+str(STA)+" network "+str(pay)+"bytes")

for i in np.arange(first, last, dif):
    config.LOAD = i
    config.LOG = 0
    main.main(Resultlist)
filename = "./OutFiles/AllData.out"
joblib.dump(Resultlist, filename, compress=3)
print("Simulation End")

