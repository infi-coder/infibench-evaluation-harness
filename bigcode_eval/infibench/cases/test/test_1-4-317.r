

f <- function(big, new_big){
    ret <- big[new_big, on = .(id), col2 := i.col][, .(id, col = fcoalesce(col2, as.numeric(col)))]
    return (ret)
}
library(data.table)
big <- structure(list(id = c('A','C','E','G','I','B','D','F','H','J'),
                          col = c(100, 300, 1000, 3000, 4, 5, 10, 9, 8, 2000)),
                          row.names = c(NA, -10L), class = c("data.table",
"data.frame"))
new_big <- structure(list(id = c('A','E','G','I','J','B'),
                              col = c(22, 42, 63, 91, 15, 66)), row.names = c(NA,
-3L), class = c("data.table", "data.frame"))


df1 = f(big, new_big)
df2 = myReplace(big, new_big)
setorder(df1, id)
setorder(df2, id)
df1 = unname(df1)
df2 = unname(df2)

assert(all.equal(df1, df2, check.attributes = FALSE))

