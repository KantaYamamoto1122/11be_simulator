import matplotlib.pyplot as plt
import config
import ieee80211
import csv


def ShowDurationThr(simx,simy):

     # figureを生成する
     fig = plt.figure()
     # axをfigureに設定する
     ax = fig.add_subplot(1, 1, 1)
     ax.grid(True)  # grid表示ON
     ax.set_xlim(left=0, right=config.END_TIME/config.USEC)  # x範囲
     ax.set_ylim(bottom=0, top=ieee80211.D_MBPS)  # y範囲
     ax.set_xlabel('Passed time (sec)')  # x軸ラベル
     ax.set_ylabel('Duration throughput (Mbps)')  # y軸ラベル
     #ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
     ax.plot(simx, simy,color = "red")
     plt.draw()
     return ax

def updateimage(simx,simy,ax):
     #ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
     ax.plot(simx, simy,color = "red")
     plt.pause(0.1)
     return ax

def makeimage(simx,simy,ax,imagename):
     #ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
     ax.plot(simx, simy,color = "red")
     plt.savefig(imagename + '.png')

def ShowQvalue(filename):
     
     #   端末の配置が記載されたcsvファイルから位置情報を取得
     csv_file = open(filename,"r", newline="" )
     f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
     array = []
     for row in f:
        array.append(row)
     
     # figureを生成する
     """
     fig = plt.figure()
     # axをfigureに設定する
     ax = fig.add_subplot(1, 1, 1)
     ax.grid(True)  # grid表示ON
     ax.set_xlim(left=0, right=config.END_TIME/config.USEC)  # x範囲
     ax.set_ylim(bottom=0, top=1)  # y範囲
     ax.set_xlabel('Passed time (sec)')  # x軸ラベル
     ax.set_ylabel('q value')  # y軸ラベル
     #ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
     ax.plot(simx, simy,color = "red")
     plt.draw()
     return ax
     """