import config
import myclass
import math
import numpy as np
import copy
import random
import event
import ieee80211
import func

#   2021.11.29 コメント追加

#
#   パケット生起イベントの処理関数
#   
def ProcessGenePacket(EVE, node, g_time, e_list):
    # バッファが満タンでなければ
    packet_set_flag = 0
    if len(node.buffer) < config.MAX_BUF:
        packet_set_flag = 1
        # 新しいパケットを生成、パケットのアプリケーションはEVEで指定
        packet = myclass.PACKET("DAT")
        packet.app = EVE.app
        packet.src_id = packet.app.src_id
        packet.dst_id = packet.app.dst_id
        # 生起数カウントを
        if g_time > config.START_TIME:
            if EVE.app.src_id == node.id:
                node.Statistics.num_gene_pk += 1
            packet.id = node.Statistics.num_gene_pk # シーケンス番号
        node.buffer.append(packet)

    if EVE.app.PkArriveRate > 0:
        flag = 0
        while flag != 1:
            t = np.random.exponential(1. / EVE.app.PkArriveRate, 1)
            #t = 1. / EVE.app.PkArriveRate
            #nextinterval = round(t)
            nextinterval = math.floor(t[0])
            if nextinterval != 0:
                flag = 1
    else:
        return
    
    # 次の生起イベント予約
    #if packet.app.src_id == node.id:
    
    nexttime = nextinterval + g_time
    app = copy.copy(random.choice(node.applist))
    eve = event.make(node, g_time, nexttime, app, "GenePacket")
    e_list.append(eve)
    
    # 　端末の状態がアイドルならバックオフイベントの予約
    if node.state == "IDLE":
        eve = event.make(node, g_time, g_time, EVE.app,"Backoff", node.buffer[0])
        e_list.append(eve)



#
#   バックオフイベントの処理
#    
def ProcessBackoff(EVE, node, g_time, e_list):
    Rxflag = 0 #受信フラグ


    # 端末の状態をBACKOFF状態に変更
    node.state = "BACKOFF"


    # バックオフタイマーの設定
    node.dcf.SetContentionWindow()

    node.agent.TotalBackoffOneTx += node.dcf.BackoffWindow
    
    temp = 0

    #   受信バッファの確認. 受信パケットの受信レベルがCS閾値以上ならばCS状態に
    if len(node.Rxpk) > 0:
        for pk in node.Rxpk:
            
            if pk.dst_mac == node.id:
                Rxflag = 1
                break
            
    if len(node.Rxpk) > 0:
        recv_signal_sum_mw = 0
        recv_signal_sum_dbm = 0
        for pk in node.Rxpk:
            if temp < pk.TxEndTime:
                temp = pk.TxEndTime
            recv_signal_sum_mw += pk.recv_signal_mw
        recv_signal_sum_dbm = func.mw_to_dbm(recv_signal_sum_mw)
        if recv_signal_sum_dbm > node.CS_THRESHOLD:
            node.CSFlag = 1
            node.state = "CS"
        else:
            node.CSFlag = 0
    else:
        node.CSFlag = 0

    # 送信パケットの準備
    pk = node.buffer[0]
    
    #   バックオフカウントイベントの設定 
    if node.CSFlag == 0:
        #   チャネルがアイドルならばイベント開始時刻をDIFS期間後に設定
        nexttime = g_time + ieee80211.DIFSTIME
        eve = event.make(node,  g_time, nexttime, EVE.app, "CountBackoff", pk)
    else:
        #   バックオフカウントのフリーズ明けであれば, イベント開始時刻をACKタイムアウト+DIFS帰還後に設定
        nexttime = temp + ieee80211.ACK_TIMEOUT + ieee80211.DIFSTIME
        eve = event.make(node,  g_time, nexttime, EVE.app, "CountBackoff", EVE.Txpk)

    # 設定したイベントに送信パケット情報を格納
    eve.Txpk = node.SetTxPk("DAT", pk.app, g_time,pk.id)

    # イベントリストに追加
    e_list.append(eve)

#
#   バックオフカウント処理
#
def ProcessCountBackoff(EVE, node, g_time, e_list):
    DataRxflag = 0

    #   バックオフタイマーのカウント
    if node.dcf.CurrentTimer > 0 and node.state == "BACKOFF":
        node.dcf.CurrentTimer -= 1



    # SINRの計算
    node.calcSINR()

    # チャネルがビジーかの判定
    temp = 0
    if len(node.Rxpk) > 0:
        recv_signal_sum_mw = 0
        recv_signal_sum_dbm = 0
        for pk in node.Rxpk:
            if temp < pk.TxEndTime:
                temp = pk.TxEndTime
            recv_signal_sum_mw += pk.recv_signal_mw
        recv_signal_sum_dbm = func.mw_to_dbm(recv_signal_sum_mw)
        if recv_signal_sum_dbm > node.CS_THRESHOLD:
            node.CSFlag = 1
            node.state = "CS"
            node.agent.TotalFreezeTimer += 1
        else:
            node.CSFlag = 0
    else:
        node.CSFlag = 0

    for pk in node.Rxpk:
        if pk.dst_mac == node.id:
            DataRxflag = 1
            node.state = "Rx"
    
    
    #   次のイベントの設定
    if node.dcf.CurrentTimer == 0 and node.CSFlag == 0:
        #   バックオフタイマーが0の場合送信開始イベントを設定
        eve = event.make(node, g_time, g_time, EVE.app, "TxStart", EVE.Txpk)
    else:
        #   バックオフタイマーが0でない場合次のカウント時刻に開始時刻を設定
        nexttime = g_time + ieee80211.SLOTTIME
        if node.CSFlag == 0 and DataRxflag == 0:
            node.state = "BACKOFF"
            eve = event.make(node,  g_time, nexttime, EVE.app,"CountBackoff", EVE.Txpk)
        else:
            eve = event.make(node,  g_time, temp + ieee80211.ACK_TIMEOUT + ieee80211.DIFSTIME, EVE.app, "CountBackoff", EVE.Txpk)
        #   イベントリストに設定したイベントを追加
    e_list.append(eve)


#
#   送信開始イベント処理
#
def ProcessTxStart(EVE, node, g_time, e_list, n_list):
    csflag = 0

    # パケット送信開始および送信終了時刻
    EVE.Txpk.TxStartTime = g_time
    if EVE.Txpk.TxDuration == 0:
        EVE.Txpk.CalcTxDuration()
    EVE.Txpk.TxEndTime = g_time + EVE.Txpk.TxDuration


    # 端末状態をTxに変更
    node.state = "Tx"

    # 送信パケットの種類ごとの処理　
    if EVE.Txpk.type == "DAT":
        node.Statistics.num_TxDatPk += 1
        #################
        #   Q学習関連
        # 学習用パラメータ
        node.agent.num_tx_episode += 1
        #################

    if EVE.Txpk.type == "ACK":
        #SIFS期間中に隠れ端末による送信がないかの確認
        if len(node.Rxpk) > 0:
            node.calcSINR()
            recv_signal_sum_mw = 0
            recv_signal_sum_dbm = 0
            for pk in node.Rxpk:
                recv_signal_sum_mw += pk.recv_signal_mw
            recv_signal_sum_dbm = func.mw_to_dbm(recv_signal_sum_mw)
            if recv_signal_sum_dbm > node.CS_THRESHOLD:
                csflag = 1
    
    #   次のイベントの設定
    if csflag == 0:
        #   隠れ端末からの送信がない場合
        
        #送信終了イベントの予約
        nexttime = EVE.Txpk.TxEndTime
        eve = event.make(node, g_time, nexttime, EVE.app, "TxEnd", EVE.Txpk)
        e_list.append(eve)

        #   全端末の受信バッファに送信パケットを格納
        for i in range(len(n_list)):
            distance = math.sqrt((node.x - n_list[i].x) ** 2 + (node.y - n_list[i].y) ** 2)
            # パケット受信に関する処理
            RxFunction(n_list[i],EVE.Txpk, distance)
            #   衝突判定であった場合, その端末の状態へIDLEへ変更
            for pk in n_list[i].Rxpk:
                if pk.col_flag == 1 and n_list[i].state == "Rx":
                    n_list[i].state = "IDLE"
                break
    else:
        #   隠れ端末からの送信があった場合
        node.state = "IDLE"
        j = 0
        #   該当パケットを送信バッファから削除
        for pk in node.Txpk:
            if pk.type == EVE.Txpk.type and pk.dst_mac == EVE.Txpk.dst_mac:
                node.Txpk.pop(j)
                break
            j += 1

#
#   衝突処理
#
def CollisionFunction(node,e_list,g_time,additional_duration,Txpk):
    node.dcf.num_retx += 1
    if g_time > config.START_TIME:
        node.Statistics.num_Col += 1

    if node.dcf.num_retx <= ieee80211.MAX_RETX:
        ################################
        #   Q学習関連
        #   報酬の計算
        #if config.QL == 1:
        #    node.CalcReward(0)
        ###############################  

        #   再送回数が最大再送回数より小さいとき
        app = Txpk.app
        eve = event.make(node, g_time, g_time+additional_duration,app,"Backoff", Txpk)
        e_list.append(eve)

    else:
        #   最大再送回数に達した場合, パケットを破棄
        node.dcf.num_retx = 0
        if g_time > config.START_TIME:
            node.Statistics.num_Drop += 1
        if len(node.buffer) > 0:
            # バッファからパケットを削除
            node.buffer.pop(0)
        if len(node.buffer) > 0:
            #   バッファに次のデータパケットがある場合BACKOFFイベントを設定し, リストへ追加  
            node.state = "BACKOFF"
            app = node.buffer[0].app
            eve = event.make(node, g_time, g_time, app,"Backoff", node.buffer[0])
            e_list.append(eve)

            #あらかじめ設定していた再送イベントがあれば削除
            for e in range(len(e_list)):
                if e_list[e].type == "noACKRx" and e_list[e].node.id == node.id:
                    del e_list[e]
                    break

        else:
            node.state = "IDLE"


#
#   パケット受信の際の処理
#
def RxFunction(node, Txpk, distance):
    RxSig_dbm = 0
    RxSig_mw = 0

    # 端末間距離に応じて受信強度の計算
    if distance == 0:
        RxSig_dbm = ieee80211.DEFAULT_TXPOWER
    elif distance > 0:
        RxSig_dbm = func.calc_RxSig(distance)

    #   受信強度の情報を格納
    RxSig_mw = func.dbm_to_mw(RxSig_dbm)
    Rxpk = copy.copy(Txpk)
    Rxpk.recv_signal = RxSig_dbm
    Rxpk.recv_signal_mw = RxSig_mw

    if Rxpk.recv_signal > ieee80211.ENERGY_THRESHOLD:
        #   受信バッファに格納
        node.Rxpk.append(Rxpk)

    #   SINRの計算
    node.calcSINR()

    # 受信バッファにある全てのパケットに対して受信判定
    for i in range(len(node.Rxpk)):
        if node.Rxpk[i].SINR < ieee80211.SINR_THRESHOLD:
            # 衝突判定
            if node.Rxpk[i].dst_mac == node.id:
                node.Rxpk[i].col_flag = 1
        else:
            # 成功判定
            if node.Rxpk[i].dst_mac == node.id:
                j = 0  
                for rate in ieee80211.MCS:
                    if rate == node.Rxpk[i].rate:
                        break
                    j += 1
                if node.Rxpk[i].recv_signal > ieee80211.minRxMCS[j]:
                    node.state = "Rx"
        
#
#   フレーム確認用
#
def checkFrame(pk1, pk2):
    flag = 0
    if pk1.type != pk2.type:
        flag = 1
    if pk1.dst_mac != pk2.dst_mac:
        flag = 1
    if pk1.src_mac != pk2.src_mac:
        flag = 1
    if pk1.TxStartTime != pk2.TxStartTime:
        flag = 1
    if pk1.TxEndTime != pk2.TxEndTime:
        flag = 1
    return flag


#
#   送信完了イベント処理
#
def ProcessTxEnd(EVE, node, g_time, e_list, n_list, now):
    # 端末の状態をWAITに
    node.state = "WAIT"
    colflag = 0

    # 全端末の全受信バッファ内の受信パケット受信確認
    for i in range(len(n_list)):
        for pk in n_list[i].Rxpk:
            # 衝突フラグがなく, 宛先が一致すると受信成功フラグ
            if pk.col_flag == 0:
                if pk.dst_mac == n_list[i].id:
                    j = 0
                    for rate in ieee80211.MCS:
                        if rate == ieee80211.D_MBPS:
                            break
                        j += 1
                    if pk.recv_signal > ieee80211.minRxMCS[j]:
                        n_list[i].RxSucFlag = 1
                        if pk.type == "ACK":
                            n_list[i].AckRxSucFlag= 1
            else:
                if pk.src_mac == node.id:
                    node.CollisionFlag = 1

    # 判定済み受信パケットを削除
    for i in range(len(n_list)):
        j = 0
        for pk in n_list[i].Rxpk:
            if checkFrame(pk, EVE.Txpk) == 0:
                n_list[i].Rxpk.pop(j)
            j += 1
    
    # データ送信時の処理
    if EVE.Txpk.type == "DAT":
        # noACKRxイベントをリストに追加 (ACK受信成功を確認後ににこのイベントは削除)
        eve = event.make(node, g_time, g_time+ieee80211.ACK_TIMEOUT+1,None,"noACKRx", EVE.Txpk)
        e_list.append(eve)
        
        #全端末に対して送信パケットの受信成功の確認
        for i in range(len(n_list)):
            if n_list[i].RxSucFlag == 1 and EVE.Txpk.dst_mac == n_list[i].id:
                # データパケットの受信が成功するとACKフレーム返答へ
                ProcessRxSucDATA(n_list[i], g_time, e_list, EVE.Txpk, now)
                if EVE.Txpk.dst_id != n_list[i].id:
                    RelayData(n_list[i],g_time,e_list,EVE.Txpk)
    
    #   ACKがセットされていないかの確認
    for i in range(len(n_list)):
        ackcheck = 0
        if n_list[i].id == EVE.Txpk.dst_mac:
            for pk in n_list[i].Txpk:
                if pk.type == 'ACK':
                    ackcheck = 1
            if ackcheck == 0:
                n_list[i].state = "IDLE"
            break
    

    # ACKフレーム送信時の処理
    if EVE.Txpk.type == "ACK":
        node.state = "IDLE"
        i = 0
        # ACKフレームを検索し, 送信バッファから削除
        for pk in node.Txpk:
            if pk.dst_mac == EVE.Txpk.dst_mac and pk.src_mac == EVE.Txpk.src_mac and pk.type == EVE.Txpk.type:
                node.Txpk.pop(i)
            i += 1

        # 
        # バックオフイベントがすでに設定されていないか確認
        backoff_flag = 0
        for eve_i in e_list:
            if eve_i.type == "CountBackoff" and node.id == eve_i.node.id:
                backoff_flag  = 1

        if backoff_flag != 1:
            if len(node.buffer) > 0 :
                # バッファに次のデータパケットがあれば, 状態バックオフに変更しバックオフイベントの設定  
                node.state = "BACKOFF"
                app = node.buffer[0].app
                eve = event.make(node, g_time, g_time, app,"Backoff", node.buffer[0])
                e_list.append(eve)
            else:
                # バッファが空の場合, 状態をIDLEへ変更
                node.state = "IDLE"

    
        #   ACKの宛先端末を検索し, ACKフレームの受信処理    
        for i in range(len(n_list)):
            if EVE.Txpk.dst_mac == n_list[i].id:
                ProcessRxACK(n_list[i], g_time, e_list,EVE.Txpk.src_mac, EVE.Txpk.dst_mac)


#
#   データ受信成功処理
#
def ProcessRxSucDATA(node, g_time, e_list, pk, now):
    AckDst = pk.src_mac
    node.RxSucFlag = 0
    if node.state == "Rx":
        #   端末の状態をWAITに変更
        node.state = "WAIT"
        if g_time > config.START_TIME:
            node.Statistics.num_RxSuc_pk += 1
            if node.id == pk.dst_id and node.Statistics.now_seq_rx_no[pk.src_id]  < pk.id:
                node.Statistics.now_seq_rx_no[pk.src_id] = pk.id
                node.Statistics.num_RxSucIP_pk += 1
                if now > config.END_TIME*config.TRAINING_TIME:
                    node.Statistics.num_rpk_training += 1

        #   ACKフレームの生成
        txFrame = node.SetTxFr('ACK', AckDst, g_time)
        #   ACK返答のためのACK送信開始イベントの設定, リストへの追加
        eve = event.make(node, g_time, txFrame.TxStartTime, 0, "TxStart", txFrame)
        e_list.append(eve)

#
#   データ中継の処理
#

def RelayData(node,g_time,e_list,pk):
    # 生起イベント予約
    nexttime = g_time
    app = copy.copy(random.choice(node.applist))
    eve = event.make(node, g_time, nexttime, app, "RelayPacket")
    eve.Txpk = pk     #シーケンス番号の格納
    e_list.append(eve)


#
#   ACKフレームの受信処理
#
def ProcessRxACK(node, g_time, e_list, AckSrc, AckDst):

    if node.state == "Rx" or "WAIT":
        # ACKを正常に受信できた時の処理
        if node.RxSucFlag == 1:
            ################################
            #   Q学習関連
            #   報酬の計算

            
            ###############################   
            #あらかじめ設定していた再送イベントがあれば削除
            for e in range(len(e_list)):
                if e_list[e].type == "noACKRx" and e_list[e].node.id == node.id:
                    del e_list[e]
                    break

            # 送信バッファから送パケットを削除
            for j in range(len(node.Txpk)):
                if node.Txpk[j].dst_mac == AckSrc and node.Txpk[j].src_mac == AckDst:
                    txpk = node.Txpk[j]
                    del node.Txpk[j]
                    break

            if config.QL == 1:
                node.CalcReward(txpk)

            # 再送回数を初期化
            node.dcf.num_retx = 0
            if len(node.buffer) > 0:
                node.buffer.pop(0)  # キューからパケットを削除
            if g_time > config.START_TIME:
                node.Statistics.num_TxSuc_pk += 1
            if len(node.buffer) > 0:
                # バッファに次のデータパケットがあれば, 状態バックオフに変更しバックオフイベントの設定  
                node.state = "BACKOFF"
                app = node.buffer[0].app
                eve = event.make(node, g_time, g_time, app,"Backoff", node.buffer[0])
                e_list.append(eve)
            else:
                # バッファが空の場合, 状態をIDLEへ変更
                node.state = "IDLE"
        """
        # ACKフレーム受信が失敗したときの処理        
        else:
            # 再送のためのバックオフイベントの設定, リストに追加
            if g_time > config.START_TIME:
                node.Statistics.num_Col += 1
            if len(node.buffer)>1:  # バグ回避用
                app = node.buffer[0].app
                eve = event.make(node, g_time, g_time, app,"Backoff", node.buffer[0])
                e_list.append(eve)
                node.dcf.num_retx += 1  # 再送回数をインクリメント
        """    

    node.RxSucFlag = 0
    node.AckRxSucFlag = 0

#
#   ACK受信がなかったときの処理
#
def ProcessnoACKRx(EVE, node, g_time, e_list,n_list):

    for p in range(len(node.Txpk)):
        if node.Txpk[p].id == EVE.Txpk.id:
            del node.Txpk[p]
            break
    #   衝突処理

    
    CollisionFunction(node,e_list,g_time,0,EVE.Txpk)


#
#   中継によるパケット生起イベントの処理関数
#   
def ProcessRelayPacket(EVE, node, g_time, e_list):

    # バッファが満タンでなければ
    packet_set_flag = 0
    if len(node.buffer) < config.MAX_BUF:
        packet_set_flag = 1
        # 新しいパケットを生成、パケットのアプリケーションはEVEで指定
        packet = myclass.PACKET("DAT")
        packet.app = EVE.app
        packet.src_id = packet.app.src_id
        packet.dst_id = packet.app.dst_id
        # 生起数カウントを
        if g_time > config.START_TIME:
            if EVE.app.src_id == node.id:
                node.Statistics.num_gene_pk += 1
            packet.id = EVE.Txpk.id
        node.buffer.append(packet)

    
    # 　端末の状態がアイドルならバックオフイベントの予約
    if node.state == "IDLE":
        eve = event.make(node, g_time, g_time, EVE.app,"Backoff", node.buffer[0])
        e_list.append(eve)