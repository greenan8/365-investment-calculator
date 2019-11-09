#imports
import sys, math, csv



#Key Variables
startAge            = 25
endAge              = 59 #do not have start and end age more then 34 years apart
startSal            = 100000
endSal              = 250000
savingGoal          = 2000000
livingPercent       = 40
yearlySal = []
savingR             = 0.05
utilityDiscountR    = 0.10
utilityTotal        = 0.0



#Determine salary growth as linear
def salFunc():
    salIncrease = (endSal - startSal) // (endAge - startAge)

    yearlySal.append(startSal)

    for x in range (1, (endAge-startAge)):
        yearlySal.append(yearlySal[x-1] + salIncrease)

    yearlySal.append(endSal)

salFunc()


#Utility Function
def utility(percent):
    if (percent <= 0.3):
        return (percent/0.3)*0.1
    elif (percent >= 0.7):
        return (percent)*0.1 + 0.9
    else:
        return (percent/0.7)*0.8 + 0.1






def recursiveFunc(year, tempUtilityTotal, tempSavingsAccount, tempYSpending, tempYUtility, tempYDiscount, tempYSavings, carryPercent):
   

    if (year > (endAge-startAge)):      
        global utilityTotal             
               
        if ((tempSavingsAccount > savingGoal) and (tempUtilityTotal > utilityTotal)):
            
            with open('results-michael.csv',"w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Age", "Salary", "Spending %", "Spending", "Utility", "PV Utility", "Saving %","Amount Saved", "Save Account"])
                for x in range(0, endAge-startAge+1):
                    writer.writerow([x + startAge, yearlySal[x], tempYSpending[x]/yearlySal[x], tempYSpending[x], tempYUtility[x], tempYDiscount[x], (yearlySal[x]*(1.0-livingPercent/100) - tempYSpending[x])/yearlySal[x], yearlySal[x]*(1.0-livingPercent/100) - tempYSpending[x], round(tempYSavings[x],4)])
                  
                writer.writerow([])
                writer.writerow(["Totals:", "", "",sum(tempYSpending), sum(tempYUtility), sum(tempYDiscount), "", "", tempSavingsAccount])
                writer.writerow([])
                writer.writerow(["start Age", "End Age", "Start Salary", "End Salary", "Savings Goal", "Living Expenses", "Saving %", "Utility Discount"])
                writer.writerow([startAge, endAge, startSal, endSal, savingGoal, livingPercent/100, savingR, utilityDiscountR])
            
        
            utilityTotal= tempUtilityTotal
        return
    if (year % 5 == 0):        
        for x in range(0, (100-livingPercent + 10),10):
            tempYSpending[year] = (x/100)*yearlySal[year]
            tempYUtility[year] = utility(x / (100-livingPercent))
            tempYDiscount[year] = tempYUtility[year] / ((1.0 + utilityDiscountR)**year)
            tempUtilityTotalLoop = tempUtilityTotal + tempYDiscount[year]
            tempSavingsAccountLoop = tempSavingsAccount * (1.0 + savingR) + yearlySal[year]*(1.0 - (x/100) - (livingPercent/100))
            tempYSavings[year] = tempSavingsAccount

            recursiveFunc(year + 1, tempUtilityTotalLoop, tempSavingsAccountLoop, tempYSpending, tempYUtility, tempYDiscount, tempYSavings, x)
        return
    else:
        tempYSpending[year] = (carryPercent/100)*yearlySal[year]
        tempYUtility[year] = utility(carryPercent / (100-livingPercent))
        tempYDiscount[year] = tempYUtility[year] / ((1.0 + utilityDiscountR)**year)
        tempUtilityTotalLoop = tempUtilityTotal + tempYDiscount[year]
        tempSavingsAccountLoop = tempSavingsAccount * (1.0 + savingR) + yearlySal[year]*(1.0 - (carryPercent/100) - (livingPercent/100))
        tempYSavings[year] = tempSavingsAccount  

        recursiveFunc(year + 1, tempUtilityTotalLoop, tempSavingsAccountLoop, tempYSpending, tempYUtility, tempYDiscount, tempYSavings, carryPercent)

        return
    
  



recursiveFunc(0, 0, 0, [0.01]*(endAge - startAge + 1), [0.01]*(endAge - startAge + 1), [0.01]*(endAge - startAge + 1), [0.01]*(endAge - startAge + 1), 0)







            