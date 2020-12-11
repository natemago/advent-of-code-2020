def read_input(inpf):
    with open(inpf) as f:
        return [[s for s in line.strip()] for line in f]


def get_adj(x, y, seats):
    adj = []

    for xx, yy in [(x-1, y-1), (x, y-1), (x+1, y-1),
                   (x-1, y),             (x+1, y),
                   (x-1, y+1), (x, y+1), (x+1, y+1)]:
        if xx < 0 or yy < 0 or xx >= len(seats[0]) or yy >= len(seats):
            continue
        adj.append(seats[yy][xx])

    return adj

def next_state(seats):
    nstate = [[s for s in row] for row in seats]
    for y in range(0, len(seats)):
        for x in range(0, len(seats[1])):
            curr = seats[y][x]
            if curr == '.':
                nstate[y][x] = curr
            elif curr == 'L':
                if sum([1 if s == '#' else 0 for s in get_adj(x, y, seats)]) == 0:
                    nstate[y][x] = '#'
                else:
                    nstate[y][x] = seats[y][x]
            else:
                if sum([1 if s == '#' else 0 for s in get_adj(x, y, seats)]) >= 4:
                    nstate[y][x] = 'L'
                else:
                    nstate[y][x] = seats[y][x]
    return nstate


def get_in_direction(x, y, dx, dy, seats):
    while True:
        x += dx
        y += dy
        if x < 0 or y < 0 or x >= len(seats[0]) or y >= len(seats):
            break
        if seats[y][x] != '.':
            return seats[y][x]

def get_adj_p2(x, y, seats):
    return map(lambda dd: get_in_direction(x, y, dd[0], dd[1], seats), [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ])

def next_state_p2(seats):
    nstate = [[s for s in row] for row in seats]
    for y in range(0, len(seats)):
        for x in range(0, len(seats[1])):
            #print(' ..', x, y)
            curr = seats[y][x]
            if curr == '.':
                nstate[y][x] = curr
            else:
                adjacent = get_adj_p2(x, y, seats)
                if curr == 'L':
                    if sum([1 if s == '#' else 0 for s in adjacent]) == 0:
                        nstate[y][x] = '#'
                    else:
                        nstate[y][x] = seats[y][x]
                else:
                    if sum([1 if s == '#' else 0 for s in adjacent]) >= 5:
                        nstate[y][x] = 'L'
                    else:
                        nstate[y][x] = seats[y][x]
    return nstate

def part1(inpf):
    seats = read_input(inpf)
    prev_state = seats
    while True:
        n_state = next_state(prev_state)
        if n_state == prev_state:
            break
        prev_state = n_state
    
    return sum(sum([1 if s == '#' else 0 for s in row]) for row in prev_state)


def part2(inpf):
    seats = read_input(inpf)
    prev_state = seats
    while True:
        n_state = next_state_p2(prev_state)
        if n_state == prev_state:
            break
        prev_state = n_state
    return sum(sum([1 if s == '#' else 0 for s in row]) for row in prev_state)

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))