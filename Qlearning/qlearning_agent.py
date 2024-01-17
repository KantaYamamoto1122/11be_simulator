import copy
import numpy as np
import ieee80211

class QLearningAgent:
    """
        Q学習 エージェント(クラス)
    """

    def __init__(self):
        """
        各種学習パラメータ
        """
        self.alpha = 0.1  # 学習率
        self.epsilon = 0.99  # 探索率
        self.minimum_epsilon = 0.001
        self.gamma = 0.0  # 割引率
        self.eps_coefficient = 0.998 # 探索率の係数

        self.actions = ["keep","up"]  # 衝突後の行動の集合
        self.CW_list = [16, 32, 64,128,256,512,1024]   # CWminの初期値の集合
        #self.CW_list = [4, 8, 16, 32, 64]   # CWminの初期値の集合
        
        self.action = 0  # 選択した行動

        self.ini_state = 0  # 最初の状態    (再送回数0回)
        

        self.state = self.ini_state  # 状態
        self.next_state = None  # 次の状態
        self.previous_state = None  # 前の状態
        self.previous_action = None  # 前の行動
        self.q_values = self._init_q_values()  # Q値
        self.q_values2 = self._init_q_values() # Q値 CWmax用
        self.CW_number = 0  # CW値
        self.CW = None
        
        #self.CW_list = [16, 24, 32, 48, 64, 96, 128]
        self.CW_log = []
        self.Backoff = None
        self.TotalBackoffOneTx = 0
        self.TotalFreezeTimer = 0
        
        self.num_re_tx = 0 # 再送回数
        self.num_suc_tx = 0  # 送信成功回数
        self.num_tx = 0  # 送信回数
        self.num_col = 0  # 衝突回数
        self.total_count = 0
        self.num_tx_episode = 0  # エピソード中の送信回数
        self.num_suc_tx_episode = 0  # エピソード中の送信成功回数
        self.num_rx_episode = 0  # エピソード中の受信回数
        self.num_rx_sta = []  # エピソード中に受信した周囲の端末の端末
        self.reward = None  # 報酬
        self.reward_log = []  # 報酬のログ
        self.reward_history = []  # 報酬履歴
        self.no = None  # 端末番号
        self.col_flag = False  # 衝突フラグ

    def _init_q_values(self):
        """
            Q テーブルの初期化
        """
        q_values = np.repeat(0.0, len(self.CW_list))
        for i in range(len(self.CW_list)):
            q_values[i] = np.random.uniform()
        #q_values = np.repeat(np.random.uniform(), len(self.CW_list))
        #q_values2 = np.repeat(0.0, len(self.CW_list))
        return q_values

    def init_state(self):
        """
            状態の初期化
        """
        self.previous_state = copy.deepcopy(self.ini_state)
        self.state = copy.deepcopy(self.ini_state)
        return self.state

    def act(self):
        # ε-greedy選択
        if np.random.uniform() < self.epsilon:  # random行動
            action = np.random.randint(0, len(self.q_values))
        else:   # greedy 行動
            action = np.argmax(self.q_values)

        if self.epsilon > self.minimum_epsilon:
            self.epsilon = self.epsilon * self.eps_coefficient

        #self.previous_action = action
        #self.action = action
        return self.CW_list[action]

    def act_CWmaxSelect(self):
        # ε-greedy選択
        if np.random.uniform() < self.epsilon:  # random行動
            #action = np.random.randint(0, len(self.q_values2))
            action = len(self.q_values2)-1
        else:   # greedy 行動
            action = np.argmax(self.q_values2)
        
        #self.previous_action = action
        #self.action = action
        return self.CW_list[action]



    def observe(self,reward,selct_cwmin):
        """
            次の状態と報酬の観測
        """
        """
        for cw_i in range(len(self.CW_list)):
            if self.CW_list[cw_i] == now_cwmin:
                break
        #for i in range(cw_i,cw_i+num_retx+1):
        index = cw_i
        if index > len(self.CW_list)-1:
            index = len(self.CW_list)-1
        q = self.q_values[index]
        self.q_values[index] = q + self.alpha * (reward - q)
        self.q_values2[index] = q + self.alpha * (reward2 - q)

        if now_cwmin != selct_cwmin:
            for cw_i in range(len(self.CW_list)):
                if self.CW_list[cw_i] == selct_cwmin:
                    break
        
            index = cw_i
            if index > len(self.CW_list)-1:
                index = len(self.CW_list)-1
            q = self.q_values[index]
            if self.epsilon > 0.1:
                self.q_values[index] = q + self.alpha * (-reward/(num_retx+1) - q)
        """    
        for cw_i in range(len(self.CW_list)):
            if selct_cwmin == self.CW_list[cw_i]:
                break
        q = self.q_values[cw_i]
        max_q = 0

        self.q_values[cw_i] = q + self.alpha * (reward + (self.gamma * max_q) - q)   
        

