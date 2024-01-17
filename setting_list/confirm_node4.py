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

        """    
        # ノードの配置 (string topology)
        if i == config.NUM_NODE - 1:
            node.x = config.DISTANCE * num_hop
            node.y = 0
        else:
            node.x = config.DISTANCE * i
            node.y = 0
        """

        # ノードの種類設定
        if i == config.NUM_NODE - 1:
            node.dev_type = "AP"
        else:
            node.dev_type = "STA"

        app = myclass.APPLICATION()
        
        # ルーティング設定
        if i == 0:
            app.dst_id = i + 2
        else:
            app.dst_id = i + 1
            
        app.src_id = i
        app.next_mac = i + 1
        app.setting(config.LOAD,config.PAYLOAD)
        node.applist.append(app)
        nodelist.append(node)

    nodelist[0].x = 0
    nodelist[0].y = 0
    nodelist[1].x = config.DISTANCE
    nodelist[1].y = 0

    nodelist[2].x = 2 * config.DISTANCE
    nodelist[2].y = 0
    nodelist[3].x = 3 * config.DISTANCE
    nodelist[3].y = 0

    
    
def first_event(n_list,e_list):
    for node in n_list:
        if node.dev_type == 'STA' and node.id != 1:
            start_time = 10
            app = random.choice(node.applist)
            eve = event.make(node, 0, start_time,app, "GenePacket")
            e_list.append(eve) 

            


        
                

                    

        


    