# https://multithreaded.stitchfix.com/blog/2016/04/21/forget-arima/

# 状態過程
# AddLocalLinearTrend(y)
y <- df$nq
x <- df$grp

# 短期の自己相関+トレンド+季節性+広告効果+残差
# ss=state.specification
ss <- list()
ss <- AddAutoAr(ss, y, lags=1)
ss <- AddLocalLinearTrend(ss, y)
ss <- AddSeasonal(ss, y, nseasons=52) # ss <- AddMonthlyAnualCycle()
ss <- AddDynamicRegression(ss, y, data=x) # ss <- AddDynamicRegression(ss, y ~ x)

# 観測過程
# https://www.rdocumentation.org/packages/bsts/versions/0.9.2/topics/bsts
model <- bsts(formula=y,
            ss,
            family="gaussian",
            niter=500,
            seed=42)

# モデルの要約統計量
# The number of MCMC iterations to discard as burn-in.
burn <- SuggestBurn(0.1, model)
summary(model, burn=burn)

# モデルの評価
# 可視化
plot(model)
plot(model, 'state', burn=burn)
plot(model, 'coef', burn=burn)
plot(model, 'seasonal', burn=burn)
plot(model, 'components', burn=burn)
plot(model, 'residuals', burn=burn)
plot(model, 'predictors', burn=burn)
plot(model, 'size', burn=burn)
plot(model, 'dynamic', burn=burn)
plot(model, 'prediction.errors', burn=burn)
plot(model, 'forecast.distribution', burn=burn)

# 残差の確認
resid <- residuals(model)
par(mfrow = c(1,2))
qqdist(resid)   ## A bit of departure in the upper tail
AcfDist(resid)

# 予測
grp_f <- future_grp$grp
pred <- predict(model, horizon=12, newdata=grp_f, burn=100)
par(mfrow=c(1,2))
plot(model)
plot(pred)

# 実際の値
y_test <- df$nq

# MAPE
# MAPE <- filter(y_test, year(Date)>1959) %>% summarise(MAPE=mean(abs(Actual-Fitted)/Actual))

# 比較
# CompareBstsModels(list(bsts_model1, bsts_model2))
