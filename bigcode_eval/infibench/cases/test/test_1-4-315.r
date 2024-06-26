f <- function(df){
    result <- cbind(df[ 1 ], mapply(paste0, df[, seq(2, 7, 2)], df[, seq(3, 7, 2)]))
    return (result)
}
# 创建一个数据框并填充示例整数值
df <- data.frame(
  X1 = c(1, 2, 3, 4, 5),
  X2 = c(6, 7, 8, 9, 10),
  X3 = c(11, 12, 13, 14, 15),
  X4 = c(16, 17, 18, 19, 20),
  X5 = c(21, 22, 23, 24, 25),
  X6 = c(26, 27, 28, 29, 30),
  X7 = c(31, 32, 33, 34, 35)
)
library(assert)
df1 = f(df)
df2 = concat(df)
df1 = unname(df1)
df2 = unname(df2)
assert(all.equal(df1, df2, check.attributes = FALSE))
