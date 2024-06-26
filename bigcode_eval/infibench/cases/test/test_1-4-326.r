library(stringr)

rmcom <- function(x) gsub(",", "", x)

f <- function(string){
   x <- str_replace_all(string, "(\"[[:alnum:]]+,[ [:alnum:],]*\")", rmcom)
    return(x)
}

s1 <- 'wreur,wIERJ,iotj32423,"sdfs,sdfdsf,aad"'
s2 <- '"skfsfka,,,,,,,asdsaddsa",,,,,,"fsaadda"'


assert(all.equal(f(s1), removeComma(s1), check.attributes = FALSE))
assert(all.equal(f(s2), removeComma(s2), check.attributes = FALSE))


