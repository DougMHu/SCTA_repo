# # Hello World!

print("Hello World!")


# # Data Types

# ## Lists
# 
# There are many ways to initialize a list. Here are 2 ways.

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


list(range(10))


# You can concatenate two lists together using ``+``

[0, 1, 2, 3, 4] + [5, 6, 7, 8, 9]


# You can access an item from the list using array indexing.
# 
# You can also access a slice from the list using ``:``

x = list(range(10))
x


x[0]


x[:5]


x[5:]


# Like any other data type, ``list``s have functions that can alter the list.
# 
# In Python, these functions that act on a data type are called __``methods``__.

x.append(10)
x


x.reverse()
x


# ## Dictionaries
# 
# A Python ``dictionary`` is a mapping. Like how a real dictionary maps each word to one definition, a Python ``dictionary`` maps each __``key``__ to one __``value``__.

dictionary = {
    "happy birthday": "feliz cumpleaños",
    "thank you": "gracias",
    "beautiful": "hermosa"
}


# Access the ``value`` by indexing the ``key``, just like you would a list.

dictionary["beautiful"]


# Create new entries:

dictionary["see you later"] = "hasta luego"


# Keys can be ``string``s, ``integer``s, ``tuple``s, and values can be anything (e.g. ``list``s)

dictionary[("July", 20, 1969)] = ["Apollo 11 landed on the Moon", "Belgium wins 56th Tour de France"]


# Unlike a ``list``, a ``dictionary`` is not ordered:

dictionary


# ## Classes
# 
# Classes let you define your own data type!
# 
# Data types are structures that store __variables__ and __methods__ for acting on their variables.
# 
# For example, we can create a __``Person``__ data type that stores their first and last name, and can print their full name.

class Person(object):
    
    def __init__(self, first_name, last_name):
        self.first = first_name
        self.last = last_name
        
    def printFullName(self):
        print(self.first + " " + self.last)


me = Person(first_name="Doug", last_name="Hu")


me.first


me.printFullName()


# # Importing libraries

# Python comes with many built-in libraries.
# 
# For example, the __``math``__ library contains common trigonometric functions, special functions, and constants:

import math


math.e


math.log(math.e)


# Plot the Complementary Error Function (erfc):

x = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
y = [math.erfc(i) for i in x]


import matplotlib.pyplot
matplotlib.pyplot.plot(x,y)
matplotlib.pyplot.ylabel('Complementary Error Function')
matplotlib.pyplot.show()


# The __``statistics``__ library comes with useful functions as well. For example, it can calculate the sample mean and standard deviation.

import statistics as stats
from random import gauss
m = 0
s = 1
samples = [gauss(m,s) for i in list(range(1000))]


stats.mean(samples)


stats.stdev(samples)


matplotlib.pyplot.hist(samples)
matplotlib.pyplot.show()

