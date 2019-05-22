# OptibusPrime

_"Solving public transport with Emoji (actually though)"_


## The Problem

Current bus numbering systems aren't particularly useful. You can't tell where they are going without a map.

https://i.imgur.com/NjGNl8p.png

## The Solution

Well, there is a simple solution! Let’s assign a prime number to each bus stop. We can now make bus lines by multiplying all the stop numbers together. A bus going to stops “5” “7” and “3” would be called 105. If “5” is your desired stop, you just need to check if an approaching bus has a number divisible by “5”? is 508735 your bus? Sure it is! Is 3618452 your bus? Of course not! EASY!

https://i.imgur.com/CRG5smU.png

In the greater Helsinki area there are over 4000 bus stops, which in turn makes some of the bus line numbers slightly inconvinient. This would require a slight redesign of the current bus fleet…

https://i.imgur.com/hPvJYvB.png

BUT, we no longer live in a world in base 10 exclusively, so we can conveniently make the bus numbers more compact by using a more efficient numbering base. Base 16 (hex encoding) would not be enough of an improvement, and base 64 encoding was deamed too complex by 15 year olds. So instead, we would like to introduce basemoji:

We took the 1000 most common emojis and made a base 1000 numeric system

https://i.imgur.com/PFLwCDX.png

We applied our amazing mathematical model to the Helsinki public transport system thought its API. Here are some interesting route suggestions:

https://i.imgur.com/xs2a8vx.png

Now you'll never miss a bus again (if you can divide really quickly...)!
