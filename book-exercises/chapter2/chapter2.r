# Exercise 2.1
#	Discussion, skipping

# Exercise 2.2
# Common statistical techniques
ages <- c(13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70)

"a) Mean "
mean(ages)
sum(ages) / length(ages)

"b) Mode"
Mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}
Mode(ages) # Bimodal because there are 2 modes 25 and 35, both with 4 occurrences

"c) Midrange"
(min(ages) + max(ages)) / 2

"d) First and third quartile"
q <- round(length(ages)/4, 0)
ages[q]
ages[q*3]

"e) Five-number summary"
min(ages)
ages[q]
median(ages)
ages[q*3]
max(ages)

"f) Boxplot"
svg("2_2f.svg", width=6, height=6)
boxplot(ages) # See output file
dev.off()

"g) Quantile and Quantile-Quantile plots"
svg("2_2g.svg", width=6, height=6)
n <- length(ages)
plot((1:n - 1)/(n - 1), sort(ages))
dev.off()