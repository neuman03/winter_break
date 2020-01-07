# https://tech.leverages.jp/entry/2019/04/24/113000

# AB testing for CTR
# LH imp: 30000, clk: 4250
# KH imp: 28000, clk: 3400 *ホームズ
install.packages("bayesAB")
library(bayesAB)

#乱数固定
set.seed(10)

a_imp <- 30000
a_clk <- 4250
b_imp <- 28000
b_clk <- 3400

# abtest <- matrix(c(a_imp-a_clk, a_clk, b_imp-b_clk, b_clk), nrow=2, ncol=2, byrow=T)
# rbinom(n, size, prob)
# n=乱数の数, size=ベルヌーイ試行の回数, prob=成功確率

a <- rbinom(a_imp, 1, a_clk/a_imp)
a <- rbinom(a_imp, 1, a_clk/a_imp)

# ベルヌーイ分布の事前分布をベータ分布として初期パラメータを一様分布を仮定してa=1,b=1とする
bayes_ab <- bayesTest(a, b, priors=c("alpha"=1, "beta"=1), distribution="bernoulli")

# 出力
summary(bayes_ab)

# 可視化
plot(bayes_ab)

