
#
#   シミュレーションシナリオ設定
#

USEC = 1 * 10**6
NUM_NODE = 11  # 端末台数
NUM_APP = NUM_NODE * 2  # アプリケーション数

START_TIME = 0 * USEC  # カウント開始時間
END_TIME = 3 * USEC  # シミュレーション時間
TRAINING_TIME = 0.6

MAX_BUF = 100  # バッファサイズ
MAX_GENE_PK = 1  # 一度に生起するパケット数

NUM_TRIAL = 10  # 1シミュレーションごとの試行回数
PAYLOAD = 1000  # ペイロードサイズ
DISTANCE = 5  # 端末間距離の基準(m)
LOAD = 0.008  # 負荷（mbps）
RTS_THRESHOLD = 500000  # RTS閾値 

QL = 0      #学習機能

OUTIMAGE = 0

#ログ出力設定
DEBUG = 0 # デバッグモード（ログがプリント）

# ログモード (node.csvとstate.csvにログを出力)
LOG = 0
Q_LOG = 0

# リアルタイム画像出力
SHOW_REALTIME_IMAGE = 0
PRINT = 1

STATISTICS = 0  # 統計情報
RESULT = 0  # 結果まとめ用エクセルが出力
TOPOLOGY = ''  # ネットワークの形状

BUG_FLAG = 0


INIT_LOAD = 10
DIF_LOAD = 1
END_LOAD = 10


