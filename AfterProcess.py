import joblib
import OutNetworkImage
import numpy as np
import csv
import matplotlib.pyplot as plt
import config

"""
統計処理プログラム
OutFilesフォルダ内の.outファイルから画像と結果出力
"""
def ShowImage(simx,simy):

    # figureを生成する
    fig = plt.figure()
    # axをfigureに設定する
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)  # grid表示ON
    ax.set_xlim(left=min(simx), right=max(simx))  # x範囲
    ax.set_ylim(bottom=0, top=max(simy))  # y範囲
    ax.set_xlabel('Passed time (sec)')  # x軸ラベル
    ax.set_ylabel('Duration throughput (Mbps)')  # y軸ラベル
    #ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
    ax.plot(simx, simy,color = "red")
    plt.show()

filename = "./OutFiles/AllData.out"
Resultlist = joblib.load(filename)
print("Outfile open")
TRACE_START = 5 # トレーススタートタイム (sec)


for result_i in Resultlist:
    time = result_i.Duration 
    throughput = result_i.DurationThr
    CWmin = result_i.DurationMeanCWmin
    trial = len(throughput)
    Throughput_list = []
    CWmin_list = []
    Off_list = []
    for trial_i in range(trial):
        for t_i in range(len(time)):
            #result_csv=[time[t_i],throughput[t_i],CWmin[t_i]]
            #writer.writerow(result_csv)
            if time[t_i] > TRACE_START:
                Throughput_list.append(throughput[trial_i][t_i])
                CWmin_list.append(CWmin[trial_i][t_i])
            timeduration = max(time) - min(time)
        for n_i in result_i.nodelist[trial_i]:
            if n_i.dev_type == "STA":
                Off_list.append(n_i.Statistics.num_gene_pk * 1000 *8 / (timeduration * config.USEC) )

    off = result_i.Off
    AverageThr = sum(Throughput_list)/len(Throughput_list)
    AverageCWmin = sum(CWmin_list)/len(CWmin_list)
    AverageOff = sum(Off_list)/len(Off_list)
    result_csv=[off,AverageOff,AverageThr,AverageCWmin]
    print("Offered load = "+ str(AverageOff) )
    print("Throughput = "+ str(AverageThr) )
    print("cwmin = "+ str(AverageCWmin) )

