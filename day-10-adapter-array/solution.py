def read_input(inpf):
    with open(inpf) as f:
        return [int(line.strip()) for line in f]


def part1(inpf):
    adapters = read_input(inpf)
    adapters = sorted(adapters)

    diffs = {}
    prev = 0
    for adapter in adapters:
        diff = adapter - prev
        diffs[diff] = diffs.get(diff, 0) + 1
        prev = adapter
    
    diffs[3] = diffs.get(3, 0) + 1  # the highest rated adapter in your bag is always on diff 3

    return diffs[1] * diffs[3]


def count_arrangements(adapters, i, arrangements):
    rating = adapters[i]

    if i == (len(adapters) - 1):
        arrangements[i] = 1
        return

    next_valid = []
    for j in range(i+1, len(adapters)):
        if adapters[j] - rating <= 3:
            next_valid.append(j)
    
    result = 0
    for j in next_valid:
        result += arrangements[j]
    arrangements[i] = result

def part2(inpf):
    adapters = sorted(read_input(inpf))
    adapters = [0] + adapters + [adapters[-1] + 3]

    arrangements = {}
    i = len(adapters) -1
    
    while i >= 0:
        count_arrangements(adapters, i, arrangements)
        i -= 1
    
    return arrangements[0]



print('Part 1:', part1('input'))
print('Part 2:', part2('input'))