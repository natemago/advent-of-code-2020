def read_input(inpf):
    directions = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            directions.append(parse_directions(line))
    return directions

def parse_directions(directions):
    result = []
    
    i = 0
    while i < len(directions):
        c = directions[i]
        if c in 'ew':
            result.append(c)
            i += 1
            continue
        if c in 'ns':
            if i + 1 >= len(directions):
                raise Exception('expected to end, but got ' + c + ' instead.')
            n = directions[i+1]
            if n not in 'ew':
                raise Exception('Expected to get one of: (e, w), but got ' + n + ' instead.')
            result.append(c+n)
            i += 2
            continue

    return result


moves = {
    'e': [1, 0],
    'ne': [0, 1],
    'nw': [-1, 1],
    'w': [-1, 0],
    'sw': [0, -1],
    'se': [1, -1],
}


def mark_tile(tiles, directions):
    start = (0, 0)  # reference tile

    x, y = start
    for move in directions:
        dx, dy = moves[move]
        x += dx
        y += dy
    
    tiles[(x, y)] = 0 if tiles.get((x, y), 0) else 1


def get_neighbours(x, y, tiles):
    result = []
    for dx, dy in moves.values():
        xx = x + dx
        yy = y + dy
        result.append((xx, yy, tiles.get((xx, yy), 0)))
    return result


def next_day(tiles):
    next_tiles = {}

    check_tiles = set()

    for pos, value in tiles.items():
        x, y = pos
        check_tiles.add((x, y))
        for neighbour in get_neighbours(x, y, tiles):
            nx, ny, _ = neighbour
            check_tiles.add((nx, ny))
    
    for x, y in check_tiles:
        value = tiles.get((x, y), 0)
        black_tiles = sum([v for _,_,v in get_neighbours(x, y, tiles)])

        if value:
            if black_tiles == 0 or black_tiles > 2:
                next_tiles[(x, y)] = 0
            else:
                next_tiles[(x, y)] = 1
        else:
            if black_tiles == 2:
                next_tiles[(x, y)] = 1

    return next_tiles


def part1(inpf):
    directions = read_input(inpf)
    tiles = {}


    for dirs in directions:
        mark_tile(tiles, dirs)
    
    return sum(tiles.values())


def part2(inpf):
    directions = read_input(inpf)
    tiles = {}
    for dirs in directions:
        mark_tile(tiles, dirs)
    
    for i in range(100):
        tiles = next_day(tiles)

    return sum(tiles.values())

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))