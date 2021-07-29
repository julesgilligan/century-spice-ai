from collections import Counter

class Caravan():
    def __init__(self, source_list):
        cnt = Counter(source_list)
        self._inv = [cnt[i] for i in range(1,5)]

    def copy(self):
        return Caravan( self.elements() )
    
    def elements(self):
        lst = []
        for i in range(1,5):
            lst.extend( [i] * self.count(i) )
        return lst

    def count(self, item: int) -> int:
        assert 1 <= item <= 4
        return self._inv[item-1]
    
    def pays_for(self, cost) -> bool:
        c_cost = Counter(cost)
        for i in range(1,5):
            if c_cost[i] > self.count(i):
                return False
        return True

    def __str__(self):
        return "".join(str(x) for x in self._inv)

    def __repr__(self):
        return "Cara:"+str(self)

    def __lt__(self, other):
        return self._inv < other._inv

    def __eq__(self, other):
        if isinstance(other, Caravan):
            return self._inv == other._inv
        if isinstance(other, list): # added to make testing comparison to list easier
            return self.elements() == other
        return False
    
    def __len__(self):
        return sum(self._inv)

def remove_each(mutable: Caravan, costly: list[int]):
    # assumes the structure of mutable to be:
    # Caravan = mutable (NOT costly)
    for x in costly:
        assert 1 <= x <= 4
        mutable._inv[x-1] -= 1
        assert mutable._inv[x-1] >= 0

def append_each(mutable: Caravan, costly: list[int]):
    # Caravan = mutable (NOT costly)
    for x in costly:
        assert 1 <= x <= 4
        mutable._inv[x-1] += 1
