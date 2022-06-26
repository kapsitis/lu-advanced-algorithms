ff <- function(x) {return (x^2)}
gg <- function(x) {return (x^3)}
hh <- function(x) {return (x^2 + 0.5*(1 + cos(x*pi))*(x^3 - x^2))}

x <- seq(0.0, 10.2, by = 0.01)

plot(x, gg(x), type="l", col="red", ylab="y")
points(x, ff(x), type="l", col="red")
points(x, hh(x), type="l", col="blue", lwd="2")

grid()
