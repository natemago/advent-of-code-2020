from math import sqrt, gcd
from functools import reduce


def read_input(inpf):
    with open(inpf) as f:
        start = int(f.readline().strip())
        bus_ids = [int(id) if id != 'x' else -1 for id in filter(lambda id: id.strip(), f.readline().strip().split(','))]

        return (start, bus_ids)


def part1(inpf):
    start, bus_ids = read_input(inpf)

    times = []
    for bid in bus_ids:
        if bid > 0:
            d = start // bid
            if start % bid:
                d += 1
            times.append((d*bid, bid))
    
    
    t, bus_id = min(times)
    return (t-start) * bus_id


def lcm(a, b):
    g = gcd(a, b)
    if not g:
        return abs(a*b)
    return abs(a*b) // g


def where_does_a_meets_b(a_step, b_offset, b_step, cutoff):
    ''' Where does bus A meets with bus B, given that B starter at b_offset time.
        step
    A|(------)(------)(------)(------)(------)(------)(------)(------) <- here
    B|  b offset ](-----------)(-----------)(-----------)(-----------)

    the step is the cycle time of the bus.

    find the bigger step (so we get fast to the poit where they meet O(log n) time, then
    add that step to the correct start time (0 for A, offset for B).
    Then check if the point is divisible with a_step and if the point minus the b_offset
    is divisible with b_step. If both are true, we got our time.

    '''

    step = max([a_step, b_step])
    start = 0 if a_step >= b_step else b_offset
    while start <= cutoff:
        if start == 0:
            start += step
            continue
        if start % a_step == 0 and (start - b_offset) % b_step == 0:
            return start
        start += step


def where_do_they_meet(a_offset, a_step, b_offset, b_step):
    lab = lcm(a_step, b_step)

    base = min([a_offset, b_offset])
    a = a_offset - base
    b = b_offset - base

    if a == 0:
        x = where_does_a_meets_b(a_step, b, b_step, lab)
    else:
        x = where_does_a_meets_b(b_step, a, a_step, lab)

    if x is None:
        raise Exception('base')

    return (x + base, lab)
    
def part2(inpf):
    _, bus_ids = read_input(inpf)

    a_step = bus_ids[0]
    a_offset = len(bus_ids) - 1
    for i in range(1, len(bus_ids)):
        bus_id = bus_ids[i]
        if bus_id < 0:
            continue
        b_offset = len(bus_ids) - i -1
        b_step = bus_id
        a_offset, a_step = where_do_they_meet(a_offset, a_step, b_offset, b_step)

    return a_offset - len(bus_ids) + 1


print('Part 1: ', part1('input'))
print('Part 2: ', part2('input'))
