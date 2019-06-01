# OptibusPrime

_"Solving public transport with Emoji (actually though)"_


## The Problem

Current bus numbering systems aren't particularly useful. You can't tell where they are going without a map.

![alt text](https://i.imgur.com/NjGNl8p.png) 

## The Solution

Well, there is a simple solution! Let’s assign a prime number to each bus stop. We can now make bus lines by multiplying all the stop numbers together. A bus going to stops “5” “7” and “3” would be called 105. If “5” is your desired stop, you just need to check if an approaching bus has a number divisible by “5”? is 508735 your bus? Sure it is! Is 3618452 your bus? Of course not! EASY!

![alt text](https://i.imgur.com/CRG5smU.png)

In the greater Helsinki area there are over 4000 bus stops, which in turn makes some of the bus line numbers slightly inconvinient. This would require a slight redesign of the current bus fleet…

![alt text](https://i.imgur.com/hPvJYvB.png)

BUT, we no longer live in a world in base 10 exclusively, so we can conveniently make the bus numbers more compact by using a more efficient numbering base. Base 16 (hex encoding) would not be enough of an improvement, and base 64 encoding was deamed too complex by 15 year olds. So instead, we would like to introduce basemoji:

We took the 1000 most common emojis and made a base 1000 numeric system

![alt text](https://i.imgur.com/PFLwCDX.png)

We applied our amazing mathematical model to the Helsinki public transport system thought its API. Here are some interesting route suggestions:

![alt text](https://i.imgur.com/xs2a8vx.png)

Now you'll never miss a bus again (if you can divide really quickly...)!

## Further Exploration

1. Why would one need to know where the bus has already been? Exactly! One doesn't! So let's make sure that the bus route number changes and a number that represents only the stops that it will be going to. A dynamic bus number!
2. Same thing applies inside the bus, with a dynamic bus number, you will always know what your next stops will be! (Not in any specific order though, so the inside number would have to be one stop ahead of the outside)
