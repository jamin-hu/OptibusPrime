import random

def multiplyList(myList):
    result = 1
    for x in myList:
         result = result * x
    return result

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))


def calcRandRouteProd(totalNumOfStops, numOfStops):

    totalStopPrimes = []

    stopPrimes = []


    for i in range(totalNumOfStops):
        totalStopPrimes.append(primes[i])
    print(totalStopPrimes)

    stopPrimes = random.sample(totalStopPrimes, k = numOfStops)
    print(stopPrimes)

    routePrime = multiplyList(stopPrimes)
    print(routePrime)
    print(len(str(routePrime)))

calcRandRouteProd(1000, 30)
