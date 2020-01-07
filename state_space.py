# Custom Causal Impact
# http://jamalsenouci.github.io/projects/causalimpact.html
# http://jamalsenouci.github.io/projects/causalimpact.html

# もう一つは pycausalimpact https://github.com/dafiti/causalimpact

# Local linear trend ‘local linear trend’
# Local linear deterministic trend ‘local linear deterministic trend’
# Xt = Xt-1 + Trendt-1 + ew + Seasont
# Yt = Xt + ev

# 基本のライブラリを読み込む
import numpy as np
import pandas as pd
from scipy import stats

# グラフ描画
from matplotlib import pylab as plt
import seaborn as sns
%matplotlib inline

# グラフを横長にする
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

# 統計モデル
import statsmodels.api as sm

# 日付形式で読み込む
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
nq = pd.read_csv('NQ.csv', index_col='Week', date_parser=dateparse, dtype='float')
grp = pd.read_csv('GRP.csv', index_col='Week', date_parser=dateparse, dtype='float')

# 日付形式にする
nq = nq['NQ'] 
grp = grp['GRP'] 

# プロット
plt.plot(nq)
plt.plot(grp)

# SARIMAX in 状態空間モデル
# from statsmodels.tsa.statespace.structural import UnobservedComponents
model = sm.tsa.UnobservedComponents(endog=nq, 
                                    level=‘local linear trend’,
                                    trend=True,
                                    seasonal=52,
                                    autoregressive=1,
                                    exog=grp)

result = model.fit(method='bfgs', maxiter=500)
# result.summary()

# ビジュアライズ
result.plot_components()

# Causal Impact
# 8. Using a custom model
# 結局こっちにする
# pip install pycausalimpact
# https://github.com/dafiti/causalimpact/blob/master/examples/getting_started.ipynb

from causalimpact import CausalImpact

# x_test, x_train =
# y_test, y_train =

# 予測期間
# pre_piriodだけ, exogを入れる必要がある
pre_period = ['2019-12-01', '2019-12-31']
post_period = ['2019-12-01', '2019-12-31']

# prior_level_sd=None, nseasons=[{'period': 52}]
ci = CausalImpact(data=nq, model=model, pre_period, post_period)

# 可視化
ci.plot(figsize=(14, 8))

# モデル・サマリー
ci.summary()





