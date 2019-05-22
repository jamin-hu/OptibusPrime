import random

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))

print(primes)
