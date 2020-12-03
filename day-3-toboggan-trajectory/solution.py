def read_input(inpf):
    trees = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = []
            for c in line:
                row.append(c)
            trees.append(row)
    return trees


def get_at(trees, x, y):
    if y >= len(trees):
        return None
    x = x % len(trees[0])
    return trees[y][x]


def part1(inpf):
    trees = read_input(inpf)
    return count_for_slope(trees, 3, 1)


def count_for_slope(trees, dx, dy):
    count = 0
    x = 0
    y = 0
    while True:
        c = get_at(trees, x, y)
        if c is None:
            break
        if c == '#':
            count += 1
        x += dx
        y += dy
    return count


def part2(inpf):
    trees = read_input(inpf)
    result = 1
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        result *= count_for_slope(trees, dx, dy)
    return result


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))