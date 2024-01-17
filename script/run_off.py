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
config.NUM_NODE = 
config.END_TIME  = 1 * config.USEC
first = 0.5
dif = 0.5
last = 8.0
sta = config.NUM_NODE - 1

for i in np.arange(0.5, 8.0, 0.5):
    config.LOAD= i
    config.LOG = 0
    main.main(Resultlist)

filename = "Output_nSTA="+str(sta)+"_Off"+str(first)+"to"+str(last)+"Mbps.out"
joblib.dump(Resultlist, filename,compress=3)
OutNetworkImage.MakeThroughputImage(Resultlist)
OutNetworkImage.MakeCollisionImage(Resultlist)
print("Simulation End")