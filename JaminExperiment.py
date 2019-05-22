import random
import numpy as np
import matplotlib.pyplot as plt



def multiplyList(myList):
    result = 1
    for x in myList:
         result = result * x
    return result

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))


def calcRandAvgRouteProd(totalNumOfStops, numOfStops):

    totalStopPrimes = []

    for i in range(totalNumOfStops):
        totalStopPrimes.append(primes[i])
    print("Total primes = ")
    print(totalStopPrimes)

    totalLength = 0

    for h in range(10):
        stopPrimes = []
        stopPrimes = random.choices(totalStopPrimes, k = numOfStops)

        print("Random sample of StopPrimes = ")
        print(stopPrimes)
        routePrime = multiplyList(stopPrimes)
        print("RoutePrime = " + str(routePrime))
        routePrimeLength = len(str(routePrime))
        print("RoutePrime Length = " + str(routePrimeLength))
        totalLength = totalLength + routePrimeLength
    averageLength = totalLength/10
    print(averageLength)
    return averageLength

#averageLength = calcRandAvgRouteProd(100, 10)
#print("Average Length = " + str(averageLength))

def getPossibilities(maxNumOfTotalStops):

    possibilityMatrix = np.zeros(shape=(maxNumOfTotalStops,maxNumOfTotalStops))
    for i in range(0, maxNumOfTotalStops, 10):
        for j in range(0, maxNumOfTotalStops, 10):
            if i>j:
                print(i)
                print(j)
                RandAvgLength = calcRandAvgRouteProd(i, j)
                possibilityMatrix[i, j] = RandAvgLength

    return possibilityMatrix

possibilityMatrix = getPossibilities(1000)

print(possibilityMatrix)

plt.xlabel('AverageRouteLength in Stops')
plt.ylabel('TotalNumOfStops in City')

plt.imshow(possibilityMatrix, cmap='hot')
plt.show()
# testMatrix = np.zeros((5,5))
# testMatrix[1, 2] = 1
#
# plt.figure("testMatrix[1, 2]")
# plt.imshow(testMatrix)
# plt.show()
