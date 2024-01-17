from Qlearning.qlearning_agent import QLearningAgent
import Qlearning.qlearning_act as Qact

from config import USEC
import ieee80211
import math
import config
import numpy as np

"""
クラスの設定
"""

#   デバイス(端末)の種類
Devicetype = {
    "AP": 0,
    "STA": 1,
}

#   端末の状態を定義
Statetype = {
    "IDLE": 0,
    "BACKOFF": 1,
    "Tx": 2,
    "Rx": 3,
    "WAIT": 4,
    "CS":   5
}

#   パケット(フレーム)の種類
Packettype = {
    "RTS": 1,
    "CTS": 2,
    "DAT": 3,
    "ACK": 4,
    "BT": 5     # Busytone信号
}

#   イベントの種類
Eventtype = {"GenePacket": 0,
            "Backoff": 1,
            "TxStart": 2,
            "TxEnd": 3,
            "CountBackoff": 4,
            "noACKRx": 5,
            "RelayPacket": 6
            }

#   イベントクラスの定義
class EVENT:
    def __init__(self):
        self.node = NODE()
        self.app = APPLICATION()
        self.no = None
        self.start_time = 0
        self.set_time = None
        self.type = None
        self.Txpk = None
        self.col_flag = 0        

#   ノードクラスの定義
class NODE:
    def __init__(self):
        self.CS_THRESHOLD = ieee80211.CS_THRESHOLD
        self.RxSucFlag = 0
        self.AckRxSucFlag = 0
        self.CSFlag = 0
        self.CSPreFlag = 0
        self.CheckSINRFlag = 0
        self.NAVflag = 0
        self.EIFSFlag = 0
        self.CollisionFlag = 0
        self.PkGoalFlag = 0

        self.id = None
        self.x = None
        self.y = None

        self.dev_type = Devicetype
        self.state = Statetype
        self.state = "IDLE"
        self.applist = []
        self.Txpk = []
        self.Rxpk = []
        self.buffer = []
        self.dcf = ieee80211.DCF()
        self.Statistics = Statistics()
        self.agent = agent = QLearningAgent()
        self.agent.CW = 16
        self.agent.CW_log .append(self.agent.CW)
        self.agent.reward_history.append(0)

    #   SINRの計算用関数
    def calcSINR(self):
        for j in range(len(self.Rxpk)):
            input = 0
            all = 0
            for k in range(len(self.Rxpk)):
                if k == j:
                    input += self.Rxpk[k].recv_signal_mw
                else:
                    all += self.Rxpk[k].recv_signal_mw
            all += pow(10, ieee80211.NOISE_LEVEL / 10)
            self.Rxpk[j].SINR = 10 * math.log10(input / all)

    #   送信パケット(DAT)の設定用関数
    def SetTxPk(self,type,app,now,pk_id):
        TxPacket = PACKET(type)
        TxPacket.id = pk_id
        # MACアドレスの設定
        TxPacket.src_mac = self.id
        TxPacket.dst_mac = app.next_mac
        # IPアドレスの設定
        TxPacket.src_id = app.src_id
        TxPacket.dst_id = app.dst_id
        TxPacket.app = app
        TxPacket.CalcTxDuration()
        TxPacket.TxStartTime = now + ieee80211.SIFSTIME
        TxPacket.TxEndTime = TxPacket.TxStartTime + TxPacket.TxDuration
        self.Txpk.append(TxPacket)
        return TxPacket
    
    #   送信フレーム(ACK,RTS,CTS)の設定用関数
    def SetTxFr(self,type,dst_id,now):
        TxFrame = PACKET(type)
        TxFrame.src_mac = self.id
        TxFrame.dst_mac = dst_id
        TxFrame.CalcTxDuration()
        TxFrame.TxStartTime = now + ieee80211.SIFSTIME
        TxFrame.TxEndTime = TxFrame.TxStartTime + TxFrame.TxDuration
        self.Txpk.append(TxFrame)
        return TxFrame

    #####################
    #
    #   Q学習関連関数
    #
    #####################
    # 報酬の計算
    def CalcReward(self,txpk):
        TxDurationSlot = int(txpk.TxDuration/ieee80211.SLOTTIME)
        #reward = Qact.calc_reward(self.agent.TotalBackoffOneTx,self.dcf.num_retx,TxDurationSlot,self.agent.TotalFreezeTimer)
        reward = Qact.calc_reward(self.dcf.num_retx,min(self.agent.CW_list),self.agent.CW_list,self.dcf.CWmin)
        #reward2 = 0#Qact.calc_reward_cwmax(self.dcf.num_retx,min(self.agent.CW_list),self.agent.CW_list,self.dcf.CW)
        self.agent.observe(reward,self.dcf.CWmin)
        self.agent.TotalBackoffOneTx = 0
        self.agent.TotalFreezeTimer = 0
        next_cw = self.agent.act()
        #next_cwmax = self.agent.act_CWmaxSelect()
        self.dcf.CWmin = next_cw
        #self.dcf.CWmax = max(next_cwmax,ieee80211.CWMIN)

        #Qact.reset(self.agent)

    # 報酬計算用のデータ収集動作
    def CollectRxPacket(self,n_list):
        for pk in self.Rxpk:
            if pk.type == "DAT" and pk.SINR > ieee80211.SINR_THRESHOLD:
                self.agent.num_rx_episode += 1
                if pk.src_id in self.agent.num_rx_sta:
                    pass
                else:
                    if pk.src_id != self.id:
                        self.agent.num_rx_sta.append(pk.src_id)

        


class APPLICATION:
    def __init__(self):
        self.id = None
        self.dst_id = None
        self.src_id = None
        self.next_mac = None
        self.pay = None
        self.offeredload = None
        self.PkArriveRate = None
        self.interval = None
        self.AverageE2EDelay = None
        self.now_seq = None

    def setting(self,load,pay):
        self.pay = pay
        self.offeredload = load
        self.PkArriveRate = float(load / (pay * 8))

class PACKET:
    def __init__(self,type):
        self.id = 0
        self.type = type
        self.app = APPLICATION()
        self.rate = None
        self.recv_signal = 0
        self.recv_signal_mw = 0
        self.SINR = 0
        self.TxStartTime = 0
        self.TxEndTime = 0
        self.TxDuration = 0
        self.src_id = 0
        self.dst_id = 0
        self.src_mac = 0
        self.dst_mac = 0
        self.col_flag = 0
        self.FlagFail = 0
    
    def CalcTxDuration(self):
        size = self.app.pay
        if self.type == "RTS":
            self.rate = ieee80211.MCS[1]
            self.TxDuration = ieee80211.RTS_TXTIME
            self.NAV = self.TxDuration + ieee80211.MACHEADER_RXTIME + math.ceil(
                (size * 8 + ieee80211.FCS + ieee80211.TAIL) / (self.rate * 4)) * 4 + ieee80211.CTS_TXTIME + ieee80211.SIFSTIME * 2
        elif self.type == "CTS":
            self.rate = ieee80211.MCS[1]
            self.TxDuration = ieee80211.CTS_TXTIME
            self.NAV = self.TxDuration + ieee80211.MACHEADER_RXTIME + math.ceil(
                (size * 8 + ieee80211.FCS + ieee80211.TAIL) / (self.rate * 4)) * 4 + ieee80211.SIFSTIME
        elif self.type == "DAT":
            self.rate = ieee80211.MCS[2]
            self.TxDuration = ieee80211.MACHEADER_RXTIME + math.ceil((size * 8 + ieee80211.FCS + ieee80211.TAIL) / (self.rate * 4)) * 4
        elif self.type == "ACK":
            self.rate = ieee80211.MCS[1]
            self.TxDuration = ieee80211.PREAMBLE_LENGTH + (
                    ieee80211.PLCP_HEADER_SIG + math.ceil((ieee80211.PLCP_HEADER_SER + 80 + ieee80211.FCS) / ieee80211.OFDM_SYMBOL_B)) * 4
            self.NAV = self.TxDuration
        else:
            print("パケットタイプが定義されていません")


class Statistics:
    def __init__(self):
        self.num_Col = 0
        self.num_Drop = 0
        self.num_RrsTx = 0
        self.num_gene_pk = 0
        self.num_RxSuc_pk = 0
        self.num_RxSucIP_pk = 0
        self.num_rpk_training = 0
        self.now_seq_rx_no = np.repeat(0, config.NUM_NODE-1)
        self.num_TxDatPk = 0
        self.num_Tx = 0
        self.num_TxSuc_pk = 0
        self.num_RxSuc_pk_list = []

class Result:
    def __init__(self):
        self.Off = 0
        self.pay = 0
        self.Thr = []
        self.Col = []
        self.nodelist = []
        self.node_alltime_list = []
        self.AveThr = 0
        self.AveCol = 0
        self.Duration = []
        self.DurationThr = []
        self.DurationMeanCWmin = []

    def CalcResult(self):
        All_nlist = self.nodelist
        sumThr = 0
        sumPrCol = 0
        trial = len(All_nlist)
        for n_list in All_nlist:
            self.Thr.append(n_list[config.NUM_NODE-1].Statistics.num_RxSuc_pk * config.PAYLOAD * 8 / (config.END_TIME-config.START_TIME)) 
            P_col = 0
            j = 0
            for node in n_list:
                if node.Statistics.num_TxDatPk != 0:
                    P_col += node.Statistics.num_Col/node.Statistics.num_TxDatPk
                j +=1
        self.Col.append(P_col/j)
        
        self.AveThr =  sum(self.Thr)/len(self.Thr)
        self.AveCol =  sum(self.Col)/len(self.Col)