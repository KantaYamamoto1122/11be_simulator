import csv
import config
import myclass

#   2021.11.30 コメント追加

#
#   端末の状態を表示   
#
def PrintNodeState(n_list, now):
    array = ["time=" + str(now), 'TxSucPk', 'RxSucPk','RxIP_Pk','nCol',
             'retx', 'Suc', 'CS', 'CW', 'BT', 'CWmin', 'CurBT','Buf']
    print(array)
    for node in n_list:
        print(node.state, node.Statistics.num_TxSuc_pk, node.Statistics.num_RxSuc_pk, node.Statistics.num_RxSucIP_pk,node.Statistics.num_Col, node.dcf.num_retx,
              node.RxSucFlag, node.CSFlag, node.dcf.CW, node.dcf.BackoffWindow, node.dcf.CWmin, node.dcf.CurrentTimer,len(node.buffer))
    print('')

#
#   イベントリストにある全てのイベント情報を表示 (GenePacketイベントは除く)   
#   (イベントの種類)  n(対象端末)   t_(開始時刻)    s_(イベント設定時刻)    
def PrintEventlist(e_list):
    newlist2 = sorted(e_list, key=lambda h: h.start_time)
    print("---------------")
    for eve in newlist2:
        #if eve.type != "GenePacket":
        print(eve.type, "n", eve.node.id, "t_",eve.start_time, "s_", eve.set_time, end=', \n')
        if eve.type == ("TxStart" or "TxEnd"):
            print("TxPK type = ",eve.Txpk.type,"")
    print("---------------")

#
#   端末の状態を表示   
#   
def PrintandWrtieAllStatistic(n_list, filename):
    file2 = open(filename, "a", newline="")
    writer = csv.writer(file2)
    array = ['id', 'GenePk', 'TxPk', 'TxSucPk',
             'RxSucPk', 'RxSucIP_Pk','nCol', 'PrCol', 'drop','CWmin','CWmax']
    writer.writerow(array)
    print(array)
    for node in n_list:
        if node.Statistics.num_TxDatPk != 0:
            P_col = node.Statistics.num_Col/node.Statistics.num_TxDatPk
        else:
            P_col = 0
        row = [node.id, node.Statistics.num_gene_pk, node.Statistics.num_TxDatPk, node.Statistics.num_TxSuc_pk,
               node.Statistics.num_RxSuc_pk, node.Statistics.num_RxSucIP_pk, node.Statistics.num_Col, P_col, node.Statistics.num_Drop,node.dcf.CWmin,node.dcf.CWmax]
        print(row)
        writer.writerow(row)




#
#   現在のイベントと端末情報をログファイルへ出力
#
def WriteNodeState(n_list, now, pretime, filename, e_list, eve_now):
    # ファイルを開く
    file2 = open(filename, "a", newline="")
    writer = csv.writer(file2)
    newlist2 = sorted(e_list, key=lambda h: h.start_time)

    write_flag = 0

    # 現在時刻の書き込み
    if now != pretime:
        write_flag = 1
        csvrow = ["Now=" + str(now)]
    else:
        csvrow = [" "]

    # イベントリストにある全てのイベント情報を出力(GenePacketイベントは除く)
    if write_flag == 1:
        writer.writerow(csvrow)
        eve_array = [" ", "no", "type", "node", "t_start", "t_set"]
        writer.writerow(eve_array)
        i = 0
        for eve in newlist2:
            if eve.type != "GenePacket":
                eve_row = [" ", i, eve.type, str(eve.node.id), str(
                    eve.start_time), str(eve.set_time)]
                writer.writerow(eve_row)
                i += 1
        writer.writerow(" ")


    # 現在のイベント情報を出力
    eve_info = ["eve="+eve_now.type, "n" +
                str(eve_now.node.id), "set_t"+str(eve_now.set_time)]
    csvrow = [" "]
    csvrow = csvrow + eve_info
    writer.writerow(csvrow)

    #   現在の端末の状態を出力

    array = [" ", "id", "State", 'TxSucPk', 'RxSucPk', 'RxSucIP_Pk','nCol',
             'retx', 'Suc', 'CS', 'CW', 'BT', 'CWmin', 'CurBT','nRxPk',"nTxPk","TxSrc","TxDst"]
    writer.writerow(array)
    for node in n_list:
        row = [" ", node.id, node.state, node.Statistics.num_TxSuc_pk, node.Statistics.num_RxSuc_pk, node.Statistics.num_RxSucIP_pk,node.Statistics.num_Col, node.dcf.num_retx,
               node.RxSucFlag, node.CSFlag, node.dcf.CW, node.dcf.BackoffWindow, node.dcf.CWmin, node.dcf.CurrentTimer,len(node.Rxpk),len(node.Txpk)]
        if len(node.Txpk)> 0:
            txpkrow = [node.Txpk[0].src_mac,node.Txpk[0].dst_mac]
            row = row + txpkrow
        writer.writerow(row)
    writer.writerow("\n")
    
    # Q値の書き出し
    csvrow = ["q_value="]
    writer.writerow(csvrow)
    for node in n_list:
        writer.writerow(node.agent.q_values)
    writer.writerow("\n")

    file2.close()

#
#   現在のイベントと端末情報をログファイルへ出力
#
def WriteQvalue(node, now, filename):
    # ファイルを開く
    file2 = open(filename, "a", newline="")  
    writer = csv.writer(file2)
    # Q値の書き出し
    csvrow = [now]
    csvrow = [now]
    q = node.agent.q_values
    csvrow.extend(q)
    csvrow.append(node.agent.epsilon)
    writer.writerow(csvrow)
    
    file2.close()

#
#   端末の状態情報をログファイルへ出力
#
def WriteNodeAllstate(n_list, now, pre_time, filename, eve):
    # ファイルを開く
    file2 = open(filename, "a", newline="")
    writer = csv.writer(file2)
    row = []

    #   現在の時刻における端末の状態情報を書き込み
    # (現在のイベント)_n(現在のイベントの対象端末ID)
    if pre_time != now:
        row.append(now)
    else:
        row.append("")
    row.append(str(eve.type)+"_n"+str(eve.node.id))
    row.append(" ")

    # (端末状態)_t(バックオフタイマ)_Cs(CSフラグ)f_CSP(CSプリフラグ)
    for node in n_list:
        row.append(str(node.state) + "_t"+str(node.dcf.CurrentTimer) +
                   "_Cs"+str(node.CSFlag)+"_CsP"+str(node.CSPreFlag))
    writer.writerow(row)
    
    #ファイルを閉じる
    file2.close()
