def read_input(inpf):
    images = {}

    with open(inpf) as f:
        image_id = None
        image = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('tile'):
                if image and image_id is not None:
                    images[image_id] = image
                image_id = line.split()[1][:-1]
                image = []
            else:
                image.append(line)
        
        if image:
            images[image_id] = image

    return images


def get_edges(data):
    return [
        data[0],
        ''.join([c[-1] for c in data]),
        data[-1],
        ''.join([c[0] for c in data]),
    ]

def rot(data):
    return [''.join([data[j][i] for j in range(len(data))]) for i in range(len(data[0])-1,-1,-1)]

def flip(data):
    result = []
    for row in data:
        result.append(''.join(list(reversed(row))))
    return result



class Tile:

    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    def rot(self):
        self.data = rot(self.data)
    
    def flip(self):
        self.data = flip(self.data)
    
    def get_edges(self):
        return get_edges(self.data)
    
    def __str__(self):
        return self.id
    
    def __repr__(self):
        return self.__str__()
    

def to_tiles(tiles):
    result = []
    for id, data in tiles.items():
        result.append(Tile(id, data))
    return result


def get_bounds(tiles_map):
    keys = tiles_map.keys()
    lx = min(keys, key=lambda k: k[0])[0]
    ly = min(keys, key=lambda k: k[1])[1]
    mx = max(keys, key=lambda k: k[0])[0]
    my = max(keys, key=lambda k: k[1])[1]
    return lx, mx, ly, my

def print_map(tiles_map, positions, checking):
    keys = set(tiles_map.keys()).union(positions).union({checking})
    lx = min(keys, key=lambda k: k[0])[0]
    ly = min(keys, key=lambda k: k[1])[1]
    mx = max(keys, key=lambda k: k[0])[0]
    my = max(keys, key=lambda k: k[1])[1]

    s = ''
    for y in range(my-ly+1):
        for x in range(mx-lx+1):
            pos = (x+lx, y+ly)
            if pos == checking:
                s += 'X'
            elif pos in tiles_map and pos in positions:
                s += 'C'
            elif pos in tiles_map:
                s += 'T'
            elif pos in positions:
                s += '?'
            else:
                s += ' '
        s += '\n'
    
    print(s)


def free_edges(x, y, tiles_map):
    result = []
    for xx, yy, idx in [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]:

        tile = tiles_map.get((x+xx, y+yy))
        #print(' .. free edges: tile=', tile, '@', (xx+x, yy+y), '; map=', tiles_map)
        if tile:
            edges = tile.get_edges()

            result.append((
                edges[(idx + 2) % 4],
                idx,
            ))
    return result

def match_tile(tile, tiles_map, positions):
    edges = tile.get_edges()
    #print('Trying to match:', edges)
    for px, py in positions:
        free = free_edges(px, py, tiles_map)
        #print(' .. with:', free, 'at', px, py)
        #print_map(tiles_map, positions, (px, py))
        match = True
        for fv, i in free:
            ev = edges[i]
            if fv != ev:
                match = False
                break
        if match:
            return (px, py)
    return False


def reconstruct(tiles_map):
    from math import sqrt
    lx, mx, ly, my = get_bounds(tiles_map)
    size = int(sqrt(len(tiles_map)))
    tile_size = len(tiles_map.get((0,0)).data) - 2
    screen = [['X' for i in range(size*tile_size)] for j in range(size * tile_size)]

    for ty in range(my - ly + 1):
        for tx in range(mx - lx + 1):
            tile = tiles_map.get((tx + lx, ty + ly))
            print(tile.id, ' ', end='')
            for y in range(tile_size):
                for x in range(tile_size):
                    screen[ty*tile_size + y][tx * tile_size + x] = tile.data[y + 1][x + 1]
        print()
    return screen


sea_monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

def mask(reg1, m):
    # print('---------------------')
    # print('Region:')
    # print('\n'.join([''.join(row) for row in reg1]))
    # print('Mask:')
    # print('\n'.join(m))
    result = []
    for y, row in enumerate(reg1):
        result_row = []
        for x, c in enumerate(row):
            mc = m[y][x]
            if mc == '#':
                result_row.append('#' if c in '#O' else 'X')
            else:
                result_row.append(' ')
        result.append(result_row)
    # print('Result:')
    # print('\n'.join([''.join(row) for row in result]))
    return result

def region(screen, x, y, width, height):
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(screen[y+i][x+j])
        result.append(row)

    return result

def look_for_sea_monsters(screen):
    mask_width = len(sea_monster[0])
    mask_height = len(sea_monster)
    dh = len(screen) - len(sea_monster)
    dw = len(screen[0]) - len(sea_monster[0])

    count = 0
    for y in range(dh+1):
        for x in range(dw+1):
            masked = mask(region(screen, x, y, mask_width, mask_height), sea_monster)
            # print('----')
            # print('\n'.join([''.join(r) for r in masked]) + ']')
            # print('\n'.join(sea_monster) + ']')
            # print()
            if '\n'.join([''.join(r) for r in masked]) == '\n'.join(sea_monster):
                count += 1

                # mark the sea monsters
                for yy in range(len(sea_monster)):
                    for xx in range(len(sea_monster[0])):
                        sm = sea_monster[yy][xx]
                        if sm == '#':
                            screen[yy+y][xx+x] = 'O'
                            

    return count


def solution(inpf):
    tiles = to_tiles(read_input(inpf))

    tiles_map = {
        (0, 0): tiles[0],
    }
    q = tiles[1:]
    

    positions = {(0, -1), (1, 0), (0, 1), (-1, 0)}
    while q:
        # print('Tile map:', tiles_map)
        # print('Remaining: ', q)
        # print('Possible Locations:', positions)
        tile = q[0]
        q = q[1:]
        found = False
        for f in ['original', 'flipped']:
            for d in range(4):
                result = match_tile(tile, tiles_map, positions)
                if result:
                    px, py = result
                    tiles_map[(px, py)] = tile
                    found = True
                    positions = positions.difference({(px, py)})

                    for ex, ey in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        if (px+ex, py+ey) in tiles_map:
                            continue
                        positions.add((px+ex, py+ey))

                    break
                if found:
                    break
                tile.rot()
            if found:
                break
            tile.flip()
        if not found:
            #print('Tile', tile.id, 'not matched')
            #print('\n')
            q.append(tile)
        else:
            print_map(tiles_map, positions, (0, 0))
        #print(len(q), 'unmatched!')
        #print(tiles_map)
        #input('...')

    print(tiles_map)


    lx, mx, ly, my = get_bounds(tiles_map)
    corners = (
        tiles_map.get((lx, ly)),
        tiles_map.get((lx, my)),
        tiles_map.get((mx, ly)),
        tiles_map.get((mx, my)),
    )
    
    from functools import reduce
    print('Part 1: ', reduce(lambda a, b: a*int(b.id), corners, 1))

    screen = reconstruct(tiles_map)
    orig_screen = load_test_screen()
    print('\n'.join([''.join(row) for row in screen]))

    #return False
    for f in ['flipped', 'original']:
        for d in range(4):
            # print('-------------------')
            # print('\n'.join([''.join(row) for row in screen]))
            # print('-------------------')
            if screen == orig_screen:
                print('Matches original screen', f, d)
            count = look_for_sea_monsters(screen)
            print(f, d, 'sea monsters=', count)
            screen = rot(screen)
            screen = [[c for c in row] for row in screen]
        screen = flip(screen)
        screen = [[c for c in row] for row in screen]
    
    print('\n'.join([''.join(row) for row in screen]))

    print('Part 2:', sum([sum([1 if c == '#' else 0 for c in row]) for row in screen]))

def load_test_screen():
    screen = []
    with open('test_screen') as f:
        for line in f:
            screen.append([c for c in line.strip()])
    return screen

solution('input')