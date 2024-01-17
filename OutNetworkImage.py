import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ieee80211
import func
import config
import myclass

"""
シミュレーション結果およびネットワークを画像として出力
"""

def imageNetworkTopology(nodelist):
    sta_x=[]
    sta_y=[]
    name = []
    num_hop = config.NUM_NODE-1

    # figureを生成する
    fig = plt.figure()
 
    # axをfigureに設定する
    arrow1=[]
    ax = fig.add_subplot(1, 1, 1)
    
    #  APのラベル
    for node in nodelist:
        if node.dev_type == "AP":
            ap = node
    # STAのラベル
    for node in nodelist:
        if node.dev_type == "STA":
            sta_x.append(node.x)
            sta_y.append(node.y)

            name.append(node.y - 3)

            # 直近の宛先端末へ矢印を描画
            point = {
                'start': [node.x, node.y],
                'end': [nodelist[node.applist[0].next_mac].x, nodelist[node.applist[0].next_mac].y]
            }
            arrow1.append(point)

    csrange = round(func.Calc_CSRange(ieee80211.CS_THRESHOLD))
    
    ax.grid(True)  # grid表示ON
    ax.set_xlim(left=-60, right=num_hop*60)  # x範囲
    ax.set_ylim(bottom=-60, top=60)  # y範囲
    ax.set_xlabel('X')  # x軸ラベル
    ax.set_ylabel('Y')  # y軸ラベル
    title = 'Network Topology'
    ax.set_title(title)  # グラフタイトル
    ax.legend(['AP', 'STA'])  # 凡例を表示
    ax.scatter(ap.x, ap.y,s=150, alpha=0.5, linewidths=2,edgecolors='r',c='#FFaaaa', marker='^',label='AP')
    ax.scatter(sta_x, sta_y,s=150, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='STA')
    #ax.scatter(sta_x, name, s=150, linewidths=1, c='k', marker='$STA$')
    #ax.scatter(ap.x, ap.y-3, s=150, linewidths=1, c='k', marker='$AP$')

    for i in range(len(arrow1)):
        ax.annotate('', xy=arrow1[i]['end'], xytext=arrow1[i]['start'],
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3',
                                facecolor='k', edgecolor='k')
        )
    
    for node in nodelist:
        c = patches.Circle(xy=(node.x, node.y), radius=csrange,fill=False, ec='r',linestyle="--")
        ax.add_patch(c)
    plt.legend()  
    #plt.show()
   
    imagename = "./image/NetworkTopology_"+str(config.NUM_NODE-1)+"hop_network"
    plt.savefig(imagename + '.png')

#
#   スループットの結果を図として作成
#
def MakeThroughputImage(simresult):
    simx=[]
    simy=[]
     # figureを生成する
    fig = plt.figure()
 
    # axをfigureに設定する
    ax = fig.add_subplot(1, 1, 1)
    for result in simresult:
        simx.append(result.Off)
        simy.append(result.AveThr)
    ax.grid(True)  # grid表示ON
    ax.set_xlim(left=0, right=max(simx))  # x範囲
    ax.set_ylim(bottom=0, top=max(simx))  # y範囲
    ax.set_xlabel('Offered load (Mbps)')  # x軸ラベル
    ax.set_ylabel('Throughput (Mbps)')  # y軸ラベル
    title = 'Multi-hop network'
    ax.set_title(title)  # グラフタイトル
    ax.legend(['Simulation'])  # 凡例を表示
    ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
    plt.legend()  
    #plt.show()
    imagename = "./image/result_Off-Thr_"+str(config.NUM_NODE-1) + "hop" 
    plt.savefig(imagename + '.png')


#
#   衝突率の結果を図として作成
#
def MakeCollisionImage(simresult):
    simx=[]
    simy=[]
     # figureを生成する
    fig = plt.figure()
 
    # axをfigureに設定する
    ax = fig.add_subplot(1, 1, 1)
    for result in simresult:
        simx.append(result.Off)
        simy.append(result.AveCol)
    ax.grid(True)  # grid表示ON
    ax.set_xlim(left=0, right=max(simx))  # x範囲
    ax.set_ylim(bottom=0, top=max(simy)+0.1)  # y範囲
    ax.set_xlabel('Offered load (Mbps)')  # x軸ラベル
    ax.set_ylabel('Collision probability')  # y軸ラベル
    title = 'Multi-hop network'
    ax.set_title(title)  # グラフタイトル
    ax.legend(['Simulation'])  # 凡例を表示
    ax.scatter(simx, simy,s=50, alpha=0.5, linewidths=2, c='#aaaaFF', edgecolors='b', marker='o', label='Simulation')
    plt.legend()  
    #plt.show()
    imagename = "./image/result_Off-Collision_"+str(config.NUM_NODE-1) + "hop" 
    plt.savefig(imagename + '.png')

