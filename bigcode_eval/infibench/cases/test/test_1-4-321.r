library(data.table)
f <- function(x){
result <- setDT(x)[
  ,
  .(segment_stemming = trimws(
    unlist(strsplit(segment_stemming, "(?<=\\)),\\s+(?=\\()", perl = TRUE)),
    whitespace = "\\[|\\]"
  )),
  id
]
return(result)
}

df <- structure(list(id = c("A", "B" ),
                    segment_stemming = c("[('Brownie', 'Noun'), ('From', 'Josa'), ('Pi', 'Noun')]",
                                          "[('Dung-caroon-gye', 'Noun'), ('in', 'Josa'), ('innovation', 'Noun')]" )),
               row.names = c(NA, -2L),
               class = c("data.table", "data.frame" ))


library(assert)
df1 = f(df)
df2 = mySplit(df)
df1 = unname(df1)
df2 = unname(df2)
assert(all.equal(df1, df2, check.attributes = FALSE))