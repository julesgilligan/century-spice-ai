from collections import Counter

class Caravan(list):
    def elements(self):
        return self

    def copy(self):
        return Caravan(super().copy())

    def pays_for(self, cost):
        return sum( (Counter(cost) - Counter(self)).values() ) == 0

def remove_each(mutable: list, costly):
    # assumes the structure of mutable to be:
    # Caravan = mutable (NOT costly)
    for x in costly:
        mutable.remove(x)

def append_each(mutable: list, costly):
    # assumes the structure of mutable to be:
    # Caravan = mutable (NOT costly)
    for x in costly:
        mutable.append(x)
    mutable.sort()

def counter_caravan(candidate):
    # assumes Caravan = candidate can be made into Counter
    return Counter(candidate)
