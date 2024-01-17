import config
import event
import math
import myclass
import func
import random
import ieee80211
import matplotlib.pyplot as plt
import matplotlib.patches as patches
'''
端末配置，アプリケーションの設定
'''
def setting(nodelist):
    AP_id = config.NUM_NODE-1

    for i in range(config.NUM_NODE):
        node = myclass.NODE()
        node.id = i
        # ノードの種類設定
        if i == config.NUM_NODE - 1:
            node.dev_type = "AP"
        else:
            node.dev_type = "STA"

        app = myclass.APPLICATION()
        # ルーティング設定
        app.src_id = i
        app.dst_id = AP_id
        app.next_mac = AP_id
        app.setting(1,config.PAYLOAD)
        node.applist.append(app)
        nodelist.append(node)
    # ノードの配置 (キャプチャエフェクトの確認用
    nodelist[0].x = -5
    nodelist[0].y = 0
    nodelist[1].x = 40
    nodelist[1].y = 0
    nodelist[2].x = 0
    nodelist[2].y = 0


    
    
def first_event(n_list,e_list):
    for node in n_list:
        if node.dev_type == 'STA':
            start_time = 10
            app = random.choice(node.applist)
            eve = event.make(node, 0, start_time,app, "GenePacket")
            e_list.append(eve) 
            


        
                

                    

        


    