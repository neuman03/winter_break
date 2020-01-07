
install.packages("dplyr") # pandas in r
install.packages("xts") # ts
install.packages("prophet")
install.packages("githubinstall")
install.packages("prophetExt")
install.packages("changepoint")
install.packages("changepointExt")

library(dplyr)
library(xts)
library(prophet)

# ds, y, cap 
cvr <- read.csv("cvr.csv")
tail(cvr)

# prophetの引数
plot(cvr)

# simple prediction
model <- prophet(cvr)
future <- make_future_dataframe(model, periods=365)
forcast <- predict(model, future)
head(forcast)
plot(model, forecast)

# componet 
prophet_plot_components(model, forcast)

# 変化点の可視化
plot(model) + add_changepoints_to_plot(model)

# トレンドの変化が過学習になっている(トレンドの柔軟性がありすぎる)場合や、学習しきれていない(柔軟性が足りていない)場合は、changepoint_prior_scaleという引数を使うことで、スパースの優先度の大きさを調整できる
model <- prophet(cvr, changepoint.prior.scale=0.99)
forcast <- predict(model)
plot(mode)

# アルゴリズム変更n.changepoints = 25, changepoint.range = 0.8, seasonality.prior.scale = 10,
cvr$cap <- 0.30
model <- prophet(df=cvr, growth="logistic", changepoints="2019-09-27", yearly.seasonality=True)
plot(model)

# 物件数減少タイミング
model <- prophet(df=cvr, growth="logistic", changepoints=c("2019-09-27", "2019-10-01"), yearly.seasonality=True)
plot(model)

# https://qiita.com/hoxo_m/items/3f5fae96ed48aebaf434
# n.changepoints = 25, changepoint.range = 0.8, seasonality.prior.scale = 10,
cvr$cap <- 0.30
model <- prophet(df=cvr, growth="logistic", n.changepoints=25, changepoint.range=0.98, yearly.seasonality=True, daily.seasonality=True)
# plot(model) + add_changepoints_to_plot(model)
plot(model)

# 変化点の抽出
head(model)
model$changepoints

as.vector(model$params$delta)
round(as.vector(model$params$delta), digits=2)

# 有効な変化点のみの抽出
# 変化量が微小なものを除いた、有効な変化点だけを抽出することができます
library(prophetExt)
model <- prophet(df=cvr, growth="logistic", n.changepoints=25, changepoint.range=0.98, yearly.seasonality=True, daily.seasonality=True)
main_cp <- prophet_pick_changepoints(model)
main_cp

# さらに、この変化点を簡単に可視化する関数 autolayer() も用意しました。 
plot(model) + autolayer(main_cp)

# event効果
# event_df <- read.csv(event.csv) # holiday, ds, lower, upper
# model <- prophet(cvr, holidays=event_df)


# 外れ値検知
# https://qiita.com/hoxo_m/items/e492e0e2e8e384804477
# 外れ値を検出する関数は prophet_detect_outliers() 
model <- prophet(df=cvr, growth="logistic", n.changepoints=25, changepoint.range=0.98, yearly.seasonality=True, daily.seasonality=True)
outliers <- prophet_detect_outliers(model, recursive=False)
head(outliers)

# 外れ値を可視化するために autolayer() 関数で Prophet plot に重ね描きできるようにしました
plot(model) + autolayer(outliers)

# カレンダー
# 外れ値のカレンダープロットを作成する機能もつけました
prophet_calendar_plot(outliers)

# Extra Regressors
# https://qiita.com/hoxo_m/items/dae5283ea045687ad2ed
# changepointExt パッケージというものを作った。
library(changepoint)
library(changepointExt)

# * cpt.mean: 平均だけが変化する場合
# * cpt.var: 分散だけが変化する場合
# * cpt.meanvar: 平均と分散が変換する場合
# Pruned Exact Liner Time（PELT）: 比較的新しい手法で、ワーストケースではO(n2)O(n2)の計算量が必要ですがペナルティが線形であればO(n)O(n)で計算できます。高速で精度も高い手法です。
# 軽いペナルティを設定すれば変化点が多く検出されます
cpm <- cpt.mean(cvr, method="PELT")
cpv <- cpt.var(cvr, method="PELT", penalty = "Manual",  pen.value = 5)
cpmv <- cpt.meanvar(cv, method="PELT", test.stat = "Poisson")

# まずはcpts()を使って検出された変化点を確認してみましょう。
cpts(cpv)

plot(cpm)
plot(cpv)
plot(cpmv)

# https://qiita.com/hoxo_m/items/2dc95330671206df3281
autoplot(cpmv)

# 要因分析: CV=UU×CVR
cv <- read.csv("cv.csv")
uu <- read.csv("uu.csv")
cvrread.csv("cvr.csv")

cp_cv <- cpt.meanvar(cv, method = "PELT")
cp_uu <- cpt.meanvar(uu, method = "PELT")
cp_cvr <- cpt.meanvar(cvr, method = "PELT")

# 可視化
combi <- combine_cpts("流入UU数" = cp_uu, "CVR" = cp_cvr, operator = "*")
autoplot(cp_cv) + autolayer(combi)


