import myclass

"""
chain
イベントの生成とリストへの追加
"""
def make(NODE, set_time, start_time, app, type, PACKET=None):
    # 新しいイベント生成
    eve = myclass.EVENT()
    eve.node = NODE
    eve.type = type
    eve.start_time = start_time
    eve.set_time = set_time
    if app != None:
        eve.app = app
    if PACKET != None:
        eve.Txpk = PACKET
    return eve


"""
release
イベントリストから外す
"""
def release(EVENT,e_list):
    for i in range(len(e_list)):
        if e_list[i].node.id == EVENT.node.id and e_list[i].start_time == EVENT.start_time and e_list[i].type == EVENT.type:
            del e_list[i]
            break


"""
search_near
最も古いイベントの検索
"""
def search_near(e_list):
    newlist2 = sorted(e_list,key=lambda h: h.start_time) 
    return newlist2[0] 

def search_duplex(e_list):
    for e_i in range(len(e_list)):
        for e_j in range(e_i+1,len(e_list)):
            if e_list[e_j].type == e_list[e_i].type \
                and e_list[e_j].node.id == e_list[e_i].node.id \
                    and e_list[e_j].start_time == e_list[e_i].start_time \
                        and e_list[e_j].set_time == e_list[e_i].set_time:
                            #print("duplex")
                            del e_list[e_j]




