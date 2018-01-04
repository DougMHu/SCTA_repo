"""
class Item(object):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
    def __repr__(self):
        return "Item(%s)" % (self.__dict__)
    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.foo == other.foo) and (self.bar == other.bar))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())

a = Item("hello", "bye")
print a
b = Item("hello", "bye")
print b

print "a == b: ", a==b      # True
print "a is b: ", a is b    # False

s = set([a, b])
print s
"""

import SCTA.Instrumentation as Instrumentation
import pyvisa
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

rm = pyvisa.ResourceManager()

SFU1=Instrumentation.SFU(id="SFU1", type="IP", port="192.168.10.9", rm=rm)
SFU1.setBroadcastStandard("DVBS")
actfreq=SFU1.getBroadcastStandard()
print (actfreq)


