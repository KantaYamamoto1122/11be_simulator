import random
#import env
import copy
import ieee80211
import numpy as np

'''
選択した行動に対してCWの値を設定する
'''
"""
def calc_reward(NumBackoffTimer,num_retx,TxDurationSlot,TotalFreeze):
    total =  TotalFreeze * TxDurationSlot + NumBackoffTimer + 1
    # 遠慮率
    alpha =  ( TotalFreeze * TxDurationSlot ) / total

    reward =  1 /((num_retx+1))
    return reward
"""
def calc_reward(num_retx,cw_c,list,selct_cwmin):
    for cw_i in range(len(list)):
        if list[cw_i] == selct_cwmin:
            break
    
    cw_list = np.array(list)
    binary_list = cw_c/cw_list

    nomalized_binary_list = binary_list/max(binary_list)

    if num_retx > 0:
        basic_reward = -1
    else:
        basic_reward =  1

    reward = basic_reward * min(list) / selct_cwmin
    return reward

def calc_reward_cwmax(num_retx,cw_c,list,selct_cwmin):
    for cw_i in range(len(list)):
        if list[cw_i] == selct_cwmin:
            break
    index = min(cw_i + num_retx,len(list)-1)
    cw_list = np.array(list)
    binary_list = cw_c/cw_list
    nomalized_binary_list = binary_list/max(binary_list)
    reward = nomalized_binary_list[index]
    return reward
    


def reset(agent):
    agent.CW = copy.deepcopy(agent.ini_state)
    agent.CW_number = 0
    agent.num_tx_episode = 0  # エピソード中の送信回数
    agent.num_suc_tx_episode = 0  # エピソード中の送信成功回数
    agent.num_rx_episode = 0  # エピソード中の受信回数
    agent.num_rx_sta = []  # エピソード中に受信した周囲の端末の端末
    agent.col_flag = False
    agent.total_count = 0
    return 0
