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
    num_sta = config.NUM_NODE-1
    num_hop = config.NUM_NODE-1
    for i in range(config.NUM_NODE):
        node = myclass.NODE()
        node.id = i


        # ノードの配置 (Ring topology)
        if i == config.NUM_NODE - 1:
            node.x = config.DISTANCE * num_hop
            node.y = 0
        else:
            node.x = config.DISTANCE * i
            node.y = 0

        # ノードの種類設定
        if i == config.NUM_NODE - 1:
            node.dev_type = "AP"
        else:
            node.dev_type = "STA"

        app = myclass.APPLICATION()
        
        # ルーティング設定
        app.src_id = 0
        app.dst_id = AP_id
        app.next_mac = i + 1
        app.setting(config.LOAD,config.PAYLOAD)
        node.applist.append(app)
        nodelist.append(node)
    
    
def first_event(n_list,e_list):
    start_time = 10
    app = random.choice(n_list[0].applist)
    eve = event.make(n_list[0], 0, start_time,app, "GenePacket")
    e_list.append(eve) 

            


        
                

                    

        


    