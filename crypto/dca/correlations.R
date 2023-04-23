aa <- c()

for (i in 1:1000) {
  x <- sample(c(0,1), size=2048, replace=TRUE)
  y <- sample(c(0,1), size=2048, replace=TRUE)
  a <- cor(x, y, method="pearson")
  aa <- c(aa, a)
} 

hist(aa)

myCor <- function(a,b) {
  ss <- 0
  sdA <- 0
  sdB <- 0
  avgA <- mean(a)
  avgB <- mean(b)
  for (i in 1:length(a)) {
    ss <- ss + (a[i] - avgA)*(b[i] - avgB)
    sdA <- sdA + (a[i] - avgA)^2
    sdB <- sdB + (b[i] - avgB)^2
  }
  return(ss/sqrt(sdA*sdB))
} 

xx <- c(1, 1, 0, 0, 0, 1, 1, 0, 1, 1)
yy <- c(0, 0, 0, 1, 1, 0, 1, 1, 0, 1)
cc <- cor(xx, yy, method="pearson")
print(sprintf("cc = %1.5f",cc))
dd <- myCor(xx, yy)
print(sprintf("dd = %1.5f",dd))


