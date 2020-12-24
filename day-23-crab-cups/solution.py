INPUT = '872495136'
TEST_INPUT = '389125467'



class Cup:

    def __init__(self, v):
        self.v = v
        self.next = None
        self.prev = None
    
    def __str__(self):
        return '[{} <- {} -> {}]'.format(self.prev.v, self.v, self.next.v)
    def __repr__(self):
        return self.__str__()

class Ring:

    def __init__(self):
        self.curr = None
        self.last = None
        self.max = None
        self.cups = {}
    
    def add(self, cup):
        if not self.curr:
            self.curr = cup
            self.curr.prev = cup
            self.curr.next = cup
            self.last = cup
            self.cups[cup.v] = cup
            return
        cup.next = self.last.next
        cup.prev = self.last
        self.last.next = cup

        self.last = cup
        self.curr.prev = self.last

        if self.max is None or self.max.v < cup.v:
            self.max = cup

        self.cups[cup.v] = cup
    
    def pick3(self):
        one = self.curr.next
        two = one.next
        three = two.next
        return (one, two, three)
    
    def crab_move(self):
        one, two, three = self.pick3()
        picked = {one.v, two.v, three.v}

        curr = self.curr
        target = three.next

        # close the chain
        curr.next = target
        target.prev = curr

        # find the destination
        dest = curr.v - 1
        while True:
            if dest < 1:
                dest = self.get_max(curr.v, picked)
                continue
            if dest not in picked:
                dest = self.find_cup(dest)
                break
            dest -= 1

        # attach the three-chain after dest
        dtarget = dest.next
        one.prev = dest
        dest.next = one
        three.next = dtarget
        dtarget.prev = three

        # set new current
        self.curr = self.curr.next


    def get_max(self, currv, picked):
        seen = {currv}.union(picked)
        v = self.max.v
        while v in seen:
            v -= 1
        
        return v

    def find_cup(self, v):
        cup = self.cups.get(v)
        if not cup:
            raise Exception('No such cup')
        return cup

    def play(self, iterations):
        for i in range(iterations):
            self.crab_move()
            if (i+1) % 100000 == 0:
                print('  at', i+1, 'iterations.')
    
    def size(self):
        count = 1
        c = self.curr
        n = c.next
        while c!=n:
            count += 1
            n = n.next
        return count
    
    def __str__(self):
        c = self.curr
        m = ''
        m += str(c)
        n = c.next
        while n != c:
            m += str(n)
            n = n.next
        return m
    
    def __repr__(self):
        return self.__str__()


def to_ring(inp):
    ring = Ring()

    for c in inp:
        cup = Cup(int(c))
        ring.add(cup)
    
    return ring


def part1(inp):
    ring = to_ring(inp)
    ring.play(100)

    one = ring.find_cup(1)
    r = ''
    n = one.next
    while n != one:
        r += str(n.v)
        n = n.next
    return r

def part2(inp):
    n = len(inp) + 1
    ring = to_ring(inp)

    while n <= 1000000:
        ring.add(Cup(n))
        n += 1
    
    assert ring.max.v == 1000000
    print('Ring now has 1 000 000 cups')
    print('Actual size:', ring.size())



    iterations = 10*1000*1000  # 10 millions
    iterations = 10000000
    print('playing...')
    ring.play(iterations)
    print('the crab is done playing.')

    one = ring.find_cup(1)

    return one.next.v * one.next.next.v


print('Part 1:', part1(INPUT))
print('Part 2:', part2(INPUT))