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
