
from math import e
from func import fairness
import myclass
import event
import setting
import config
import process
import log
import os
import csv
import func
import numpy as np
import OutNetworkImage

#from Qlearning.qlearning_agent import QLearningAgent

from show.real_time import ShowDurationThr as ShowDurationThr
from show.real_time import updateimage
from show.real_time import makeimage
from show.real_time import ShowQvalue

def main(list):
    new_dir_path_log = './OutFiles'
    os.makedirs(new_dir_path_log, exist_ok=True)
    new_dir_path_log = './image'
    os.makedirs(new_dir_path_log, exist_ok=True)

    #シミュレーション結果格納用のフォルダ作成
    new_dir_path_log = './csv/log'
    os.makedirs(new_dir_path_log, exist_ok=True)
    #シミュレーション結果格納用のフォルダ作成
    new_dir_path_results = './csv/results'
    os.makedirs(new_dir_path_results, exist_ok=True)
    new_dir_path_Qvalue = './csv/Qvalue'
    os.makedirs(new_dir_path_Qvalue, exist_ok=True)
    
    #   端末情報のLOGを出力するファイル名を指定
    log_node_info_csv = new_dir_path_log + '/node.csv'
    if os.path.exists(log_node_info_csv):
        os.remove(log_node_info_csv)

    #   Q値の出力
    log_Qvalue_info_csv = []
    for n_i in range(config.NUM_NODE):
        log_Qvalue_info_csv.append(new_dir_path_Qvalue + '/Qvalue_n'+str(n_i)+'.csv')
        if os.path.exists(log_Qvalue_info_csv[n_i]):
            os.remove(log_Qvalue_info_csv[n_i])

    #   端末の状態ログを出力するファイル名を指定
    log_state_csv = new_dir_path_log + '/state.csv'
    if os.path.exists(log_state_csv):
        os.remove(log_state_csv)

    #   端末情報をまとめたファイル名を指定
    AllResult_csv = new_dir_path_results + '/AllResult.csv'
    if os.path.exists(AllResult_csv):
        os.remove(AllResult_csv)

    result_sim = myclass.Result()
    AllResult = []

    Thall = []

    for trial in range(config.NUM_TRIAL):
        
        now = 0
        pre_time = None
        e_list = []
        n_list = []
        # ネットワークの設定
        setting.setting(n_list)

        # 最初のイベント作成
        setting.first_event(n_list, e_list)
        AveGenePk = 0
        prev_int_now = 0
        prev_show_time = 0
        prev_show_time_float = 0
        prev_rxpk = 0
        prev_rxpk_list = np.repeat(0.0, config.NUM_NODE-1)
        time_list = []
        duration_thr_list = []
        duration_FI_list = []
        duration_mean_cwmin = []
        time_list.append(0)
        duration_mean_cwmin.append(0)
        duration_thr_list.append(0)
        duration_FI_list.append(0)
        node_time_alllist = []

        rxpk_prex_list = []
        for n_i in n_list:
            if n_i.dev_type == "STA":
                rxpk_prex_list.append(0) 
        if config.SHOW_REALTIME_IMAGE == 1:                
            ax = ShowDurationThr(time_list,duration_thr_list)

        while now < config.END_TIME:    #   終了時刻でシミュレーションを終了
        #while AveGenePk < 10:       #   生起パケット数でシミュレーション終了
            event.search_duplex(e_list)
            eve_now = event.search_near(e_list)
            now = eve_now.start_time

            ######################################
            # ログ書き出し用
            if config.LOG == 1:
                #   各イベント開始時刻における端末の情報をファイル出力 (GenePacketは除く)
                #   if eve_now.type != "GenePacket":
                    log.WriteNodeAllstate(n_list, now,pre_time,log_state_csv, eve_now)
                    log.WriteNodeState(n_list,now,pre_time,log_node_info_csv,e_list,eve_now)
                    pre_time = now
                #   先頭イベント
            
            # デバック様
            if config.DEBUG == 1:
                #if eve_now.type != "GenePacket":
                print("e_list")
                log.PrintEventlist(e_list)
                log.PrintNodeState(n_list, now)
                print("")

            if config.Q_LOG== 1:
                if int(now/1000) > prev_int_now:
                    prev_int_now = int(now/1000)
                    for n_i in range(len(n_list)):
                        log.WriteQvalue(n_list[n_i], now,log_Qvalue_info_csv[n_i])

            # 区間スループットの表示
            if int(now /(config.USEC* 0.1 )) > prev_show_time:
                node_time_alllist.append(n_list)
                prev_show_time = int(now/(config.USEC* 0.1) )
                showtime_end = prev_show_time* 0.1
                showtime_start = (prev_show_time - 1) * 0.1
                now_rxpk = n_list[config.NUM_NODE-1].Statistics.num_RxSucIP_pk
                durtion_rxpk = now_rxpk - prev_rxpk
                prev_rxpk = n_list[config.NUM_NODE-1].Statistics.num_RxSucIP_pk
                duration =  (now - prev_show_time_float)
                duration_throughput = durtion_rxpk * config.PAYLOAD * 8 / duration
                
                rxpk_list = []
                rxpk_now_list = []
                cwmin_node_list = []
                
                for n_i in n_list:
                    if n_i.dev_type == "STA":
                        rxpk_list.append(n_i.Statistics.num_TxSuc_pk)
                        cwmin_node_list.append(n_i.dcf.CWmin)
                
                for rx_pk_i in range(len(rxpk_list)): 
                    rxpk_now_list.append(rxpk_list[rx_pk_i] - rxpk_prex_list[rx_pk_i])
                meanCWmin = np.mean(cwmin_node_list)    
                FI = func.fairness(rxpk_now_list)
                if config.PRINT == 1:
                    text = "Simulation duration {:,.2f}--{:,.2f} sec, "
                    text_thr = " Througput = {:,.2f} Mbps, FI = {:,.4f}, mean CWmin =  {:,.2f}"
                    print(text.format(showtime_start,showtime_end)+text_thr.format(duration_throughput,FI,meanCWmin)) 
                
                duration_FI_list.append(FI)
                time_list.append(showtime_end)
                duration_thr_list.append(duration_throughput)
                duration_mean_cwmin.append(meanCWmin)
                if config.SHOW_REALTIME_IMAGE == 1:
                    ax = updateimage(time_list,duration_thr_list,ax)

                
                prev_show_time_float = now

                

            ######################################
            
            # パケット生起イベント処理
            if eve_now.type == "GenePacket":
                process.ProcessGenePacket(eve_now, n_list[eve_now.node.id], now, e_list)
                event.release(eve_now, e_list)

            #   バックオフイベント処理   
            if eve_now.type == "Backoff":
                if len(n_list[eve_now.node.id].buffer)> 0:
                    process.ProcessBackoff(eve_now, n_list[eve_now.node.id], now, e_list)
                event.release(eve_now, e_list)

            #   バックオフカウント
            if eve_now.type == "CountBackoff":
                process.ProcessCountBackoff(eve_now, n_list[eve_now.node.id], now, e_list)
                event.release(eve_now, e_list)

            #   送信開始イベント処理
            if eve_now.type == "TxStart":
                process.ProcessTxStart(eve_now, n_list[eve_now.node.id], now, e_list, n_list)
                event.release(eve_now, e_list)

            #   送信終了イベント処理
            if eve_now.type == "TxEnd":
                process.ProcessTxEnd(eve_now, n_list[eve_now.node.id], now, e_list, n_list, now)
                event.release(eve_now, e_list)

            #   ACK受信失敗時の処理
            if eve_now.type == "noACKRx":
                process.ProcessnoACKRx(eve_now, n_list[eve_now.node.id], now, e_list, n_list)
                event.release(eve_now, e_list)

            #  中継によるパケット生成イベント処理
            if eve_now.type == "RelayPacket":
                process.ProcessRelayPacket(eve_now, n_list[eve_now.node.id], now, e_list)
                event.release(eve_now, e_list)

            if len(e_list) == 0:
                break
            
            genePk = []
            for n in n_list:
                genePk.append(n.Statistics.num_gene_pk)
            AveGenePk = sum(genePk)/len(genePk)

        # 全てのシミュレーション結果をリストへ格納    
        AllResult.append(n_list)
        result_sim.nodelist.append(n_list)

        #トライアルごとの時系列データの格納
        result_sim.DurationThr.append(duration_thr_list)
        result_sim.DurationMeanCWmin.append(duration_mean_cwmin)

        # スループットの計算
        if config.QL == 1:
            Throughput = n_list[config.NUM_NODE-1].Statistics.num_rpk_training * config.PAYLOAD * 8 / ((config.END_TIME-config.START_TIME)*(1-config.TRAINING_TIME))
        else:
            Throughput = n_list[config.NUM_NODE-1].Statistics.num_RxSucIP_pk * config.PAYLOAD * 8 / (config.END_TIME-config.START_TIME)
        Thall.append(Throughput)
        rxpk_list = []
        for n_i in n_list:
            if n_i.dev_type == "STA":
                rxpk_list.append(n_i.Statistics.num_TxSuc_pk)
        FairnessIndex = func.fairness(rxpk_list)
        print("")
        print("Trail"+str(trial)+", Offered load="+str(config.LOAD)+"Mbps, Througput="+str(Throughput)+"Mbps")
        print("FI="+str(FairnessIndex))
        log.PrintandWrtieAllStatistic(n_list, AllResult_csv)
        print("Simulation end time = " + str(now) + " usec")
        print("")

    if config.SHOW_REALTIME_IMAGE == 1:
        makeimage(time_list,duration_thr_list,ax,"./image/DurationThr")
    
    #   結果の出力
    file2 = open("throughput.csv", "a", newline="")
    writer = csv.writer(file2)
    result_sim.CalcResult()
    Throughput = result_sim.Thr
    PrCollision =  result_sim.Col

    #   時系列データ用 
    result_sim.Duration = time_list
    #result_sim.DurationThr = duration_thr_list
    #result_sim.DurationMeanCWmin = duration_mean_cwmin

    result_sim.Off = config.LOAD
    result_sim.pay = config.PAYLOAD
    result_sim.node_alltime_list = node_time_alllist
    list.append(result_sim)
    result=[config.NUM_NODE-1,Throughput,PrCollision]
    writer.writerow(result)
    file2.close

    if config.NUM_TRIAL > 1:
        print("Throughput Average = " + str(sum(Thall)/config.NUM_TRIAL) + "Mbps")


if __name__ == "__main__":
    list=[]
    main(list)
