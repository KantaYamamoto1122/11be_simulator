import ieee80211
import math
import numpy as np

'''
受信強度の計算（dBm）
'''
def calc_RxSig(distance):
    dbm = ieee80211.DEFAULT_TXPOWER - (ieee80211.PATH_LOSS_REF_DISTANCE + 10 * ieee80211.TRANSFER_COEFFICIENT * math.log10(distance))
    return dbm

'''
dbmをmwに変換
'''
def dbm_to_mw(dbm):
    mw = pow(10, (dbm/10))
    return mw

'''
mwをdBmに変換
'''
def mw_to_dbm(mw):
    dbm = 10 * math.log10(mw)
    return dbm

"""
キャリアセンス範囲を計算
"""
def Calc_CSRange(th):
    d0 = 1
    Pt = ieee80211.DEFAULT_TXPOWER
    L0 = ieee80211.PATH_LOSS_REF_DISTANCE
    n = ieee80211.TRANSFER_COEFFICIENT
    d = d0 * 10 ** ((Pt - th - L0)/(10*n))
    return d 

def fairness(x):

    numer = pow( sum(x),2)
    num = len(x)
    denom = sum(np.power(x,2)) * num
    return numer / denom














