def read_input(inpf):
    state = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            state.append([c for c in line])
    return state


def input_to_cube_state(state):
    cube = {}

    for y in range(0, len(state)):
        row = state[y]
        for x in range(0, len(row)):
            if row[x] == '#':
                cube[(x, y, 0, 0)] = 1

    return cube

def get_min_max(cube, axis):
    return (
        min(cube.keys(), key=lambda k: k[axis])[axis],
        max(cube.keys(), key=lambda k: k[axis])[axis],
    )

def get_neighbours(cube, x, y, z, w=0, verbose=False, ignore_w=True):
    neighbours = []
    for xx in range(x-1, x+2):
        for yy in range(y-1, y+2):
            for zz in range(z-1, z+2):
                for ww in range(w-1, w+2):
                    if verbose:
                        print((xx, yy, zz, ww), '=>', cube.get((xx, yy, zz, ww)))
                    if ignore_w and w != 0:
                        continue
                    if (x,y,z,w) == (xx, yy, zz, ww):
                        continue
                    neighbours.append(cube.get((xx, yy, zz, ww), 0))
    return neighbours


def next_state(cube, ignore_w=True):
    ns = {}

    x_min, x_max = get_min_max(cube, 0)
    y_min, y_max = get_min_max(cube, 1)
    z_min, z_max = get_min_max(cube, 2)
    w_min, w_max = get_min_max(cube, 3)

    for x in range(x_min-1, x_max + 2):
        for y in range(y_min-1, y_max + 2):
            for z in range(z_min-1, z_max + 2):
                for w in range(w_min - 1, w_max + 2):
                    neighbours = get_neighbours(cube, x, y, z, w, ignore_w=ignore_w)
                    active_neighbours = sum(neighbours)
                    curr = cube.get((x, y, z, w), 0)
                    if curr:
                        if active_neighbours == 2 or active_neighbours == 3:
                            ns[(x, y, z, w)] = 1
                    else:
                        if active_neighbours == 3:
                            ns[(x, y, z, w)] = 1

    return ns


def print_cube(cube):

    x_min, x_max = get_min_max(cube, 0)
    y_min, y_max = get_min_max(cube, 1)
    z_min, z_max = get_min_max(cube, 2)
    w_min, w_max = get_min_max(cube, 3)

    for w in range(w_min, w_max + 1):
        print('w=', w)
        for z in range(z_min, z_max + 1):
            print('z=', z)

            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    v = cube.get((x, y, z))
                    print('#' if v else '.', end='')
                print()
            print()
        print('++++++++++++++++++')


def part1(inpf):
    cube = input_to_cube_state(read_input(inpf))

    curr_state = cube
    #print_cube(curr_state)
    for i in range(0, 6):
        curr_state = next_state(curr_state)
        #print_cube(curr_state)
    
    return sum(curr_state.values())

def part2(inpf):
    cube = input_to_cube_state(read_input(inpf))

    curr_state = cube
    #print_cube(curr_state)
    for i in range(0, 6):
        curr_state = next_state(curr_state, ignore_w=False)
        #print_cube(curr_state)
    
    return sum(curr_state.values())


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))