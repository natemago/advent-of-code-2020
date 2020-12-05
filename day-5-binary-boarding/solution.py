def read_input(inpf):
    boarding_passes = []

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if line:
                boarding_passes.append((line, line[:7], line[7:]))

    return boarding_passes

def decode_row(spec):
    row = 0
    deg = 6
    for c in spec:
        if c == 'B':
            row += 2**deg
        deg -= 1
    return row

def decode_seat(spec):
    seat = 0
    deg = 2
    for c in spec:
        if c == 'R':
            seat += 2**deg
        deg -= 1
    return seat


def part1(inpf):
    bpasses = read_input(inpf)

    max_seat = 0

    for _, rowspec, seatspec in bpasses:
        seat_id = decode_row(rowspec)*8 + decode_seat(seatspec)
        if max_seat < seat_id:
            max_seat = seat_id
    return max_seat


def part2(inpf):
    bpasses = read_input(inpf)

    seats = list(map(lambda b: decode_row(b[1]) * 8 + decode_seat(b[2]), bpasses))
    first = min(seats)
    last = max(seats)

    return ((last*(last+1)//2) - (first*(first-1)//2)) - sum(seats)

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))
