# 仮定
# 1. 平行トレンド仮定…施策実施がないとき、両群ともに観測データは同傾向のまま
# 2. 共通ショック仮定…期間前後において、両群ともに施策以外に同様の処置のみ受けている
# 3. スピルオーバー効果がない…両群間に施策影響の波及・漏洩が起きていない
# https://qiita.com/wtnVegna/items/6d7d729ea2001243133c
# tjo: https://tjo.hatenablog.com/entry/2016/08/02/190000
# 介入、時期、DID(B-A)-(D-C)

# 平行トレンド仮定・数量の効果差分 → OLS回帰
# 平行トレンド仮定・比率の効果差分 → GLMロジスティック回帰（二項分布）

import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# 数量を目的変数とする場合
# 広島と宮城の指名検索実数
nq = pd.read_csv('nq_hiroshima_vs_miyagi.csv')
nq.head()

# prefecture, treatment, period, value, did
# 4×4になる
# pre: 広島, 広島, 宮城, 宮城
# tre: 1, 1, 0, 0
# per: 0, 1, 0, 1
# val: 200, 1800, 300, 1700

# 指名検索結果: 広島, 広島, 宮城, 宮城
nq = [200, 1800, 300, 1700]

# params
params = pd.DataFrame({
    'Treated' : np.array([1, 1, 0, 0]), # D_t 項： [比較群, 対象群] で [0,1,0,1...] 
    'Period' : np.array([0, 1, 0, 1]), # D_p項 : [前期間, 前期間, 後期間, 後期間] で [0,0,1,1,...]
    'DID' : np.array([1, 1, 0, 0] * np.array([0, 1, 0, 1]) # D_t*D_g項
})

#OLS回帰による検証
import statsmodels.api as sm

# NQ: 施策効果の差
dif = (nq[1]-nq[0]) - (nq[2]-nq[3])
print(dif)

# 定数項（切片の追加）に注意
model = sm.OLS(endog=nq, exog=sm.add_constant(params))
result = model.fit()
print(result.summary())

# P>|t|列の値からDID変数が（もし有意水準0.05と設定するならば）統計的に有意である
# # この施策は結果に関係がある可能性が見えてくる



# 比率を目的変数とする場合
# 広島と宮城のCTR
ctr = pd.read_csv('ctr_hiroshima_vs_miyagi.csv')
ctr.head()

# ctr: 広島, 広島, 宮城, 宮城
ctr = [0.14, 0.23, 0.12, 0,20]

# params
params = pd.DataFrame({
    'Treated' : np.array([1, 1, 0, 0]), # D_t 項： [比較群, 対象群] で [0,1,0,1...] 
    'Period' : np.array([0, 1, 0, 1]), # D_p項 : [前期間, 前期間, 後期間, 後期間] で [0,0,1,1,...]
    'DID' : np.array([1, 1, 0, 0] * np.array([0, 1, 0, 1]) # D_t*D_g項
})

# CTR: 施策効果の差
dif = (ctr[1]-ctr[0]) - (ctr[2]-ctr[3])
print(dif)

# GLMロジスティック回帰による検証
# statmodelsのGLMには切片が必要なので、 sm.ad_constant()で追加
# family=確率分布, リンク関数も指定可能, Bnom(link = sm.genmod.families.links.log)
model = sm.GLM(endog=ctr, exog=sm.add_constant(params), family=sm.families.Binomial())
result = model.fit()
print(result.summary())

# P>|z|列の値から（もし有意水準0.05と設定するならば）DID変数が統計的に有意である
# 施策が結果に影響がある
# またPeriodとTreated変数は有意でない点から、施策効果の可能性がより見えてくる


