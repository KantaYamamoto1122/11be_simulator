import config
import event
import math
import numpy as np
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
    for i in range(config.NUM_NODE):
        node = myclass.NODE()
        node.id = i
        # ノードの配置 (Random topology)
        if i == config.NUM_NODE - 1:
            node.x = 0
            node.y = 0
        else:
            r = math.sqrt(2*np.random.uniform(0, 0.5*config.DISTANCE**2))
            theta = np.random.uniform(0,2*np.math.pi)
            node.x = r * math.cos(theta)
            node.y = r * math.sin(theta)

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
        app.setting(config.LOAD/num_sta,config.PAYLOAD)
        node.applist.append(app)
        nodelist.append(node)
    
    
def first_event(n_list,e_list):
    for node in n_list:
        if node.dev_type == 'STA':
            start_time = 10
            app = random.choice(node.applist)
            eve = event.make(node, 0, start_time,app, "GenePacket")
            e_list.append(eve) 
            


        
                

                    

        


    