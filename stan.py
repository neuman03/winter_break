# https://qiita.com/hrkz_szk/items/25a7f48e980ffe685207

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-darkgrid')

from matplotlib.pylab import rcParams
import pystan

# 反響と広告費
# ts, hankyo, tvad_cost
df = pd.read_csv("promotion.csv")

# 反響データの可視化
rcParams['figure.figsize'] = 12, 8
plt.plot(df.hankyo)
plt.title('Hankyo')
plt.show()

# 広告費データの可視化
rcParams['figure.figsize'] = 12, 8
plt.plot(df.dummy_ad)
plt.title('TV Advirtisement')
plt.show()

# アドストック効果の可視化
adstock = 10 - np.log(np.arange(1,51))*2
rcParams['figure.figsize'] = 12, 8
plt.plot(adstock)
plt.title('Adstock effects')
plt.show()

# データ数
# N = len(df)

# 回帰係数が時間よって変化する時変係数のモデリングが可能
# 時間とともにその効果が薄れていくことを表現することが可能
# 整数, 小数点ありは実数
stanmodel = 
"""
// 推定に使う入力データ
data{
    int<lower=0> N; // N個の整数（データそのものではなく、後に必要なデータの長さ）
    int<lower=0> hankyo[N]; // N個の整数を要素とする配列 "hankyo"
    real<lower=0> tvad_cost[N]; // N個の実数を要素とする配列 "tvad_cost"
}

// 推定したいパラメータ
parameters{
    real beta[N]; // 推定したい母平均
    real beta_zero; // わからない: 事前分布?
    real<lower=0> sigma_w; // 誤差の母分散
    
    real mu[N]; // 推定したい母平均
    real mu_zero; // わからない: 事前分布?
    real<lower=0> sigma_v; // 誤差の母分散

    real<lower=0> sigma_e; // 誤差の母分散
}

// モデル: 尤度関数と事前分布について記述
model{ 
    beta[1] ~ normal(beta_zero, sigma_w); // 推定値 ~ 分布(パラメータ1, パラメータ2)
    for(i in 2:N) 
        beta[i] ~ normal(beta[i-1], sigma_w); // なぜ2?わからない: 0がないから

    mu[1] ~ normal(mu_zero, sigma_v);
    for(i in 2:N)
        mu[i] ~ normal(mu[i-1], sigma_v);

    for(i in 2:N)
        hankyo[i] ~ normal(mu[i] + beta[i]*tvad_cost[i], sigma_e);
}
"""

# Stanモデルの呼び出し
model = pystan.StanModel(file="hankyo_tvad.stan")

# データの呼び出し, data{}に記述したものにフィット
data = dict(N=len(df), hankyo=df.hankyo, tvad_cost=df.tvad_cost)

fit = model.sampling(data=data, iter=5000, warmup=500, chains=4, thin=1, seed=1, n_jobs=-1)
print(fit)

# 可視化
rcParams['figure.figsize'] = 15, 10
fit.plot()
plt.title('Bayesian DLM: Dynamic Linear Model')
plt.show()

# 推定したパラメータの抽出
result = fit.extract()

# muの事後平均を算出
mean_mu = result["mu"].mean(axis=0)

# 広告効果の回帰係数の事後平均を算出
mean_beta = ms['beta'].mean(axis=0)

# 広告効果を算出
ad_effects = mean_beta * df.tvad_cost

# 95パーセンタイルを抽出
mu_5 = np.array(pd.DataFrame(result['mu']).apply(lambda x: np.percentile(x, 5), axis=0))
mu_95 = np.array(pd.DataFrame(result['mu']).apply(lambda x: np.percentile(x, 95), axis=0))
beta_5 = np.array(pd.DataFrame(result['beta']).apply(lambda x: np.percentile(x, 5), axis=0))
beta_95 = np.array(pd.DataFrame(result['beta']).apply(lambda x: np.percentile(x, 95), axis=0))
ad_effects5 = beta_5 * df.tvad_cost
ad_effects95 = beta_95 * df.tvad_cost

# トレンドの推定
X = df.index
rcParams['figure.figsize'] = 15, 5
plt.plot(X, df.hankyo, label='observed')
plt.plot(X, mu, label='true trend', c='green')
plt.plot(X, mean_mu, label='predicted trend', c='red')
plt.fill_between(X, mu_5, mu_95, color='red', alpha=0.2)
plt.legend(loc='upper left', borderaxespad=0, fontsize=15)

# 広告効果の推定
rcParams['figure.figsize'] = 15, 5
plt.plot(X, np.concatenate((np.repeat(0,200), adstock, np.repeat(0,200))), label='true effects', c='green')
plt.plot(X, ad_effects, label='predicted effects', c='red')
plt.fill_between(X, ad_effects5, ad_effects95, color='red', alpha=0.2)
plt.legend(loc='upper left', borderaxespad=0, fontsize=15)

# 広告期間のみにフォーカス
rcParams['figure.figsize'] = 15, 5
plt.plot(X[201:250], np.concatenate((np.repeat(0,200), adstock, np.repeat(0,200)))[201:250], label='true effects', c='green')
plt.plot(X[201:250], ad_effects[201:250], label='predicted effects', c='red')
plt.fill_between(X[201:250], ad_effects5[201:250], ad_effects95[201:250], color='red', alpha=0.2)
plt.legend(loc='upper right', borderaxespad=0, fontsize=15)

# トレンドと広告効果によるリフト値
rcParams['figure.figsize'] = 15, 5
plt.plot(X, data.sales_ad, label='observed')
plt.plot(X, mean_mu+adstock, label='predicted trend + predicted ad effects', c='orange')
plt.plot(X, mean_mu, label='predicted trend', c='tomato')
#plt.fill_between(X, mu_5, mu_95, color='red', alpha=0.2)
plt.legend(loc='upper left', borderaxespad=0, fontsize=15)