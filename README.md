# This project is a simple boids simulator.

Boids is an artificial life program developed by Craig Reynolds in 1986.
It is a wonderful example of how simple rules can give rise to complex behavior.

I am not yet very skilled in python. All of my classwork has been in C++
In fact, this is the first python project I've created.

# Bugs
 - While boids wraparound the screen, their functions determining locality do not account for this.

# Possible Improvements
 - O(N^2) efficency in some functions hehe.
 - Style and organization could use some work.
 - This game only runs on a single thread of my CPU. Multithread support for larger flocks?