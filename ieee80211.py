import math
import random

# 2021.11.30 コメント追加
"""
IEEE 802.11 関連のPHYおよびMACの設定
"""

#device setting 
DEFAULT_TXPOWER = 16.02    #送信電力(mw)

#pass loss model
PATH_LOSS_REF_DISTANCE = 46.667     #
TRANSFER_COEFFICIENT = 3.0          #
SINR_THRESHOLD = 10                 #受信成功SN比
CS_THRESHOLD = -82                  #CS閾値
ENERGY_THRESHOLD = -82              # 最低受信強度
NOISE_LEVEL = -130                  #ノイズ強度(dbm)
FREQENCY = 5 * pow(10, 9)
ATTENUATION_COEFFICIENT = 2         #損失係数

# IEEE 802.11
# PHY layer parameter  
MCS = [6,12,18,24,36,48,54]
minRxMCS = [-82,-82,-81,-79,-77,-74,-74,-70,-66,-65]

#   伝送速度の設定
D_MBPS = MCS[2]     #   データフレーム
C_MBPS = MCS[0]     #   制御フレーム(RTS/CTS)
B_MBPS = MCS[1]     #   ACKフレーム

#   
PREAMBLE_LENGTH = 16   
PLCP_HEADER_SIG = 1     
PLCP_HEADER_SER = 2 * 8
PHY_HEADER = 16
MAC_HEADER = 24 * 8
LLC_HEADER = 8 * 8

# MAC layer parameter
SLOTTIME = 9
SIFSTIME = 16
DIFSTIME = 34
CWMIN = 16
CWMAX = 1024
MAX_RETX = 7

RTS_LENGTH = 160
CTS_LENGTH = 112
FCS = 4 * 8
TAIL = 6

OFDM_SYMBOL_D = D_MBPS * 4
OFDM_SYMBOL_B = B_MBPS * 4

MACHEADER_RXTIME = (PREAMBLE_LENGTH + (PLCP_HEADER_SIG + math.ceil((PLCP_HEADER_SER + MAC_HEADER + LLC_HEADER) / OFDM_SYMBOL_D)) * 4)

RTS_TXTIME = 16 + (4 + round(((20) * 8) / C_MBPS))
CTS_TXTIME = (16 + (4 + round(((20) * 8) / C_MBPS)))

ACK_TIMEOUT = (PREAMBLE_LENGTH + (PLCP_HEADER_SIG + math.ceil(((PLCP_HEADER_SER + 80 + FCS) / OFDM_SYMBOL_B))) * 4) + SIFSTIME
CTS_TIMEOUT = (SIFSTIME + CTS_TXTIME + 1)
DAT_TIMEOUT = (SIFSTIME + DIFSTIME + 1)


"""
IEEE 802.11 DCF用のクラス
"""
class DCF:
    def __init__(self):
        self.num_retx = 0
        self.CW = CWMIN
        self.CWmin = CWMIN
        self.CWmax = CWMAX
        self.BackoffWindow = 0
        self.BackoffTimer = 0
        self.CurrentTimer = None
        self.PreTimer = None

    # CW値を設定
    def SetContentionWindow(self):
        self.CW = (2 ** self.num_retx) * self.CWmin
        #self.CW = self.CWmin
        if self.CW > self.CWmax:
            self.CW = self.CWmax
        self.BackoffWindow = random.randint(0, self.CW - 1)
        self.BackoffTimer = self.BackoffWindow * SLOTTIME
        self.CurrentTimer = self.BackoffWindow
    
    #   CW値を固定値で設定
    def SetFixedContentionWindow(self,val):
        self.BackoffWindow = val
        self.BackoffTimer = self.BackoffWindow * SLOTTIME
        self.CurrentTimer = self.BackoffWindow
