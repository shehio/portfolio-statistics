#-------------------------------------------------------------------------------
# Scripts for calculating weights and returns of assets
# See below the functions for an example of use.
#-------------------------------------------------------------------------------
calcWeightsAndReturns <- function(holdings, AccountSummary, begindate, enddate, 
                                  prices, splitfactors, divps){
  # Calculates the weights and returns of assets over a weekly period 
  # given the holdings at the beginning of the week
  # and the cash flow data in the Account Summary.
  # Returns are calculated assuming assets are held over the full period
  # and assuming all cash flows occur at the end of the period.
  # Holdings are adjusted for splits.
  # Asset returns are total returns including dividends.
  # The liquidity reserve absorbs all fees and transaction costs.
  # Args:
  #   holdings: a data frame with columns "ticker", "num.shares"
  #   AccountSummary: a data frame with columns "as.of.date", "fees", "tc", "total.return"
  #   begindate: the beginning date of the period
  #   enddate: the ending date of the period
  #   prices: the xts object created by getPrices()
  #   splitfactors: the xts object created by getSplitfactors()
  #   divps: the xts object created by getDivpershare()
  # Returns:
  #   a data frame with columns "ticker", "ABV", "weight", "AEV", "return", and related items
  
  # Find the begin and end rows in AccountSummary
  as.of.dates <- AccountSummary[ , "as.of.date"]
  for (i in 1:length(as.of.dates)){
    if (as.of.dates[i] == begindate){
      ibegindate <- i
    }
    if (as.of.dates[i] == enddate){
      ienddate <- i
    }
  }
    
  # Get tickers
  myTickers <- holdings[ , "ticker"]
  
  # Get prices
  myPrices <- prices[c(begindate, enddate), ]
  
  # Assemble beginning values and weights
  holdings <- data.frame(holdings, price.beg=as.numeric(myPrices[1, ]))
  ABV <- holdings[ , 2] * holdings[ , "price.beg"]
  holdings <- data.frame(holdings, ABV=ABV)
  holdings <- data.frame(holdings, weight=calcWeights(holdings[ , "ABV"]))

  # Adjust the beginning shares for splits if necessary to calculate ending shares
  myShares <- holdings[ , 2]
  if (prod(splitfactors[ienddate, ]) != 1) {
    print("WARNING: Adjust shares for splits")
    myShares <- myShares / as.numeric(splitfactors[ienddate, ])
  }
  holdings <- data.frame(holdings, num.shares.end=myShares)
  
  # Assemble the ending values
  holdings <- data.frame(holdings, price.end=as.numeric(myPrices[2, ]))
  EV <- holdings[ , "num.shares.end"] * holdings[ , "price.end"]
  holdings <- data.frame(holdings, EV=EV)
  
  # Dividend amount is based on holdings from prior date.
  # In the rare situation of a split and dividend in the same week, this may fail.
  if (sum(divps[ienddate, ]) != 0) {
    print("WARNING: Account for dividends")
  }
  # Calculate dividend amounts
  tdividends <- myShares * as.numeric(divps[ienddate, ])
  holdings <- data.frame(holdings, dividend=tdividends)
  
  # Calculate AEV
  AEV <- holdings[ , "EV"] + holdings[ , "dividend"]
  holdings <- data.frame(holdings, AEV=AEV)
  
  # Get fees and tc from AccountSummary
  tfees <- AccountSummary[ienddate, "fees"]
  ttc <- AccountSummary[ienddate, "tc"]
  #tvalue <- AccountSummary[ienddate, "value"]
  #cash.flow <- AccountSummary[ienddate, "deposits"] - AccountSummary[ienddate, "withdrawals"]
  
  # Calculate the liquidity reserve AEV
  # AEV[21] <- tvalue - cash.flow  - sum(AEV[1:20])
  AEV[21] <- holdings[21, "EV"] - tfees - ttc
  holdings[which(holdings[ , "ticker"] == "CASHX"), "AEV"] <- AEV[21]
  
  # Calculate returns
  returns <- ((holdings[ , "AEV"] / holdings[ , "ABV"]) - 1) * 100
  holdings <- data.frame(holdings, return=returns)
  
  # Check for consistency
  treturn <- sum((holdings[ , "weight"] / 100) * holdings[ , "return"])
  print(paste("Weighted returns =", treturn))
  print(paste("Account Summary return = ", AccountSummary[ienddate, "total.return"]))
  if (abs(treturn - AccountSummary[ienddate, "total.return"]) > 1e-7){
    print("Weighted returns not consistent with Account Summary return")
  }
  
  return(holdings)
}#end calcWeightsAndReturns()

#-------------------------------------------------------------------------------
# Example of use:
# Build a history table of sector weights and returns
# Required functions: getPrices(), getSplitfactors(), getDivpershare()
# Reads holdings files and account summary files.
# Reads the file: ".//Data//H-R3000-2020-03-27.csv"
# Note: This script assumes that the tickers are the same for all dates.
# If they list of tickers changes, then getPrices, getSplitfactors, 
# and getDivpershare should be moved to within the loop.
#-------------------------------------------------------------------------------
library(quantmod)

account.name <- "dcarino"
folder <- ".//HW submitted//dcarino//"

as.of.dates <- c("2020-03-27", "2020-04-03", "2020-04-09", "2020-04-17", "2020-04-24",
                 "2020-05-01", "2020-05-08", "2020-05-15", "2020-05-22", "2020-05-29")
ibegindate <- 1
ienddate <- 8

# Read the R3000 constituents file
R3000.const <- read.csv(".//Data//H-R3000-2020-03-27.csv", stringsAsFactors=FALSE)

# Read an Account Summary file
filename <- paste(folder, "A-", account.name, "-", as.of.dates[ienddate], ".csv", sep="")
AccountSummary <- read.csv(filename, stringsAsFactors=FALSE)

# Read the first holdings file, get tickers
filename <- paste(folder, "H-", account.name, "-", as.Date(as.of.dates[ibegindate]), ".csv", sep="")
holdings <- read.csv(filename, stringsAsFactors=FALSE)
myTickers <- holdings[ , "ticker"]

# Get prices, split factors, and dividends per share
myPrices <- getPrices(myTickers, as.of.dates[1:ienddate])
print("Getting split factors and dividends per share...")
splitfactors <- NULL
divps <- NULL
for (tkr in myTickers){
  print(tkr)
  if (tkr != "CASHX"){
    
    # Get split factors
    tkrtmp <- getSplitfactors(tkr, as.of.dates[1:ienddate])
    splitfactors <- cbind(splitfactors, tkrtmp)
    
    # Get dividend per share
    tkrtmp <- getDivpershare(tkr, as.of.dates[1:ienddate])
    divps <- cbind(divps, tkrtmp)
  }
}
# Add a column for CASHX
colnames(tkrtmp) <- "CASHX"
tkrtmp[ , "CASHX"] <- 1.0
splitfactors <- cbind(splitfactors, tkrtmp)
tkrtmp[ , "CASHX"] <- 0.0
divps <- cbind(divps, tkrtmp)

# Build a history table of sector weights and returns
# Initialize a history table
sector.wtret.hist <- NULL
# Loop starts here
for (idate in ibegindate:(ienddate - 1)){
  
  ibegin <- idate
  iend <- idate + 1
  writeLines(paste("\nWeek from", as.of.dates[ibegin], "to", as.of.dates[iend]))

  # Read a holdings file
  filename <- paste(folder, "H-", account.name, "-", as.Date(as.of.dates[ibegin]), ".csv", sep="")
  holdings <- read.csv(filename, stringsAsFactors=FALSE)
  
  wtret <- calcWeightsAndReturns(holdings, AccountSummary, as.of.dates[ibegin], as.of.dates[iend],
                                          myPrices, splitfactors, divps)

  # Continue computing here ... see getICBIndustries.R for an example

  # Get the sector classification info, merge with the wtret table
  tmp <- getSectors(myTickers, R3000.const)
  wtret <- merge(wtret, tmp)
  
  # Aggregate the ABV and AEV by sector to create a sector.wtret table
  # Assign the sector table here
  sector.wtret <- aggregate(
    wtret[ , c("ABV", "AEV")], 
    by = list(ICB.industry.num=wtret[ , "ICB.industry.num"], ICB.industry.name=wtret[, "ICB.industry.name"]),
    FUN = sum)

  # Calculate weights from ABV and add to the sector table
  sector.wtret <- data.frame(
    sector.wtret, 
    weight=calcWeights(sector.wtret[ , "ABV"]))
  
  # Calculate returns from the AEV and ABV and add to the sector table
  sector.wtret <- data.frame(
    sector.wtret, 
    return=((sector.wtret[ , "AEV"] / sector.wtret[ , "ABV"]) - 1) * 100)

  # Add rows for sectors with zero holdings, replace NA with 0.0
  allSectors <- unique(R3000.const[ , c("ICB.industry.num", "ICB.industry.name")])
  sector.wtret <- merge(sector.wtret, allSectors, all=TRUE)
  sector.wtret[is.na(sector.wtret[ , "ABV"]), "ABV"] <- 0.0
  sector.wtret[is.na(sector.wtret[ , "AEV"]), "AEV"] <- 0.0
  sector.wtret[is.na(sector.wtret[ , "weight"]), "weight"] <- 0.0
  sector.wtret[is.na(sector.wtret[ , "return"]), "return"] <- 0.0
  
  # Add a date column
  sector.wtret <- data.frame(week.ending=as.of.dates[idate+1], sector.wtret)
  
  # Concatenate to the history table
  sector.wtret.hist <- rbind(sector.wtret.hist, sector.wtret)
  
}#end for (idate in ibegindate:(ienddate - 1))

# Write the history table to a file named like "S-UWNetID-2020-04-17"
filename <- paste("S-", account.name, "-", as.of.dates[ienddate], ".csv", sep="")
write.csv(sector.wtret.hist, file=filename, row.names=FALSE)

# Clean up
rm(myTickers, tkr, tkrtmp, idate, ibegin, iend, holdings,
   wtret, tmp, sector.wtret, allSectors, sector.wtret.hist)